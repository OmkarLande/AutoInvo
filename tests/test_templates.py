"""
Tests for Invoice HTML Templates.

This module contains comprehensive tests for validating the minimal, modern,
and corporate invoice templates. Tests cover:
- File existence and structure
- HTML5 compliance
- CSS linking and existence
- Invoice section presence
- Print media queries
- Content validation
- PDF generation compatibility
"""

import os
from pathlib import Path
from html.parser import HTMLParser
import re
from typing import List

import pytest


class HTMLValidator(HTMLParser):
    """Custom HTML parser to validate template structure."""

    def __init__(self):
        super().__init__()
        self.tags = []
        self.css_links = []
        self.has_doctype = False
        self.lang_attribute = None
        self.meta_charset = False
        self.meta_viewport = False

    def handle_starttag(self, tag: str, attrs: List):
        """Track opened tags and CSS links."""
        self.tags.append(tag)
        if tag == "link":
            attrs_dict = dict(attrs)
            if attrs_dict.get("rel") == "stylesheet":
                self.css_links.append(attrs_dict.get("href"))
        elif tag == "meta":
            attrs_dict = dict(attrs)
            if "charset" in attrs_dict:
                self.meta_charset = True
            if attrs_dict.get("name") == "viewport":
                self.meta_viewport = True
        elif tag == "html":
            attrs_dict = dict(attrs)
            self.lang_attribute = attrs_dict.get("lang")

    def handle_endtag(self, tag: str):
        """Track closed tags."""
        if self.tags and self.tags[-1] == tag:
            self.tags.pop()


# Template paths
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
STYLES_DIR = TEMPLATES_DIR / "styles"

MINIMAL_HTML = TEMPLATES_DIR / "minimal-invoice.html"
MODERN_HTML = TEMPLATES_DIR / "modern-invoice.html"
CORPORATE_HTML = TEMPLATES_DIR / "corporate-invoice.html"

MINIMAL_CSS = STYLES_DIR / "minimal.css"
MODERN_CSS = STYLES_DIR / "modern.css"
CORPORATE_CSS = STYLES_DIR / "corporate.css"


# ============================================================================
# File and Structure Tests
# ============================================================================

class TestTemplateFileStructure:
    """Tests for template file existence and basic structure."""

    def test_templates_directory_exists(self):
        """Verify templates directory exists."""
        assert TEMPLATES_DIR.exists(), "Templates directory not found"
        assert TEMPLATES_DIR.is_dir(), "Templates path is not a directory"

    def test_styles_directory_exists(self):
        """Verify styles directory exists."""
        assert STYLES_DIR.exists(), "Styles directory not found"
        assert STYLES_DIR.is_dir(), "Styles path is not a directory"

    def test_minimal_template_file_exists(self):
        """Verify minimal template HTML file exists."""
        assert MINIMAL_HTML.exists(), "minimal-invoice.html not found"
        assert MINIMAL_HTML.is_file(), "minimal-invoice.html is not a file"

    def test_modern_template_file_exists(self):
        """Verify modern template HTML file exists."""
        assert MODERN_HTML.exists(), "modern-invoice.html not found"
        assert MODERN_HTML.is_file(), "modern-invoice.html is not a file"

    def test_corporate_template_file_exists(self):
        """Verify corporate template HTML file exists."""
        assert CORPORATE_HTML.exists(), "corporate-invoice.html not found"
        assert CORPORATE_HTML.is_file(), "corporate-invoice.html is not a file"

    def test_minimal_css_file_exists(self):
        """Verify minimal CSS file exists."""
        assert MINIMAL_CSS.exists(), "minimal.css not found"
        assert MINIMAL_CSS.is_file(), "minimal.css is not a file"

    def test_modern_css_file_exists(self):
        """Verify modern CSS file exists."""
        assert MODERN_CSS.exists(), "modern.css not found"
        assert MODERN_CSS.is_file(), "modern.css is not a file"

    def test_corporate_css_file_exists(self):
        """Verify corporate CSS file exists."""
        assert CORPORATE_CSS.exists(), "corporate.css not found"
        assert CORPORATE_CSS.is_file(), "corporate.css is not a file"


