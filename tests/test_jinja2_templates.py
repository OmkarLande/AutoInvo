"""
Tests for Jinja2 Invoice Templates.

This module contains comprehensive tests for validating the dynamic Jinja2-based
invoice templates (minimal, modern, and corporate). Tests cover:
- Template file existence
- Jinja2 syntax validity
- Variable declarations and usage
- Template rendering with sample data
- Output HTML validation
- Edge cases and error handling
"""

import re
from pathlib import Path
from typing import Dict, Any

import pytest

try:
    from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError, UndefinedError
except ImportError:
    pytest.skip("Jinja2 not installed", allow_module_level=True)


# Template paths
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
JINJA2_MINIMAL = TEMPLATES_DIR / "minimal-invoice.jinja2"
JINJA2_MODERN = TEMPLATES_DIR / "modern-invoice.jinja2"
JINJA2_CORPORATE = TEMPLATES_DIR / "corporate-invoice.jinja2"


# Sample data for rendering tests
SAMPLE_COMPANY = {
    "name": "ACME Corporation",
    "address": "123 Business Street",
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "email": "contact@acme.com",
    "phone": "(555) 123-4567",
    "website": "www.acmecorp.com",
    "headquarters": "123 Business Street, New York, NY 10001",
    "fax": "(555) 123-4568",
    "year": 2024,
    "tax_id": "12-3456789",
}

SAMPLE_INVOICE = {
    "number": "INV-2024-001234",
    "date": "June 24, 2024",
    "due_date": "July 24, 2024",
    "po_number": "PO-2024-5678",
    "status": "pending",
    "payment_method": "Bank Transfer",
    "payment_terms": "Net 30 days from invoice date",
    "notes": "Thank you for your business!",
    "footer_text": "Thank you for your business!",
    "client_reference": "CORP-ACME-2024",
    "banking_details": "Wire transfers preferred. Please reference invoice number with payment.",
    "service_terms": "All services rendered are subject to our Master Service Agreement.",
    "warranty": "All products and services are provided with standard warranties.",
    "late_payment_policy": "Invoices not paid within 60 days subject to 1.5% monthly interest.",
    "footer_notes": "This invoice is a legal document. Please retain for your records.",
}

SAMPLE_CLIENT = {
    "name": "John Smith",
    "company": "ABC Company",
    "address": "456 Client Avenue",
    "city": "Los Angeles",
    "state": "CA",
    "zip": "90001",
    "email": "john.smith@abcco.com",
    "contact_person": "John Smith",
    "title": "VP, Operations",
    "country": "United States",
    "tax_id": "45-1234567",
}

SAMPLE_SHIPPING = {
    "name": "John Smith",
    "company": "ABC Company",
    "address": "456 Client Avenue",
    "city": "Los Angeles",
    "state": "CA",
    "zip": "90001",
    "department": "Receiving Department",
    "country": "United States",
}

SAMPLE_ITEMS = [
    {
        "description": "Web Design Services - Homepage",
        "quantity": 1,
        "unit_price": 1500.00,
    },
    {
        "description": "Frontend Development",
        "quantity": 40,
        "unit_price": 75.00,
    },
    {
        "description": "Database Setup & Configuration",
        "quantity": 8,
        "unit_price": 100.00,
    },
]

SAMPLE_TOTALS = {
    "subtotal": 6260.00,
    "tax": 626.00,
    "shipping": 0.00,
    "total": 6886.00,
}

TAX_RATE = 0.10


def get_jinja_environment() -> Environment:
    """Create and return Jinja2 environment."""
    return Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))


# ============================================================================
# File Existence Tests
# ============================================================================

