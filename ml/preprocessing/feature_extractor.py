import numpy as np
import pickle
import os
import logging

logger = logging.getLogger(__name__)

def extract_features(measurements: dict) -> np.ndarray:
    """Extract and vectorize features from landmarks measurements."""
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
    return np.array([features])

def load_scaler(scaler_path: str):
    if os.path.exists(scaler_path):
        with open(scaler_path, 'rb') as f:
            data = pickle.load(f)
            return data.get('scaler')
    return None

def normalize_features(features: np.ndarray, scaler) -> np.ndarray:
    if scaler:
        return scaler.transform(features)
    return features
