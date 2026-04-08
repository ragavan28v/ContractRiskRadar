from sqlalchemy.orm import Session

from ..models.contract import Contract
from ..models.clause import Clause


def get_contract_dashboard_stats(db: Session, user_id: int) -> dict:
    q = db.query(Contract).filter(Contract.owner_id == user_id)
    contracts = q.all()
    total_contracts = len(contracts)

    if not contracts:
        return {
            "total_contracts": 0,
            "average_overall_risk": 0,
            "total_clauses": 0,
            "high_risk_clauses": 0,
            "risk_distribution": {"Low": 0, "Moderate": 0, "High": 0},
        }

    total_clauses = 0
    high_risk_clauses = 0
    risk_scores = []
    distribution = {"Low": 0, "Moderate": 0, "High": 0}

    for c in contracts:
        risk_scores.append(c.overall_risk_score)
        total_clauses += c.total_clauses
        high_risk_clauses += c.high_risk_clauses

    for level in distribution.keys():
        distribution[level] = (
            db.query(Clause)
            .join(Contract, Clause.contract_id == Contract.id)
            .filter(Contract.owner_id == user_id, Clause.risk_level == level)
            .count()
        )

    avg_risk = sum(risk_scores) / len(risk_scores)

    return {
        "total_contracts": total_contracts,
        "average_overall_risk": avg_risk,
        "total_clauses": total_clauses,
        "high_risk_clauses": high_risk_clauses,
        "risk_distribution": distribution,
    }