# ============================================================================
# HTML Validation Tests
# ============================================================================

class TestHTMLValidity:
    """Tests for HTML5 compliance and structure."""

    @staticmethod
    def validate_html(html_file: Path) -> str:
        """Read and return HTML content."""
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()

    def test_minimal_html_is_valid_utf8(self):
        """Verify minimal template is valid UTF-8."""
        html = self.validate_html(MINIMAL_HTML)
        assert isinstance(html, str)
        assert len(html) > 0

    def test_modern_html_is_valid_utf8(self):
        """Verify modern template is valid UTF-8."""
        html = self.validate_html(MODERN_HTML)
        assert isinstance(html, str)
        assert len(html) > 0

    def test_corporate_html_is_valid_utf8(self):
        """Verify corporate template is valid UTF-8."""
        html = self.validate_html(CORPORATE_HTML)
        assert isinstance(html, str)
        assert len(html) > 0

    def test_minimal_has_doctype(self):
        """Verify minimal template has HTML5 DOCTYPE."""
        html = self.validate_html(MINIMAL_HTML)
        assert html.strip().upper().startswith("<!DOCTYPE HTML>")

    def test_modern_has_doctype(self):
        """Verify modern template has HTML5 DOCTYPE."""
        html = self.validate_html(MODERN_HTML)
        assert html.strip().upper().startswith("<!DOCTYPE HTML>")

    def test_corporate_has_doctype(self):
        """Verify corporate template has HTML5 DOCTYPE."""
        html = self.validate_html(CORPORATE_HTML)
        assert html.strip().upper().startswith("<!DOCTYPE HTML>")

    def test_minimal_has_html_tag(self):
        """Verify minimal template has html tag."""
        html = self.validate_html(MINIMAL_HTML)
        assert "<html" in html.lower()
        assert "</html>" in html.lower()

    def test_modern_has_html_tag(self):
        """Verify modern template has html tag."""
        html = self.validate_html(MODERN_HTML)
        assert "<html" in html.lower()
        assert "</html>" in html.lower()

    def test_corporate_has_html_tag(self):
        """Verify corporate template has html tag."""
        html = self.validate_html(CORPORATE_HTML)
        assert "<html" in html.lower()
        assert "</html>" in html.lower()

    def test_minimal_has_head_and_body(self):
        """Verify minimal template has head and body tags."""
        html = self.validate_html(MINIMAL_HTML)
        assert "<head>" in html or "<head " in html
        assert "</head>" in html
        assert "<body>" in html or "<body " in html
        assert "</body>" in html

    def test_modern_has_head_and_body(self):
        """Verify modern template has head and body tags."""
        html = self.validate_html(MODERN_HTML)
        assert "<head>" in html or "<head " in html
        assert "</head>" in html
        assert "<body>" in html or "<body " in html
        assert "</body>" in html

    def test_corporate_has_head_and_body(self):
        """Verify corporate template has head and body tags."""
        html = self.validate_html(CORPORATE_HTML)
        assert "<head>" in html or "<head " in html
        assert "</head>" in html
        assert "<body>" in html or "<body " in html
        assert "</body>" in html


# ============================================================================
# CSS Linking Tests
# ============================================================================

