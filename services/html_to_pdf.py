import os
import uuid
from weasyprint import HTML

UPLOAD_DIR = "uploads/html-pdf"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def convert_html_to_pdf(file) -> str:
    """
    Converts an uploaded HTML file to PDF and returns the PDF filename.
    """
    if not file.filename.endswith(".html"):
        return ""

    # ✅ Save uploaded HTML file temporarily
    html_filename = f"{uuid.uuid4()}.html"
    html_path = os.path.join(UPLOAD_DIR, html_filename)

    with open(html_path, "wb") as f:
        f.write(await file.read())

    # ✅ Generate PDF filename & path
    pdf_filename = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join(UPLOAD_DIR, pdf_filename)

    try:
        HTML(html_path).write_pdf(pdf_path)
    except Exception as e:
        print(f"HTML to PDF conversion failed: {e}")
        return ""
    finally:
        # ✅ Delete original HTML after conversion
        if os.path.exists(html_path):
            os.remove(html_path)

    return pdf_filename
