import os
import uuid
import subprocess

UPLOAD_DIR = "uploads/doc-pdf"
PDF_DIR = "uploads/pdf"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

async def convert_doc_to_pdf(file) -> tuple[str, str]:
    """
    Converts a DOC/DOCX file to PDF and returns:
    (pdf_filename, pdf_filename_for_url)
    """
    if not (file.filename.endswith(".docx") or file.filename.endswith(".doc")):
        return "", ""

    # ✅ Save uploaded DOC/DOCX file
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # ✅ Convert DOC/DOCX to PDF using LibreOffice (headless mode)
    subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf",
        "--outdir", PDF_DIR, file_path
    ], check=True)

    # ✅ PDF file name (same as saved file, but with .pdf extension)
    pdf_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}.pdf"

    # ✅ Optionally delete the original DOC/DOCX file (like you did in HTML version)
    os.remove(file_path)

    return pdf_filename, pdf_filename
