from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.hairstyle_repository import HairstyleRepository
from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.recommendation import UserPreferences, RecommendationResponse, RecommendationResult
from app.schemas.hairstyle import HairstyleResponse
from app.ml.recommendation.engine import RecommendationEngine

class RecommendationService:
    def __init__(self, recommendation_repo: RecommendationRepository, hairstyle_repo: HairstyleRepository, analysis_repo: AnalysisRepository):
        self.recommendation_repo = recommendation_repo
        self.hairstyle_repo = hairstyle_repo
        self.analysis_repo = analysis_repo
        self.engine = RecommendationEngine()

    async def get_recommendations(self, session_id: str, prefs: UserPreferences) -> RecommendationResponse:
        session = await self.analysis_repo.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")
            
        # Fetch all available hairstyles to rank
        hairstyles = await self.hairstyle_repo.get_all()
        
        # Map DB session data to input expected by engine
        # In actual prod, we would extract FaceShape and HairType from session.face_analysis / session.hair_profile
        analysis_data = {
            "face_shape": "oval",  # Replace with actual extraction
            "hair_type": "straight" # Replace with actual extraction
        }
        
        # Engine execution
        ranked_results = self.engine.rank(hairstyles, analysis_data, prefs.model_dump())
        
        recommendations = []
        for idx, result in enumerate(ranked_results):
            rec = RecommendationResult(
                id=f"rec-{idx}",
                score=result.get("score", 0.0),
                reasons=result.get("reasons", []),
                explanation=result.get("explanation", ""),
                rank=idx + 1,
                hairstyle=HairstyleResponse.model_validate(result["hairstyle"])
            )
            recommendations.append(rec)
            
        return RecommendationResponse(session_id=session_id, recommendations=recommendations)
