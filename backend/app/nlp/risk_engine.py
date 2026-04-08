from typing import List, Tuple

from .segmentation import rule_based_segmentation
from .llm_client import analyze_clause_via_llm
from ..schemas.analysis import ClauseAnalysis


async def analyze_contract_text(text: str) -> List[Tuple[str, str, ClauseAnalysis]]:
    clauses = rule_based_segmentation(text)
    results: List[Tuple[str, str, ClauseAnalysis]] = []

    for clause_id, clause_text in clauses:
        raw = await analyze_clause_via_llm(clause_text)
        analysis = ClauseAnalysis(**raw)
        results.append((clause_id, clause_text, analysis))

    return results

