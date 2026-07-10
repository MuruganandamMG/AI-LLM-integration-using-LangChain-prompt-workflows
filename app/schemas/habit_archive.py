from pydantic import BaseModel
from datetime import datetime

class HabitArchiveRequest(BaseModel):
    habit_id: str
    archive_reason: str | None = None

class HabitArchiveOut(BaseModel):
    habit_id: str
    is_archived: bool
    archived_at: datetime
