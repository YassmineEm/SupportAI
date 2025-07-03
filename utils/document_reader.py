from bs4 import BeautifulSoup
from docx import Document as DocxDocument
import PyPDF2

def read_txt(file_bytes):
    return file_bytes.decode('utf-8')

def read_docx(file_bytes):
    from io import BytesIO
    doc = DocxDocument(BytesIO(file_bytes))
    return '\n'.join([para.text for para in doc.paragraphs])

def read_pdf(file_bytes):
    from io import BytesIO
    reader = PyPDF2.PdfReader(BytesIO(file_bytes))
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

def read_html(file_bytes):
    soup = BeautifulSoup(file_bytes, 'html.parser')
    return soup.get_text(separator='\n')

def extract_text_from_file(file: bytes, filename: str) -> str:
    if filename.endswith('.txt'):
        return read_txt(file)
    elif filename.endswith('.docx'):
        return read_docx(file)
    elif filename.endswith('.pdf'):
        return read_pdf(file)
    elif filename.endswith('.html') or filename.endswith('.htm'):
        return read_html(file)
    else:
        raise ValueError("Unsupported file type")
