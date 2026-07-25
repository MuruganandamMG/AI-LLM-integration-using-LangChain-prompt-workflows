from pydantic import BaseModel

class DailyQuest(BaseModel):
    id: str
    title: str
    xp_reward: int
    is_completed: bool
