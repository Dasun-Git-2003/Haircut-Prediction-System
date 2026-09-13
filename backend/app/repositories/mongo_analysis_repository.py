from app.database.mongodb import get_mongo_db
from app.repositories.analysis_repository import AnalysisRepository
from app.models.analysis import AnalysisSession, FaceAnalysis, HairProfile
from typing import Optional
import uuid

class MongoAnalysisRepository:
    def __init__(self, fallback_repo: Optional[AnalysisRepository] = None):
        self.fallback_repo = fallback_repo

    @property
    def db_col(self):
        db = get_mongo_db()
        return db.analysis_sessions if db is not None else None

    @property
    def db(self):
        return getattr(self.fallback_repo, "db", None)

    async def get_by_id(self, id: str) -> Optional[AnalysisSession]:
        if self.db_col is not None:
            try:
                doc = await self.db_col.find_one({"_id": id})
                if doc:
                    session = AnalysisSession(
                        id=doc["_id"],
                        user_id=doc.get("user_id"),
                        original_image_path=doc.get("original_image_path", ""),
                        status=doc.get("status", "pending")
                    )
                    if doc.get("face_analysis"):
                        fa = doc["face_analysis"]
                        session.face_analysis = FaceAnalysis(
                            id=fa.get("id", str(uuid.uuid4())),
                            session_id=id,
                            face_shape=fa.get("face_shape", "oval"),
                            confidence=fa.get("confidence", 0.9),
                            face_length=fa.get("face_length", 1.4),
                            forehead_width=fa.get("forehead_width", 1.0),
                            cheekbone_width=fa.get("cheekbone_width", 1.1),
                            jaw_width=fa.get("jaw_width", 0.9),
                            chin_width=fa.get("chin_width", 0.5),
                            face_width=fa.get("face_width", 1.1),
                            face_aspect_ratio=fa.get("face_aspect_ratio", 1.3),
                            jaw_ratio=fa.get("jaw_ratio", 0.8),
                            forehead_ratio=fa.get("forehead_ratio", 0.9),
                            cheekbone_ratio=fa.get("cheekbone_ratio", 1.0),
                            explanation=fa.get("explanation", "")
                        )
                    if doc.get("hair_profile"):
                        hp = doc["hair_profile"]
                        session.hair_profile = HairProfile(
                            id=hp.get("id", str(uuid.uuid4())),
                            session_id=id,
                            hair_type=hp.get("hair_type", "wavy"),
                            hair_type_confidence=hp.get("hair_type_confidence", 0.9),
                            hair_length=hp.get("hair_length", "medium"),
                            hair_density=hp.get("hair_density", "medium"),
                            hair_volume=hp.get("hair_volume", "average"),
                            raw_predictions=hp.get("raw_predictions", {})
                        )
                    return session
            except Exception:
                pass
        if self.fallback_repo:
            return await self.fallback_repo.get_by_id(id)
        return None

    async def create_session(self, session: AnalysisSession) -> AnalysisSession:
        if self.db_col is not None:
            try:
                s_id = getattr(session, "id", None) or str(uuid.uuid4())
                doc = {
                    "_id": s_id,
                    "id": s_id,
                    "user_id": getattr(session, "user_id", None),
                    "original_image_path": session.original_image_path,
                    "status": session.status,
                    "face_analysis": None,
                    "hair_profile": None
                }
                await self.db_col.insert_one(doc)
            except Exception:
                pass
        if self.fallback_repo:
            try:
                return await self.fallback_repo.create_session(session)
            except Exception:
                pass
        return session
