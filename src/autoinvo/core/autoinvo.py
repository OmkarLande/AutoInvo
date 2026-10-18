"""Facade module for autoinvo package."""

from typing import TYPE_CHECKING

from autoinvo.importers.contracts import ImportSource
from autoinvo.importers.models import CsvImportOptions, ImportResult, XlsxImportOptions
from autoinvo.pdf.contracts import PdfEngine
from autoinvo.pdf.generator import PdfGenerator
from autoinvo.pdf.models import PdfOptions
from autoinvo.pdf.weasyprint_engine import WeasyPrintEngine
from autoinvo.templates.contracts import TemplateData, TemplateRenderOptions, TemplateRenderer
from autoinvo.templates.service import JinjaTemplateRenderer

if TYPE_CHECKING:
    from autoinvo.importers.service import ImportService


class AutoInvo:
    """Facade for the autoinvo library, serving as the main public entry point.

    Coordinates document generation by orchestrating configured layout settings
    and rendering engines.
    """

    def __init__(
        self,
        engine: PdfEngine | None = None,
        import_service: "ImportService | None" = None,
        template_renderer: TemplateRenderer | None = None,
    ) -> None:
        """Initializes the AutoInvo facade."""
        self._engine: PdfEngine = engine or WeasyPrintEngine()
        self._pdf_generator = PdfGenerator(self._engine)

        if import_service is None:
            from autoinvo.importers.service import ImportService
            self._import_service = ImportService()
        else:
            self._import_service = import_service

        self._template_renderer: TemplateRenderer = template_renderer or JinjaTemplateRenderer()

    def generate_pdf(self, html: str, options: PdfOptions | None = None) -> bytes:
        return self._pdf_generator.generate(html, options)

    def import_csv(self, source: ImportSource, options: CsvImportOptions | None = None) -> ImportResult:
        return self._import_service.import_csv(source, options)

    def import_xlsx(self, source: ImportSource, options: XlsxImportOptions | None = None) -> ImportResult:
        return self._import_service.import_xlsx(source, options)

    def generate_invoice(
        self,
        template_name: str,
        data: TemplateData,
        pdf_options: PdfOptions | None = None,
        template_options: TemplateRenderOptions | None = None,
    ) -> bytes:
        """Render an invoice template and generate a PDF."""
        html = self._template_renderer.render(
            template_name=template_name,
            data=data,
            options=template_options,
        )
        return self.generate_pdf(html, pdf_options)