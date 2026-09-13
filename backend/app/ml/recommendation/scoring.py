from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

def face_shape_score(detected_shape: str, hairstyle_shapes: List[str]) -> float:
    if not detected_shape or not hairstyle_shapes:
        return 0.5
    detected_shape = detected_shape.lower()
    shapes = [s.lower() for s in hairstyle_shapes]
    
    if detected_shape in shapes:
        return 1.0
        
    # Compatible mapping
    compatible = {
        'oval': ['round', 'heart'],
        'round': ['oval', 'square'],
        'square': ['round', 'oval'],
        'heart': ['oval', 'diamond'],
        'diamond': ['heart', 'oval'],
        'oblong': ['oval', 'square']
    }
    
    if any(comp in shapes for comp in compatible.get(detected_shape, [])):
        return 0.7
        
    return 0.3

def hair_type_score(detected_type: str, hairstyle_types: List[str]) -> float:
    if not detected_type or not hairstyle_types or detected_type == "unknown":
        return 0.5
    
    detected = detected_type.lower()
    types = [t.lower() for t in hairstyle_types]
    
    if detected in types:
        return 1.0
    
    # Adjacent/compatible types
    compatible = {
        'straight': ['wavy'],
        'wavy': ['straight', 'curly'],
        'curly': ['wavy', 'coily'],
        'coily': ['curly', 'dreadlocks', 'braids'],
        'braids': ['coily', 'dreadlocks'],
        'dreadlocks': ['coily', 'braids'],
        'short': ['straight', 'wavy']
    }
    
    if any(comp in types for comp in compatible.get(detected, [])):
        return 0.5
        
    return 0.1

def length_score(current_length: str, required_lengths: List[str]) -> float:
    if not current_length or not required_lengths:
        return 0.5
        
    lengths = ['very_short', 'short', 'medium', 'long']
    
    current_idx = lengths.index(current_length) if current_length in lengths else 1
    
    req_indices = [lengths.index(l) for l in required_lengths if l in lengths]
    if not req_indices:
        return 0.5
        
    if current_idx in req_indices:
        return 1.0
        
    # If the user has longer hair than required, it's easily doable (cut)
    # If they have shorter hair, it takes time to grow
    min_req_idx = min(req_indices)
    
    if current_idx > min_req_idx:
        return 0.8 # Just needs a cut
    
    diff = min_req_idx - current_idx
    if diff == 1:
        return 0.5 # One step away
    else:
        return 0.2 # Requires significant growth

def density_score(detected_density: str, suitable_densities: List[str]) -> float:
    if not detected_density or not suitable_densities:
        return 0.5
    if detected_density in suitable_densities:
        return 1.0
    return 0.5

def preference_score(preferences: Dict, hairstyle: Dict) -> float:
    if not preferences:
        return 1.0
        
    score = 0.0
    max_score = 0.0
    
    pref_style = preferences.get("style")
    if pref_style:
        max_score += 1.0
        if pref_style.lower() in [t.lower() for t in hairstyle.get("tags", [])]:
            score += 1.0
            
    pref_category = preferences.get("category")
    if pref_category:
        max_score += 1.0
        if pref_category.lower() == hairstyle.get("category", "").lower():
            score += 1.0
            
    return score / max_score if max_score > 0 else 1.0

def maintenance_score(preferred_maintenance: Optional[str], hairstyle_maintenance: str) -> float:
    if not preferred_maintenance or not hairstyle_maintenance:
        return 1.0
        
    levels = ["low", "medium", "high"]
    
    try:
        pref_idx = levels.index(preferred_maintenance.lower())
        hair_idx = levels.index(hairstyle_maintenance.lower())
        
        if pref_idx >= hair_idx:
            return 1.0 # User willing to do more or equal maintenance
        
        diff = hair_idx - pref_idx
        if diff == 1:
            return 0.5
        return 0.1
    except ValueError:
        return 1.0
