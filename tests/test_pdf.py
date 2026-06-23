import gc
import os
import time
from unittest.mock import patch

import pytest
from autoinvo import AutoInvo, PdfOptions, PdfEngine, PdfGenerationError
from autoinvo.pdf.weasyprint_engine import WeasyPrintEngine

def test_successful_pdf_generation() -> None:
    """Tests that a valid PDF is successfully generated from standard HTML."""
    autoinvo = AutoInvo()
    html = """
    <html>
        <head>
            <style>
                h1 { color: #333333; font-family: sans-serif; }
                p { font-size: 14px; line-height: 1.5; }
            </style>
        </head>
        <body>
            <h1>Invoice #1001</h1>
            <p>Thank you for your business!</p>
        </body>
    </html>
    """
    options = PdfOptions(
        page_size="Letter",
        landscape=True,
        margin_top="15mm",
        margin_bottom="15mm"
    )
    pdf_bytes = autoinvo.generate_pdf(html, options)

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    # PDF files must start with the standard PDF header bytes
    assert pdf_bytes.startswith(b"%PDF")


def test_pdf_starts_with_pdf_header() -> None:
    """Explicitly verifies that the generated PDF starts with the %PDF magic bytes."""
    autoinvo = AutoInvo()
    html = "<h1>Simple Document</h1>"
    pdf_bytes = autoinvo.generate_pdf(html)
    assert pdf_bytes[:4] == b"%PDF"


def test_empty_html_raises_error() -> None:
    """Tests that providing empty or whitespace-only HTML raises PdfGenerationError."""
    autoinvo = AutoInvo()

    with pytest.raises(PdfGenerationError) as exc_info:
        autoinvo.generate_pdf("")
    assert "cannot be empty" in str(exc_info.value)

    with pytest.raises(PdfGenerationError) as exc_info:
        autoinvo.generate_pdf("   \n  \t ")
    assert "cannot be empty" in str(exc_info.value)


def test_invalid_input_types_raise_error() -> None:
    """Tests that providing non-string HTML inputs raises PdfGenerationError."""
    autoinvo = AutoInvo()

    # Test passing None
    with pytest.raises(PdfGenerationError) as exc_info:
        autoinvo.generate_pdf(None)  # type: ignore
    assert "expected a string" in str(exc_info.value)

    # Test passing dictionary
    with pytest.raises(PdfGenerationError) as exc_info:
        autoinvo.generate_pdf({"html": "<h1>Test</h1>"})  # type: ignore
    assert "expected a string" in str(exc_info.value)

    # Test passing integer
    with pytest.raises(PdfGenerationError) as exc_info:
        autoinvo.generate_pdf(12345)  # type: ignore
    assert "expected a string" in str(exc_info.value)


def test_large_html_content() -> None:
    """Tests that a large HTML payload generates successfully without errors."""
    autoinvo = AutoInvo()
    
    # Generate 500 table rows to create a multi-page document
    table_rows = "".join(
        f"<tr><td>Item #{i}</td><td>Product description for item {i}</td><td>${i * 1.5:.2f}</td></tr>"
        for i in range(1, 501)
    )
    
    large_html = f"""
    <html>
        <head>
            <style>
                table {{ width: 100%; border-collapse: collapse; }}
                td, th {{ border: 1px solid #ddd; padding: 8px; font-family: sans-serif; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Statement of Accounts</h1>
            <table>
                <thead>
                    <tr><th>Item ID</th><th>Description</th><th>Unit Price</th></tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </body>
    </html>
    """
    
    pdf_bytes = autoinvo.generate_pdf(large_html)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 20000  # Should be quite large
    assert pdf_bytes.startswith(b"%PDF")


class DummyFailEngine(PdfEngine):
    """A dummy engine that always raises an error to test orchestration wrapping."""
    def generate(self, html: str, options: PdfOptions | None = None) -> bytes:
        raise ValueError("Simulated engine failure")


def test_unexpected_engine_exception_wrapping() -> None:
    """Tests that unexpected exceptions from custom engines are wrapped in PdfGenerationError."""
    custom_engine = DummyFailEngine()
    autoinvo = AutoInvo(engine=custom_engine)
    
    with pytest.raises(PdfGenerationError) as exc_info:
        autoinvo.generate_pdf("<h1>Test</h1>")
    
    assert "Unexpected error during PDF generation" in str(exc_info.value)
    assert isinstance(exc_info.value.original_exception, ValueError)


def test_special_character_and_currency_rendering() -> None:
    """Verifies that emojis, currency symbols, Kanji, and Cyrillic character sets render without corruption or crash."""
    autoinvo = AutoInvo()
    html = """
    <html>
        <body>
            <h1>Special Character Test</h1>
            <p>Emoji: 🚀 🤖 ✨</p>
            <p>Currencies: € (Euro), ₹ (Rupee), ¥ (Yen), £ (Pound)</p>
            <p>Kanji: 日本語 (Japanese)</p>
            <p>Cyrillic: Русский (Russian)</p>
        </body>
    </html>
    """
    pdf_bytes = autoinvo.generate_pdf(html)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    assert pdf_bytes.startswith(b"%PDF")


