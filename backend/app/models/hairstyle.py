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
