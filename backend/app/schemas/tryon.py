from pydantic import BaseModel, ConfigDict
from typing import Optional

class TryOnRequest(BaseModel):
    recommendation_id: str

class TryOnResponse(BaseModel):
    id: str
    session_id: str
    recommendation_id: str
    hairstyle_id: str
    original_image_url: str
    generated_image_url: Optional[str] = None
    status: str
    generation_time_ms: int
    
    model_config = ConfigDict(from_attributes=True)

class TryOnStatusResponse(BaseModel):
    id: str
    status: str
    generated_image_url: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