class TestJinja2FileExistence:
    """Tests for Jinja2 template file existence."""

    def test_minimal_jinja2_template_exists(self):
        """Verify minimal Jinja2 template file exists."""
        assert JINJA2_MINIMAL.exists(), "minimal-invoice.jinja2 not found"
        assert JINJA2_MINIMAL.is_file(), "minimal-invoice.jinja2 is not a file"

    def test_modern_jinja2_template_exists(self):
        """Verify modern Jinja2 template file exists."""
        assert JINJA2_MODERN.exists(), "modern-invoice.jinja2 not found"
        assert JINJA2_MODERN.is_file(), "modern-invoice.jinja2 is not a file"

    def test_corporate_jinja2_template_exists(self):
        """Verify corporate Jinja2 template file exists."""
        assert JINJA2_CORPORATE.exists(), "corporate-invoice.jinja2 not found"
        assert JINJA2_CORPORATE.is_file(), "corporate-invoice.jinja2 is not a file"


# ============================================================================
# Jinja2 Syntax Validation Tests
# ============================================================================

class TestJinja2Syntax:
    """Tests for Jinja2 template syntax validity."""

    def test_minimal_jinja2_has_valid_syntax(self):
        """Verify minimal template has valid Jinja2 syntax."""
        env = get_jinja_environment()
        try:
            env.get_template("minimal-invoice.jinja2")
        except TemplateSyntaxError as e:
            pytest.fail(f"Minimal template has syntax error: {e}")

    def test_modern_jinja2_has_valid_syntax(self):
        """Verify modern template has valid Jinja2 syntax."""
        env = get_jinja_environment()
        try:
            env.get_template("modern-invoice.jinja2")
        except TemplateSyntaxError as e:
            pytest.fail(f"Modern template has syntax error: {e}")

    def test_corporate_jinja2_has_valid_syntax(self):
        """Verify corporate template has valid Jinja2 syntax."""
        env = get_jinja_environment()
        try:
            env.get_template("corporate-invoice.jinja2")
        except TemplateSyntaxError as e:
            pytest.fail(f"Corporate template has syntax error: {e}")


# ============================================================================
# Variable Usage Tests
# ============================================================================

