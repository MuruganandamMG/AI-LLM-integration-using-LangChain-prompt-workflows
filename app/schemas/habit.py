from datetime import datetime
from pydantic import BaseModel, ConfigDict

class HabitCreate(BaseModel):
    title: str
    description: str | None = None
    category: str = "General"
    frequency: str = "daily"

class HabitUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    frequency: str | None = None

class HabitLogCreate(BaseModel):
    notes: str | None = None
    mood_score: int | None = None

class HabitLogOut(BaseModel):
    id: str
    habit_id: str
    user_id: str
    completed_at: datetime
    notes: str | None
    mood_score: int | None

    model_config = ConfigDict(from_attributes=True)

class HabitOut(BaseModel):
    id: str
    user_id: str
    title: str
    description: str | None
    category: str
    frequency: str
    created_at: datetime
    logs: list[HabitLogOut] = []

    model_config = ConfigDict(from_attributes=True)
