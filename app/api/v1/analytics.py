from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.analytics import AnalyticsSummaryOut, AnalyticsReportOut
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Productivity Analytics"])

@router.get("/summary", response_model=AnalyticsSummaryOut)
async def get_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AnalyticsService.calculate_summary(db, current_user.id)

@router.post("/generate-report", response_model=AnalyticsReportOut, status_code=status.HTTP_201_CREATED)
async def generate_report(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AnalyticsService.generate_report(db, current_user)

@router.get("/reports", response_model=list[AnalyticsReportOut])
async def list_reports(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AnalyticsService.get_user_reports(db, current_user.id)