class TestJinja2Variables:
    """Tests for Jinja2 variable declarations and usage."""

    @staticmethod
    def read_template(template_file: Path) -> str:
        """Read template file content."""
        with open(template_file, "r", encoding="utf-8") as f:
            return f.read()

    def test_minimal_uses_company_variables(self):
        """Verify minimal template uses company variables."""
        content = self.read_template(JINJA2_MINIMAL)
        assert "{{ company.name }}" in content
        assert "{{ company.address }}" in content
        assert "{{ company.email }}" in content
        assert "{{ company.phone }}" in content

    def test_modern_uses_company_variables(self):
        """Verify modern template uses company variables."""
        content = self.read_template(JINJA2_MODERN)
        assert "{{ company.name }}" in content
        assert "{{ company.email }}" in content
        assert "{{ company.phone }}" in content

    def test_corporate_uses_company_variables(self):
        """Verify corporate template uses company variables."""
        content = self.read_template(JINJA2_CORPORATE)
        assert "{{ company.name }}" in content
        assert "{{ company.phone }}" in content

    def test_minimal_uses_invoice_variables(self):
        """Verify minimal template uses invoice variables."""
        content = self.read_template(JINJA2_MINIMAL)
        assert "{{ invoice.number }}" in content
        assert "{{ invoice.date }}" in content
        assert "{{ invoice.due_date }}" in content

    def test_modern_uses_invoice_variables(self):
        """Verify modern template uses invoice variables."""
        content = self.read_template(JINJA2_MODERN)
        assert "{{ invoice.number }}" in content
        assert "{{ invoice.date }}" in content

    def test_corporate_uses_invoice_variables(self):
        """Verify corporate template uses invoice variables."""
        content = self.read_template(JINJA2_CORPORATE)
        assert "{{ invoice.number }}" in content
        assert "{{ invoice.date }}" in content

    def test_minimal_uses_client_variables(self):
        """Verify minimal template uses client variables."""
        content = self.read_template(JINJA2_MINIMAL)
        assert "{{ client.name }}" in content
        assert "{{ client.company }}" in content
        assert "{{ client.email }}" in content

    def test_modern_uses_client_variables(self):
        """Verify modern template uses client variables."""
        content = self.read_template(JINJA2_MODERN)
        assert "{{ client.name }}" in content
        assert "{{ client.company }}" in content

    def test_corporate_uses_client_variables(self):
        """Verify corporate template uses client variables."""
        content = self.read_template(JINJA2_CORPORATE)
        assert "{{ client.contact_person }}" in content
        assert "{{ client.company }}" in content

    def test_templates_use_items_loop(self):
        """Verify templates use for loop for line items."""
        minimal = self.read_template(JINJA2_MINIMAL)
        modern = self.read_template(JINJA2_MODERN)
        corporate = self.read_template(JINJA2_CORPORATE)

        assert "{% for item in items %}" in minimal
        assert "{% for item in items %}" in modern
        assert "{% for item in items %}" in corporate

        assert "{% endfor %}" in minimal
        assert "{% endfor %}" in modern
        assert "{% endfor %}" in corporate

    def test_templates_use_item_properties(self):
        """Verify templates use item properties in loop."""
        minimal = self.read_template(JINJA2_MINIMAL)
        modern = self.read_template(JINJA2_MODERN)
        corporate = self.read_template(JINJA2_CORPORATE)

        for template_content in [minimal, modern, corporate]:
            assert "{{ item.description }}" in template_content
            assert "{{ item.quantity }}" in template_content
            assert "item.unit_price" in template_content

    def test_templates_use_totals_variables(self):
        """Verify templates use totals variables."""
        minimal = self.read_template(JINJA2_MINIMAL)
        modern = self.read_template(JINJA2_MODERN)
        corporate = self.read_template(JINJA2_CORPORATE)

        for template_content in [minimal, modern, corporate]:
            assert "totals.subtotal" in template_content
            assert "totals.tax" in template_content
            assert "totals.total" in template_content

    def test_templates_use_tax_rate_variable(self):
        """Verify templates use tax_rate variable."""
        minimal = self.read_template(JINJA2_MINIMAL)
        modern = self.read_template(JINJA2_MODERN)
        corporate = self.read_template(JINJA2_CORPORATE)

        for template_content in [minimal, modern, corporate]:
            assert "{{ tax_rate" in template_content


# ============================================================================
# Jinja2 Filters Tests
# ============================================================================

class TestJinja2Filters:
    """Tests for Jinja2 filters usage."""

    @staticmethod
    def read_template(template_file: Path) -> str:
        """Read template file content."""
        with open(template_file, "r", encoding="utf-8") as f:
            return f.read()

    def test_templates_use_format_filter(self):
        """Verify templates use format filter for currency."""
        minimal = self.read_template(JINJA2_MINIMAL)
        modern = self.read_template(JINJA2_MODERN)
        corporate = self.read_template(JINJA2_CORPORATE)

        for template_content in [minimal, modern, corporate]:
            assert '"|format(' in template_content or "|format(" in template_content

    def test_templates_use_upper_filter(self):
        """Verify templates use upper filter where applicable."""
        modern = self.read_template(JINJA2_MODERN)
        assert "|upper" in modern


# ============================================================================
# Template Rendering Tests
# ============================================================================

