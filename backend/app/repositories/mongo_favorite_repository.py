from app.database.mongodb import get_mongo_db
from app.repositories.favorite_repository import FavoriteRepository
from app.models.favorite import Favorite
from typing import List, Optional
import uuid

class MongoFavoriteRepository:
    def __init__(self, fallback_repo: Optional[FavoriteRepository] = None):
        self.fallback_repo = fallback_repo

    @property
    def col(self):
        db = get_mongo_db()
        return db.favorites if db is not None else None

    async def get_by_id(self, id: str) -> Optional[Favorite]:
        if self.col is not None:
            try:
                doc = await self.col.find_one({"_id": id})
                if doc:
                    return Favorite(
                        id=doc["_id"],
                        user_id=doc.get("user_id"),
                        hairstyle_id=doc.get("hairstyle_id"),
                        tryon_result_id=doc.get("tryon_result_id")
                    )
            except Exception:
                pass
        if self.fallback_repo:
            return await self.fallback_repo.get_by_id(id)
        return None

    async def get_by_user_id(self, user_id: str) -> List[Favorite]:
        if self.col is not None:
            try:
                cursor = self.col.find({"user_id": user_id})
                docs = await cursor.to_list(length=100)
                if docs:
                    return [
                        Favorite(
                            id=doc["_id"],
                            user_id=doc.get("user_id"),
                            hairstyle_id=doc.get("hairstyle_id"),
                            tryon_result_id=doc.get("tryon_result_id")
                        )
                        for doc in docs
                    ]
            except Exception:
                pass
        if self.fallback_repo:
            return await self.fallback_repo.get_by_user_id(user_id)
        return []

    async def create(self, favorite: Favorite) -> Favorite:
        if self.col is not None:
            try:
                f_id = getattr(favorite, "id", None) or str(uuid.uuid4())
                doc = {
                    "_id": f_id,
                    "id": f_id,
                    "user_id": favorite.user_id,
                    "hairstyle_id": favorite.hairstyle_id,
                    "tryon_result_id": favorite.tryon_result_id
                }
                await self.col.insert_one(doc)
            except Exception:
                pass
        if self.fallback_repo:
            try:
                return await self.fallback_repo.create(favorite)
            except Exception:
                pass
        return favorite

    async def delete(self, favorite: Favorite) -> None:
        if self.col is not None:
            try:
                await self.col.delete_one({"_id": favorite.id})
            except Exception:
                pass
        if self.fallback_repo:
            await self.fallback_repo.delete(favorite)
