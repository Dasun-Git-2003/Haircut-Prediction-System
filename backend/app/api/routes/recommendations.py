from fastapi import APIRouter, Depends
from app.schemas.recommendation import UserPreferences, RecommendationResponse

router = APIRouter()

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(session_id: str, prefs: UserPreferences):
    return RecommendationResponse(session_id=session_id, recommendations=[])
