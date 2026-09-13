import cv2
import numpy as np
from dataclasses import dataclass, field
from typing import List, Union
import logging

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

def validate_image(image_input: Union[bytes, np.ndarray]) -> ValidationResult:
    """Validate image quality, size, resolution, and format."""
    errors = []
    warnings = []

    if isinstance(image_input, bytes):
        if len(image_input) > 10 * 1024 * 1024:
            errors.append("Image size exceeds 10MB limit.")
            return ValidationResult(is_valid=False, errors=errors)

        nparr = np.frombuffer(image_input, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    elif isinstance(image_input, np.ndarray):
        img = image_input
    else:
        errors.append("Unsupported image input type.")
        return ValidationResult(is_valid=False, errors=errors)

    if img is None or img.size == 0:
        errors.append("Invalid image format or corrupted image. Only JPEG, PNG, and WebP are supported.")
        return ValidationResult(is_valid=False, errors=errors)

    # Resolution check (min 200x200)
    h, w = img.shape[:2]
    if h < 200 or w < 200:
        errors.append(f"Image resolution too low ({w}x{h}). Minimum required is 200x200.")

    # Blur detection via Laplacian variance
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        variance = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        if variance < 100.0:
            warnings.append(f"Image might be blurry (variance: {variance:.2f}).")
    except Exception as e:
        warnings.append(f"Blur calculation skipped: {str(e)}")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

class ImageValidator:
    def validate(self, image_input: Union[bytes, np.ndarray]) -> ValidationResult:
        return validate_image(image_input)
