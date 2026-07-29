from fastapi import APIRouter, Depends, HTTPException

from . import get_current_active_user
from ..services.contracts_service import get_owned_clause

router = APIRouter(prefix="/clauses", tags=["clauses"])


@router.get("/{clause_id}")
async def get_clause(clause_id: int, current_user=Depends(get_current_active_user)):
    result = await get_owned_clause(current_user["id"], clause_id)
    if not result:
        raise HTTPException(status_code=404, detail="Clause not found")
    contract, clause = result
    return {
        "id": clause.get("id"),
        "contract_id": contract.get("_id"),
        "clause_id": clause.get("clause_id"),
        "clause_type": clause.get("clause_type"),
        "text": clause.get("text"),
        "risk_level": clause.get("risk_level"),
        "risk_category": clause.get("risk_category"),
        "risk_score": clause.get("risk_score"),
        "why_risky": clause.get("why_risky"),
        "trigger_phrases": clause.get("trigger_phrases", []),
        "financial_exposure": clause.get("financial_exposure"),
        "power_imbalance": clause.get("power_imbalance"),
        "safer_alternative": clause.get("safer_alternative"),
        "negotiation_tip": clause.get("negotiation_tip"),
        "confidence_score": clause.get("confidence_score"),
    }

