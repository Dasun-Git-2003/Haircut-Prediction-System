import numpy as np
import cv2
from dataclasses import dataclass
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

@dataclass
class HairAttributes:
    hair_length: str
    hair_density: str
    hair_volume: str
    confidence: float

class HairAttributeEstimator:
    def __init__(self):
        logger.info("Initialized HairAttributeEstimator")

    def estimate_attributes(
        self, 
        image: np.ndarray, 
        hair_mask: Optional[np.ndarray] = None, 
        landmarks: Optional[List[tuple]] = None
    ) -> HairAttributes:
        """Estimate length, density, and volume of hair."""
        
        if hair_mask is not None and landmarks is not None:
            return self._estimate_with_mask(image, hair_mask, landmarks)
        else:
            # DEV_FALLBACK
            logger.info("Using DEV_FALLBACK for hair attributes.")
            return self._estimate_heuristics(image, landmarks)

    def _estimate_with_mask(self, image: np.ndarray, mask: np.ndarray, landmarks: List[tuple]) -> HairAttributes:
        h, w = mask.shape
        
        # Face metrics from landmarks
        forehead_top = landmarks[10]
        chin_bottom = landmarks[152]
        face_height = chin_bottom[1] - forehead_top[1]
        
        # Hair bounds
        y_indices, x_indices = np.where(mask > 127)
        if len(y_indices) == 0:
            return HairAttributes("very_short", "low", "low", 0.1)
            
        hair_top = np.min(y_indices)
        hair_bottom = np.max(y_indices)
        hair_extent = hair_bottom - hair_top
        
        # Length estimation
        relative_length = hair_extent / max(face_height, 1)
        if relative_length < 0.3:
            length = "very_short"
        elif relative_length < 0.8:
            length = "short"
        elif relative_length < 1.5:
            length = "medium"
        else:
            length = "long"
            
        # Volume estimation (Area ratio)
        hair_area = np.sum(mask > 127)
        face_area = (chin_bottom[1] - forehead_top[1]) * (landmarks[454][0] - landmarks[234][0])
        vol_ratio = hair_area / max(face_area, 1)
        
        if vol_ratio < 0.4:
            volume = "low"
        elif vol_ratio < 1.0:
            volume = "medium"
        else:
            volume = "high"
            
        # Density estimation (edge detection within mask)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edges_in_hair = cv2.bitwise_and(edges, edges, mask=(mask > 127).astype(np.uint8)*255)
        edge_density = np.sum(edges_in_hair > 0) / max(hair_area, 1)
        
        if edge_density < 0.05:
            density = "low"
        elif edge_density < 0.12:
            density = "medium"
        else:
            density = "high"
            
        return HairAttributes(length, density, volume, 0.8)

    def _estimate_heuristics(self, image: np.ndarray, landmarks: Optional[List[tuple]]) -> HairAttributes:
        # DEV_FALLBACK: Simple heuristics
        if not landmarks:
            return HairAttributes("medium", "medium", "medium", 0.1)
            
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Look above the forehead for edges
        forehead_top = landmarks[10]
        y_max = max(0, forehead_top[1] - 10)
        
        if y_max <= 0:
             return HairAttributes("very_short", "low", "low", 0.2)
             
        upper_head_edges = edges[0:y_max, :]
        edge_count = np.sum(upper_head_edges > 0)
        
        length = "medium"
        volume = "medium"
        if edge_count < 1000:
            length = "short"
            volume = "low"
        elif edge_count > 5000:
            length = "long"
            volume = "high"
            
        return HairAttributes(length, "medium", volume, 0.3)