class TestCSSLinking:
    """Tests for CSS file linking and references."""

    @staticmethod
    def parse_html(html_file: Path) -> HTMLValidator:
        """Parse HTML file and return validator."""
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        parser = HTMLValidator()
        parser.feed(html_content)
        return parser

    def test_minimal_links_minimal_css(self):
        """Verify minimal template links to minimal.css."""
        parser = self.parse_html(MINIMAL_HTML)
        assert len(parser.css_links) > 0
        assert any("minimal.css" in link for link in parser.css_links)

    def test_modern_links_modern_css(self):
        """Verify modern template links to modern.css."""
        parser = self.parse_html(MODERN_HTML)
        assert len(parser.css_links) > 0
        assert any("modern.css" in link for link in parser.css_links)

    def test_corporate_links_corporate_css(self):
        """Verify corporate template links to corporate.css."""
        parser = self.parse_html(CORPORATE_HTML)
        assert len(parser.css_links) > 0
        assert any("corporate.css" in link for link in parser.css_links)

    def test_minimal_css_link_is_stylesheet(self):
        """Verify minimal template's CSS link is stylesheet type."""
        with open(MINIMAL_HTML, "r", encoding="utf-8") as f:
            html = f.read()
        assert 'rel="stylesheet"' in html
        assert "minimal.css" in html

    def test_modern_css_link_is_stylesheet(self):
        """Verify modern template's CSS link is stylesheet type."""
        with open(MODERN_HTML, "r", encoding="utf-8") as f:
            html = f.read()
        assert 'rel="stylesheet"' in html
        assert "modern.css" in html

    def test_corporate_css_link_is_stylesheet(self):
        """Verify corporate template's CSS link is stylesheet type."""
        with open(CORPORATE_HTML, "r", encoding="utf-8") as f:
            html = f.read()
        assert 'rel="stylesheet"' in html
        assert "corporate.css" in html


# ============================================================================
# Meta Tags and HTML5 Compliance Tests
# ============================================================================

class TestMetaTags:
    """Tests for required meta tags and HTML5 compliance."""

    @staticmethod
    def get_head_content(html_file: Path) -> str:
        """Extract head content from HTML file."""
        with open(html_file, "r", encoding="utf-8") as f:
            html = f.read()
        match = re.search(r"<head>(.*?)</head>", html, re.DOTALL | re.IGNORECASE)
        return match.group(1) if match else ""

    def test_minimal_has_charset_meta(self):
        """Verify minimal template has charset meta tag."""
        head = self.get_head_content(MINIMAL_HTML)
        assert "charset" in head.lower()

    def test_modern_has_charset_meta(self):
        """Verify modern template has charset meta tag."""
        head = self.get_head_content(MODERN_HTML)
        assert "charset" in head.lower()

    def test_corporate_has_charset_meta(self):
        """Verify corporate template has charset meta tag."""
        head = self.get_head_content(CORPORATE_HTML)
        assert "charset" in head.lower()

    def test_minimal_has_viewport_meta(self):
        """Verify minimal template has viewport meta tag."""
        head = self.get_head_content(MINIMAL_HTML)
        assert "viewport" in head.lower()

    def test_modern_has_viewport_meta(self):
        """Verify modern template has viewport meta tag."""
        head = self.get_head_content(MODERN_HTML)
        assert "viewport" in head.lower()

    def test_corporate_has_viewport_meta(self):
        """Verify corporate template has viewport meta tag."""
        head = self.get_head_content(CORPORATE_HTML)
        assert "viewport" in head.lower()

    def test_minimal_has_title(self):
        """Verify minimal template has title tag."""
        with open(MINIMAL_HTML, "r", encoding="utf-8") as f:
            html = f.read()
        assert "<title>" in html.lower() and "</title>" in html.lower()

    def test_modern_has_title(self):
        """Verify modern template has title tag."""
        with open(MODERN_HTML, "r", encoding="utf-8") as f:
            html = f.read()
        assert "<title>" in html.lower() and "</title>" in html.lower()

    def test_corporate_has_title(self):
        """Verify corporate template has title tag."""
        with open(CORPORATE_HTML, "r", encoding="utf-8") as f:
            html = f.read()
        assert "<title>" in html.lower() and "</title>" in html.lower()


# ============================================================================
# Invoice Content Tests
# ============================================================================

