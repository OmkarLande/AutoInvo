"""Orchestration service for generating PDFs."""

from autoinvo.pdf.contracts import PdfEngine
from autoinvo.pdf.models import PdfOptions
from autoinvo.pdf.exceptions import PdfGenerationError

class PdfGenerator:
    """Orchestrator for PDF generation.

    Validates inputs and coordinates layout configuration before handing off
    the actual document compiling task to a selected engine implementation.
    """

    def __init__(self, engine: PdfEngine) -> None:
        """Initializes the PdfGenerator with a specific PdfEngine implementation.

        Args:
            engine: The PDF rendering engine to delegate generating tasks to.
        """
        self.engine = engine

    def generate(self, html: str, options: PdfOptions | None = None) -> bytes:
        """Validates inputs, prepares options, and invokes the underlying PDF engine.

        Args:
            html: HTML markup string to render.
            options: Optional PDF options.

        Returns:
            The rendered PDF bytes.

        Raises:
            PdfGenerationError: If the input HTML is invalid or the PDF generation fails.
        """
        if not isinstance(html, str):
            raise PdfGenerationError(
                f"Invalid HTML input: expected a string, got {type(html).__name__}."
            )

        if not html.strip():
            raise PdfGenerationError("HTML input cannot be empty or whitespace only.")

        opts = options or PdfOptions()

        try:
            return self.engine.generate(html, opts)
        except PdfGenerationError:
            # Propagate our own errors directly
            raise
        except Exception as e:
            # Wrap any unhandled errors from the engine implementation layer
            raise PdfGenerationError(
                f"Unexpected error during PDF generation: {str(e)}",
                original_exception=e
            ) from e
