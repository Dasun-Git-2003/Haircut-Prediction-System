from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.models.recommendation import Recommendation

class RecommendationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_by_session_id(self, session_id: str) -> List[Recommendation]:
        result = await self.db.execute(select(Recommendation).where(Recommendation.session_id == session_id))
        return result.scalars().all()
        
    async def create(self, recommendation: Recommendation) -> Recommendation:
        self.db.add(recommendation)
        await self.db.commit()
        await self.db.refresh(recommendation)
        return recommendation
