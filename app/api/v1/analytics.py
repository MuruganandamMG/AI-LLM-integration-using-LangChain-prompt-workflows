from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.models.focus_session import FocusSession
from app.core.deps import get_current_user
from app.schemas.analytics import AnalyticsSummaryOut, AnalyticsReportOut
from app.services.analytics_service import AnalyticsService
from app.services.habit_service import HabitService
from app.services.mood_matrix_service import MoodMatrixService
from app.ai.focus_assistant_chain import run_focus_assistant_chain

router = APIRouter(prefix="/analytics", tags=["Productivity Analytics"])

class FocusRequest(BaseModel):
    task_title: str = "Deep Work Session"
    duration_minutes: int = 25

class FocusSessionLog(BaseModel):
    task_title: str = "Deep Work Session"
    duration_minutes: int = 25
    soundscape: str = "binaural"

@router.get("/summary", response_model=AnalyticsSummaryOut)
async def get_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AnalyticsService.calculate_summary(db, current_user.id)

@router.post("/focus-session", status_code=status.HTTP_201_CREATED)
async def log_focus_session(
    session_in: FocusSessionLog,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = FocusSession(
        user_id=current_user.id,
        task_title=session_in.task_title,
        duration_minutes=session_in.duration_minutes,
        soundscape=session_in.soundscape
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return {
        "id": session.id,
        "task_title": session.task_title,
        "duration_minutes": session.duration_minutes,
        "soundscape": session.soundscape,
        "completed_at": session.completed_at.isoformat()
    }

@router.get("/focus-sessions")
async def get_focus_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(FocusSession).where(FocusSession.user_id == current_user.id).order_by(FocusSession.completed_at.desc())
    res = await db.execute(stmt)
    sessions = res.scalars().all()
    total_focus_mins = sum(s.duration_minutes for s in sessions)
    return {
        "total_sessions": len(sessions),
        "total_focus_minutes": total_focus_mins,
        "sessions": [
            {
                "id": s.id,
                "task_title": s.task_title,
                "duration_minutes": s.duration_minutes,
                "soundscape": s.soundscape,
                "completed_at": s.completed_at.isoformat()
            }
            for s in sessions
        ]
    }

@router.get("/mood-trends")
async def get_mood_trends(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habits = await HabitService.get_user_habits(db, current_user.id)
    all_logs = []
    category_moods = {}
    
    for h in habits:
        for l in h.logs:
            if l.mood_score is not None:
                all_logs.append({
                    "habit_id": h.id,
                    "habit_title": h.title,
                    "category": h.category,
                    "mood_score": l.mood_score,
                    "completed_at": l.completed_at.isoformat() if l.completed_at else None
                })
                category_moods.setdefault(h.category, []).append(l.mood_score)

    impact = MoodMatrixService.calculate_mood_impact(all_logs)
    cat_averages = {
        cat: round(sum(scores) / len(scores), 2)
        for cat, scores in category_moods.items()
    }

    return {
        "summary": impact,
        "category_averages": cat_averages,
        "recent_mood_logs": all_logs[-20:]
    }

@router.post("/generate-report", response_model=AnalyticsReportOut, status_code=status.HTTP_201_CREATED)
async def generate_report(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AnalyticsService.generate_report(db, current_user)

@router.get("/reports", response_model=list[AnalyticsReportOut])
async def list_reports(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AnalyticsService.get_user_reports(db, current_user.id)

@router.post("/focus-strategy")
async def get_focus_strategy(
    request: FocusRequest,
    current_user: User = Depends(get_current_user)
):
    return await run_focus_assistant_chain(
        task_title=request.task_title,
        duration_minutes=request.duration_minutes
    )
