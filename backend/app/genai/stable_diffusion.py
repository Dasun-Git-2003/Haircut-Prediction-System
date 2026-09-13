import os
import logging
from typing import Optional
from .base import AIImageProvider
from .prompts import build_hairstyle_prompt

logger = logging.getLogger(__name__)

class StableDiffusionProvider(AIImageProvider):
    def __init__(self, sd_url: str = None):
        self.sd_url = sd_url or os.environ.get("STABLE_DIFFUSION_URL")
        self.client_available = bool(self.sd_url)
        if self.client_available:
            logger.info(f"StableDiffusionProvider initialized with URL: {self.sd_url}")
        else:
            logger.warning("StableDiffusionProvider not available. STABLE_DIFFUSION_URL not set.")

    async def generate_hairstyle_preview(
        self,
        image: bytes,
        hairstyle_name: str,
        hairstyle_description: str,
        hair_type: str = "",
        mask: Optional[bytes] = None,
    ) -> bytes:
        if not self.is_available():
            raise Exception("StableDiffusionProvider is not available.")
            
        prompt = build_hairstyle_prompt(hairstyle_name, hairstyle_description, hair_type, high_quality=False)
        logger.info(f"SD Prompt: {prompt}")
        
        # Placeholder for A1111/ComfyUI API call
        return image

    async def generate_high_quality_preview(
        self,
        image: bytes,
        hairstyle_name: str,
        hairstyle_description: str,
        hair_type: str = "",
        mask: Optional[bytes] = None,
    ) -> bytes:
        if not self.is_available():
            raise Exception("StableDiffusionProvider is not available.")
            
        prompt = build_hairstyle_prompt(hairstyle_name, hairstyle_description, hair_type, high_quality=True)
        return image

    def is_available(self) -> bool:
        return self.client_available
