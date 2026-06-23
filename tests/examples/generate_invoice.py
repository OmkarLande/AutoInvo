"""Example usage of the autoinvo PDF Generation Engine.

This script demonstrates how to generate a PDF in-memory using autoinvo
with custom styling and layout options.
"""

import sys
from pathlib import Path

# Add src to python path to run without installing
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from autoinvo import AutoInvo, PdfOptions

def main() -> None:
    # 1. Define custom HTML template for the invoice
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Invoice #1024</title>
        <style>
            body {
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                color: #333;
                padding: 10px;
            }
            .invoice-box {
                max-width: 800px;
                margin: auto;
                border: 1px solid #eee;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
                padding: 30px;
                border-radius: 8px;
            }
            .header-table {
                width: 100%;
                margin-bottom: 40px;
            }
            .logo-text {
                font-size: 28px;
                font-weight: bold;
                color: #2563eb;
            }
            .invoice-details {
                text-align: right;
            }
            .details-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            .details-table th {
                background-color: #f3f4f6;
                text-align: left;
                padding: 12px;
                font-weight: 600;
                border-bottom: 2px solid #e5e7eb;
            }
            .details-table td {
                padding: 12px;
                border-bottom: 1px solid #e5e7eb;
            }
            .total-row {
                font-weight: bold;
                font-size: 18px;
            }
            .total-row td {
                border-top: 2px solid #2563eb;
            }
        </style>
    </head>
    <body>
        <div class="invoice-box">
            <table class="header-table">
                <tr>
                    <td>
                        <div class="logo-text">AutoInvo</div>
                        <div>123 Innovation Way<br>Tech Suite 400</div>
                    </td>
                    <td class="invoice-details">
                        <h2>INVOICE</h2>
                        <strong>Invoice #:</strong> 1024<br>
                        <strong>Date:</strong> June 23, 2026<br>
                        <strong>Due Date:</strong> July 23, 2026
                    </td>
                </tr>
            </table>

            <table class="details-table">
                <thead>
                    <tr>
                        <th>Item Description</th>
                        <th>Quantity</th>
                        <th>Unit Price</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Enterprise PDF Generation Engine Integration</td>
                        <td>1</td>
                        <td>$1,500.00</td>
                        <td>$1,500.00</td>
                    </tr>
                    <tr>
                        <td>Custom Templating Extension & Mapping Support</td>
                        <td>1</td>
                        <td>$750.00</td>
                        <td>$750.00</td>
                    </tr>
                    <tr class="total-row">
                        <td colspan="2"></td>
                        <td>Total Due:</td>
                        <td>$2,250.00</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    # 2. Configure layout options
    options = PdfOptions(
        page_size="A4",
        landscape=False,
        margin_top="15mm",
        margin_right="15mm",
        margin_bottom="15mm",
        margin_left="15mm"
    )

    # 3. Instantiate AutoInvo facade (uses WeasyPrintEngine by default)
    print("Initializing AutoInvo engine...")
    autoinvo = AutoInvo()

    # 4. Generate PDF bytes completely in-memory
    print("Generating invoice PDF in-memory...")
    pdf_bytes = autoinvo.generate_pdf(html_content, options=options)

    # 5. Output statistics
    print("\nGeneration Success!")
    print(f"Resulting object type: {type(pdf_bytes)}")
    print(f"File magic bytes: {pdf_bytes[:4]}")
    print(f"Total size: {len(pdf_bytes)} bytes")

if __name__ == "__main__":
    main()
