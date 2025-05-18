import os
import uuid
import mammoth
from fastapi import UploadFile
from tempfile import SpooledTemporaryFile
from pdf2docx import Converter

UPLOAD_DIR = "uploads/pdf-html"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_pdf_to_disk(file: UploadFile) -> str:
    """Save uploaded PDF to disk and return the path."""
    pdf_filename = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join(UPLOAD_DIR, pdf_filename)
    with open(pdf_path, "wb") as f:
        f.write(await file.read())
    return pdf_path


def convert_pdf_to_docx_file(pdf_path: str) -> str:
    """Convert saved PDF file to DOCX and return its path."""
    docx_filename = f"{uuid.uuid4()}.docx"
    docx_path = os.path.join(UPLOAD_DIR, docx_filename)
    try:
        converter = Converter(pdf_path)
        converter.convert(docx_path)
        converter.close()
        return docx_path
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


async def convert_docx_file_to_html(docx_path: str) -> tuple[str, str]:
    """Convert DOCX file on disk to HTML using mammoth and return content + filename."""
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html_content = result.value

    html_filename = f"{uuid.uuid4()}.html"
    html_path = os.path.join(UPLOAD_DIR, html_filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"<html><body>{html_content}</body></html>")

    if os.path.exists(docx_path):
        os.remove(docx_path)

    return html_content, html_filename


async def convert_pdf_to_html_via_docx(file: UploadFile) -> tuple[str, str]:
    """
    High-level function: Converts uploaded PDF to HTML by:
    1. Saving PDF
    2. Converting PDF → DOCX
    3. Converting DOCX → HTML
    """
    if not file.filename.endswith(".pdf"):
        return "", ""

    pdf_path = await save_pdf_to_disk(file)
    docx_path = convert_pdf_to_docx_file(pdf_path)
    html_content, html_filename = await convert_docx_file_to_html(docx_path)
    return html_content, html_filename
