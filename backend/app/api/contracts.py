from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from . import get_current_active_user
from ..core.mongo import contracts_collection
from ..core.security import verify_password
from ..nlp.risk_engine import analyze_contract_text
from ..services.contracts_service import (
    create_contract,
    get_owned_contract,
    save_clause_analyses,
    serialize_contract,
)
from ..utils.file_utils import extract_text_from_file

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.post("/upload")
async def upload_contract(
    file: UploadFile = File(...),
    title: str = Form(...),
    consent_store: bool = Form(False),
    access_password: str | None = Form(None),
    current_user=Depends(get_current_active_user),
):
    content = await file.read()
    try:
        text = extract_text_from_file(file.filename, content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    contract = await create_contract(
        owner_id=current_user["id"],
        title=title,
        original_filename=file.filename,
        content_text=text,
        consent_store=consent_store,
        access_password=access_password,
    )

    try:
        analyses = await analyze_contract_text(text)
        await save_clause_analyses(contract["_id"], analyses)
    except Exception:
        await contracts_collection.delete_one({"_id": contract["_id"]})
        raise

    return {"contract_id": contract["_id"]}


@router.get("/stored")
async def list_stored_contracts(current_user=Depends(get_current_active_user)):
    docs = await contracts_collection.find(
        {"owner_id": current_user["id"], "consent_store": True}
    ).sort("created_at", -1).to_list(length=100)
    return [{"id": d["_id"], "title": d.get("title"), "created_at": d.get("created_at")} for d in docs]


class UnlockRequest(BaseModel):
    password: str


@router.post("/{contract_id}/unlock")
async def unlock_contract(contract_id: int, body: UnlockRequest, current_user=Depends(get_current_active_user)):
    contract = await get_owned_contract(current_user["id"], contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found or not stored")
    if not contract.get("access_password_hash"):
        raise HTTPException(status_code=403, detail="No access password set for this document")
    if not verify_password(body.password, contract["access_password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    return serialize_contract(contract)


@router.get("/{contract_id}")
async def get_contract(contract_id: int, current_user=Depends(get_current_active_user)):
    contract = await get_owned_contract(current_user["id"], contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return serialize_contract(contract)

