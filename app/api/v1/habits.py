from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.habit import HabitCreate, HabitOut, HabitLogCreate, HabitLogOut
from app.services.habit_service import HabitService

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.post("/", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
async def create_habit(
    habit_in: HabitCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await HabitService.create_habit(db, current_user.id, habit_in)

@router.get("/", response_model=list[HabitOut])
async def list_habits(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await HabitService.get_user_habits(db, current_user.id)

@router.get("/{habit_id}", response_model=HabitOut)
async def get_habit(
    habit_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = await HabitService.get_habit_by_id(db, habit_id, current_user.id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.post("/{habit_id}/log", response_model=HabitLogOut, status_code=status.HTTP_201_CREATED)
async def log_habit_completion(
    habit_id: str,
    log_in: HabitLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = await HabitService.get_habit_by_id(db, habit_id, current_user.id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return await HabitService.log_completion(db, habit_id, current_user.id, log_in)
