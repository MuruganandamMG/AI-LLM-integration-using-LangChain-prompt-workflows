from pydantic import BaseModel, ConfigDict
from datetime import datetime, timezone

class WeeklyReviewOut(BaseModel):
    user_id: str
    overall_sentiment: str
    wins: list[str]
    improvement_areas: list[str]
    next_week_smart_goals: list[str]
    coach_note: str
    generated_at: datetime = datetime.now(timezone.utc)

    model_config = ConfigDict(from_attributes=True)
