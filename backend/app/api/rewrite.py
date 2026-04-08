from fastapi import APIRouter, Depends

from . import get_current_active_user
from ..schemas.analysis import RewriteRequest
from ..nlp.llm_client import analyze_clause_via_llm

router = APIRouter(prefix="/rewrite", tags=["rewrite"])


@router.post("")
async def rewrite_clause(payload: RewriteRequest, user=Depends(get_current_active_user)):
    raw = await analyze_clause_via_llm(payload.clause_text)
    return {
        "safer_alternative": raw.get("safer_alternative", ""),
        "negotiation_tip": raw.get("negotiation_tip", ""),
        "confidence_score": raw.get("confidence_score", 0.0),
    }

