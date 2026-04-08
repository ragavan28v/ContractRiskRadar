from sqlalchemy.orm import Session

from passlib.hash import bcrypt

from ..core.mongo import contracts_collection

from ..models.contract import Contract
from ..models.clause import Clause
from ..schemas.analysis import ClauseAnalysis


def create_contract(
    db: Session,
    *,
    owner_id: int,
    title: str,
    original_filename: str,
    content_text: str,
    consent_store: bool,
    access_password: str | None = None,
) -> Contract:
    contract = Contract(
        owner_id=owner_id,
        title=title,
        original_filename=original_filename,
        content_text=content_text,
        consent_store=consent_store,
    )
    if access_password:
        contract.access_password_hash = bcrypt.hash(access_password)
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


async def save_clause_analyses(
    db: Session,
    contract: Contract,
    analyses: list[tuple[str, str, ClauseAnalysis]],
) -> None:
    total = len(analyses)
    high_risk_count = 0
    total_risk_score = 0.0

    clauses_list = []

    for clause_id, clause_text, a in analyses:
        normalized_level = (a.risk_level or "").strip().title()
        if normalized_level == "High":
            high_risk_count += 1
        total_risk_score += a.risk_score
        clause = Clause(
            contract_id=contract.id,
            clause_id=clause_id,
            clause_type=a.clause_type,
            text=clause_text,
            risk_detected=a.risk_detected,
            risk_level=normalized_level,
            risk_category=a.risk_category,
            risk_score=a.risk_score,
            why_risky=a.why_risky,
            trigger_phrases=",".join(a.trigger_phrases),
            financial_exposure=a.financial_exposure or "",
            power_imbalance=a.power_imbalance or "",
            safer_alternative=a.safer_alternative,
            negotiation_tip=a.negotiation_tip,
            confidence_score=a.confidence_score,
        )
        db.add(clause)

        # prepare for mongo
        clauses_list.append({
            "clause_id": clause_id,
            "clause_type": a.clause_type,
            "text": clause_text,
            "risk_detected": a.risk_detected,
            "risk_level": normalized_level,
            "risk_category": a.risk_category,
            "risk_score": a.risk_score,
            "why_risky": a.why_risky,
            "trigger_phrases": a.trigger_phrases,
            "financial_exposure": a.financial_exposure,
            "power_imbalance": a.power_imbalance,
            "safer_alternative": a.safer_alternative,
            "negotiation_tip": a.negotiation_tip,
            "confidence_score": a.confidence_score,
        })

    avg_risk = total_risk_score / total if total else 0.0
    contract.total_clauses = total
    contract.high_risk_clauses = high_risk_count
    contract.overall_risk_score = avg_risk

    db.commit()
    db.refresh(contract)

    # after commit, ensure we have real SQL ids for each clause
    if contract.consent_store:
        sql_clauses = (
            db.query(Clause)
            .filter(Clause.contract_id == contract.id)
            .order_by(Clause.id.asc())
            .all()
        )
        mongo_clauses = []
        for c in sql_clauses:
            mongo_clauses.append({
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
            })

        await contracts_collection.replace_one(
            {"_id": contract.id},
            {
                "_id": contract.id,
                "owner_id": contract.owner_id,
                "title": contract.title,
                "content_text": contract.content_text,
                "consent_store": True,
                "clauses": mongo_clauses,
                "overall_risk_score": avg_risk,
                "total_clauses": total,
                "high_risk_clauses": high_risk_count,
                "created_at": contract.created_at,
            },
            upsert=True,
        )


async def sync_sql_to_mongo(db: Session):
    """Copy all consented contracts from SQL into Mongo, used at startup."""
    contracts = db.query(Contract).filter(Contract.consent_store == True).all()
    for contract in contracts:
        clauses = (
            db.query(Clause)
            .filter(Clause.contract_id == contract.id)
            .order_by(Clause.id.asc())
            .all()
        )
        mongo_clauses = []
        for c in clauses:
            mongo_clauses.append({
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
            })
        await contracts_collection.replace_one(
            {"_id": contract.id},
            {
                "_id": contract.id,
                "owner_id": contract.owner_id,
                "title": contract.title,
                "content_text": contract.content_text,
                "consent_store": True,
                "clauses": mongo_clauses,
                "overall_risk_score": contract.overall_risk_score,
                "total_clauses": contract.total_clauses,
                "high_risk_clauses": contract.high_risk_clauses,
                "created_at": contract.created_at,
            },
            upsert=True,
        )

