from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.recommendation import Recommendation
from app.models.user import User
from app.services.habit_service import HabitService
from app.ai.growth_chain import run_growth_recommendation_chain

class RecommendationService:
    @staticmethod
    async def generate_recommendation(db: AsyncSession, user: User) -> Recommendation:
        habits = await HabitService.get_user_habits(db, user.id)
        habits_data = [{"title": h.title, "category": h.category, "logs_count": len(h.logs)} for h in habits]
        
        ai_res = await run_growth_recommendation_chain(user.full_name, habits_data)
        
        rec = Recommendation(
            user_id=user.id,
            title=ai_res.get("title", "Personalized Growth Advice"),
            category=ai_res.get("category", "General"),
            action_items=ai_res.get("action_items", []),
            reasoning=ai_res.get("reasoning", "AI analysis based on active daily routines."),
            llm_provider=ai_res.get("provider", "gemini")
        )
        db.add(rec)
        await db.commit()
        await db.refresh(rec)
        return rec

    @staticmethod
    async def get_user_recommendations(db: AsyncSession, user_id: str) -> list[Recommendation]:
        stmt = select(Recommendation).where(Recommendation.user_id == user_id).order_by(Recommendation.created_at.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())
