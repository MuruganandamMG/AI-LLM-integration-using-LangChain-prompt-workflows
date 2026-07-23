from pydantic import BaseModel

class HabitFilterParams(BaseModel):
    category: str | None = None
    search: str | None = None
