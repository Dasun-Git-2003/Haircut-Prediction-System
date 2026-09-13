from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.models.hairstyle import Hairstyle

class HairstyleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_by_id(self, id: str) -> Optional[Hairstyle]:
        return await self.db.get(Hairstyle, id)
        
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Hairstyle]:
        result = await self.db.execute(select(Hairstyle).offset(skip).limit(limit))
        return result.scalars().all()
        
    async def create(self, hairstyle: Hairstyle) -> Hairstyle:
        self.db.add(hairstyle)
        await self.db.commit()
        await self.db.refresh(hairstyle)
        return hairstyle
