# Dynamic Invoice Templates - Jinja2 Implementation

## Overview

The AutoInvo project includes **3 dynamic Jinja2-based invoice templates** that support variable injection for generating personalized invoices. Each template is available in both static HTML and dynamic Jinja2 formats.

## Template Files

### Static HTML Templates (for reference/display)
- `templates/minimal-invoice.html` - Basic static example
- `templates/modern-invoice.html` - Modern static example
- `templates/corporate-invoice.html` - Corporate static example

### Dynamic Jinja2 Templates (for rendering)
- `templates/minimal-invoice.jinja2` - Minimal design with Jinja2 variables
- `templates/modern-invoice.jinja2` - Modern design with Jinja2 variables
- `templates/corporate-invoice.jinja2` - Corporate design with Jinja2 variables

### External Stylesheets
- `templates/styles/minimal.css` - Minimal template styles
- `templates/styles/modern.css` - Modern template styles
- `templates/styles/corporate.css` - Corporate template styles

## Template Variables

Each template uses the following variable structure:

### Company Information
```python
company = {
    "name": str,              # Company legal name
    "address": str,           # Street address
    "city": str,              # City name
    "state": str,             # State/Province code
    "zip": str,               # Postal code
    "email": str,             # Contact email
    "phone": str,             # Phone number
    "website": str,           # Website URL (optional)
    "headquarters": str,      # Full headquarters address (corporate template)
    "fax": str,               # Fax number (corporate template)
    "year": int,              # Year for footer (modern template)
    "tax_id": str,            # Federal tax ID (corporate template)
}
```

### Invoice Metadata
```python
invoice = {
    "number": str,            # Invoice number (e.g., "INV-2024-001234")
    "date": str,              # Issue date (e.g., "June 24, 2024")
    "due_date": str,          # Payment due date
    "po_number": str,         # Purchase order number
    "status": str,            # Status (e.g., "pending", "sent", "paid")
    "payment_method": str,    # Payment method
    "payment_terms": str,     # Payment terms description
    "notes": str,             # Additional notes
    "footer_text": str,       # Footer message
    "client_reference": str,  # Client reference code (corporate)
    "banking_details": str,   # Banking information (modern/corporate)
    "service_terms": str,     # Service terms (corporate)
    "warranty": str,          # Warranty information (corporate)
    "late_payment_policy": str, # Late payment policy (corporate)
    "footer_notes": str,      # Footer notes (corporate)
}
```

### Client Information
```python
client = {
    "name": str,              # Contact person name
    "company": str,           # Company name
    "address": str,           # Street address
    "city": str,              # City
    "state": str,             # State/Province
    "zip": str,               # Postal code
    "email": str,             # Email address
    "contact_person": str,    # Contact person (corporate)
    "title": str,             # Job title (corporate)
    "country": str,           # Country (corporate)
    "tax_id": str,            # Client tax ID (corporate)
}
```

### Shipping Information
```python
shipping = {
    "name": str,              # Recipient name
    "company": str,           # Company name
    "address": str,           # Street address
    "city": str,              # City
    "state": str,             # State/Province
    "zip": str,               # Postal code
    "department": str,        # Department (corporate)
    "country": str,           # Country (corporate)
}
```

### Line Items (Array)
```python
items = [
    {
        "description": str,   # Item/service description
        "quantity": float,    # Quantity
        "unit_price": float,  # Price per unit
    },
    # ... more items
]
```

### Totals
```python
totals = {
    "subtotal": float,        # Subtotal before tax
    "tax": float,             # Tax amount
    "shipping": float,        # Shipping cost (optional, corporate)
    "total": float,           # Final total amount
}
```

### Tax Rate
```python
tax_rate = 0.10  # 10% (as decimal)
```

## Usage Examples

### Basic Usage with Jinja2

```python
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# Setup environment
templates_dir = Path("templates")
env = Environment(loader=FileSystemLoader(str(templates_dir)))

# Load template
template = env.get_template("minimal-invoice.jinja2")

# Prepare context data
context = {
    "company": {
        "name": "My Company",
        "address": "123 Main St",
        "city": "Boston",
        "state": "MA",
        "zip": "02101",
        "email": "info@mycompany.com",
        "phone": "(617) 555-0100",
    },
    "invoice": {
        "number": "INV-2024-001",
        "date": "June 25, 2024",
        "due_date": "July 25, 2024",
        "po_number": "PO-2024-001",
        "notes": "Thank you for your business!",
        "footer_text": "Thank you!",
    },
    "client": {
        "name": "John Doe",
        "company": "Client Corp",
        "address": "456 Client Ave",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "email": "john@client.com",
    },
    "shipping": {
        "name": "John Doe",
        "company": "Client Corp",
        "address": "456 Client Ave",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
    },
    "items": [
        {
            "description": "Service A",
            "quantity": 10,
            "unit_price": 100.00,
        },
    ],
    "totals": {
        "subtotal": 1000.00,
        "tax": 100.00,
        "total": 1100.00,
    },
    "tax_rate": 0.10,
}

# Render template
html = template.render(context)
print(html)
```

### Convert to PDF with WeasyPrint

```python
from weasyprint import HTML

# Render template to HTML string (as above)
html_string = template.render(context)

# Convert to PDF
HTML(string=html_string).write_pdf("invoice.pdf")
```

### Save as HTML File

