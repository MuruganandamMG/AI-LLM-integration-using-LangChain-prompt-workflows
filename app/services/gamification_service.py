from sqlalchemy.ext.asyncio import AsyncSession
from app.services.habit_service import HabitService
from app.schemas.gamification import Badge, GamificationStatsOut

class GamificationService:
    @staticmethod
    async def get_user_stats(db: AsyncSession, user_id: str) -> GamificationStatsOut:
        habits = await HabitService.get_user_habits(db, user_id)
        total_logs = sum(len(h.logs) for h in habits)
        longest_streak = max([len(h.logs) for h in habits], default=0)
        
        # 50 XP per completed habit log + 100 XP per habit created
        total_xp = (total_logs * 50) + (len(habits) * 100)
        level = max(1, (total_xp // 250) + 1)
        
        # Determine Tier
        if level >= 10:
            tier = "Diamond"
        elif level >= 6:
            tier = "Gold"
        elif level >= 3:
            tier = "Silver"
        else:
            tier = "Bronze"

        badges = [
            Badge(
                name="First Step",
                description="Logged your very first habit completion",
                icon="🌱",
                unlocked=total_logs >= 1
            ),
            Badge(
                name="Consistency Champion",
                description="Achieved a 7-day habit streak",
                icon="🔥",
                unlocked=longest_streak >= 7
            ),
            Badge(
                name="Habit Architect",
                description="Created 3 or more tracked habits",
                icon="🏛️",
                unlocked=len(habits) >= 3
            ),
            Badge(
                name="Centurion",
                description="Completed 100 total habit sessions",
                icon="👑",
                unlocked=total_logs >= 100
            )
        ]

        return GamificationStatsOut(
            user_id=user_id,
            total_xp=total_xp,
            level=level,
            tier=tier,
            completed_logs=total_logs,
            streak_days=longest_streak,
            badges=badges
        )
