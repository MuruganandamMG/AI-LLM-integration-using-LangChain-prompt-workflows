from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.weekly_review import WeeklyReviewOut
from app.services.weekly_review_service import WeeklyReviewService

router = APIRouter(prefix="/reviews", tags=["AI Weekly Reviews"])

@router.post("/weekly", response_model=WeeklyReviewOut, status_code=status.HTTP_201_CREATED)
async def generate_weekly_review(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await WeeklyReviewService.generate_weekly_review(db, current_user)
