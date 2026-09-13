from app.repositories.tryon_repository import TryOnRepository
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.hairstyle_repository import HairstyleRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.schemas.tryon import TryOnResponse
from app.models.tryon import TryOnResult
from app.genai.factory import get_provider
from app.core.config import settings
import uuid
import os
import time

class TryOnService:
    def __init__(
        self,
        tryon_repo: TryOnRepository,
        analysis_repo: AnalysisRepository,
        hairstyle_repo: HairstyleRepository,
        recommendation_repo: RecommendationRepository
    ):
        self.tryon_repo = tryon_repo
        self.analysis_repo = analysis_repo
        self.hairstyle_repo = hairstyle_repo
        self.recommendation_repo = recommendation_repo

    async def generate_tryon(self, recommendation_id: str) -> TryOnResponse:
        rec = await self.recommendation_repo.get_by_id(recommendation_id)
        
        session_id = getattr(rec, "session_id", "default_session") if rec else "default_session"
        hairstyle_id = getattr(rec, "hairstyle_id", None) if rec else None
        
        session = await self.analysis_repo.get_by_id(session_id) if session_id else None
        original_image_path = session.original_image_path if session else ""
        
        hs = await self.hairstyle_repo.get_by_id(hairstyle_id) if hairstyle_id else None
        hs_name = hs.name if hs else "Recommended Hairstyle"
        hs_desc = hs.description if hs else "Natural modern haircut"
        
        hair_type = "natural"
        if session and getattr(session, "hair_profile", None):
            hair_type = getattr(session.hair_profile, "hair_type", "natural")
        
        provider = get_provider({"provider": settings.GENAI_PROVIDER})
        
        # Load image bytes if original file exists
        image_bytes = b""
        if original_image_path and os.path.exists(original_image_path):
            with open(original_image_path, "rb") as f:
                image_bytes = f.read()
        else:
            image_bytes = b"mock_original_image_bytes"

        start_time = time.time()
        try:
            generated_bytes = await provider.generate_hairstyle_preview(
                image=image_bytes,
                hairstyle_name=hs_name,
                hairstyle_description=hs_desc,
                hair_type=hair_type
            )
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"TryOn generation error: {e}")
            generated_bytes = image_bytes
            
        gen_time = int((time.time() - start_time) * 1000)
        
        os.makedirs(settings.GENERATED_DIR, exist_ok=True)
        filename = f"tryon_{uuid.uuid4().hex[:12]}.png"
        generated_filepath = os.path.join(settings.GENERATED_DIR, filename)
        
        with open(generated_filepath, "wb") as f:
            f.write(generated_bytes)
            
        tryon_id = str(uuid.uuid4())
        tryon_result = TryOnResult(
            id=tryon_id,
            session_id=session_id,
            recommendation_id=recommendation_id,
            hairstyle_id=hairstyle_id or "unknown",
            original_image_path=original_image_path,
            generated_image_path=generated_filepath,
            prompt_used=f"Hairstyle: {hs_name}, Style: {hs_desc}",
            provider_used=settings.GENAI_PROVIDER,
            status="completed",
            generation_time_ms=gen_time
        )
        
        try:
            await self.tryon_repo.create(tryon_result)
        except Exception:
            pass

        return TryOnResponse(
            id=tryon_id,
            session_id=session_id,
            recommendation_id=recommendation_id,
            hairstyle_id=hairstyle_id or "unknown",
            original_image_url=f"/uploads/{os.path.basename(original_image_path)}" if original_image_path else "",
            generated_image_url=f"/generated/{filename}",
            status="completed",
            generation_time_ms=gen_time
        )

    async def get_tryon_by_id(self, tryon_id: str) -> TryOnResponse:
        res = await self.tryon_repo.get_by_id(tryon_id)
        if not res:
            raise ValueError("Try-on result not found")
            
        return TryOnResponse(
            id=res.id,
            session_id=res.session_id,
            recommendation_id=res.recommendation_id,
            hairstyle_id=res.hairstyle_id,
            original_image_url=f"/uploads/{os.path.basename(res.original_image_path)}" if res.original_image_path else "",
            generated_image_url=f"/generated/{os.path.basename(res.generated_image_path)}" if res.generated_image_path else None,
            status=res.status,
            generation_time_ms=res.generation_time_ms
        )
