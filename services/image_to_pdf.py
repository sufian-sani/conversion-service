import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from fastapi import UploadFile

async def convert_images_to_pdf(files: list[UploadFile]) -> str:
    """
    Convert uploaded images to a single PDF.
    Returns the output PDF path.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        pdf_path = os.path.join(tmpdirname, "output.pdf")

        # Create PDF
        c = canvas.Canvas(pdf_path, pagesize=letter)

        for file in files:
            img_path = os.path.join(tmpdirname, file.filename)
            with open(img_path, "wb") as f:
                f.write(await file.read())

            img = Image.open(img_path)
            width, height = img.size

            # Scale image to fit page
            page_width, page_height = letter
            scale = min(page_width / width, page_height / height)
            new_width, new_height = width * scale, height * scale

            x = (page_width - new_width) / 2
            y = (page_height - new_height) / 2

            c.drawImage(img_path, x, y, new_width, new_height)
            c.showPage()

        c.save()

        # Save PDF to static folder so it can be viewed/downloaded
        output_path = "static/output.pdf"
        os.makedirs("static", exist_ok=True)
        os.replace(pdf_path, output_path)

        return output_path