class TestJinja2Rendering:
    """Tests for rendering Jinja2 templates with sample data."""

    @staticmethod
    def get_context() -> Dict[str, Any]:
        """Get sample context data for rendering."""
        return {
            "company": SAMPLE_COMPANY,
            "invoice": SAMPLE_INVOICE,
            "client": SAMPLE_CLIENT,
            "shipping": SAMPLE_SHIPPING,
            "items": SAMPLE_ITEMS,
            "totals": SAMPLE_TOTALS,
            "tax_rate": TAX_RATE,
        }

    def test_minimal_renders_successfully(self):
        """Verify minimal template renders without errors."""
        env = get_jinja_environment()
        template = env.get_template("minimal-invoice.jinja2")
        html = template.render(self.get_context())
        assert isinstance(html, str)
        assert len(html) > 0

    def test_modern_renders_successfully(self):
        """Verify modern template renders without errors."""
        env = get_jinja_environment()
        template = env.get_template("modern-invoice.jinja2")
        html = template.render(self.get_context())
        assert isinstance(html, str)
        assert len(html) > 0

    def test_corporate_renders_successfully(self):
        """Verify corporate template renders without errors."""
        env = get_jinja_environment()
        template = env.get_template("corporate-invoice.jinja2")
        html = template.render(self.get_context())
        assert isinstance(html, str)
        assert len(html) > 0

    def test_minimal_rendered_output_is_valid_html(self):
        """Verify minimal rendered output is valid HTML."""
        env = get_jinja_environment()
        template = env.get_template("minimal-invoice.jinja2")
        html = template.render(self.get_context())
        assert html.startswith("<!DOCTYPE html>") or "<!doctype html>" in html.lower()
        assert "<html" in html
        assert "</html>" in html

    def test_modern_rendered_output_is_valid_html(self):
        """Verify modern rendered output is valid HTML."""
        env = get_jinja_environment()
        template = env.get_template("modern-invoice.jinja2")
        html = template.render(self.get_context())
        assert html.startswith("<!DOCTYPE html>") or "<!doctype html>" in html.lower()
        assert "<html" in html
        assert "</html>" in html

    def test_corporate_rendered_output_is_valid_html(self):
        """Verify corporate rendered output is valid HTML."""
        env = get_jinja_environment()
        template = env.get_template("corporate-invoice.jinja2")
        html = template.render(self.get_context())
        assert html.startswith("<!DOCTYPE html>") or "<!doctype html>" in html.lower()
        assert "<html" in html
        assert "</html>" in html


# ============================================================================
# Rendered Content Tests
# ============================================================================

