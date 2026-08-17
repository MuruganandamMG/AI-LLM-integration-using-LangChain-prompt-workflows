from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.weekly_review import WeeklyReviewOut
from app.services.weekly_review_service import WeeklyReviewService
from app.ai.quote_chain import run_motivational_quote_chain

router = APIRouter(prefix="/reviews", tags=["AI Weekly Reviews"])

@router.post("/weekly", response_model=WeeklyReviewOut, status_code=status.HTTP_201_CREATED)
async def generate_weekly_review(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await WeeklyReviewService.generate_weekly_review(db, current_user)

@router.get("/quote")
async def get_daily_quote(
    category: str = "General",
    current_user: User = Depends(get_current_user)
):
    return await run_motivational_quote_chain(
        user_name=current_user.full_name or "Explorer",
        category=category
    )
