from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.dependencies import get_db
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.hairstyle_repository import HairstyleRepository
from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.recommendation import UserPreferences, RecommendationResponse
from app.services.recommendation_service import RecommendationService

router = APIRouter()

from app.repositories.mongo_recommendation_repository import MongoRecommendationRepository
from app.repositories.mongo_hairstyle_repository import MongoHairstyleRepository
from app.repositories.mongo_analysis_repository import MongoAnalysisRepository

def get_recommendation_service(db: AsyncSession = Depends(get_db)) -> RecommendationService:
    rec_repo = MongoRecommendationRepository(RecommendationRepository(db))
    hs_repo = MongoHairstyleRepository(HairstyleRepository(db))
    analysis_repo = MongoAnalysisRepository(AnalysisRepository(db))
    return RecommendationService(rec_repo, hs_repo, analysis_repo)

@router.post("/", response_model=RecommendationResponse)
@router.post("/{session_id}", response_model=RecommendationResponse)
async def create_recommendations(
    session_id: Optional[str] = None,
    prefs: Optional[UserPreferences] = None,
    service: RecommendationService = Depends(get_recommendation_service)
):
    try:
        if not session_id:
            raise HTTPException(status_code=400, detail="session_id is required")
        return await service.get_recommendations(session_id, prefs)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")

@router.get("/{analysis_id}", response_model=RecommendationResponse)
async def get_recommendations_by_session(
    analysis_id: str,
    service: RecommendationService = Depends(get_recommendation_service)
):
    try:
        return await service.get_recommendations(analysis_id, None)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recommendations: {str(e)}")
