import re
from typing import List, Tuple


def rule_based_segmentation(text: str) -> List[Tuple[str, str]]:
    """
    Basic heading/number-based segmentation with a fallback by paragraphs.
    Returns a list of (clause_id, clause_text).
    """
    lines = text.splitlines()
    clauses: List[Tuple[str, str]] = []
    current_id = "0"
    current_lines: list[str] = []

    heading_pattern = re.compile(r"^(\d+(\.\d+)*)[\.\)]\s+(.+)$")

    for line in lines:
        match = heading_pattern.match(line.strip())
        if match:
            if current_lines:
                clauses.append((current_id, "\n".join(current_lines).strip()))
                current_lines = []
            current_id = match.group(1)
            current_lines.append(line)
        else:
            current_lines.append(line)
    if current_lines:
        clauses.append((current_id, "\n".join(current_lines).strip()))

    if not clauses:
        chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
        clauses = [(str(i + 1), c) for i, c in enumerate(chunks)]

    return clauses

