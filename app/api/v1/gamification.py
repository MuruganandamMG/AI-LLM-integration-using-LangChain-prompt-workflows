from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.gamification import GamificationStatsOut
from app.schemas.quest import DailyQuest
from app.services.gamification_service import GamificationService
from app.services.quest_service import QuestService
from app.services.habit_service import HabitService

router = APIRouter(prefix="/gamification", tags=["Gamification & Badges"])

@router.get("/profile", response_model=GamificationStatsOut)
async def get_gamification_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await GamificationService.get_user_stats(db, current_user.id)

@router.get("/quests", response_model=list[DailyQuest])
async def get_daily_quests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habits = await HabitService.get_user_habits(db, current_user.id)
    total_logs = sum(len(h.logs) for h in habits)
    return QuestService.get_daily_quests(total_logs)

@router.post("/quests/{quest_id}/claim")
async def claim_quest_reward(
    quest_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habits = await HabitService.get_user_habits(db, current_user.id)
    total_logs = sum(len(h.logs) for h in habits)
    quests = QuestService.get_daily_quests(total_logs)
    quest = next((q for q in quests if q.id == quest_id), None)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    if not quest.is_completed:
        raise HTTPException(status_code=400, detail="Quest requirements not yet completed")
    return {
        "status": "claimed",
        "quest_id": quest_id,
        "xp_earned": quest.xp_reward,
        "message": f"Claimed {quest.xp_reward} XP for '{quest.title}'!"
    }
