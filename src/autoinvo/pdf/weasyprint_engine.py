import logging
import os
import sys

# Windows DLL loading helper for WeasyPrint.
# If a local gtk3-runtime directory exists in the workspace root, register it.
if sys.platform == "win32":
    # Resolve src/autoinvo/pdf/weasyprint_engine.py -> root/gtk3-runtime
    local_gtk = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "gtk3-runtime"))
    if os.path.isdir(local_gtk):
        try:
            os.add_dll_directory(local_gtk)
        except Exception:
            pass

from weasyprint import HTML, CSS
from weasyprint.urls import FatalURLFetchingError

from autoinvo.pdf.contracts import PdfEngine
from autoinvo.pdf.models import PdfOptions
from autoinvo.pdf.exceptions import PdfGenerationError

logger = logging.getLogger(__name__)

class WeasyPrintEngine(PdfEngine):
    """PDF generation engine implementation using WeasyPrint.

    Converts HTML markup into a PDF document entirely in-memory.
    """

    def generate(self, html: str, options: PdfOptions | None = None) -> bytes:
        """Converts an HTML string into PDF bytes using WeasyPrint.

        Args:
            html: HTML markup string to render.
            options: PDF configuration options including page size, margins, and base URL.

        Returns:
            The rendered PDF content as bytes.

        Raises:
            PdfGenerationError: If the document rendering or layout compilation fails.
        """
        opts = options or PdfOptions()

        # Build @page rule to configure page size, orientation, and margins
        size_part = f"{opts.page_size}"
        if opts.landscape:
            size_part += " landscape"

        css_string = f"""
        @page {{
            size: {size_part};
            margin-top: {opts.margin_top};
            margin-right: {opts.margin_right};
            margin-bottom: {opts.margin_bottom};
            margin-left: {opts.margin_left};
        }}
        """

        try:
            # HTML input compiled entirely in memory.
            # Passing base_url allows resolving local/remote assets like images and stylesheets.
            url_fetcher = None
            if opts.timeout is not None:
                from weasyprint import default_url_fetcher
                from weasyprint.urls import FatalURLFetchingError
                def custom_fetcher(url, timeout=opts.timeout, **kwargs):
                    try:
                        return default_url_fetcher(url, timeout=timeout, **kwargs)
                    except Exception as e:
                        raise FatalURLFetchingError(f"URL fetching failed or timed out: {e}") from e
                url_fetcher = custom_fetcher

            html_doc = HTML(string=html, base_url=opts.base_url, url_fetcher=url_fetcher)
            css_doc = CSS(string=css_string)
            
            # Calling write_pdf without a target file will return bytes.
            pdf_bytes = html_doc.write_pdf(stylesheets=[css_doc])
            if not pdf_bytes:
                raise ValueError("WeasyPrint returned empty PDF bytes.")
            return pdf_bytes
        except (Exception, FatalURLFetchingError) as e:
            logger.error("Failed to generate PDF with WeasyPrint: %s", str(e), exc_info=True)
            raise PdfGenerationError(
                message=f"WeasyPrint engine failed to generate PDF: {str(e)}",
                original_exception=e
            ) from e
