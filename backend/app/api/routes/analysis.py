from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.repositories.analysis_repository import AnalysisRepository
from app.services.image_service import ImageService
from app.services.analysis_service import AnalysisService
from app.schemas.analysis import ImageUploadResponse, FullAnalysisResponse

router = APIRouter()

from app.repositories.mongo_analysis_repository import MongoAnalysisRepository

def get_analysis_service(db: AsyncSession = Depends(get_db)) -> AnalysisService:
    return AnalysisService(MongoAnalysisRepository(AnalysisRepository(db)))

@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    service: AnalysisService = Depends(get_analysis_service)
):
    try:
        path = await ImageService.save_upload(file)
        session = await service.create_session(image_path=path)
        return ImageUploadResponse(
            session_id=session.id,
            message="Image uploaded and validated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyze/{session_id}", response_model=FullAnalysisResponse)
@router.post("/{session_id}/analyze", response_model=FullAnalysisResponse)
async def analyze(
    session_id: str,
    service: AnalysisService = Depends(get_analysis_service)
):
    try:
        return await service.analyze_image(session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/{session_id}", response_model=FullAnalysisResponse)
async def get_analysis(
    session_id: str,
    service: AnalysisService = Depends(get_analysis_service)
):
    session = await service.analysis_repo.get_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Analysis session not found")
        
    return await service.analyze_image(session_id)
