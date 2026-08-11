from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.habit_service import HabitService
from app.schemas.weekly_review import WeeklyReviewOut
from app.ai.weekly_review_chain import run_weekly_review_chain

class WeeklyReviewService:
    @staticmethod
    async def generate_weekly_review(db: AsyncSession, user: User) -> WeeklyReviewOut:
        habits = await HabitService.get_user_habits(db, user.id)
        summary_data = {
            "total_habits": len(habits),
            "habits_overview": [{"title": h.title, "logs": len(h.logs)} for h in habits]
        }
        
        ai_res = await run_weekly_review_chain(user.full_name, summary_data)
        
        return WeeklyReviewOut(
            user_id=user.id,
            overall_sentiment=ai_res.get("overall_sentiment", "Positive"),
            wins=ai_res.get("wins", ["Consistent engagement"]),
            improvement_areas=ai_res.get("improvement_areas", ["Optimize routines"]),
            next_week_smart_goals=ai_res.get("next_week_smart_goals", ["Focus on daily execution"]),
            coach_note=ai_res.get("coach_note", "Great progress!")
        )
