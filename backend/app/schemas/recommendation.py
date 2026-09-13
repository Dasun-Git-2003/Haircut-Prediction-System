from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.schemas.common import HairLength, MaintenanceLevel, StyleTag, LifestyleTag
from app.schemas.hairstyle import HairstyleResponse

class UserPreferences(BaseModel):
    preferred_length: Optional[HairLength] = None
    maintenance: Optional[MaintenanceLevel] = None
    style: Optional[StyleTag] = None
    lifestyle: Optional[LifestyleTag] = None
    haircut_category: Optional[str] = None

class RecommendationResult(BaseModel):
    id: str
    score: float
    reasons: List[str]
    explanation: str
    rank: int
    hairstyle: HairstyleResponse
    
    model_config = ConfigDict(from_attributes=True)

class RecommendationResponse(BaseModel):
    session_id: str
    recommendations: List[RecommendationResult]
    
    model_config = ConfigDict(from_attributes=True)