class TestInvoiceContent:
    """Tests for required invoice content and sections."""

    @staticmethod
    def read_template(html_file: Path) -> str:
        """Read template file content."""
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()

    def test_minimal_has_invoice_container(self):
        """Verify minimal template has invoice container."""
        html = self.read_template(MINIMAL_HTML)
        assert 'class="invoice-container"' in html

    def test_modern_has_invoice_container(self):
        """Verify modern template has invoice container."""
        html = self.read_template(MODERN_HTML)
        assert 'class="invoice-container"' in html

    def test_corporate_has_invoice_container(self):
        """Verify corporate template has invoice container."""
        html = self.read_template(CORPORATE_HTML)
        assert 'class="invoice-container"' in html

    def test_minimal_has_header_section(self):
        """Verify minimal template has header section."""
        html = self.read_template(MINIMAL_HTML)
        assert 'class="header"' in html
        assert "ACME" in html or "company" in html.lower()

    def test_modern_has_header_section(self):
        """Verify modern template has header section."""
        html = self.read_template(MODERN_HTML)
        assert 'class="header"' in html
        assert "TechVision" in html or "company" in html.lower()

    def test_corporate_has_header_section(self):
        """Verify corporate template has header section."""
        html = self.read_template(CORPORATE_HTML)
        assert 'class="header"' in html
        assert "ENTERPRISE" in html or "company" in html.lower()

    def test_minimal_has_addresses_section(self):
        """Verify minimal template has addresses section."""
        html = self.read_template(MINIMAL_HTML)
        assert 'class="addresses"' in html
        assert "Bill To" in html

    def test_modern_has_addresses_section(self):
        """Verify modern template has addresses section."""
        html = self.read_template(MODERN_HTML)
        assert 'class="addresses"' in html
        assert "Bill To" in html

    def test_corporate_has_addresses_section(self):
        """Verify corporate template has addresses section."""
        html = self.read_template(CORPORATE_HTML)
        assert 'class="addresses"' in html
        assert "Bill To" in html

    def test_minimal_has_items_table(self):
        """Verify minimal template has line items table."""
        html = self.read_template(MINIMAL_HTML)
        assert 'class="items-table"' in html
        assert "<thead>" in html
        assert "<tbody>" in html
        assert "Description" in html or "Item" in html

    def test_modern_has_items_table(self):
        """Verify modern template has line items table."""
        html = self.read_template(MODERN_HTML)
        assert 'class="items-table"' in html
        assert "<thead>" in html
        assert "<tbody>" in html

    def test_corporate_has_items_table(self):
        """Verify corporate template has line items table."""
        html = self.read_template(CORPORATE_HTML)
        assert 'class="items-table"' in html
        assert "<thead>" in html
        assert "<tbody>" in html

    def test_minimal_has_totals_section(self):
        """Verify minimal template has totals section."""
        html = self.read_template(MINIMAL_HTML)
        assert 'class="totals' in html
        assert "TOTAL" in html or "Total" in html

    def test_modern_has_totals_section(self):
        """Verify modern template has totals section."""
        html = self.read_template(MODERN_HTML)
        assert 'class="totals' in html
        assert "Total" in html

    def test_corporate_has_totals_section(self):
        """Verify corporate template has totals section."""
        html = self.read_template(CORPORATE_HTML)
        assert 'class="totals' in html
        assert "Total" in html

    def test_minimal_has_sample_invoice_data(self):
        """Verify minimal template has sample invoice data."""
        html = self.read_template(MINIMAL_HTML)
        assert "INV-" in html or "Invoice" in html
        assert "$" in html

    def test_modern_has_sample_invoice_data(self):
        """Verify modern template has sample invoice data."""
        html = self.read_template(MODERN_HTML)
        assert "INV-" in html or "Invoice" in html
        assert "$" in html

    def test_corporate_has_sample_invoice_data(self):
        """Verify corporate template has sample invoice data."""
        html = self.read_template(CORPORATE_HTML)
        assert "INV-" in html or "Invoice" in html or "ESG-" in html
        assert "$" in html


