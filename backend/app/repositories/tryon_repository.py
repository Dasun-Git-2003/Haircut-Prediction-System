from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.models.tryon import TryOnResult

class TryOnRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_by_id(self, id: str) -> Optional[TryOnResult]:
        return await self.db.get(TryOnResult, id)
        
    async def create(self, tryon: TryOnResult) -> TryOnResult:
        self.db.add(tryon)
        await self.db.commit()
        await self.db.refresh(tryon)
        return tryon
