"""Facade module for autoinvo package."""

from typing import TYPE_CHECKING

from autoinvo.pdf.contracts import PdfEngine
from autoinvo.pdf.models import PdfOptions
from autoinvo.pdf.generator import PdfGenerator
from autoinvo.pdf.weasyprint_engine import WeasyPrintEngine

if TYPE_CHECKING:
    from autoinvo.importers.service import ImportService

from autoinvo.importers.contracts import ImportSource
from autoinvo.importers.models import ImportResult, CsvImportOptions, XlsxImportOptions

class AutoInvo:
    """Facade for the autoinvo library, serving as the main public entry point.

    Coordinates document generation by orchestrating configured layout settings
    and rendering engines.
    """

    def __init__(
        self,
        engine: PdfEngine | None = None,
        import_service: 'ImportService | None' = None
    ) -> None:
        """Initializes the AutoInvo facade.

        Args:
            engine: Optional custom PdfEngine implementation. Defaults to WeasyPrintEngine.
            import_service: Optional custom ImportService. Defaults to standard ImportService.
        """
        if engine is None:
            self._engine: PdfEngine = WeasyPrintEngine()
        else:
            self._engine = engine

        self._pdf_generator = PdfGenerator(self._engine)
        
        if import_service is None:
            from autoinvo.importers.service import ImportService
            self._import_service = ImportService()
        else:
            self._import_service = import_service

    def generate_pdf(self, html: str, options: PdfOptions | None = None) -> bytes:
        """Generates a PDF from an HTML string and options.

        Args:
            html: The HTML document content to render.
            options: Optional PDF options to customize the layout.

        Returns:
            The generated PDF content as bytes.

        Raises:
            PdfGenerationError: If the input validation or rendering fails.
        """
        return self._pdf_generator.generate(html, options)

    def import_csv(self, source: ImportSource, options: CsvImportOptions | None = None) -> ImportResult:
        """Imports data from a CSV file.

        Args:
            source: The input data source (e.g., path, str, bytes, BinaryIO).
            options: Configuration options for CSV import.

        Returns:
            An ImportResult containing the standardized parsed data.
        """
        return self._import_service.import_csv(source, options)

    def import_xlsx(self, source: ImportSource, options: XlsxImportOptions | None = None) -> ImportResult:
        """Imports data from an Excel (XLSX) file.

        Args:
            source: The input data source (e.g., path, str, bytes, BinaryIO).
            options: Configuration options for XLSX import.

        Returns:
            An ImportResult containing the standardized parsed data.
        """
        return self._import_service.import_xlsx(source, options)