```python
with open("invoice.html", "w", encoding="utf-8") as f:
    f.write(html_string)
```

## Jinja2 Features Used

### Variable Substitution
```jinja2
{{ company.name }}
{{ invoice.number }}
{{ client.email }}
```

### Loops (for line items)
```jinja2
{% for item in items %}
  <tr>
    <td>{{ item.description }}</td>
    <td>{{ item.quantity }}</td>
    <td>${{ "%.2f"|format(item.unit_price) }}</td>
    <td>${{ "%.2f"|format(item.quantity * item.unit_price) }}</td>
  </tr>
{% endfor %}
```

### Conditionals (for optional fields)
```jinja2
{% if invoice.banking_details %}
  <strong>Banking Details:</strong> {{ invoice.banking_details }}<br>
{% endif %}

{% if totals.shipping %}
  <div>Shipping: ${{ "%.2f"|format(totals.shipping) }}</div>
{% endif %}
```

### Filters (for formatting)
```jinja2
{{ "%.2f"|format(total_amount) }}  <!-- Format as currency -->
{{ invoice.status|upper }}          <!-- Convert to uppercase -->
{{ tax_rate * 100 }}                <!-- Arithmetic operations -->
```

## Test Coverage

### Static Template Tests (78 tests)
- File structure validation
- HTML5 compliance
- CSS linking
- Meta tags presence
- Invoice section presence
- Content validation

**Run with:** `python -m pytest tests/test_templates.py -v`

### Jinja2 Template Tests (51 tests)
- Template file existence
- Jinja2 syntax validity
- Variable declarations
- Template rendering
- Rendered content validation
- Edge cases (empty items, multiple items, calculations)

**Run with:** `python -m pytest tests/test_jinja2_templates.py -v`

### All Tests (129 total)
**Run with:** `python -m pytest tests/test_templates.py tests/test_jinja2_templates.py -v`

## Template Design Differences

### Minimal Template
- **Design:** Clean, simplistic, bare essentials
- **Colors:** Mostly black and white with minimal gray
- **Features:** Basic layout, easy to customize
- **Best for:** Simple transactions, basic invoicing

### Modern Template
- **Design:** Contemporary with blue accents
- **Colors:** Blue (#3498db), dark gray, light background
- **Features:** Grid layout, colored headers, status badges
- **Best for:** Tech companies, modern businesses, professional look

### Corporate Template
- **Design:** Formal, professional, corporate standard
- **Colors:** Dark blue (#1a3a5c), white, structured borders
- **Features:** Formal typography, borders, terms & conditions section
- **Best for:** Enterprise clients, formal invoicing, government contracts

## Integration with AutoInvo Core

To integrate with the main PDF generation:

```python
from autoinvo import AutoInvo, PdfOptions
from jinja2 import Environment, FileSystemLoader

# Render Jinja2 template
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("minimal-invoice.jinja2")
html = template.render(context)

# Generate PDF
autoinvo = AutoInvo()
pdf_bytes = autoinvo.generate_pdf(html, PdfOptions())

# Save to file
with open("invoice.pdf", "wb") as f:
    f.write(pdf_bytes)
```

## Print Optimization

All templates include `@media print` CSS rules for:
- Removing shadows and backgrounds for printing
- Optimizing margins and spacing
- Ensuring page breaks work correctly
- Maintaining professional appearance in print

## Variable Formatting Tips

### Currency Formatting
```jinja2
${{ "%.2f"|format(amount) }}  <!-- $1,234.56 -->
```

### Percentage Formatting
```jinja2
{{ tax_rate * 100 }}%  <!-- 10% -->
```

### Calculations in Templates
```jinja2
{{ item.quantity * item.unit_price }}  <!-- Inline calculations -->
```

### Upper/Lower Case
```jinja2
{{ status|upper }}    <!-- Convert to uppercase -->
{{ text|lower }}      <!-- Convert to lowercase -->
```

## Extending Templates

To add custom variables:

1. **In context dict:** Add new variables before rendering
   ```python
   context["custom_field"] = "value"
   ```

2. **In template:** Use the variable
   ```jinja2
   {{ custom_field }}
   ```

3. **With conditionals:**
   ```jinja2
   {% if custom_field %}
     <div>{{ custom_field }}</div>
   {% endif %}
   ```

## Error Handling

Common issues and solutions:

### TemplateNotFound Error
- **Cause:** Template file path is incorrect
- **Solution:** Verify template filename and directory path

### UndefinedError
- **Cause:** Variable not provided in context
- **Solution:** Add missing variable to context dictionary

### TypeError in Calculations
- **Cause:** Non-numeric values in calculations
- **Solution:** Ensure quantity and unit_price are numbers

## Performance Considerations

- Templates are compiled once and can be reused
- For batch processing, cache the compiled templates:
  ```python
  template = env.get_template("minimal-invoice.jinja2")
  for invoice_data in batch:
      html = template.render(invoice_data)
      # Process...
  ```

## Related Files

- `templates/minimal-invoice.jinja2` - Template source
- `templates/styles/minimal.css` - Associated stylesheet
- `tests/test_jinja2_templates.py` - Test suite
- `tests/examples/render_jinja2_invoices.py` - Usage examples

## Dependencies

- **jinja2>=3.0** - Template engine
- **weasyprint>=61.0** - PDF generation (optional, for PDF conversion)
