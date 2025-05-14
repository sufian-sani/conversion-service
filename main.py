from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from services.pdf_to_html import convert_pdf_to_text
from services.docx_to_html import convert_docx_to_html
from services.pdf_to_docx import convert_pdf_to_docx

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/html", StaticFiles(directory="uploads/html"), name="html")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/convert/pdf-to-html")
async def pdf_form(request: Request):
    return templates.TemplateResponse("pdf_convert.html", {"request": request})


@app.post("/convert/pdf-to-html")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    text, html_filename = await convert_pdf_to_text(file)
    return templates.TemplateResponse("pdf_convert.html", {
        "request": request,
        "converted": True,
        "content": text,
        "download_link": f"/html/{html_filename}" if html_filename else None
    })

@app.get("/convert/pdf-to-docx")
async def pdf_to_docx_form(request: Request):
    return templates.TemplateResponse("pdf_to_docx.html", {"request": request})


@app.post("/convert/pdf-to-docx")
async def pdf_to_docx_upload(request: Request, file: UploadFile = File(...)):
    docx_filename = await convert_pdf_to_docx(file)
    return templates.TemplateResponse("pdf_to_docx.html", {
        "request": request,
        "converted": bool(docx_filename),
        "download_link": f"/html/{docx_filename}" if docx_filename else None
    })


@app.get("/convert/docx-to-html")
async def docx_form(request: Request):
    return templates.TemplateResponse("docx_convert.html", {"request": request})


@app.post("/convert/docx-to-html")
async def upload_docx(request: Request, file: UploadFile = File(...)):
    text, html_filename = await convert_docx_to_html(file)
    return templates.TemplateResponse("docx_convert.html", {
        "request": request,
        "converted": True,
        "content": text,
        "download_link": f"/html/{html_filename}" if html_filename else None
    })
