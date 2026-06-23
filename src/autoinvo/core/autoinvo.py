"""Facade module for autoinvo package."""

from autoinvo.pdf.contracts import PdfEngine
from autoinvo.pdf.models import PdfOptions
from autoinvo.pdf.generator import PdfGenerator
from autoinvo.pdf.weasyprint_engine import WeasyPrintEngine

class AutoInvo:
    """Facade for the autoinvo library, serving as the main public entry point.

    Coordinates document generation by orchestrating configured layout settings
    and rendering engines.
    """

    def __init__(self, engine: PdfEngine | None = None) -> None:
        """Initializes the AutoInvo facade.

        Args:
            engine: Optional custom PdfEngine implementation. Defaults to WeasyPrintEngine.
        """
        if engine is None:
            self._engine: PdfEngine = WeasyPrintEngine()
        else:
            self._engine = engine

        self._pdf_generator = PdfGenerator(self._engine)

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
