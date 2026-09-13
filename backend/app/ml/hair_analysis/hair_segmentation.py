import os
import torch
import numpy as np
import cv2
import mediapipe as mp
from torchvision import transforms
from PIL import Image
from dataclasses import dataclass
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class SegmentationResult:
    hair_mask: np.ndarray
    confidence: float

class HairSegmenter:
    def __init__(self, model_path: str = None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.mp_selfie = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
        
        if model_path and os.path.exists(model_path):
            try:
                # Load a DeepLabV3 or UNet model here
                # self.model = ...
                # self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                # self.model.eval()
                logger.info(f"Loaded trained HairSegmenter from {model_path}")
            except Exception as e:
                logger.warning(f"Failed to load segmentation model: {e}")
                self.model = None
                
    def segment(self, image: np.ndarray, landmarks: Optional[list] = None) -> SegmentationResult:
        if self.model is not None:
            return self._segment_ml(image)
        else:
            logger.info("Using DEV_FALLBACK for hair segmentation.")
            return self._segment_fallback(image, landmarks)
            
    def _segment_ml(self, image: np.ndarray) -> SegmentationResult:
        # Placeholder for real model inference
        pass

    def _segment_fallback(self, image: np.ndarray, landmarks: Optional[list] = None) -> SegmentationResult:
        # DEV_FALLBACK: Use mediapipe selfie segmentation + heuristics
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.mp_selfie.process(rgb_image)
        
        person_mask = (results.segmentation_mask > 0.5).astype(np.uint8) * 255
        
        if landmarks:
            # Mask out the face area using landmarks
            h, w = image.shape[:2]
            face_pts = np.array([(lm[0], lm[1]) for lm in landmarks], dtype=np.int32)
            hull = cv2.convexHull(face_pts)
            cv2.fillConvexPoly(person_mask, hull, 0)
            
        return SegmentationResult(
            hair_mask=person_mask,
            confidence=0.4 # Low confidence because it's a fallback
        )
