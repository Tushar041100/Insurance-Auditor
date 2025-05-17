import io
import pandas as pd
import docx
from PyPDF2 import PdfReader

def extract_text_from_file(file_name, file_bytes):
    ext = file_name.lower().split(".")[-1]
    if ext == "pdf":
        return extract_text_pdf(file_bytes)
    elif ext == "docx":
        return extract_text_docx(file_bytes)
    elif ext in ("xls", "xlsx"):
        return extract_text_xlsx(file_bytes)
    elif ext == "txt":
        return file_bytes.decode("utf-8", errors="ignore")
    raise ValueError(f"Unsupported file type: {ext}")

def extract_text_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_docx(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_xlsx(file_bytes):
    excel_file = pd.ExcelFile(io.BytesIO(file_bytes))
    text = ""
    for sheet in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        text += f"\nSheet: {sheet}\n" + df.astype(str).apply(" ".join, axis=1).str.cat(sep="\n")
    return text