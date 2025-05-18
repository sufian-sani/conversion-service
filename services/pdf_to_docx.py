import os
import uuid
import fitz  # PyMuPDF
from pdf2docx import Converter
from docx import Document
from docx.shared import Inches
from fastapi import UploadFile

UPLOAD_DIR = "uploads/pdf-doc"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def convert_pdf_to_docx(uploaded_file: UploadFile) -> str:
    """
    Save PDF, convert it to DOCX, adjust margins, and return DOCX filename.
    """
    # Save uploaded PDF to disk
    pdf_filename = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join(UPLOAD_DIR, pdf_filename)

    try:
        with open(pdf_path, "wb") as out_file:
            out_file.write(await uploaded_file.read())
    except Exception as e:
        print(f"Failed to save PDF: {e}")
        return ""

    docx_filename = f"{uuid.uuid4()}.docx"
    docx_path = os.path.join(UPLOAD_DIR, docx_filename)

    try:
        # Convert PDF to DOCX
        converter = Converter(pdf_path)
        converter.convert(docx_path)
        converter.close()

        # Adjust DOCX margins based on original PDF size
        with fitz.open(pdf_path) as doc:
            page = doc[0]
            width_in = round(page.rect.width / 72, 2)
            height_in = round(page.rect.height / 72, 2)

        doc = Document(docx_path)
        for section in doc.sections:
            section.page_width = Inches(width_in)
            section.page_height = Inches(height_in)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
        doc.save(docx_path)

    except Exception as e:
        print(f"Conversion failed: {e}")
        return ""

    finally:
        # Clean up temp PDF file
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

    return docx_filename
