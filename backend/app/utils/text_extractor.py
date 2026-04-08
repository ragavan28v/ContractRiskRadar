from typing import Optional


def extract_text_from_txt(file_bytes: bytes, encoding: str = "utf-8") -> Optional[str]:
    try:
        return file_bytes.decode(encoding, errors="ignore")
    except Exception:
        return None

