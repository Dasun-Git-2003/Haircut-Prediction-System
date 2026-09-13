from dataclasses import dataclass
from typing import List, Dict, Any
from .scoring import (
    face_shape_score, hair_type_score, length_score,
    density_score, preference_score, maintenance_score
)
from .explainer import RecommendationExplainer
import logging

logger = logging.getLogger(__name__)

@dataclass
class RecommendationResult:
    hairstyle_id: str
    score: float
    individual_scores: Dict[str, float]
    reasons: List[str]
    explanation: Dict[str, Any]

class RecommendationEngine:
    def __init__(self):
        self.weights = {
            "face_shape_weight": 0.35,
            "hair_type_weight": 0.25,
            "length_weight": 0.10,
            "density_weight": 0.10,
            "preference_weight": 0.15,
            "maintenance_weight": 0.05
        }
        self.explainer = RecommendationExplainer()
        logger.info("RecommendationEngine initialized")

    def recommend(
        self, 
        face_analysis: dict, 
        hair_analysis: dict, 
        preferences: dict, 
        hairstyles: List[dict], 
        top_k: int = 5
    ) -> List[RecommendationResult]:
        
        results = []
        
        detected_shape = face_analysis.get("face_shape")
        detected_type = hair_analysis.get("hair_type")
        current_length = hair_analysis.get("hair_length")
        current_density = hair_analysis.get("hair_density")
        
        for hs in hairstyles:
            scores = {
                "face_shape": face_shape_score(detected_shape, hs.get("suitable_face_shapes", [])),
                "hair_type": hair_type_score(detected_type, hs.get("suitable_hair_types", [])),
                "length": length_score(current_length, hs.get("length_requirements", [])),
                "density": density_score(current_density, hs.get("suitable_densities", [])),
                "preference": preference_score(preferences, hs),
                "maintenance": maintenance_score(preferences.get("maintenance_level"), hs.get("maintenance_level", "medium"))
            }
            
            # Weighted average
            total_score = sum(scores[k] * self.weights[f"{k}_weight"] for k in scores) * 100.0
            
            explanation_res = self.explainer.explain(
                hs, scores, detected_shape, detected_type, preferences
            )
            
            results.append(
                RecommendationResult(
                    hairstyle_id=hs.get("id"),
                    score=total_score,
                    individual_scores=scores,
                    reasons=explanation_res.detailed_reasons,
                    explanation={
                        "summary": explanation_res.summary,
                        "pros": explanation_res.pros,
                        "cons": explanation_res.cons
                    }
                )
            )
            
        # Sort descending by score
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
