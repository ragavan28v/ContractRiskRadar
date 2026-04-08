from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship

from ..core.db import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    content_text = Column(String, nullable=False)
    overall_risk_score = Column(Float, default=0.0)
    total_clauses = Column(Integer, default=0)
    high_risk_clauses = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    consent_store = Column(Boolean, default=False)
    access_password_hash = Column(String, nullable=True)

    owner = relationship("User")
    clauses = relationship("Clause", back_populates="contract")
