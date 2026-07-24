from pydantic import BaseModel
from datetime import datetime

class AuditLogOut(BaseModel):
    user_id: str
    action: str
    ip_address: str | None = None
    user_agent: str | None = None
    timestamp: datetime