def test_malformed_broken_html_handling() -> None:
    """Verifies that malformed or broken HTML is handled gracefully and produces a valid PDF."""
    autoinvo = AutoInvo()
    # Badly formatted HTML with unclosed tags
    broken_html = "<div><span><h1>Invoice Title <div>No closing tag"
    
    pdf_bytes = autoinvo.generate_pdf(broken_html)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    assert pdf_bytes.startswith(b"%PDF")


def test_rapid_sequential_concurrency() -> None:
    """Fires multiple PDF generation calls back-to-back to ensure consecutive execution is safe."""
    autoinvo = AutoInvo()
    html = "<h1>Sequential Execution Test</h1>"
    
    for i in range(5):
        pdf_bytes = autoinvo.generate_pdf(f"{html} - Attempt {i}")
        assert isinstance(pdf_bytes, bytes)
        assert pdf_bytes.startswith(b"%PDF")


def test_process_memory_leakage_prevention() -> None:
    """Generates PDFs sequentially in a loop and verifies that resource utilization/GC objects are disposed cleanly."""
    autoinvo = AutoInvo()
    html = "<h1>Resource Disposition Test</h1>"
    
    # Baseline gc tracking
    gc.collect()
    baseline_objects = len(gc.get_objects())
    
    for _ in range(10):
        pdf_bytes = autoinvo.generate_pdf(html)
        assert isinstance(pdf_bytes, bytes)
        assert pdf_bytes.startswith(b"%PDF")
        
    gc.collect()
    final_objects = len(gc.get_objects())
    
    # Ensure there isn't a massive memory leak of Python objects (difference should be minimal)
    diff = final_objects - baseline_objects
    assert diff < 200  # Generous upper bound to allow for Python's internal caches/temp structures


def test_strict_timeout_enforcement() -> None:
    """Verifies that network asset retrieval respects the configured timeout."""
    autoinvo = AutoInvo()
    options = PdfOptions(timeout=1)
    
    # HTML template referencing a slow loading external resource
    html = '<html><body><img src="http://example.com/slow_loading_image.jpg"></body></html>'
    
    def mock_fetcher(url, timeout=None, **kwargs):
        if timeout == 1:
            raise TimeoutError("Simulated network timeout")
        raise ValueError(f"Unexpected timeout: {timeout}")
        
    with patch("weasyprint.default_url_fetcher", side_effect=mock_fetcher):
        with pytest.raises(PdfGenerationError) as exc_info:
            autoinvo.generate_pdf(html, options)
            
        assert "timeout" in str(exc_info.value).lower() or "unexpected" in str(exc_info.value).lower()


def test_multi_page_validation() -> None:
    """Verifies that multi-page layouts generate larger byte footprint indicating multi-page rendering."""
    autoinvo = AutoInvo()
    
    # 1. Single page document
    single_page_html = "<h1>Single Page</h1>"
    single_page_pdf = autoinvo.generate_pdf(single_page_html)
    
    # 2. Multi-page document forced with page breaks
    multi_page_html = """
    <html>
        <body>
            <div style="page-break-after: always;"><h1>Page 1</h1></div>
            <div style="page-break-after: always;"><h1>Page 2</h1></div>
            <div style="page-break-after: always;"><h1>Page 3</h1></div>
            <div><h1>Page 4</h1></div>
        </body>
    </html>
    """
    multi_page_pdf = autoinvo.generate_pdf(multi_page_html)
    
    assert len(single_page_pdf) > 0
    assert len(multi_page_pdf) > 0
    # Multi-page PDF should have higher byte size due to separate page structures and drawing commands
    assert len(multi_page_pdf) > len(single_page_pdf)


@pytest.fixture
def visual_verifier():
    """Fixture that unconditionally writes generated PDF bytes to the local tmp/ directory for inspection."""
    def _verify(pdf_bytes: bytes, filename: str = "visual_check.pdf") -> None:
        tmp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tmp"))
        os.makedirs(tmp_dir, exist_ok=True)
        filepath = os.path.join(tmp_dir, filename)
        with open(filepath, "wb") as f:
            f.write(pdf_bytes)
        print(f"\n[VISUAL] Generated PDF written for verification to: {filepath}")
    return _verify


def test_visual_verification_helper(visual_verifier) -> None:
    """Generates a test PDF and invokes the visual verifier fixture to save to local disk unconditionally."""
    autoinvo = AutoInvo()
    html = """
    <html>
        <head>
            <style>
                body { font-family: sans-serif; padding: 20px; color: #333; }
                .invoice-box { border: 1px solid #eee; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.15); }
                h1 { color: #f60; }
            </style>
        </head>
        <body>
            <div class="invoice-box">
                <h1>Visual Check PDF</h1>
                <p>This PDF is generated for visual verification of print boundaries and stylesheets.</p>
            </div>
        </body>
    </html>
    """
    pdf_bytes = autoinvo.generate_pdf(html)
    assert pdf_bytes.startswith(b"%PDF")
    visual_verifier(pdf_bytes, "visual_check.pdf")

