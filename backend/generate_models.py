import os

base_dir = "c:/Users/dasun/OneDrive/Documents/GitHub/Haircut-Prediction-System/backend/app"

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# -- MODELS --
user_model = """
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
import uuid
from app.database.base import Base, TimestampMixin, generate_uuid

class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
"""
write_file("models/user.py", user_model)

hairstyle_model = """
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, JSON
from app.database.base import Base, TimestampMixin, generate_uuid

class Hairstyle(Base, TimestampMixin):
    __tablename__ = "hairstyles"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    face_shapes: Mapped[list] = mapped_column(JSON)
    hair_types: Mapped[list] = mapped_column(JSON)
    hair_lengths: Mapped[list] = mapped_column(JSON)
    hair_density: Mapped[list] = mapped_column(JSON)
    maintenance_level: Mapped[str] = mapped_column(String)
    style_tags: Mapped[list] = mapped_column(JSON)
    lifestyle_tags: Mapped[list] = mapped_column(JSON)
    gender_target: Mapped[str] = mapped_column(String)
    difficulty: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str] = mapped_column(String)
    thumbnail_url: Mapped[str] = mapped_column(String)
"""
write_file("models/hairstyle.py", hairstyle_model)

analysis_model = """
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
"""
write_file("models/analysis.py", analysis_model)

recommendation_model = """
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
"""
write_file("models/recommendation.py", recommendation_model)

tryon_model = """
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
"""
write_file("models/tryon.py", tryon_model)

favorite_model = """
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from app.database.base import Base, TimestampMixin, generate_uuid

class Favorite(Base, TimestampMixin):
    __tablename__ = "favorites"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    hairstyle_id: Mapped[str] = mapped_column(String, ForeignKey("hairstyles.id"))
    tryon_result_id: Mapped[str | None] = mapped_column(String, ForeignKey("tryon_results.id"), nullable=True)
"""
write_file("models/favorite.py", favorite_model)

model_init = """
from app.models.user import User
from app.models.hairstyle import Hairstyle
from app.models.analysis import AnalysisSession, FaceAnalysis, HairProfile
from app.models.recommendation import Recommendation
from app.models.tryon import TryOnResult
from app.models.favorite import Favorite
"""
write_file("models/__init__.py", model_init)

print("Generated models successfully!")
