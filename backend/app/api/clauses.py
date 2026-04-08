from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import get_current_active_user
from ..core.db import get_db
from ..models.clause import Clause
from ..models.contract import Contract

router = APIRouter(prefix="/clauses", tags=["clauses"])


@router.get("/{clause_id}")
def get_clause(clause_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    clause = db.query(Clause).filter(Clause.id == clause_id).first()
    if not clause:
        raise HTTPException(status_code=404, detail="Clause not found")
    contract = db.query(Contract).filter(Contract.id == clause.contract_id).first()
    if not contract or contract.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return {
        "id": clause.id,
        "contract_id": clause.contract_id,
        "clause_id": clause.clause_id,
        "clause_type": clause.clause_type,
        "text": clause.text,
        "risk_level": clause.risk_level,
        "risk_category": clause.risk_category,
        "risk_score": clause.risk_score,
        "why_risky": clause.why_risky,
        "trigger_phrases": (clause.trigger_phrases or "").split(",") if clause.trigger_phrases else [],
        "financial_exposure": clause.financial_exposure,
        "power_imbalance": clause.power_imbalance,
        "safer_alternative": clause.safer_alternative,
        "negotiation_tip": clause.negotiation_tip,
        "confidence_score": clause.confidence_score,
    }

