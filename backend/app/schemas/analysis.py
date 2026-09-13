from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from app.schemas.common import FaceShape, HairType, HairLength, HairDensity, HairVolume, AnalysisStatus

class ImageUploadResponse(BaseModel):
    session_id: str
    message: str

class FaceAnalysisResult(BaseModel):
    face_shape: FaceShape
    confidence: float
    face_length: float
    forehead_width: float
    cheekbone_width: float
    jaw_width: float
    chin_width: float
    face_width: float
    face_aspect_ratio: float
    jaw_ratio: float
    forehead_ratio: float
    cheekbone_ratio: float
    explanation: str
    
    model_config = ConfigDict(from_attributes=True)

class HairAnalysisResult(BaseModel):
    hair_type: HairType
    hair_type_confidence: float
    hair_length: HairLength
    hair_density: HairDensity
    hair_volume: HairVolume
    raw_predictions: Dict[str, Any]
    
    model_config = ConfigDict(from_attributes=True)

class FullAnalysisResponse(BaseModel):
    session_id: str
    status: AnalysisStatus
    original_image_url: str
    face_analysis: Optional[FaceAnalysisResult] = None
    hair_profile: Optional[HairAnalysisResult] = None
    
    model_config = ConfigDict(from_attributes=True)
