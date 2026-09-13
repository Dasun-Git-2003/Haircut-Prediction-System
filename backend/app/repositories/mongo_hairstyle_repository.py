from app.database.mongodb import get_mongo_db
from app.repositories.hairstyle_repository import HairstyleRepository
from app.models.hairstyle import Hairstyle
from typing import List, Optional
import uuid

class MongoHairstyleRepository:
    def __init__(self, fallback_repo: Optional[HairstyleRepository] = None):
        self.fallback_repo = fallback_repo

    @property
    def col(self):
        db = get_mongo_db()
        return db.hairstyles if db is not None else None

    async def get_by_id(self, id: str) -> Optional[Hairstyle]:
        if self.col is not None:
            try:
                doc = await self.col.find_one({"_id": id})
                if doc:
                    return Hairstyle(
                        id=doc["_id"],
                        name=doc["name"],
                        description=doc["description"],
                        category=doc["category"],
                        face_shapes=doc.get("face_shapes", []),
                        hair_types=doc.get("hair_types", []),
                        hair_lengths=doc.get("hair_lengths", []),
                        hair_density=doc.get("hair_density", []),
                        maintenance_level=doc.get("maintenance_level", "medium"),
                        style_tags=doc.get("style_tags", []),
                        lifestyle_tags=doc.get("lifestyle_tags", []),
                        gender_target=doc.get("gender_target", "unisex"),
                        difficulty=doc.get("difficulty", 1),
                        image_url=doc.get("image_url", ""),
                        thumbnail_url=doc.get("thumbnail_url", "")
                    )
            except Exception:
                pass
        if self.fallback_repo:
            return await self.fallback_repo.get_by_id(id)
        return None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Hairstyle]:
        if self.col is not None:
            try:
                cursor = self.col.find({}).skip(skip).limit(limit)
                docs = await cursor.to_list(length=limit)
                if docs:
                    return [
                        Hairstyle(
                            id=doc["_id"],
                            name=doc["name"],
                            description=doc["description"],
                            category=doc["category"],
                            face_shapes=doc.get("face_shapes", []),
                            hair_types=doc.get("hair_types", []),
                            hair_lengths=doc.get("hair_lengths", []),
                            hair_density=doc.get("hair_density", []),
                            maintenance_level=doc.get("maintenance_level", "medium"),
                            style_tags=doc.get("style_tags", []),
                            lifestyle_tags=doc.get("lifestyle_tags", []),
                            gender_target=doc.get("gender_target", "unisex"),
                            difficulty=doc.get("difficulty", 1),
                            image_url=doc.get("image_url", ""),
                            thumbnail_url=doc.get("thumbnail_url", "")
                        )
                        for doc in docs
                    ]
            except Exception:
                pass
        if self.fallback_repo:
            return await self.fallback_repo.get_all(skip=skip, limit=limit)
        return []

    async def create(self, hairstyle: Hairstyle) -> Hairstyle:
        if self.col is not None:
            try:
                h_id = getattr(hairstyle, "id", None) or str(uuid.uuid4())
                doc = {
                    "_id": h_id,
                    "id": h_id,
                    "name": hairstyle.name,
                    "description": hairstyle.description,
                    "category": hairstyle.category,
                    "face_shapes": hairstyle.face_shapes,
                    "hair_types": hairstyle.hair_types,
                    "hair_lengths": hairstyle.hair_lengths,
                    "hair_density": hairstyle.hair_density,
                    "maintenance_level": hairstyle.maintenance_level,
                    "style_tags": hairstyle.style_tags,
                    "lifestyle_tags": hairstyle.lifestyle_tags,
                    "gender_target": hairstyle.gender_target,
                    "difficulty": hairstyle.difficulty,
                    "image_url": hairstyle.image_url,
                    "thumbnail_url": hairstyle.thumbnail_url
                }
                await self.col.insert_one(doc)
            except Exception:
                pass
        if self.fallback_repo:
            try:
                return await self.fallback_repo.create(hairstyle)
            except Exception:
                pass
        return hairstyle
