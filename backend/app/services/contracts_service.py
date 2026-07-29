from datetime import datetime
from typing import Any

from ..core.mongo import contracts_collection, next_sequence
from ..core.security import get_password_hash
from ..schemas.analysis import ClauseAnalysis


def _serialize_clause(clause: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": clause.get("id"),
        "clause_id": clause.get("clause_id"),
        "clause_type": clause.get("clause_type"),
        "text": clause.get("text"),
        "risk_detected": clause.get("risk_detected", False),
        "risk_level": clause.get("risk_level", "Low"),
        "risk_category": clause.get("risk_category"),
        "risk_score": clause.get("risk_score", 0.0),
        "why_risky": clause.get("why_risky"),
        "trigger_phrases": clause.get("trigger_phrases", []),
        "financial_exposure": clause.get("financial_exposure"),
        "power_imbalance": clause.get("power_imbalance"),
        "safer_alternative": clause.get("safer_alternative"),
        "negotiation_tip": clause.get("negotiation_tip"),
        "confidence_score": clause.get("confidence_score", 0.0),
    }


def serialize_contract(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": contract.get("_id"),
        "owner_id": contract.get("owner_id"),
        "title": contract.get("title"),
        "original_filename": contract.get("original_filename"),
        "overall_risk_score": contract.get("overall_risk_score", 0.0),
        "total_clauses": contract.get("total_clauses", 0),
        "high_risk_clauses": contract.get("high_risk_clauses", 0),
        "content_text": contract.get("content_text", ""),
        "consent_store": contract.get("consent_store", False),
        "created_at": contract.get("created_at"),
        "clauses": [_serialize_clause(clause) for clause in contract.get("clauses", [])],
    }


async def create_contract(
    *,
    owner_id: int,
    title: str,
    original_filename: str,
    content_text: str,
    consent_store: bool,
    access_password: str | None = None,
) -> dict[str, Any]:
    contract_id = await next_sequence("contracts")
    contract_doc: dict[str, Any] = {
        "_id": contract_id,
        "owner_id": owner_id,
        "title": title,
        "original_filename": original_filename,
        "content_text": content_text,
        "overall_risk_score": 0.0,
        "total_clauses": 0,
        "high_risk_clauses": 0,
        "created_at": datetime.utcnow(),
        "consent_store": consent_store,
        "access_password_hash": get_password_hash(access_password) if access_password else None,
        "clauses": [],
    }
    await contracts_collection.insert_one(contract_doc)
    return contract_doc


async def save_clause_analyses(
    contract_id: int,
    analyses: list[tuple[str, str, ClauseAnalysis]],
) -> dict[str, Any]:
    total = len(analyses)
    high_risk_count = 0
    total_risk_score = 0.0
    clauses_list: list[dict[str, Any]] = []

    for clause_id, clause_text, analysis in analyses:
        normalized_level = (analysis.risk_level or "").strip().title()
        if normalized_level == "High":
            high_risk_count += 1
        total_risk_score += analysis.risk_score
        clauses_list.append(
            {
                "id": await next_sequence("clauses"),
                "clause_id": clause_id,
                "clause_type": analysis.clause_type,
                "text": clause_text,
                "risk_detected": analysis.risk_detected,
                "risk_level": normalized_level,
                "risk_category": analysis.risk_category,
                "risk_score": analysis.risk_score,
                "why_risky": analysis.why_risky,
                "trigger_phrases": list(analysis.trigger_phrases),
                "financial_exposure": analysis.financial_exposure or "",
                "power_imbalance": analysis.power_imbalance or "",
                "safer_alternative": analysis.safer_alternative,
                "negotiation_tip": analysis.negotiation_tip,
                "confidence_score": analysis.confidence_score,
            }
        )

    avg_risk = total_risk_score / total if total else 0.0
    await contracts_collection.update_one(
        {"_id": contract_id},
        {
            "$set": {
                "clauses": clauses_list,
                "total_clauses": total,
                "high_risk_clauses": high_risk_count,
                "overall_risk_score": avg_risk,
            }
        },
    )

    updated_contract = await contracts_collection.find_one({"_id": contract_id})
    if not updated_contract:
        raise ValueError("Contract not found after saving analyses")
    return updated_contract


async def get_owned_contract(owner_id: int, contract_id: int) -> dict[str, Any] | None:
    return await contracts_collection.find_one({"_id": contract_id, "owner_id": owner_id})


async def get_owned_clause(owner_id: int, clause_id: int) -> tuple[dict[str, Any], dict[str, Any]] | None:
    contract = await contracts_collection.find_one({"owner_id": owner_id, "clauses.id": clause_id})
    if not contract:
        return None
    clause = next((item for item in contract.get("clauses", []) if item.get("id") == clause_id), None)
    if not clause:
        return None
    return contract, clause

