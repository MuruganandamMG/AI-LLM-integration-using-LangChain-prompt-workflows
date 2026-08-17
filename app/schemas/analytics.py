from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AnalyticsSummaryOut(BaseModel):
    total_habits: int
    total_logs: int
    completion_rate: float
    longest_streak: int

class AnalyticsReportOut(BaseModel):
    id: str
    user_id: str
    total_habits: int
    completion_rate: float
    longest_streak: int
    ai_summary: str
    key_takeaways: list[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
