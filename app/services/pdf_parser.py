from io import BytesIO
from pypdf import PdfReader


def get_number_of_pages(file_content: bytes):
    pdf_reader = PdfReader(BytesIO(file_content))
    return len(pdf_reader.pages)


def extract_text_from_pdf(file_content: bytes):
    pages_text = []
    pdf_reader = PdfReader(BytesIO(file_content))
    
    for page in pdf_reader.pages:
        pages_text.append(page.extract_text())

    return pages_text



