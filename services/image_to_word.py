import os
import tempfile
from docx import Document
from docx.shared import Inches
from fastapi import UploadFile

async def convert_images_to_word(files: list[UploadFile]) -> str:
    with tempfile.TemporaryDirectory() as tmpdirname:
        doc = Document()

        for file in files:
            img_path = os.path.join(tmpdirname, file.filename)
            with open(img_path, "wb") as f:
                f.write(await file.read())

            # Insert image into Word doc (scaled to width = 5 inches)
            doc.add_picture(img_path, width=Inches(5))
            doc.add_page_break()

        # Save Word file
        output_path = "static/output.docx"
        os.makedirs("static", exist_ok=True)
        doc.save(output_path)

        return output_path
