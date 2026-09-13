from enum import Enum
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, ConfigDict

class FaceShape(str, Enum):
    OVAL = "oval"
    ROUND = "round"
    SQUARE = "square"
    DIAMOND = "diamond"
    HEART = "heart"
    OBLONG = "oblong"

class HairType(str, Enum):
    STRAIGHT = "straight"
    WAVY = "wavy"
    CURLY = "curly"
    COILY = "coily"

class HairLength(str, Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
    BALD = "bald"

class HairDensity(str, Enum):
    THIN = "thin"
    MEDIUM = "medium"
    THICK = "thick"

class HairVolume(str, Enum):
    FLAT = "flat"
    AVERAGE = "average"
    VOLUMINOUS = "voluminous"

class MaintenanceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class StyleTag(str, Enum):
    CLASSIC = "classic"
    MODERN = "modern"
    EDGY = "edgy"
    PROFESSIONAL = "professional"
    CASUAL = "casual"

class LifestyleTag(str, Enum):
    ACTIVE = "active"
    CORPORATE = "corporate"
    OUTDOOR = "outdoor"
    FASHION = "fashion"

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    
    model_config = ConfigDict(from_attributes=True)

class ErrorResponse(BaseModel):
    error: str
