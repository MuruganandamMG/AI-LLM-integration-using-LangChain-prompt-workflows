from pydantic import BaseModel, ConfigDict

class Badge(BaseModel):
    name: str
    description: str
    icon: str
    unlocked: bool

class GamificationStatsOut(BaseModel):
    user_id: str
    total_xp: int
    level: int
    tier: str
    completed_logs: int
    streak_days: int
    badges: list[Badge]

    model_config = ConfigDict(from_attributes=True)
