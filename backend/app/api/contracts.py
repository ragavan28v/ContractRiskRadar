from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from . import get_current_active_user
from ..core.db import get_db
from ..core.mongo import contracts_collection
from ..models.contract import Contract
from ..models.clause import Clause
from ..utils.file_utils import extract_text_from_file
from ..nlp.risk_engine import analyze_contract_text
from ..services.contracts_service import create_contract, save_clause_analyses

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.post("/upload")
async def upload_contract(
    file: UploadFile = File(...),
    title: str = Form(...),
    consent_store: bool = Form(False),
    access_password: str | None = Form(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    content = await file.read()
    try:
        text = extract_text_from_file(file.filename, content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    contract = create_contract(
        db,
        owner_id=current_user.id,
        title=title,
        original_filename=file.filename,
        content_text=text,
        consent_store=consent_store,
        access_password=access_password,
    )

    analyses = await analyze_contract_text(text)
    await save_clause_analyses(db, contract, analyses)

    return {"contract_id": contract.id}


@router.get("/stored")
async def list_stored_contracts(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    # fetch from mongo collection
    docs = await contracts_collection.find({"owner_id": current_user.id}).sort("created_at", -1).to_list(length=100)
    return [{"id": d["_id"], "title": d.get("title"), "created_at": d.get("created_at")} for d in docs]


class UnlockRequest(BaseModel):
    password: str


@router.post("/{contract_id}/unlock")
async def unlock_contract(contract_id: int, body: UnlockRequest, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    # try mongo first
    mongo_doc = await contracts_collection.find_one({"_id": contract_id, "owner_id": current_user.id})
    if mongo_doc:
        # check password in SQL for verification
        contract = (
            db.query(Contract)
            .filter(Contract.id == contract_id, Contract.owner_id == current_user.id)
            .first()
        )
        if not contract or not contract.access_password_hash:
            raise HTTPException(status_code=403, detail="No access password set for this document")
        if not bcrypt.verify(body.password, contract.access_password_hash):
            raise HTTPException(status_code=401, detail="Invalid password")
        return mongo_doc

    # fallback to SQL behavior
    contract = (
        db.query(Contract)
        .filter(Contract.id == contract_id, Contract.owner_id == current_user.id, Contract.consent_store == True)
        .first()
    )
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found or not stored")
    if not contract.access_password_hash:
        raise HTTPException(status_code=403, detail="No access password set for this document")
    if not bcrypt.verify(body.password, contract.access_password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    clauses = (
        db.query(Clause)
        .filter(Clause.contract_id == contract.id)
        .order_by(Clause.id.asc())
        .all()
    )

    return {
        "id": contract.id,
        "title": contract.title,
        "overall_risk_score": contract.overall_risk_score,
        "total_clauses": contract.total_clauses,
        "high_risk_clauses": contract.high_risk_clauses,
        "content_text": contract.content_text,
        "clauses": [
            {
                "id": c.id,
                "clause_id": c.clause_id,
                "clause_type": c.clause_type,
                "text": c.text,
                "risk_detected": c.risk_detected,
                "risk_level": c.risk_level,
                "risk_category": c.risk_category,
                "risk_score": c.risk_score,
                "why_risky": c.why_risky,
                "trigger_phrases": (c.trigger_phrases or "").split(",") if c.trigger_phrases else [],
                "financial_exposure": c.financial_exposure,
                "power_imbalance": c.power_imbalance,
                "safer_alternative": c.safer_alternative,
                "negotiation_tip": c.negotiation_tip,
                "confidence_score": c.confidence_score,
            }
            for c in clauses
        ],
    }


@router.get("/{contract_id}")
async def get_contract(contract_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    # prefer mongo document if stored
    mongo_doc = await contracts_collection.find_one({"_id": contract_id, "owner_id": current_user.id})
    if mongo_doc:
        # return doc with same format as SQL
        return mongo_doc

    contract = (
        db.query(Contract)
        .filter(Contract.id == contract_id, Contract.owner_id == current_user.id)
        .first()
    )
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    clauses = (
        db.query(Clause)
        .filter(Clause.contract_id == contract.id)
        .order_by(Clause.id.asc())
        .all()
    )

    return {
        "id": contract.id,
        "title": contract.title,
        "overall_risk_score": contract.overall_risk_score,
        "total_clauses": contract.total_clauses,
        "high_risk_clauses": contract.high_risk_clauses,
        "content_text": contract.content_text,
        "clauses": [
            {
                "id": c.id,
                "clause_id": c.clause_id,
                "clause_type": c.clause_type,
                "text": c.text,
                "risk_detected": c.risk_detected,
                "risk_level": c.risk_level,
                "risk_category": c.risk_category,
                "risk_score": c.risk_score,
                "why_risky": c.why_risky,
                "trigger_phrases": (c.trigger_phrases or "").split(",") if c.trigger_phrases else [],
                "financial_exposure": c.financial_exposure,
                "power_imbalance": c.power_imbalance,
                "safer_alternative": c.safer_alternative,
                "negotiation_tip": c.negotiation_tip,
                "confidence_score": c.confidence_score,
            }
            for c in clauses
        ],
    }

