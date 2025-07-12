import fitz  # PyMuPDF
import docx
import os

def extract_text_from_cv(filepath):
    text = ""
    _, ext = os.path.splitext(filepath)

    if ext.lower() == '.pdf':
        doc = fitz.open(filepath)
        for page in doc:
            text += page.get_text()
        doc.close()

    elif ext.lower() == '.docx':
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"

    else:
        raise ValueError("Unsupported file type: only PDF and DOCX are supported.")

    return text
