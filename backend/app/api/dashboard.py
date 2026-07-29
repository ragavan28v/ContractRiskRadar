from fastapi import APIRouter, Depends

from . import get_current_active_user
from ..services.analysis_service import get_contract_dashboard_stats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
async def dashboard_stats(current_user=Depends(get_current_active_user)):
    stats = await get_contract_dashboard_stats(current_user["id"])
    return stats

