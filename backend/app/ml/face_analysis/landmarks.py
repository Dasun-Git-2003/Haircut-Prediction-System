import cv2
import numpy as np
import mediapipe as mp
from dataclasses import dataclass
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class LandmarkResult:
    is_valid: bool
    measurements: Dict[str, float]
    raw_landmarks: Optional[List[tuple]] = None
    error_message: Optional[str] = None

class FaceLandmarkExtractor:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )
        logger.info("FaceLandmarkExtractor initialized with MediaPipe Face Mesh.")

    def _calc_distance(self, p1: tuple, p2: tuple) -> float:
        return np.linalg.norm(np.array(p1) - np.array(p2))

    def extract_landmarks(self, image: np.ndarray) -> LandmarkResult:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_image)

        if not results.multi_face_landmarks:
            return LandmarkResult(is_valid=False, measurements={}, error_message="Could not extract facial landmarks.")

        h, w, _ = image.shape
        landmarks = results.multi_face_landmarks[0].landmark
        
        # Convert normalized coordinates to pixel coordinates
        pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

        # Geometric points
        forehead_top = pts[10]
        chin_bottom = pts[152]
        forehead_left = pts[70]
        forehead_right = pts[300]
        cheek_left = pts[234]
        cheek_right = pts[454]
        jaw_left = pts[172]
        jaw_right = pts[397]
        chin_left = pts[202]
        chin_right = pts[422]

        # Absolute measurements (in pixels)
        face_length = self._calc_distance(forehead_top, chin_bottom)
        forehead_width = self._calc_distance(forehead_left, forehead_right)
        cheekbone_width = self._calc_distance(cheek_left, cheek_right)
        jaw_width = self._calc_distance(jaw_left, jaw_right)
        chin_width = self._calc_distance(chin_left, chin_right)
        face_width = max(forehead_width, cheekbone_width, jaw_width)

        # Normalized features
        measurements = {
            "face_length": face_length / face_width,
            "face_width": 1.0,
            "forehead_width": forehead_width / face_width,
            "cheekbone_width": cheekbone_width / face_width,
            "jaw_width": jaw_width / face_width,
            "chin_width": chin_width / face_width,
            "face_aspect_ratio": face_length / face_width,
            "jaw_ratio": jaw_width / face_width,
            "forehead_ratio": forehead_width / face_width,
            "cheekbone_ratio": cheekbone_width / face_width,
        }

        return LandmarkResult(
            is_valid=True,
            measurements=measurements,
            raw_landmarks=pts
        )
