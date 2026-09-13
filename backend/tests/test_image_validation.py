import cv2
import numpy as np
from app.ml.face_analysis.image_validator import validate_image, ImageValidator

def create_dummy_image(w=300, h=300, color=(120, 150, 180)):
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:] = color
    # Add some texture/lines to avoid false blur flag
    for i in range(10, h, 20):
        cv2.line(img, (0, i), (w, i), (255, 255, 255), 2)
    _, encoded = cv2.imencode(".jpg", img)
    return encoded.tobytes()

def test_valid_image():
    img_bytes = create_dummy_image(300, 300)
    res = validate_image(img_bytes)
    assert res.is_valid is True
    assert len(res.errors) == 0

def test_invalid_image_corrupted():
    res = validate_image(b"not_an_image_random_bytes")
    assert res.is_valid is False
    assert len(res.errors) > 0

def test_resolution_too_low():
    small_bytes = create_dummy_image(100, 100)
    res = validate_image(small_bytes)
    assert res.is_valid is False
    assert any("resolution too low" in err.lower() for err in res.errors)

def test_size_limits():
    huge_bytes = b"0" * (11 * 1024 * 1024)
    res = validate_image(huge_bytes)
    assert res.is_valid is False
    assert any("exceeds 10mb" in err.lower() for err in res.errors)

def test_validator_class():
    validator = ImageValidator()
    img_bytes = create_dummy_image(250, 250)
    res = validator.validate(img_bytes)
    assert res.is_valid is True
