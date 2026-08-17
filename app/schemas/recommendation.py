from datetime import datetime
from pydantic import BaseModel, ConfigDict

class RecommendationOut(BaseModel):
    id: str
    user_id: str
    title: str
    category: str
    action_items: list[str]
    reasoning: str
    llm_provider: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
