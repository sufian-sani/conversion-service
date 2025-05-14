# pdf_converter.py

import os
import uuid
from fastapi import UploadFile
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract

UPLOAD_DIR = "uploads"
HTML_OUTPUT_DIR = "uploads/html"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(HTML_OUTPUT_DIR, exist_ok=True)

async def convert_pdf_to_text(file: UploadFile) -> tuple[str, str]:
    if not file.filename.endswith(".pdf"):
        return "Only PDF files are supported.", ""

    filename = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        text = extract_text(file_path).strip()
        if not text or text == "\f":
            images = convert_from_path(file_path)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image)

        # Save text to HTML file
        html_content = f"<html><body><pre>{text}</pre></body></html>"
        html_filename = f"{uuid.uuid4()}.html"
        html_path = os.path.join(HTML_OUTPUT_DIR, html_filename)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    except Exception as e:
        return f"Error: {str(e)}", ""
    finally:
        os.remove(file_path)

    return text, html_filename
