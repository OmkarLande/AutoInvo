"""Contracts/interfaces for PDF generation engines."""

from abc import ABC, abstractmethod
from autoinvo.pdf.models import PdfOptions

class PdfEngine(ABC):
    """Abstract base class representing a PDF generation engine.

    All custom PDF generation engines (e.g. WeasyPrintEngine, PuppeteerEngine,
    ChromiumEngine, Remote API engines) must implement this contract.
    """

    @abstractmethod
    def generate(self, html: str, options: PdfOptions | None = None) -> bytes:
        """Converts an HTML string into PDF bytes in-memory.

        Args:
            html: The HTML document content to render.
            options: Optional PDF options to customize layout, page size, margins, and base URL.

        Returns:
            The generated PDF content as bytes.

        Raises:
            PdfGenerationError: If the PDF generation fails.
        """
        pass
