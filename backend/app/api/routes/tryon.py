from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.schemas.tryon import TryOnRequest, TryOnResponse
from app.repositories.tryon_repository import TryOnRepository
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.hairstyle_repository import HairstyleRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.services.tryon_service import TryOnService

router = APIRouter()

from app.repositories.mongo_tryon_repository import MongoTryOnRepository
from app.repositories.mongo_analysis_repository import MongoAnalysisRepository
from app.repositories.mongo_hairstyle_repository import MongoHairstyleRepository
from app.repositories.mongo_recommendation_repository import MongoRecommendationRepository

def get_tryon_service(db: AsyncSession = Depends(get_db)) -> TryOnService:
    return TryOnService(
        tryon_repo=MongoTryOnRepository(TryOnRepository(db)),
        analysis_repo=MongoAnalysisRepository(AnalysisRepository(db)),
        hairstyle_repo=MongoHairstyleRepository(HairstyleRepository(db)),
        recommendation_repo=MongoRecommendationRepository(RecommendationRepository(db))
    )

@router.post("/generate", response_model=TryOnResponse)
@router.post("/{recommendation_id}", response_model=TryOnResponse)
async def generate_tryon(
    recommendation_id: Optional[str] = None,
    request: Optional[TryOnRequest] = None,
    service: TryOnService = Depends(get_tryon_service)
):
    try:
        rec_id = (request.recommendation_id if request else None) or recommendation_id
        if not rec_id:
            raise HTTPException(status_code=400, detail="Recommendation ID required")
        return await service.generate_tryon(rec_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate try-on: {str(e)}")

@router.get("/{id}", response_model=TryOnResponse)
async def get_tryon(
    id: str,
    service: TryOnService = Depends(get_tryon_service)
):
    try:
        return await service.get_tryon_by_id(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve try-on: {str(e)}")
