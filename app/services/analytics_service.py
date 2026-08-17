from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.analytics import AnalyticsReport
from app.models.user import User
from app.services.habit_service import HabitService
from app.ai.analytics_chain import run_productivity_analytics_chain

class AnalyticsService:
    @staticmethod
    async def calculate_summary(db: AsyncSession, user_id: str) -> dict:
        habits = await HabitService.get_user_habits(db, user_id)
        total_habits = len(habits)
        total_logs = sum(len(h.logs) for h in habits)
        completion_rate = min(100.0, round((total_logs / max(1, total_habits * 7)) * 100, 1))
        longest_streak = max([len(h.logs) for h in habits], default=0)
        
        return {
            "total_habits": total_habits,
            "total_logs": total_logs,
            "completion_rate": completion_rate,
            "longest_streak": longest_streak
        }

    @staticmethod
    async def generate_report(db: AsyncSession, user: User) -> AnalyticsReport:
        stats = await AnalyticsService.calculate_summary(db, user.id)
        ai_res = await run_productivity_analytics_chain(user.full_name, stats)
        
        report = AnalyticsReport(
            user_id=user.id,
            total_habits=stats["total_habits"],
            completion_rate=stats["completion_rate"],
            longest_streak=stats["longest_streak"],
            ai_summary=ai_res.get("ai_summary", "Productivity evaluation completed."),
            key_takeaways=ai_res.get("key_takeaways", ["Maintain consistency"])
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report

    @staticmethod
    async def get_user_reports(db: AsyncSession, user_id: str) -> list[AnalyticsReport]:
        stmt = select(AnalyticsReport).where(AnalyticsReport.user_id == user_id).order_by(AnalyticsReport.created_at.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())
