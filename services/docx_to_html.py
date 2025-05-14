import os, uuid
import mammoth

UPLOAD_DIR = "uploads/html"

async def convert_docx_to_html(file) -> tuple[str, str]:
    if not file.filename.endswith(".docx"):
        return "", ""

    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.docx")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    with open(file_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html_content = result.value  # This is the clean HTML

    html_filename = f"{uuid.uuid4()}.html"
    html_path = os.path.join(UPLOAD_DIR, html_filename)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"<html><body>{html_content}</body></html>")

    os.remove(file_path)
    return html_content, html_filename