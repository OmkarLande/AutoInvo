"""
Example: Using Jinja2 Invoice Templates

This script demonstrates how to use the dynamic Jinja2-based invoice templates
to generate rendered HTML invoices with real data.
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Setup Jinja2 environment pointing to templates directory
TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"
env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))


def render_minimal_invoice():
    """Example: Render minimal invoice template."""
    template = env.get_template("minimal-invoice.jinja2")
    
    context = {
        "company": {
            "name": "ABC Services Inc.",
            "address": "100 Main Street",
            "city": "Boston",
            "state": "MA",
            "zip": "02101",
            "email": "billing@abcservices.com",
            "phone": "(617) 555-0100",
        },
        "invoice": {
            "number": "INV-2024-005001",
            "date": "June 25, 2024",
            "due_date": "July 25, 2024",
            "po_number": "PO-2024-9999",
            "notes": "Payment due within 30 days. Thank you for your business!",
            "footer_text": "Thank you for choosing ABC Services Inc.",
        },
        "client": {
            "name": "Jane Doe",
            "company": "Tech Startup Ltd.",
            "address": "500 Innovation Drive",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94105",
            "email": "jane@techstartup.com",
        },
        "shipping": {
            "name": "Jane Doe",
            "company": "Tech Startup Ltd.",
            "address": "500 Innovation Drive",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94105",
        },
        "items": [
            {
                "description": "Consulting Services - Phase 1",
                "quantity": 20,
                "unit_price": 150.00,
            },
            {
                "description": "Development Hours",
                "quantity": 40,
                "unit_price": 125.00,
            },
            {
                "description": "Deployment & Setup",
                "quantity": 8,
                "unit_price": 200.00,
            },
        ],
        "totals": {
            "subtotal": 9800.00,
            "tax": 980.00,
            "total": 10780.00,
        },
        "tax_rate": 0.10,
    }
    
    html = template.render(context)
    return html


def render_modern_invoice():
    """Example: Render modern invoice template."""
    template = env.get_template("modern-invoice.jinja2")
    
    context = {
        "company": {
            "name": "Creative Digital Studio",
            "address": "250 Tech Park Avenue",
            "city": "Austin",
            "state": "TX",
            "zip": "78701",
            "email": "hello@creativedigital.com",
            "phone": "(512) 555-0100",
            "website": "www.creativedigital.com",
            "year": 2024,
        },
        "invoice": {
            "number": "INV-2024-008521",
            "date": "June 25, 2024",
            "due_date": "July 25, 2024",
            "po_number": "PO-2024-4455",
            "status": "sent",
            "payment_method": "Credit Card",
            "payment_terms": "Net 30 days",
            "banking_details": "Please use credit card or wire transfer.",
            "notes": "Thank you for your partnership! We look forward to working with you on the next phase.",
        },
        "client": {
            "name": "Michael Johnson",
            "company": "Fashion Retail Co.",
            "address": "1000 Fashion Boulevard",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "email": "michael@fashionretail.com",
        },
        "shipping": {
            "name": "Michael Johnson",
            "company": "Fashion Retail Co.",
            "address": "1000 Fashion Boulevard",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
        },
        "items": [
            {
                "description": "Website Redesign - Premium Package",
                "quantity": 1,
                "unit_price": 5000.00,
            },
            {
                "description": "E-commerce Integration",
                "quantity": 1,
                "unit_price": 3500.00,
            },
            {
                "description": "Mobile App Design",
                "quantity": 1,
                "unit_price": 2500.00,
            },
            {
                "description": "Performance Optimization",
                "quantity": 20,
                "unit_price": 125.00,
            },
        ],
        "totals": {
            "subtotal": 14000.00,
            "tax": 1207.50,
            "total": 15207.50,
        },
        "tax_rate": 0.08625,
    }
    
    html = template.render(context)
    return html


def render_corporate_invoice():
    """Example: Render corporate invoice template."""
    template = env.get_template("corporate-invoice.jinja2")
    
    context = {
        "company": {
            "name": "GLOBAL SOLUTIONS CORPORATION",
            "headquarters": "2000 Corporate Drive, Houston, TX 77002",
            "phone": "(713) 555-0100",
            "fax": "(713) 555-0101",
            "email": "contracts@globalsolutions.com",
            "tax_id": "56-7890123",
        },
        "invoice": {
            "number": "GSC-2024-100245",
            "date": "June 25, 2024",
            "due_date": "July 25, 2024",
            "client_reference": "ENTERPRISE-CLIENT-2024",
            "po_number": "PO-2024-7722",
            "payment_terms": "Net 45 days",
            "payment_method": "Wire Transfer",
            "service_terms": "Services governed by Master Service Agreement dated January 1, 2024.",
            "warranty": "24-month hardware warranty included. Software support via separate agreement.",
            "late_payment_policy": "2% interest on payments received after 60 days.",
            "footer_notes": "Questions? Contact accounting@globalsolutions.com or (713) 555-0100 ext. 5001",
        },
        "client": {
            "contact_person": "Dr. Robert Williams",
            "title": "Chief Technology Officer",
            "company": "Enterprise Holdings Inc.",
            "address": "3000 Enterprise Park",
            "city": "Chicago",
            "state": "IL",
            "zip": "60601",
            "country": "United States",
            "email": "robert.williams@enterpriseholdings.com",
            "tax_id": "45-0000001",
        },
        "shipping": {
            "company": "Enterprise Holdings Inc.",
            "department": "IT Procurement",
            "address": "3000 Enterprise Park",
            "city": "Chicago",
            "state": "IL",
            "zip": "60601",
            "country": "United States",
        },
        "items": [
            {
                "description": "Enterprise Software License - 100 Users (Annual)",
                "quantity": 1,
                "unit_price": 50000.00,
            },
            {
                "description": "Implementation & Integration Services",
                "quantity": 150,
                "unit_price": 250.00,
            },
            {
                "description": "Staff Training (2 days, 30 participants)",
                "quantity": 1,
                "unit_price": 15000.00,
            },
            {
                "description": "24/7 Technical Support (12 months)",
                "quantity": 1,
                "unit_price": 25000.00,
            },
        ],
        "totals": {
            "subtotal": 115000.00,
            "tax": 10208.75,
            "shipping": 500.00,
            "total": 125708.75,
        },
        "tax_rate": 0.08875,
    }
    
    html = template.render(context)
    return html


if __name__ == "__main__":
    print("=" * 70)
    print("INVOICE TEMPLATE RENDERING EXAMPLES")
    print("=" * 70)
    
    # Example 1: Minimal Template
    print("\n1. Rendering Minimal Invoice Template...")
    minimal_html = render_minimal_invoice()
    print(f"   Generated {len(minimal_html)} bytes of HTML")
    print(f"   Company: ABC Services Inc.")
    print(f"   Invoice: INV-2024-005001")
    print(f"   Total: $10,780.00")
    
    # Example 2: Modern Template
    print("\n2. Rendering Modern Invoice Template...")
    modern_html = render_modern_invoice()
    print(f"   Generated {len(modern_html)} bytes of HTML")
    print(f"   Company: Creative Digital Studio")
    print(f"   Invoice: INV-2024-008521")
    print(f"   Total: $15,207.50")
    
    # Example 3: Corporate Template
    print("\n3. Rendering Corporate Invoice Template...")
    corporate_html = render_corporate_invoice()
    print(f"   Generated {len(corporate_html)} bytes of HTML")
    print(f"   Company: GLOBAL SOLUTIONS CORPORATION")
    print(f"   Invoice: GSC-2024-100245")
    print(f"   Total: $125,708.75")
    
    print("\n" + "=" * 70)
    print("All templates rendered successfully!")
    print("=" * 70)
    print("\nTo save as PDF files, integrate with weasyprint:")
    print("  from weasyprint import HTML")
    print("  HTML(string=html).write_pdf('invoice.pdf')")
    print("\nTo save as HTML files:")
    print("  with open('invoice.html', 'w') as f:")
    print("      f.write(html)")
