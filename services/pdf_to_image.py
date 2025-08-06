import os
import uuid
import fitz  # PyMuPDF

UPLOAD_DIR = "uploads/pdf-images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def convert_pdf_to_images(file) -> list[str]:
    """
    Converts an uploaded PDF file to images (one per page).
    Returns list of image filenames.
    """
    if not file.filename.endswith(".pdf"):
        return []

    # ✅ Save uploaded PDF file
    pdf_filename = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join(UPLOAD_DIR, pdf_filename)

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # ✅ Convert PDF to images
    doc = fitz.open(pdf_path)
    image_filenames = []

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        image_filename = f"{uuid.uuid4()}.png"
        image_path = os.path.join(UPLOAD_DIR, image_filename)
        pix.save(image_path)
        image_filenames.append(image_filename)

    doc.close()
    os.remove(pdf_path)  # clean up original

    return image_filenames