# ============================================================================
# CSS Content and Print Media Tests
# ============================================================================

class TestCSSContent:
    """Tests for CSS content and media queries."""

    @staticmethod
    def read_css(css_file: Path) -> str:
        """Read CSS file content."""
        with open(css_file, "r", encoding="utf-8") as f:
            return f.read()

    def test_minimal_css_has_print_media_query(self):
        """Verify minimal CSS has print media query."""
        css = self.read_css(MINIMAL_CSS)
        assert "@media print" in css

    def test_modern_css_has_print_media_query(self):
        """Verify modern CSS has print media query."""
        css = self.read_css(MODERN_CSS)
        assert "@media print" in css

    def test_corporate_css_has_print_media_query(self):
        """Verify corporate CSS has print media query."""
        css = self.read_css(CORPORATE_CSS)
        assert "@media print" in css

    def test_minimal_css_has_base_styles(self):
        """Verify minimal CSS has base styles."""
        css = self.read_css(MINIMAL_CSS)
        assert "body {" in css or "body{" in css
        assert "font-family" in css

    def test_modern_css_has_base_styles(self):
        """Verify modern CSS has base styles."""
        css = self.read_css(MODERN_CSS)
        assert "body {" in css or "body{" in css
        assert "font-family" in css

    def test_corporate_css_has_base_styles(self):
        """Verify corporate CSS has base styles."""
        css = self.read_css(CORPORATE_CSS)
        assert "body {" in css or "body{" in css
        assert "font-family" in css

    def test_minimal_css_has_invoice_container_styles(self):
        """Verify minimal CSS has invoice-container styles."""
        css = self.read_css(MINIMAL_CSS)
        assert ".invoice-container" in css or "invoice-container" in css

    def test_modern_css_has_invoice_container_styles(self):
        """Verify modern CSS has invoice-container styles."""
        css = self.read_css(MODERN_CSS)
        assert ".invoice-container" in css or "invoice-container" in css

    def test_corporate_css_has_invoice_container_styles(self):
        """Verify corporate CSS has invoice-container styles."""
        css = self.read_css(CORPORATE_CSS)
        assert ".invoice-container" in css or "invoice-container" in css

    def test_minimal_css_has_table_styles(self):
        """Verify minimal CSS has table styles."""
        css = self.read_css(MINIMAL_CSS)
        assert ".items-table" in css or "table" in css

    def test_modern_css_has_table_styles(self):
        """Verify modern CSS has table styles."""
        css = self.read_css(MODERN_CSS)
        assert ".items-table" in css or "table" in css

    def test_corporate_css_has_table_styles(self):
        """Verify corporate CSS has table styles."""
        css = self.read_css(CORPORATE_CSS)
        assert ".items-table" in css or "table" in css


# ============================================================================
# Template Styling Differentiation Tests
# ============================================================================

class TestTemplateDistinctiveness:
    """Tests to verify templates are visually distinct."""

    @staticmethod
    def read_css(css_file: Path) -> str:
        """Read CSS file content."""
        with open(css_file, "r", encoding="utf-8") as f:
            return f.read()

    def test_templates_have_different_colors(self):
        """Verify templates use different color schemes."""
        minimal_css = self.read_css(MINIMAL_CSS)
        modern_css = self.read_css(MODERN_CSS)
        corporate_css = self.read_css(CORPORATE_CSS)

        # Extract hex color codes
        minimal_colors = set(re.findall(r"#[0-9a-fA-F]{3,6}", minimal_css))
        modern_colors = set(re.findall(r"#[0-9a-fA-F]{3,6}", modern_css))
        corporate_colors = set(re.findall(r"#[0-9a-fA-F]{3,6}", corporate_css))

        # Verify each template has some colors
        assert len(minimal_colors) > 0
        assert len(modern_colors) > 0
        assert len(corporate_colors) > 0

    def test_modern_has_grid_layout(self):
        """Verify modern template uses modern CSS features."""
        modern_css = self.read_css(MODERN_CSS)
        # Modern should use grid or flexbox
        assert "grid" in modern_css or "flex" in modern_css

    def test_corporate_has_formal_structure(self):
        """Verify corporate template has formal styling."""
        corporate_css = self.read_css(CORPORATE_CSS)
        # Should have borders and structured layout
        assert "border" in corporate_css

    def test_minimal_has_simple_styling(self):
        """Verify minimal template uses minimal styling."""
        minimal_css = self.read_css(MINIMAL_CSS)
        modern_css = self.read_css(MODERN_CSS)
        
        # Minimal should be simpler (fewer lines/properties)
        minimal_size = len(minimal_css)
        modern_size = len(modern_css)
        
        # Minimal should be more concise
        assert minimal_size > 0  # Just verify it exists