class TestRenderedContent:
    """Tests for validating rendered template content."""

    @staticmethod
    def get_context() -> Dict[str, Any]:
        """Get sample context data for rendering."""
        return {
            "company": SAMPLE_COMPANY,
            "invoice": SAMPLE_INVOICE,
            "client": SAMPLE_CLIENT,
            "shipping": SAMPLE_SHIPPING,
            "items": SAMPLE_ITEMS,
            "totals": SAMPLE_TOTALS,
            "tax_rate": TAX_RATE,
        }

    def test_minimal_renders_company_name(self):
        """Verify minimal template renders company name."""
        env = get_jinja_environment()
        template = env.get_template("minimal-invoice.jinja2")
        html = template.render(self.get_context())
        assert "ACME Corporation" in html

    def test_modern_renders_company_name(self):
        """Verify modern template renders company name."""
        env = get_jinja_environment()
        template = env.get_template("modern-invoice.jinja2")
        html = template.render(self.get_context())
        assert "ACME Corporation" in html

    def test_corporate_renders_company_name(self):
        """Verify corporate template renders company name."""
        env = get_jinja_environment()
        template = env.get_template("corporate-invoice.jinja2")
        html = template.render(self.get_context())
        assert "ACME Corporation" in html

    def test_minimal_renders_invoice_number(self):
        """Verify minimal template renders invoice number."""
        env = get_jinja_environment()
        template = env.get_template("minimal-invoice.jinja2")
        html = template.render(self.get_context())
        assert "INV-2024-001234" in html

    def test_modern_renders_invoice_number(self):
        """Verify modern template renders invoice number."""
        env = get_jinja_environment()
        template = env.get_template("modern-invoice.jinja2")
        html = template.render(self.get_context())
        assert "INV-2024-001234" in html

    def test_corporate_renders_invoice_number(self):
        """Verify corporate template renders invoice number."""
        env = get_jinja_environment()
        template = env.get_template("corporate-invoice.jinja2")
        html = template.render(self.get_context())
        assert "INV-2024-001234" in html

    def test_minimal_renders_client_name(self):
        """Verify minimal template renders client name."""
        env = get_jinja_environment()
        template = env.get_template("minimal-invoice.jinja2")
        html = template.render(self.get_context())
        assert "John Smith" in html

    def test_modern_renders_client_name(self):
        """Verify modern template renders client name."""
        env = get_jinja_environment()
        template = env.get_template("modern-invoice.jinja2")
        html = template.render(self.get_context())
        assert "John Smith" in html

    def test_corporate_renders_client_name(self):
        """Verify corporate template renders client name."""
        env = get_jinja_environment()
        template = env.get_template("corporate-invoice.jinja2")
        html = template.render(self.get_context())
        assert "John Smith" in html

    def test_minimal_renders_line_items(self):
        """Verify minimal template renders all line items."""
        env = get_jinja_environment()
        template = env.get_template("minimal-invoice.jinja2")
        html = template.render(self.get_context())
        assert "Web Design Services - Homepage" in html
        assert "Frontend Development" in html
        assert "Database Setup & Configuration" in html

    def test_modern_renders_line_items(self):
        """Verify modern template renders all line items."""
        env = get_jinja_environment()
        template = env.get_template("modern-invoice.jinja2")
        html = template.render(self.get_context())
        assert "Web Design Services - Homepage" in html
        assert "Frontend Development" in html
        assert "Database Setup & Configuration" in html

    def test_corporate_renders_line_items(self):
        """Verify corporate template renders all line items."""
        env = get_jinja_environment()
        template = env.get_template("corporate-invoice.jinja2")
        html = template.render(self.get_context())
        assert "Web Design Services - Homepage" in html
        assert "Frontend Development" in html
        assert "Database Setup & Configuration" in html

    def test_minimal_renders_totals(self):
        """Verify minimal template renders total amounts."""
        env = get_jinja_environment()
        template = env.get_template("minimal-invoice.jinja2")
        html = template.render(self.get_context())
        assert "$6260.00" in html or "6260.00" in html
        assert "$626.00" in html or "626.00" in html
        assert "$6886.00" in html or "6886.00" in html

    def test_modern_renders_totals(self):
        """Verify modern template renders total amounts."""
        env = get_jinja_environment()
        template = env.get_template("modern-invoice.jinja2")
        html = template.render(self.get_context())
        assert "$6260.00" in html or "6260.00" in html
        assert "$626.00" in html or "626.00" in html
        assert "$6886.00" in html or "6886.00" in html

    def test_corporate_renders_totals(self):
        """Verify corporate template renders total amounts."""
        env = get_jinja_environment()
        template = env.get_template("corporate-invoice.jinja2")
        html = template.render(self.get_context())
        assert "$6260.00" in html or "6260.00" in html
        assert "$626.00" in html or "626.00" in html
        assert "$6886.00" in html or "6886.00" in html


