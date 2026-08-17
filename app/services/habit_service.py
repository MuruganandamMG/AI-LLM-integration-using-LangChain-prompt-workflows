from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.habit import Habit, HabitLog
from app.schemas.habit import HabitCreate, HabitUpdate, HabitLogCreate

class HabitService:
    @staticmethod
    async def create_habit(db: AsyncSession, user_id: str, habit_in: HabitCreate) -> Habit:
        habit = Habit(
            user_id=user_id,
            title=habit_in.title,
            description=habit_in.description,
            category=habit_in.category,
            frequency=habit_in.frequency
        )
        db.add(habit)
        await db.commit()
        await db.refresh(habit)
        # Load logs attribute for schema serialization
        stmt = select(Habit).where(Habit.id == habit.id).options(selectinload(Habit.logs))
        res = await db.execute(stmt)
        return res.scalar_one()

    @staticmethod
    async def get_user_habits(db: AsyncSession, user_id: str) -> list[Habit]:
        stmt = select(Habit).where(Habit.user_id == user_id).options(selectinload(Habit.logs))
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_habit_by_id(db: AsyncSession, habit_id: str, user_id: str) -> Habit | None:
        stmt = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id).options(selectinload(Habit.logs))
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def log_completion(db: AsyncSession, habit_id: str, user_id: str, log_in: HabitLogCreate) -> HabitLog:
        habit_log = HabitLog(
            habit_id=habit_id,
            user_id=user_id,
            notes=log_in.notes,
            mood_score=log_in.mood_score
        )
        db.add(habit_log)
        await db.commit()
        await db.refresh(habit_log)
        return habit_log
