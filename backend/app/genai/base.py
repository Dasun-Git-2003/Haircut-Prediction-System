from abc import ABC, abstractmethod
from typing import Optional

class AIImageProvider(ABC):
    @abstractmethod
    async def generate_hairstyle_preview(
        self,
        image: bytes,
        hairstyle_name: str,
        hairstyle_description: str,
        hair_type: str = "",
        mask: Optional[bytes] = None,
    ) -> bytes:
        """Generate a hairstyle preview. Returns image bytes."""
        pass
    
    @abstractmethod
    async def generate_high_quality_preview(
        self,
        image: bytes,
        hairstyle_name: str,
        hairstyle_description: str,
        hair_type: str = "",
        mask: Optional[bytes] = None,
    ) -> bytes:
        """Generate a higher quality preview. Returns image bytes."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is configured and available."""
        pass
