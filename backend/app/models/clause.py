from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..core.db import Base


class Clause(Base):
    __tablename__ = "clauses"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    clause_id = Column(String, nullable=False)
    clause_type = Column(String, nullable=True)
    text = Column(String, nullable=False)

    risk_detected = Column(Boolean, default=False)
    risk_level = Column(String, default="Low")
    risk_category = Column(String, nullable=True)
    risk_score = Column(Float, default=0.0)
    why_risky = Column(String, nullable=True)
    trigger_phrases = Column(String, nullable=True)
    financial_exposure = Column(String, nullable=True)
    power_imbalance = Column(String, nullable=True)
    safer_alternative = Column(String, nullable=True)
    negotiation_tip = Column(String, nullable=True)
    confidence_score = Column(Float, default=0.0)

    contract = relationship("Contract", back_populates="clauses")
