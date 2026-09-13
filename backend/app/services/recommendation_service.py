from typing import Optional
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.hairstyle_repository import HairstyleRepository
from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.recommendation import UserPreferences, RecommendationResponse, RecommendationResult
from app.schemas.hairstyle import HairstyleResponse
from app.ml.recommendation.engine import RecommendationEngine
from app.models.recommendation import Recommendation
import uuid

class RecommendationService:
    def __init__(
        self, 
        recommendation_repo: RecommendationRepository, 
        hairstyle_repo: HairstyleRepository, 
        analysis_repo: AnalysisRepository
    ):
        self.recommendation_repo = recommendation_repo
        self.hairstyle_repo = hairstyle_repo
        self.analysis_repo = analysis_repo
        self.engine = RecommendationEngine()

    async def get_recommendations(self, session_id: str, prefs: Optional[UserPreferences] = None) -> RecommendationResponse:
        session = await self.analysis_repo.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")
            
        hairstyles = await self.hairstyle_repo.get_all(limit=100)
        if not hairstyles:
            return RecommendationResponse(session_id=session_id, recommendations=[])

        # Extract features from session if available
        face_shape = "oval"
        hair_type = "straight"
        hair_length = "medium"
        hair_density = "medium"
        
        if getattr(session, "face_analysis", None):
            face_shape = getattr(session.face_analysis, "face_shape", "oval")
        if getattr(session, "hair_profile", None):
            hair_type = getattr(session.hair_profile, "hair_type", "straight")
            hair_length = getattr(session.hair_profile, "hair_length", "medium")
            hair_density = getattr(session.hair_profile, "hair_density", "medium")

        face_analysis_data = {"face_shape": face_shape}
        hair_analysis_data = {
            "hair_type": hair_type,
            "hair_length": hair_length,
            "hair_density": hair_density
        }

        pref_dict = prefs.model_dump() if prefs else {}
        ranked_results = self.engine.recommend(
            face_analysis=face_analysis_data,
            hair_analysis=hair_analysis_data,
            preferences=pref_dict,
            hairstyles=hairstyles,
            top_k=5
        )
        
        hairstyle_map = {h.id: h for h in hairstyles}
        
        recommendations = []
        for idx, res in enumerate(ranked_results):
            hs = hairstyle_map.get(res.hairstyle_id)
            if not hs:
                continue

            # Persist to database if possible
            rec_id = str(uuid.uuid4())
            try:
                db_rec = Recommendation(
                    id=rec_id,
                    session_id=session_id,
                    hairstyle_id=hs.id,
                    score=res.score,
                    face_shape_score=res.individual_scores.get("face_shape", 1.0),
                    hair_type_score=res.individual_scores.get("hair_type", 1.0),
                    length_score=res.individual_scores.get("length", 1.0),
                    density_score=res.individual_scores.get("density", 1.0),
                    preference_score=res.individual_scores.get("preference", 1.0),
                    maintenance_score=res.individual_scores.get("maintenance", 1.0),
                    reasons=res.reasons,
                    explanation=res.explanation.get("summary", ""),
                    rank=idx + 1
                )
                await self.recommendation_repo.create(db_rec)
            except Exception:
                # If already created or error occurs, fall back to in-memory ID
                pass

            rec_schema = RecommendationResult(
                id=rec_id,
                score=res.score,
                reasons=res.reasons,
                explanation=res.explanation.get("summary", ""),
                rank=idx + 1,
                hairstyle=HairstyleResponse.model_validate(hs)
            )
            recommendations.append(rec_schema)
            
        return RecommendationResponse(session_id=session_id, recommendations=recommendations)
