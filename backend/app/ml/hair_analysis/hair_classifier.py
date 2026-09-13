import os
try:
    import torch
    import torch.nn as nn
    from torchvision import transforms, models
    HAS_TORCH = True
except ImportError:
    torch = None
    nn = None
    transforms = None
    models = None
    HAS_TORCH = False

import numpy as np
from PIL import Image
import cv2
from dataclasses import dataclass
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class HairClassificationResult:
    hair_type: str
    confidence: float
    all_probabilities: Dict[str, float]
    explanation: Optional[str] = None

class HairTypeClassifier:
    def __init__(self, model_path: str = None):
        self.classes = ['straight', 'wavy', 'curly', 'kinky', 'braids', 'dreadlocks', 'short-men']
        self.class_mapping = {
            'straight': 'Straight',
            'wavy': 'Wavy',
            'curly': 'Curly',
            'kinky': 'Coily',
            'braids': 'Braids',
            'dreadlocks': 'Dreadlocks',
            'short-men': 'Short'
        }
        
        if HAS_TORCH:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
        else:
            self.device = "cpu"
            self.transform = None
        
        self.model = None
        
        if model_path and os.path.exists(model_path):
            try:
                # Assuming MobileNetV3-Small
                self.model = models.mobilenet_v3_small(pretrained=False)
                self.model.classifier[3] = nn.Linear(self.model.classifier[3].in_features, len(self.classes))
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                self.model.to(self.device)
                self.model.eval()
                logger.info(f"Loaded trained HairTypeClassifier from {model_path}")
            except Exception as e:
                logger.warning(f"Failed to load hair classifier model: {e}")
                self.model = None

    def classify(self, image: np.ndarray) -> HairClassificationResult:
        if self.model is None:
            # DEV_FALLBACK
            logger.info("Using DEV_FALLBACK for hair classification.")
            return HairClassificationResult(
                hair_type="unknown",
                confidence=0.0,
                all_probabilities={k: 0.0 for k in self.classes},
                explanation="Hair type classification requires a trained model. Please train the model using the Figaro1k dataset."
            )
            
        try:
            # Convert BGR to RGB and to PIL
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            
            input_tensor = self.transform(pil_img).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probs = torch.nn.functional.softmax(outputs, dim=1)[0]
                
            prob_dict = {self.classes[i]: float(probs[i]) for i in range(len(self.classes))}
            max_idx = torch.argmax(probs).item()
            raw_class = self.classes[max_idx]
            conf = float(probs[max_idx])
            
            mapped_type = self.class_mapping.get(raw_class, raw_class)
            
            return HairClassificationResult(
                hair_type=mapped_type,
                confidence=conf,
                all_probabilities=prob_dict
            )
        except Exception as e:
            logger.error(f"Error during hair classification: {e}")
            return HairClassificationResult(
                hair_type="unknown",
                confidence=0.0,
                all_probabilities={k: 0.0 for k in self.classes},
                explanation=f"Error analyzing hair type: {str(e)}"
            )