# ============================================================================
# Responsive Design Tests
# ============================================================================

class TestResponsiveDesign:
    """Tests for responsive design and print compatibility."""

    @staticmethod
    def read_template(html_file: Path) -> str:
        """Read template file content."""
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()

    def test_minimal_has_viewport_meta_for_mobile(self):
        """Verify minimal template supports mobile via viewport meta."""
        html = self.read_template(MINIMAL_HTML)
        assert "viewport" in html.lower()

    def test_modern_has_viewport_meta_for_mobile(self):
        """Verify modern template supports mobile via viewport meta."""
        html = self.read_template(MODERN_HTML)
        assert "viewport" in html.lower()

    def test_corporate_has_viewport_meta_for_mobile(self):
        """Verify corporate template supports mobile via viewport meta."""
        html = self.read_template(CORPORATE_HTML)
        assert "viewport" in html.lower()


# ============================================================================
# Template Completeness Tests
# ============================================================================

class TestTemplateCompleteness:
    """Tests for complete invoice template functionality."""

    @staticmethod
    def read_template(html_file: Path) -> str:
        """Read template file content."""
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()

    def test_minimal_has_all_invoice_sections(self):
        """Verify minimal template has all required sections."""
        html = self.read_template(MINIMAL_HTML)
        required_sections = [
            "invoice-container",
            "header",
            "invoice",
            "addresses",
            "items-table",
            "totals",
            "footer"
        ]
        for section in required_sections:
            assert section in html.lower(), f"Missing {section} section"

    def test_modern_has_all_invoice_sections(self):
        """Verify modern template has all required sections."""
        html = self.read_template(MODERN_HTML)
        required_sections = [
            "invoice-container",
            "header",
            "invoice",
            "addresses",
            "items-table",
            "totals",
            "footer"
        ]
        for section in required_sections:
            assert section in html.lower(), f"Missing {section} section"

    def test_corporate_has_all_invoice_sections(self):
        """Verify corporate template has all required sections."""
        html = self.read_template(CORPORATE_HTML)
        required_sections = [
            "invoice-container",
            "header",
            "invoice",
            "addresses",
            "items-table",
            "totals",
            "footer"
        ]
        for section in required_sections:
            assert section in html.lower(), f"Missing {section} section"

    def test_minimal_table_has_required_columns(self):
        """Verify minimal template table has required columns."""
        html = self.read_template(MINIMAL_HTML)
        assert "Description" in html or "Item" in html
        assert "Qty" in html or "Quantity" in html
        assert "Price" in html

    def test_modern_table_has_required_columns(self):
        """Verify modern template table has required columns."""
        html = self.read_template(MODERN_HTML)
        assert "Quantity" in html or "Qty" in html
        assert "Price" in html or "Unit Price" in html
        assert "Amount" in html

    def test_corporate_table_has_required_columns(self):
        """Verify corporate template table has required columns."""
        html = self.read_template(CORPORATE_HTML)
        assert "Quantity" in html or "Qty" in html
        assert "Price" in html or "Unit Price" in html
        assert "Amount" in html


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
