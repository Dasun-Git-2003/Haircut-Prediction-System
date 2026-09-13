from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.models.favorite import Favorite

class FavoriteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_by_id(self, id: str) -> Optional[Favorite]:
        return await self.db.get(Favorite, id)

    async def get_by_user_id(self, user_id: str) -> List[Favorite]:
        result = await self.db.execute(select(Favorite).where(Favorite.user_id == user_id))
        return list(result.scalars().all())
        
    async def create(self, favorite: Favorite) -> Favorite:
        self.db.add(favorite)
        await self.db.commit()
        await self.db.refresh(favorite)
        return favorite

    async def delete(self, favorite: Favorite) -> None:
        await self.db.delete(favorite)
        await self.db.commit()
