from enum import Enum
from pydantic import BaseModel

class TimeOfDaySlot(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    ANYTIME = "anytime"

class HabitSchedule(BaseModel):
    time_slot: TimeOfDaySlot = TimeOfDaySlot.ANYTIME
    reminder_time: str | None = "09:00"
