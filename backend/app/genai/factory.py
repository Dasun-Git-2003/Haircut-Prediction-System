import os
import logging
from .base import AIImageProvider
from .gemini import GeminiProvider
from .openai_provider import OpenAIProvider
from .stable_diffusion import StableDiffusionProvider

logger = logging.getLogger(__name__)

def get_provider(config: dict = None) -> AIImageProvider:
    provider_name = os.environ.get("GENAI_PROVIDER", "gemini").lower()
    if config and "provider" in config:
        provider_name = config["provider"].lower()
        
    logger.info(f"Requested GenAI Provider: {provider_name}")
    
    if provider_name == "openai":
        provider = OpenAIProvider()
        if provider.is_available():
            return provider
            
    elif provider_name == "stable_diffusion":
        provider = StableDiffusionProvider()
        if provider.is_available():
            return provider
            
    # Default/Fallback to Gemini
    provider = GeminiProvider()
    if provider.is_available():
        return provider
        
    logger.warning("No requested provider is fully configured/available. Returning unconfigured GeminiProvider as fallback.")
    return GeminiProvider()
