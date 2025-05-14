import os, uuid
from pdf2docx import Converter

UPLOAD_DIR = "uploads/html"

async def convert_pdf_to_docx(file) -> str:
    if not file.filename.endswith(".pdf"):
        return ""

    pdf_filename = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join(UPLOAD_DIR, pdf_filename)

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    docx_filename = f"{uuid.uuid4()}.docx"
    docx_path = os.path.join(UPLOAD_DIR, docx_filename)

    try:
        converter = Converter(pdf_path)
        converter.convert(docx_path, start=0, end=None)
        converter.close()
    except Exception:
        return ""
    finally:
        os.remove(pdf_path)

    return docx_filename
