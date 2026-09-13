from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Float, Integer, JSON
from app.database.base import Base, TimestampMixin, generate_uuid

class Recommendation(Base, TimestampMixin):
    __tablename__ = "recommendations"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String, ForeignKey("analysis_sessions.id"))
    hairstyle_id: Mapped[str] = mapped_column(String, ForeignKey("hairstyles.id"))
    score: Mapped[float] = mapped_column(Float)
    face_shape_score: Mapped[float] = mapped_column(Float)
    hair_type_score: Mapped[float] = mapped_column(Float)
    length_score: Mapped[float] = mapped_column(Float)
    density_score: Mapped[float] = mapped_column(Float)
    preference_score: Mapped[float] = mapped_column(Float)
    maintenance_score: Mapped[float] = mapped_column(Float)
    reasons: Mapped[list] = mapped_column(JSON)
    explanation: Mapped[str] = mapped_column(String)
    rank: Mapped[int] = mapped_column(Integer)
