import os
import logging
from typing import Optional
from .base import AIImageProvider
from .prompts import build_hairstyle_prompt

logger = logging.getLogger(__name__)

class OpenAIProvider(AIImageProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.client_available = False
        
        if self.api_key:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=self.api_key)
                self.client_available = True
                logger.info("OpenAIProvider initialized successfully.")
            except ImportError:
                logger.error("openai package not installed.")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAIProvider: {e}")

    async def generate_hairstyle_preview(
        self,
        image: bytes,
        hairstyle_name: str,
        hairstyle_description: str,
        hair_type: str = "",
        mask: Optional[bytes] = None,
    ) -> bytes:
        if not self.is_available():
            raise Exception("OpenAIProvider is not available.")
            
        prompt = build_hairstyle_prompt(hairstyle_name, hairstyle_description, hair_type, high_quality=False)
        logger.info(f"OpenAI prompt: {prompt}")
        
        # In a real scenario, use self.client.images.edit(...)
        # Returning image as fallback
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
            raise Exception("OpenAIProvider is not available.")
            
        prompt = build_hairstyle_prompt(hairstyle_name, hairstyle_description, hair_type, high_quality=True)
        return image

    def is_available(self) -> bool:
        return self.client_available and self.api_key is not None
