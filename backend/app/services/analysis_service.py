from ..core.mongo import contracts_collection


async def get_contract_dashboard_stats(user_id: int) -> dict:
    contracts = await contracts_collection.find({"owner_id": user_id}).to_list(length=1000)
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

    for contract in contracts:
        risk_scores.append(contract.get("overall_risk_score", 0.0))
        total_clauses += contract.get("total_clauses", 0)
        high_risk_clauses += contract.get("high_risk_clauses", 0)
        for clause in contract.get("clauses", []):
            level = (clause.get("risk_level") or "Low").title()
            if level not in distribution:
                level = "Low"
            distribution[level] += 1

    avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0.0

    return {
        "total_contracts": total_contracts,
        "average_overall_risk": avg_risk,
        "total_clauses": total_clauses,
        "high_risk_clauses": high_risk_clauses,
        "risk_distribution": distribution,
    }

