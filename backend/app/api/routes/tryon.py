from fastapi import APIRouter
from app.schemas.tryon import TryOnRequest, TryOnResponse
import uuid

router = APIRouter()

@router.post("/generate", response_model=TryOnResponse)
async def generate_tryon(request: TryOnRequest):
    return TryOnResponse(
        id=str(uuid.uuid4()),
        session_id="mock",
        recommendation_id=request.recommendation_id,
        hairstyle_id="mock",
        original_image_url="",
        status="pending",
        generation_time_ms=0
    )
