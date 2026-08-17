from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.services.habit_service import HabitService
from app.services.gamification_service import GamificationService
from app.ai.coach_chat_chain import run_coach_chat_chain

router = APIRouter(prefix="/coach", tags=["AI Conversational Coach"])

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_with_coach(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habits = await HabitService.get_user_habits(db, current_user.id)
    habits_str = ", ".join([f"{h.title} ({h.category})" for h in habits]) if habits else "No active habits"
    stats = await GamificationService.get_user_stats(db, current_user.id)

    return await run_coach_chat_chain(
        user_name=current_user.full_name or "Explorer",
        message=request.message,
        habits_context=habits_str,
        streak_days=stats.streak_days,
        level=stats.level,
        total_xp=stats.total_xp
    )
