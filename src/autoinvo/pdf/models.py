"""Options for the PDF generation process."""

from dataclasses import dataclass

@dataclass
class PdfOptions:
    """Configuration options for PDF generation.

    Attributes:
        page_size: The page size (e.g., 'A4', 'Letter'). Defaults to 'A4'.
        landscape: If True, landscape orientation is used; otherwise portrait. Defaults to False.
        margin_top: Top margin with CSS units (e.g., '10mm', '1in'). Defaults to '10mm'.
        margin_right: Right margin with CSS units. Defaults to '10mm'.
        margin_bottom: Bottom margin with CSS units. Defaults to '10mm'.
        margin_left: Left margin with CSS units. Defaults to '10mm'.
        base_url: Optional base URL or file path used to resolve relative resources (images, stylesheets). Defaults to None.
    """
    page_size: str = "A4"
    landscape: bool = False
    margin_top: str = "10mm"
    margin_right: str = "10mm"
    margin_bottom: str = "10mm"
    margin_left: str = "10mm"
    base_url: str | None = None
    timeout: int | None = None

