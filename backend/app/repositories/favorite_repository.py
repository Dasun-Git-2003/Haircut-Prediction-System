from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models.favorite import Favorite

class FavoriteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_by_id(self, id: str) -> Optional[Favorite]:
        return await self.db.get(Favorite, id)
        
    async def create(self, favorite: Favorite) -> Favorite:
        self.db.add(favorite)
        await self.db.commit()
        await self.db.refresh(favorite)
        return favorite
