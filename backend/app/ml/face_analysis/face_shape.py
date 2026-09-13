import os
import pickle
from dataclasses import dataclass
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

@dataclass
class FaceShapeResult:
    face_shape: str
    confidence: float
    explanation: str

class FaceShapeClassifier:
    def __init__(self, model_path: str = None):
        self.model = None
        self.scaler = None
        
        if model_path and os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.model = data.get('model')
                    self.scaler = data.get('scaler')
                logger.info(f"Loaded trained FaceShape model from {model_path}")
            except Exception as e:
                logger.warning(f"Failed to load model from {model_path}: {e}. Falling back to rules.")

    def classify(self, measurements: Dict[str, float]) -> FaceShapeResult:
        if self.model and self.scaler:
            return self._classify_ml(measurements)
        else:
            logger.info("Using DEV_FALLBACK for face shape classification.")
            return self._classify_rule_based(measurements)

    def _classify_ml(self, measurements: Dict[str, float]) -> FaceShapeResult:
        # Expected feature order: face_length, face_width, forehead_width, cheekbone_width, jaw_width, chin_width, face_aspect_ratio, jaw_ratio, forehead_ratio
        features = [
            measurements.get("face_length", 0),
            measurements.get("face_width", 0),
            measurements.get("forehead_width", 0),
            measurements.get("cheekbone_width", 0),
            measurements.get("jaw_width", 0),
            measurements.get("chin_width", 0),
            measurements.get("face_aspect_ratio", 0),
            measurements.get("jaw_ratio", 0),
            measurements.get("forehead_ratio", 0)
        ]
        
        try:
            import numpy as np
            X = np.array([features])
            if self.scaler:
                X = self.scaler.transform(X)
            
            pred = self.model.predict(X)[0]
            probs = self.model.predict_proba(X)[0]
            conf = float(np.max(probs))
            
            shape = str(pred).lower()
            return FaceShapeResult(
                face_shape=shape,
                confidence=conf,
                explanation=f"Your face appears {shape} based on our trained ML analysis."
            )
        except Exception as e:
            logger.error(f"ML classification failed: {e}. Falling back to rules.")
            return self._classify_rule_based(measurements)

    # DEV_FALLBACK
    def _classify_rule_based(self, measurements: Dict[str, float]) -> FaceShapeResult:
        ratio = measurements.get("face_aspect_ratio", 1.0)
        forehead = measurements.get("forehead_ratio", 1.0)
        cheekbone = measurements.get("cheekbone_ratio", 1.0)
        jaw = measurements.get("jaw_ratio", 1.0)

        # Simple rule-based heuristics
        if ratio > 1.35:
            shape = "oblong"
            explanation = "Your face appears oblong because it is noticeably longer than it is wide."
        elif ratio > 1.15:
            if jaw > cheekbone:
                shape = "square"
                explanation = "Your face appears square because it has balanced proportions with an angular, prominent jaw."
            elif forehead > cheekbone and forehead > jaw:
                shape = "heart"
                explanation = "Your face appears heart-shaped because your forehead is wider than your cheekbones and jaw."
            elif cheekbone > forehead and cheekbone > jaw:
                shape = "diamond"
                explanation = "Your face appears diamond-shaped because your cheekbones are the widest part of your face."
            else:
                shape = "oval"
                explanation = "Your face appears oval because it is slightly longer than it is wide, with a relatively balanced forehead, cheekbones, and jaw."
        else:
            if jaw > cheekbone * 0.95:
                shape = "square"
                explanation = "Your face appears square because its length and width are similar, with an angular jaw."
            else:
                shape = "round"
                explanation = "Your face appears round because its length and width are roughly equal with softer, rounded features."
                
        return FaceShapeResult(face_shape=shape, confidence=0.7, explanation=explanation)
