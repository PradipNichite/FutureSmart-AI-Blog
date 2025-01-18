import io
import PyPDF2  
from docx import Document
from fastapi import  HTTPException
import asyncio

# Async version of the extract_text_from_docx
async def extract_text_from_docx(file_content: bytes) -> str:
    """
    Extract text from a DOCX file.
    """
    return await asyncio.to_thread(extract_text_from_docx_sync, file_content)

def extract_text_from_docx_sync(file_content: bytes) -> str:
    """
    Extract text from a DOCX file (blocking version).
    """
    doc = Document(io.BytesIO(file_content))
    extracted_text = ""
    for para in doc.paragraphs:
        extracted_text += para.text + "\n"
    return extracted_text

# Async version of the extract_text_from_pdf
async def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from a PDF file.
    """
    return await asyncio.to_thread(extract_text_from_pdf_sync, file_content)

def extract_text_from_pdf_sync(file_content: bytes) -> str:
    """
    Extract text from a PDF file (blocking version).
    """
    content = ""
    pdf_reader = PyPDF2.PdfReader(file_content)
    num_pages = len(pdf_reader.pages)
    for i in range(num_pages):
        page = pdf_reader.pages[i]
        content += page.extract_text()
    return content


# Async version of extract_text_from_txt
async def extract_text_from_txt(file_content: bytes) -> str:
    """
    Extract text from a text file.
    """
    return await asyncio.to_thread(extract_text_from_txt_sync, file_content)

def extract_text_from_txt_sync(file_content: bytes) -> str:
    """
    Extract text from a text file (blocking version).
    """
    return file_content.decode("utf-8")  # Assuming the file is in UTF-8 encoding

# Asynchronous file text extraction
async def extract_text_from_file(file_content: bytes, file_type: str) -> str:
    """
    Extract text from different file types based on the file type.
    """
    if file_type == "txt":
        return await extract_text_from_txt(file_content)
    elif file_type == "pdf":
        return await extract_text_from_pdf(file_content)
    elif file_type == "docx":
        return await extract_text_from_docx(file_content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

