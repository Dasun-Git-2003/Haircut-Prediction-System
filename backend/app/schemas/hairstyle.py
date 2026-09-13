from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.schemas.common import FaceShape, HairType, HairLength, HairDensity, MaintenanceLevel, StyleTag, LifestyleTag

class HairstyleBase(BaseModel):
    name: str
    description: str
    category: str
    face_shapes: List[FaceShape]
    hair_types: List[HairType]
    hair_lengths: List[HairLength]
    hair_density: List[HairDensity]
    maintenance_level: MaintenanceLevel
    style_tags: List[StyleTag]
    lifestyle_tags: List[LifestyleTag]
    gender_target: str
    difficulty: int
    image_url: str
    thumbnail_url: str

class HairstyleCreate(HairstyleBase):
    pass

class HairstyleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    # Add optional fields for partial update

class HairstyleResponse(HairstyleBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)

class HairstyleListResponse(BaseModel):
    items: List[HairstyleResponse]
    total: int
    page: int
    size: int
    
    model_config = ConfigDict(from_attributes=True)
