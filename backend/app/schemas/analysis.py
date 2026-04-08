from typing import List, Optional

from pydantic import BaseModel


class ClauseAnalysis(BaseModel):
    clause_type: str
    risk_detected: bool
    risk_level: str
    risk_category: str
    risk_score: float
    why_risky: str
    trigger_phrases: List[str]
    financial_exposure: Optional[str] = None
    power_imbalance: Optional[str] = None
    safer_alternative: str
    negotiation_tip: str
    confidence_score: float


class RewriteRequest(BaseModel):
    clause_text: str
    target_tone: Optional[str] = None

