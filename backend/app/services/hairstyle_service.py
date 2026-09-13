from app.repositories.hairstyle_repository import HairstyleRepository
from app.models.hairstyle import Hairstyle
from app.schemas.hairstyle import HairstyleResponse, HairstyleCreate, HairstyleUpdate
from typing import List, Optional
import uuid

class HairstyleService:
    def __init__(self, hairstyle_repo: HairstyleRepository):
        self.hairstyle_repo = hairstyle_repo

    async def get_all_hairstyles(self, skip: int = 0, limit: int = 100) -> List[HairstyleResponse]:
        hairstyles = await self.hairstyle_repo.get_all(skip=skip, limit=limit)
        return [HairstyleResponse.model_validate(h) for h in hairstyles]

    async def get_hairstyle_by_id(self, hairstyle_id: str) -> Optional[HairstyleResponse]:
        h = await self.hairstyle_repo.get_by_id(hairstyle_id)
        if not h:
            return None
        return HairstyleResponse.model_validate(h)

    async def create_hairstyle(self, data: HairstyleCreate) -> HairstyleResponse:
        data_dict = data.model_dump()
        new_id = str(uuid.uuid4())
        hairstyle = Hairstyle(id=new_id, **data_dict)
        created = await self.hairstyle_repo.create(hairstyle)
        return HairstyleResponse.model_validate(created)

    async def update_hairstyle(self, hairstyle_id: str, data: HairstyleUpdate) -> Optional[HairstyleResponse]:
        h = await self.hairstyle_repo.get_by_id(hairstyle_id)
        if not h:
            return None
            
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(h, key, value)
            
        await self.hairstyle_repo.db.commit()
        await self.hairstyle_repo.db.refresh(h)
        return HairstyleResponse.model_validate(h)

    async def delete_hairstyle(self, hairstyle_id: str) -> bool:
        h = await self.hairstyle_repo.get_by_id(hairstyle_id)
        if not h:
            return False
            
        await self.hairstyle_repo.db.delete(h)
        await self.hairstyle_repo.db.commit()
        return True
