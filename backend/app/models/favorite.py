from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from app.database.base import Base, TimestampMixin, generate_uuid

class Favorite(Base, TimestampMixin):
    __tablename__ = "favorites"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    hairstyle_id: Mapped[str] = mapped_column(String, ForeignKey("hairstyles.id"))
    tryon_result_id: Mapped[str | None] = mapped_column(String, ForeignKey("tryon_results.id"), nullable=True)
