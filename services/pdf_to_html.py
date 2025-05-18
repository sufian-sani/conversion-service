import os, uuid
from PyPDF2 import PdfReader

UPLOAD_DIR = "uploads/pdf-html"

async def convert_pdf_to_text(file) -> tuple[str, str]:
    if not file.filename.endswith(".pdf"):
        return "", ""

    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.pdf")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(file_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    html_filename = f"{uuid.uuid4()}.html"
    html_path = os.path.join(UPLOAD_DIR, html_filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"<html><body><pre>{text}</pre></body></html>")

    os.remove(file_path)
    return text, html_filename
