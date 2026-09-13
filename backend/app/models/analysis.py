from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Float, JSON
from app.database.base import Base, TimestampMixin, generate_uuid

class AnalysisSession(Base, TimestampMixin):
    __tablename__ = "analysis_sessions"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[str | None] = mapped_column(String, ForeignKey("users.id"), nullable=True)
    original_image_path: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)

    face_analysis = relationship("FaceAnalysis", back_populates="session", uselist=False)
    hair_profile = relationship("HairProfile", back_populates="session", uselist=False)

class FaceAnalysis(Base, TimestampMixin):
    __tablename__ = "face_analyses"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String, ForeignKey("analysis_sessions.id"))
    face_shape: Mapped[str] = mapped_column(String)
    confidence: Mapped[float] = mapped_column(Float)
    face_length: Mapped[float] = mapped_column(Float)
    forehead_width: Mapped[float] = mapped_column(Float)
    cheekbone_width: Mapped[float] = mapped_column(Float)
    jaw_width: Mapped[float] = mapped_column(Float)
    chin_width: Mapped[float] = mapped_column(Float)
    face_width: Mapped[float] = mapped_column(Float)
    face_aspect_ratio: Mapped[float] = mapped_column(Float)
    jaw_ratio: Mapped[float] = mapped_column(Float)
    forehead_ratio: Mapped[float] = mapped_column(Float)
    cheekbone_ratio: Mapped[float] = mapped_column(Float)
    explanation: Mapped[str] = mapped_column(String)
    
    session = relationship("AnalysisSession", back_populates="face_analysis")

class HairProfile(Base, TimestampMixin):
    __tablename__ = "hair_profiles"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String, ForeignKey("analysis_sessions.id"))
    hair_type: Mapped[str] = mapped_column(String)
    hair_type_confidence: Mapped[float] = mapped_column(Float)
    hair_length: Mapped[str] = mapped_column(String)
    hair_density: Mapped[str] = mapped_column(String)
    hair_volume: Mapped[str] = mapped_column(String)
    raw_predictions: Mapped[dict] = mapped_column(JSON)

    session = relationship("AnalysisSession", back_populates="hair_profile")
