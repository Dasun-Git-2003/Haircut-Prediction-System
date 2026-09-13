from app.repositories.tryon_repository import TryOnRepository
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.hairstyle_repository import HairstyleRepository
from app.schemas.tryon import TryOnResponse
from app.genai.factory import get_provider
from app.core.config import settings
import uuid
import os

class TryOnService:
    def __init__(self, tryon_repo: TryOnRepository, analysis_repo: AnalysisRepository, hairstyle_repo: HairstyleRepository):
        self.tryon_repo = tryon_repo
        self.analysis_repo = analysis_repo
        self.hairstyle_repo = hairstyle_repo

    async def generate_tryon(self, recommendation_id: str) -> TryOnResponse:
        # NOTE: Ideally we fetch TryOn, Recommendation, AnalysisSession and Hairstyle objects.
        # For simplicity, we are mocking the references.
        
        provider = get_provider(settings.GENAI_PROVIDER)
        
        # Mocking data to send to GenAI
        original_image_path = "mock/path/original.jpg" 
        hairstyle_details = {"name": "Textured Crop", "style": "Modern"}
        
        gen_result = await provider.generate_image(original_image_path, hairstyle_details)
        
        generated_image_path = os.path.join(settings.GENERATED_DIR, f"{uuid.uuid4()}.png")
        
        # Assuming the provider returned image bytes or a URL to save
        if "bytes" in gen_result:
            with open(generated_image_path, "wb") as f:
                f.write(gen_result["bytes"])
                
        return TryOnResponse(
            id=str(uuid.uuid4()),
            session_id="mock_session",
            recommendation_id=recommendation_id,
            hairstyle_id="mock_hairstyle",
            original_image_url=original_image_path,
            generated_image_url=f"/generated/{os.path.basename(generated_image_path)}",
            status="completed",
            generation_time_ms=gen_result.get("generation_time_ms", 0)
        )
