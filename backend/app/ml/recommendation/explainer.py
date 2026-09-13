from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ExplanationResult:
    summary: str
    detailed_reasons: List[str]
    pros: List[str]
    cons: List[str]

class RecommendationExplainer:
    def explain(
        self, 
        hairstyle: Dict, 
        scores: Dict[str, float], 
        face_shape: str, 
        hair_type: str, 
        preferences: Dict
    ) -> ExplanationResult:
        reasons = []
        pros = []
        cons = []
        
        # Face shape explanation
        if scores.get("face_shape", 0) >= 0.7:
            reasons.append(f"✓ Suitable for your {face_shape} face shape")
            pros.append(f"Enhances {face_shape} facial features")
        else:
            cons.append(f"May not be optimal for {face_shape} faces")
            
        # Hair type explanation
        if scores.get("hair_type", 0) >= 0.7:
            reasons.append(f"✓ Works well with {hair_type} hair")
            pros.append("Matches natural hair texture")
        else:
            cons.append(f"Might require extra styling for {hair_type} hair")
            
        # Length explanation
        if scores.get("length", 0) >= 0.8:
            reasons.append("✓ Suitable for your current hair length")
        elif scores.get("length", 0) < 0.5:
            cons.append("Requires time to grow out to target length")
            
        # Preference and Maintenance
        if scores.get("preference", 0) > 0.5:
            reasons.append("✓ Matches your personal style preferences")
            
        if scores.get("maintenance", 0) < 0.5:
            reasons.append("✗ May require more maintenance than preferred")
            cons.append("Higher maintenance routine needed")
            
        summary_name = hairstyle.get("name", "This style")
        if sum(scores.values()) / len(scores) > 0.8:
            summary = f"{summary_name} is an excellent match for you!"
        elif sum(scores.values()) / len(scores) > 0.6:
            summary = f"{summary_name} is a good option with some minor adjustments."
        else:
            summary = f"{summary_name} might require significant styling effort."
            
        return ExplanationResult(
            summary=summary,
            detailed_reasons=reasons,
            pros=pros,
            cons=cons
        )
