from io import BytesIO
from typing import Optional

import docx


def extract_text_from_docx(file_bytes: bytes) -> Optional[str]:
    try:
        doc = docx.Document(BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception:
        return None

