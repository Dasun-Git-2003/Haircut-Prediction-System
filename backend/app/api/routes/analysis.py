from fastapi import APIRouter, UploadFile, File, Depends
from app.services.image_service import ImageService
from app.schemas.analysis import ImageUploadResponse, FullAnalysisResponse

router = APIRouter()

@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    path = await ImageService.save_upload(file)
    # mock session
    return ImageUploadResponse(session_id="mock_session", message="Uploaded successfully")

@router.post("/analyze/{session_id}", response_model=FullAnalysisResponse)
async def analyze(session_id: str):
    # mock analyze
    return FullAnalysisResponse(session_id=session_id, status="completed", original_image_url="")
