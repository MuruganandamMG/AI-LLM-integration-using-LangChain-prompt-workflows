from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.gamification import GamificationStatsOut
from app.services.gamification_service import GamificationService

router = APIRouter(prefix="/gamification", tags=["Gamification & Badges"])

@router.get("/profile", response_model=GamificationStatsOut)
async def get_gamification_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await GamificationService.get_user_stats(db, current_user.id)
