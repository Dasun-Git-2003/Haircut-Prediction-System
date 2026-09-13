import cv2
import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

def validate_image(image_bytes: bytes) -> ValidationResult:
    """Validate image quality, size, and type."""
    errors = []
    warnings = []
    
    # Check size (10MB max)
    if len(image_bytes) > 10 * 1024 * 1024:
        errors.append("Image size exceeds 10MB limit.")
        return ValidationResult(is_valid=False, errors=errors)

    # Decode image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        errors.append("Invalid image format or corrupted image. Only JPEG, PNG, and WebP are supported.")
        return ValidationResult(is_valid=False, errors=errors)

    # Check resolution (min 200x200)
    h, w = img.shape[:2]
    if h < 200 or w < 200:
        errors.append(f"Image resolution too low ({w}x{h}). Minimum required is 200x200.")
    
    # Blur detection using Laplacian variance
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    if variance < 100.0:
        warnings.append(f"Image might be blurry (variance: {variance:.2f}).")
        
    return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)
