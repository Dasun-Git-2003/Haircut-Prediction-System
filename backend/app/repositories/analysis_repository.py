from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.models.analysis import AnalysisSession, FaceAnalysis, HairProfile

class AnalysisRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_by_id(self, id: str) -> Optional[AnalysisSession]:
        return await self.db.get(AnalysisSession, id)
        
    async def create_session(self, session: AnalysisSession) -> AnalysisSession:
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session
