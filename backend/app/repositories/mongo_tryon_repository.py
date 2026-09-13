from app.database.mongodb import get_mongo_db
from app.repositories.tryon_repository import TryOnRepository
from app.models.tryon import TryOnResult
from typing import Optional
import uuid

class MongoTryOnRepository:
    def __init__(self, fallback_repo: Optional[TryOnRepository] = None):
        self.fallback_repo = fallback_repo

    @property
    def col(self):
        db = get_mongo_db()
        return db.tryon_results if db is not None else None

    async def get_by_id(self, id: str) -> Optional[TryOnResult]:
        if self.col is not None:
            try:
                doc = await self.col.find_one({"_id": id})
                if doc:
                    return TryOnResult(
                        id=doc["_id"],
                        session_id=doc.get("session_id"),
                        recommendation_id=doc.get("recommendation_id"),
                        hairstyle_id=doc.get("hairstyle_id"),
                        original_image_path=doc.get("original_image_path", ""),
                        generated_image_path=doc.get("generated_image_path", ""),
                        prompt_used=doc.get("prompt_used", ""),
                        provider_used=doc.get("provider_used", ""),
                        status=doc.get("status", "completed"),
                        generation_time_ms=doc.get("generation_time_ms", 0)
                    )
            except Exception:
                pass
        if self.fallback_repo:
            return await self.fallback_repo.get_by_id(id)
        return None

    async def create(self, tryon: TryOnResult) -> TryOnResult:
        if self.col is not None:
            try:
                t_id = getattr(tryon, "id", None) or str(uuid.uuid4())
                doc = {
                    "_id": t_id,
                    "id": t_id,
                    "session_id": tryon.session_id,
                    "recommendation_id": tryon.recommendation_id,
                    "hairstyle_id": tryon.hairstyle_id,
                    "original_image_path": tryon.original_image_path,
                    "generated_image_path": tryon.generated_image_path,
                    "prompt_used": tryon.prompt_used,
                    "provider_used": tryon.provider_used,
                    "status": tryon.status,
                    "generation_time_ms": tryon.generation_time_ms
                }
                await self.col.insert_one(doc)
            except Exception:
                pass
        if self.fallback_repo:
            try:
                return await self.fallback_repo.create(tryon)
            except Exception:
                pass
        return tryon
