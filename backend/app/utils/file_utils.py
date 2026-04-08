from .pdf_extractor import extract_text_from_pdf
from .docx_extractor import extract_text_from_docx
from .text_extractor import extract_text_from_txt


def extract_text_from_file(filename: str, content: bytes) -> str:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif lower.endswith(".docx"):
        text = extract_text_from_docx(content)
    else:
        text = extract_text_from_txt(content)

    if not text:
        raise ValueError("Unable to extract text from file.")
    return text

