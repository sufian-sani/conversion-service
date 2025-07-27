from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from services.pdf_to_html import convert_pdf_to_html_via_docx
from services.docx_to_html import convert_docx_to_html
from services.pdf_to_docx import convert_pdf_to_docx
from services.doc_to_pdf import convert_doc_to_pdf
from services.html_to_pdf import convert_html_to_pdf

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/html", StaticFiles(directory="uploads/html"), name="html")
app.mount("/doc-html", StaticFiles(directory="uploads/doc-html"), name="doc-html")
app.mount("/pdf-doc", StaticFiles(directory="uploads/pdf-doc"), name="pdf-doc")
app.mount("/pdf-html", StaticFiles(directory="uploads/pdf-html"), name="pdf-html")
app.mount("/doc-pdf", StaticFiles(directory="uploads/doc-pdf"), name="doc-pdf")
app.mount("/html-pdf", StaticFiles(directory="uploads/html-pdf"), name="html-pdf")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/convert/pdf-to-html")
async def pdf_form(request: Request):
    return templates.TemplateResponse("pdf_to_html.html", {"request": request})


@app.post("/convert/pdf-to-html")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    text, html_filename = await convert_pdf_to_html_via_docx(file)
    return templates.TemplateResponse("pdf_to_html.html", {
        "request": request,
        "converted": True,
        "content": text,
        "download_link": f"/pdf-html/{html_filename}" if html_filename else None
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
        "download_link": f"/pdf-doc/{docx_filename}" if docx_filename else None
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
        "download_link": f"/doc-html/{html_filename}" if html_filename else None
    })


# word to pdf
@app.get("/convert/doc-to-pdf")
async def doc_to_pdf_form(request: Request):
    return templates.TemplateResponse("doc-to-pdf-convert.html", {"request": request})

@app.post("/convert/doc-to-pdf")
async def upload_docx_pdf(request: Request, file: UploadFile = File(...)):
    pdf_filename = await convert_doc_to_pdf(file)
    return templates.TemplateResponse("doc-to-pdf-convert.html", {
        "request": request,
        "converted": bool(pdf_filename),
        "download_link": f"/doc-pdf/{pdf_filename}" if pdf_filename else None
    })

# html to pdf
@app.get("/convert/html-to-pdf")
async def html_to_pdf_form(request: Request):
    return templates.TemplateResponse("html_to_pdf.html", {"request": request})

@app.post("/convert/html-to-pdf")
async def html_to_pdf_upload(request: Request, file: UploadFile = File(...)):
    pdf_filename = await convert_html_to_pdf(file)
    return templates.TemplateResponse("html_to_pdf.html", {
        "request": request,
        "converted": bool(pdf_filename),
        "download_link": f"/html-pdf/{pdf_filename}" if pdf_filename else None
    })