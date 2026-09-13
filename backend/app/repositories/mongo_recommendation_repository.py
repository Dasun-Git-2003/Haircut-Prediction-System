from app.database.mongodb import get_mongo_db
from app.repositories.recommendation_repository import RecommendationRepository
from app.models.recommendation import Recommendation
from typing import List, Optional
import uuid

class MongoRecommendationRepository:
    def __init__(self, fallback_repo: Optional[RecommendationRepository] = None):
        self.fallback_repo = fallback_repo

    @property
    def col(self):
        db = get_mongo_db()
        return db.recommendations if db is not None else None

    async def get_by_id(self, id: str) -> Optional[Recommendation]:
        if self.col is not None:
            try:
                doc = await self.col.find_one({"_id": id})
                if doc:
                    return Recommendation(
                        id=doc["_id"],
                        session_id=doc.get("session_id"),
                        hairstyle_id=doc.get("hairstyle_id"),
                        score=doc.get("score", 0.0),
                        face_shape_score=doc.get("face_shape_score", 1.0),
                        hair_type_score=doc.get("hair_type_score", 1.0),
                        length_score=doc.get("length_score", 1.0),
                        density_score=doc.get("density_score", 1.0),
                        preference_score=doc.get("preference_score", 1.0),
                        maintenance_score=doc.get("maintenance_score", 1.0),
                        reasons=doc.get("reasons", []),
                        explanation=doc.get("explanation", ""),
                        rank=doc.get("rank", 1)
                    )
            except Exception:
                pass
        if self.fallback_repo:
            return await self.fallback_repo.get_by_id(id)
        return None

    async def get_by_session_id(self, session_id: str) -> List[Recommendation]:
        if self.col is not None:
            try:
                cursor = self.col.find({"session_id": session_id})
                docs = await cursor.to_list(length=100)
                if docs:
                    return [
                        Recommendation(
                            id=doc["_id"],
                            session_id=doc.get("session_id"),
                            hairstyle_id=doc.get("hairstyle_id"),
                            score=doc.get("score", 0.0),
                            face_shape_score=doc.get("face_shape_score", 1.0),
                            hair_type_score=doc.get("hair_type_score", 1.0),
                            length_score=doc.get("length_score", 1.0),
                            density_score=doc.get("density_score", 1.0),
                            preference_score=doc.get("preference_score", 1.0),
                            maintenance_score=doc.get("maintenance_score", 1.0),
                            reasons=doc.get("reasons", []),
                            explanation=doc.get("explanation", ""),
                            rank=doc.get("rank", 1)
                        )
                        for doc in docs
                    ]
            except Exception:
                pass
        if self.fallback_repo:
            return await self.fallback_repo.get_by_session_id(session_id)
        return []

    async def create(self, recommendation: Recommendation) -> Recommendation:
        if self.col is not None:
            try:
                rec_id = getattr(recommendation, "id", None) or str(uuid.uuid4())
                doc = {
                    "_id": rec_id,
                    "id": rec_id,
                    "session_id": recommendation.session_id,
                    "hairstyle_id": recommendation.hairstyle_id,
                    "score": recommendation.score,
                    "face_shape_score": recommendation.face_shape_score,
                    "hair_type_score": recommendation.hair_type_score,
                    "length_score": recommendation.length_score,
                    "density_score": recommendation.density_score,
                    "preference_score": recommendation.preference_score,
                    "maintenance_score": recommendation.maintenance_score,
                    "reasons": recommendation.reasons,
                    "explanation": recommendation.explanation,
                    "rank": recommendation.rank
                }
                await self.col.insert_one(doc)
            except Exception:
                pass
        if self.fallback_repo:
            try:
                return await self.fallback_repo.create(recommendation)
            except Exception:
                pass
        return recommendation
