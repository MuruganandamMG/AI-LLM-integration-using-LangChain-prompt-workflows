from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.habit import HabitCreate, HabitUpdate, HabitOut, HabitLogCreate, HabitLogOut
from app.services.habit_service import HabitService
from app.services.ics_export_service import ICSExportService
from app.services.export_service import ExportService

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

@router.get("/export/ics")
async def export_all_habits_ics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habits = await HabitService.get_user_habits(db, current_user.id)
    ics_events = []
    for h in habits:
        ics_events.append(f"""BEGIN:VEVENT
SUMMARY:{h.title}
DESCRIPTION:Category: {h.category} | Frequency: {h.frequency}
RRULE:FREQ={'DAILY' if h.frequency == 'daily' else 'WEEKLY'}
DTSTART;TZID=UTC:20260101T090000
END:VEVENT""")
    
    events_str = "\n".join(ics_events)
    content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Aura AI Self-Improvement Platform//EN
{events_str}
END:VCALENDAR"""
    return Response(content=content, media_type="text/calendar", headers={
        "Content-Disposition": 'attachment; filename="aura_habits.ics"'
    })

@router.get("/export/csv")
async def export_habits_csv(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habits = await HabitService.get_user_habits(db, current_user.id)
    csv_content = ExportService.export_habits_csv(habits)
    return Response(content=csv_content, media_type="text/csv", headers={
        "Content-Disposition": 'attachment; filename="aura_habits.csv"'
    })

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

@router.put("/{habit_id}", response_model=HabitOut)
async def update_habit(
    habit_id: str,
    habit_in: HabitUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = await HabitService.update_habit(db, habit_id, current_user.id, habit_in)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
    habit_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await HabitService.delete_habit(db, habit_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

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
