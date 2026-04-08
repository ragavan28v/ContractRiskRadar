from io import BytesIO
from typing import Optional


def extract_text_from_pdf(file_bytes: bytes) -> Optional[str]:
    """
    Optional PDF extraction.
    If pdfminer.six is not installed, returns None so the caller can handle it gracefully.
    """
    try:
        from pdfminer.high_level import extract_text  # type: ignore
    except ImportError:
        return None

    try:
        return extract_text(BytesIO(file_bytes))
    except Exception:
        return None

