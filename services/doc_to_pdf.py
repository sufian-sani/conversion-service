import os
import uuid
import subprocess

UPLOAD_DIR = "uploads/doc-pdf"
PDF_DIR = "uploads/doc-pdf"  # keep in the same folder for easy access

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

async def convert_doc_to_pdf(file) -> str:
    """
    Converts a DOC/DOCX file to PDF and returns the PDF filename.
    """
    if not (file.filename.endswith(".docx") or file.filename.endswith(".doc")):
        return ""

    # ✅ Save uploaded DOC/DOCX file
    ext = os.path.splitext(file.filename)[1]
    saved_docx_filename = f"{uuid.uuid4()}{ext}"
    saved_docx_path = os.path.join(UPLOAD_DIR, saved_docx_filename)

    with open(saved_docx_path, "wb") as f:
        f.write(await file.read())

    # ✅ Convert DOC/DOCX to PDF using LibreOffice
    try:
        subprocess.run([
            "libreoffice", "--headless",
            "--convert-to", "pdf",
            "--outdir", PDF_DIR,
            saved_docx_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e}")
        return ""

    # ✅ Find generated PDF name (LibreOffice uses original filename)
    pdf_filename = f"{os.path.splitext(os.path.basename(saved_docx_filename))[0]}.pdf"
    pdf_path = os.path.join(PDF_DIR, pdf_filename)

    # ✅ Delete original DOC/DOCX to save space
    if os.path.exists(saved_docx_path):
        os.remove(saved_docx_path)

    # ✅ Ensure the PDF was generated
    if not os.path.exists(pdf_path):
        print("PDF was not generated!")
        return ""

    return pdf_filename
