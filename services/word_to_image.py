import os
import subprocess
from datetime import datetime
from fastapi import UploadFile
from pdf2image import convert_from_path

UPLOAD_DIR = "uploads/word-image"

async def convert_docx_to_images(file: UploadFile) -> list[str]:
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Unique folder per upload
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        folder_path = os.path.join(UPLOAD_DIR, timestamp)
        os.makedirs(folder_path, exist_ok=True)

        # Save DOCX
        docx_path = os.path.join(folder_path, file.filename)
        with open(docx_path, "wb") as f:
            f.write(await file.read())

        # Convert DOCX to PDF using LibreOffice headless
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf",
            "--outdir", folder_path, docx_path
        ], check=True)

        pdf_path = docx_path.replace(".docx", ".pdf")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError("PDF conversion failed")

        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=200)
        image_urls = []
        for i, img in enumerate(images):
            img_name = f"page_{i+1}.png"
            img_path = os.path.join(folder_path, img_name)
            img.save(img_path, "PNG")
            image_urls.append(f"/word-image/{timestamp}/{img_name}")

        return image_urls

    except Exception as e:
        raise RuntimeError(str(e))
