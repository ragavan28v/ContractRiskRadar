from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import get_current_active_user
from ..core.db import get_db
from ..services.analysis_service import get_contract_dashboard_stats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
def dashboard_stats(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    stats = get_contract_dashboard_stats(db, current_user.id)
    return stats

