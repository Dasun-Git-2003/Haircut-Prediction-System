from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class HairstyleBase(BaseModel):
    name: str
    description: str
    category: str
    face_shapes: List[str]
    hair_types: List[str]
    hair_lengths: List[str]
    hair_density: List[str]
    maintenance_level: str
    style_tags: List[str]
    lifestyle_tags: List[str]
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
    face_shapes: Optional[List[str]] = None
    hair_types: Optional[List[str]] = None
    hair_lengths: Optional[List[str]] = None
    hair_density: Optional[List[str]] = None
    maintenance_level: Optional[str] = None
    style_tags: Optional[List[str]] = None
    lifestyle_tags: Optional[List[str]] = None
    gender_target: Optional[str] = None
    difficulty: Optional[int] = None
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

class HairstyleResponse(HairstyleBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)

class HairstyleListResponse(BaseModel):
    items: List[HairstyleResponse]
    total: int
    page: int
    size: int
    
    model_config = ConfigDict(from_attributes=True)
