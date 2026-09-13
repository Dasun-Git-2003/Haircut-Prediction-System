from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Integer
from app.database.base import Base, TimestampMixin, generate_uuid

class TryOnResult(Base, TimestampMixin):
    __tablename__ = "tryon_results"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String, ForeignKey("analysis_sessions.id"))
    recommendation_id: Mapped[str] = mapped_column(String, ForeignKey("recommendations.id"))
    hairstyle_id: Mapped[str] = mapped_column(String, ForeignKey("hairstyles.id"))
    original_image_path: Mapped[str] = mapped_column(String)
    generated_image_path: Mapped[str] = mapped_column(String)
    prompt_used: Mapped[str] = mapped_column(String)
    provider_used: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    generation_time_ms: Mapped[int] = mapped_column(Integer)
