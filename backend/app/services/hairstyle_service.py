from app.repositories.hairstyle_repository import HairstyleRepository
from app.schemas.hairstyle import HairstyleResponse
from typing import List

class HairstyleService:
    def __init__(self, hairstyle_repo: HairstyleRepository):
        self.hairstyle_repo = hairstyle_repo

    async def get_all_hairstyles(self) -> List[HairstyleResponse]:
        hairstyles = await self.hairstyle_repo.get_all()
        return [HairstyleResponse.model_validate(h) for h in hairstyles]
