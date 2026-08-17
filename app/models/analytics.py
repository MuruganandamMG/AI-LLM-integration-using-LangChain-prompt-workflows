import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, Float, JSON, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class AnalyticsReport(Base):
    __tablename__ = "analytics_reports"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    total_habits: Mapped[int] = mapped_column(Integer, nullable=False)
    completion_rate: Mapped[float] = mapped_column(Float, nullable=False)
    longest_streak: Mapped[int] = mapped_column(Integer, nullable=False)
    ai_summary: Mapped[str] = mapped_column(Text, nullable=False)
    key_takeaways: Mapped[list] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="analytics_reports")
