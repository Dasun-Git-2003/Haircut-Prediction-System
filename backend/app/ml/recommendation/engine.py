from typing import List, Dict, Any
from dataclasses import dataclass
from app.ml.recommendation.scoring import (
    face_shape_score, hair_type_score, length_score,
    density_score, preference_score, maintenance_score
)
from app.ml.recommendation.explainer import RecommendationExplainer
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
        
        detected_shape = str(face_analysis.get("face_shape") or "oval").lower()
        detected_type = str(hair_analysis.get("hair_type") or "straight").lower()
        current_length = str(hair_analysis.get("hair_length") or "medium").lower()
        current_density = str(hair_analysis.get("hair_density") or "medium").lower()
        
        pref_dict = preferences or {}
        
        for hs in hairstyles:
            # Safely handle both dict and model instances
            hs_id = getattr(hs, "id", None) or (hs.get("id") if isinstance(hs, dict) else None)
            hs_name = getattr(hs, "name", "") or (hs.get("name") if isinstance(hs, dict) else "")
            hs_category = getattr(hs, "category", "") or (hs.get("category") if isinstance(hs, dict) else "")
            hs_face_shapes = getattr(hs, "face_shapes", []) or (hs.get("face_shapes") if isinstance(hs, dict) else [])
            hs_hair_types = getattr(hs, "hair_types", []) or (hs.get("hair_types") if isinstance(hs, dict) else [])
            hs_hair_lengths = getattr(hs, "hair_lengths", []) or (hs.get("hair_lengths") if isinstance(hs, dict) else [])
            hs_hair_density = getattr(hs, "hair_density", []) or (hs.get("hair_density") if isinstance(hs, dict) else [])
            hs_maintenance = getattr(hs, "maintenance_level", "medium") or (hs.get("maintenance_level") if isinstance(hs, dict) else "medium")
            hs_style_tags = getattr(hs, "style_tags", []) or (hs.get("style_tags") if isinstance(hs, dict) else [])
            hs_lifestyle_tags = getattr(hs, "lifestyle_tags", []) or (hs.get("lifestyle_tags") if isinstance(hs, dict) else [])
            
            # Combine tags for matching
            all_tags = list(hs_style_tags) + list(hs_lifestyle_tags)
            
            hs_dict = {
                "id": hs_id,
                "name": hs_name,
                "category": hs_category,
                "face_shapes": hs_face_shapes,
                "hair_types": hs_hair_types,
                "hair_lengths": hs_hair_lengths,
                "hair_density": hs_hair_density,
                "maintenance_level": hs_maintenance,
                "tags": all_tags
            }
            
            user_pref_style = pref_dict.get("style") or pref_dict.get("lifestyle")
            user_pref_cat = pref_dict.get("haircut_category")
            pref_scoring_input = {
                "style": str(user_pref_style) if user_pref_style else None,
                "category": str(user_pref_cat) if user_pref_cat else None
            }
            
            user_pref_maintenance = pref_dict.get("maintenance")
            
            scores = {
                "face_shape": face_shape_score(detected_shape, hs_face_shapes),
                "hair_type": hair_type_score(detected_type, hs_hair_types),
                "length": length_score(current_length, hs_hair_lengths),
                "density": density_score(current_density, hs_hair_density),
                "preference": preference_score(pref_scoring_input, hs_dict),
                "maintenance": maintenance_score(str(user_pref_maintenance) if user_pref_maintenance else None, hs_maintenance)
            }
            
            total_score = sum(scores[k] * self.weights[f"{k}_weight"] for k in scores) * 100.0
            
            explanation_res = self.explainer.explain(
                hs_dict, scores, detected_shape, detected_type, pref_dict
            )
            
            results.append(
                RecommendationResult(
                    hairstyle_id=hs_id,
                    score=round(total_score, 1),
                    individual_scores=scores,
                    reasons=explanation_res.detailed_reasons,
                    explanation={
                        "summary": explanation_res.summary,
                        "pros": explanation_res.pros,
                        "cons": explanation_res.cons
                    }
                )
            )
            
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
