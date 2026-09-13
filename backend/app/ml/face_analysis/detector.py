import cv2
import numpy as np
import mediapipe as mp
from dataclasses import dataclass
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

@dataclass
class FaceDetectionResult:
    is_valid: bool
    bounding_box: Optional[Tuple[int, int, int, int]] = None
    confidence: float = 0.0
    error_message: Optional[str] = None

class FaceDetector:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        # Use model_selection=1 for full range (further away faces), 0 for close up.
        self.detector = self.mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5
        )
        logger.info("FaceDetector initialized with MediaPipe Face Detection.")

    def detect_face(self, image: np.ndarray) -> FaceDetectionResult:
        """Detect exactly one face in the image."""
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.detector.process(rgb_image)

        if not results.detections:
            return FaceDetectionResult(
                is_valid=False,
                error_message="No face detected in the image."
            )
            
        if len(results.detections) > 1:
            return FaceDetectionResult(
                is_valid=False,
                error_message=f"Multiple faces ({len(results.detections)}) detected. Please provide an image with exactly one face."
            )
            
        detection = results.detections[0]
        confidence = detection.score[0]
        
        # Get bounding box
        bboxC = detection.location_data.relative_bounding_box
        h, w, _ = image.shape
        x = int(bboxC.xmin * w)
        y = int(bboxC.ymin * h)
        width = int(bboxC.width * w)
        height = int(bboxC.height * h)
        
        # Ensure bounding box is within image bounds
        x = max(0, x)
        y = max(0, y)
        width = min(w - x, width)
        height = min(h - y, height)
        
        return FaceDetectionResult(
            is_valid=True,
            bounding_box=(x, y, width, height),
            confidence=confidence
        )
