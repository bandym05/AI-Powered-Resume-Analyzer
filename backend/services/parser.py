# backend/services/parser.py
import pdfplumber
from docx import Document
from fastapi import UploadFile

async def extract_text_from_file(uploaded_file: UploadFile) -> str:
    if uploaded_file.filename.endswith(".pdf"):
        return await extract_text_from_pdf(uploaded_file)
    elif uploaded_file.filename.endswith(".docx"):
        return await extract_text_from_docx(uploaded_file)
    else:
        return (await uploaded_file.read()).decode('utf-8')

async def extract_text_from_pdf(uploaded_file: UploadFile) -> str:
    text = ""
    with pdfplumber.open(uploaded_file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

async def extract_text_from_docx(uploaded_file: UploadFile) -> str:
    document = Document(uploaded_file.file)
    text = "\n".join([para.text for para in document.paragraphs])
    return text