# ============================================================================
# Edge Cases and Error Handling Tests
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    @staticmethod
    def get_minimal_context() -> Dict[str, Any]:
        """Get minimal context with required fields only."""
        return {
            "company": {"name": "Company", "address": "", "city": "", "state": "", "zip": "", "email": "", "phone": ""},
            "invoice": {
                "number": "INV-001",
                "date": "2024-01-01",
                "due_date": "2024-02-01",
                "po_number": "",
                "status": "draft",
                "payment_method": "",
                "payment_terms": "",
                "notes": "",
                "footer_text": "",
            },
            "client": {
                "name": "Client",
                "company": "",
                "address": "",
                "city": "",
                "state": "",
                "zip": "",
                "email": "",
            },
            "shipping": {
                "name": "Shipping",
                "company": "",
                "address": "",
                "city": "",
                "state": "",
                "zip": "",
            },
            "items": [],
            "totals": {"subtotal": 0.0, "tax": 0.0, "total": 0.0},
            "tax_rate": 0.0,
        }

    def test_minimal_renders_with_empty_items(self):
        """Verify minimal template renders with empty items list."""
        env = get_jinja_environment()
        template = env.get_template("minimal-invoice.jinja2")
        context = self.get_minimal_context()
        html = template.render(context)
        assert isinstance(html, str)
        assert len(html) > 0

    def test_modern_renders_with_empty_items(self):
        """Verify modern template renders with empty items list."""
        env = get_jinja_environment()
        template = env.get_template("modern-invoice.jinja2")
        context = self.get_minimal_context()
        html = template.render(context)
        assert isinstance(html, str)
        assert len(html) > 0

    def test_corporate_renders_with_empty_items(self):
        """Verify corporate template renders with empty items list."""
        env = get_jinja_environment()
        template = env.get_template("corporate-invoice.jinja2")
        context = self.get_minimal_context()
        html = template.render(context)
        assert isinstance(html, str)
        assert len(html) > 0

    def test_templates_render_with_single_item(self):
        """Verify templates render with single item."""
        env = get_jinja_environment()
        context = self.get_minimal_context()
        context["items"] = [
            {
                "description": "Single Item",
                "quantity": 1,
                "unit_price": 100.00,
            }
        ]

        for template_name in ["minimal-invoice.jinja2", "modern-invoice.jinja2", "corporate-invoice.jinja2"]:
            template = env.get_template(template_name)
            html = template.render(context)
            assert "Single Item" in html

    def test_templates_render_with_many_items(self):
        """Verify templates render with many items."""
        env = get_jinja_environment()
        context = self.get_minimal_context()
        context["items"] = [
            {"description": f"Item {i}", "quantity": i, "unit_price": 100.00} for i in range(1, 11)
        ]

        for template_name in ["minimal-invoice.jinja2", "modern-invoice.jinja2", "corporate-invoice.jinja2"]:
            template = env.get_template(template_name)
            html = template.render(context)
            assert "Item 1" in html
            assert "Item 9" in html

    def test_templates_calculate_item_amounts(self):
        """Verify templates calculate item amounts correctly."""
        env = get_jinja_environment()
        context = self.get_minimal_context()
        context["items"] = [
            {"description": "Item A", "quantity": 5, "unit_price": 20.00},
        ]

        for template_name in ["minimal-invoice.jinja2", "modern-invoice.jinja2", "corporate-invoice.jinja2"]:
            template = env.get_template(template_name)
            html = template.render(context)
            # 5 * 20.00 = 100.00
            assert "100.00" in html


# ============================================================================
# Template Comparison Tests
# ============================================================================

class TestTemplateComparison:
    """Tests comparing Jinja2 template structure."""

    @staticmethod
    def read_template(template_file: Path) -> str:
        """Read template file content."""
        with open(template_file, "r", encoding="utf-8") as f:
            return f.read()

    def test_all_templates_have_jinja2_syntax(self):
        """Verify all templates use Jinja2 syntax."""
        minimal = self.read_template(JINJA2_MINIMAL)
        modern = self.read_template(JINJA2_MODERN)
        corporate = self.read_template(JINJA2_CORPORATE)

        for content in [minimal, modern, corporate]:
            assert "{{" in content
            assert "}}" in content
            assert "{%" in content or "{#" in content

    def test_all_templates_render_line_items_dynamically(self):
        """Verify all templates use dynamic line items."""
        minimal = self.read_template(JINJA2_MINIMAL)
        modern = self.read_template(JINJA2_MODERN)
        corporate = self.read_template(JINJA2_CORPORATE)

        for content in [minimal, modern, corporate]:
            assert "for item in items" in content

    def test_jinja2_templates_use_same_variable_names(self):
        """Verify all templates use consistent variable naming."""
        minimal = self.read_template(JINJA2_MINIMAL)
        modern = self.read_template(JINJA2_MODERN)
        corporate = self.read_template(JINJA2_CORPORATE)

        common_vars = ["company", "invoice", "client", "items", "totals", "tax_rate"]

        for template_content in [minimal, modern, corporate]:
            for var in common_vars:
                assert var in template_content, f"Variable '{var}' not found in template"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
