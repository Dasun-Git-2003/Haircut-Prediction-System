import pytest
from app.ml.recommendation.scoring import (
    face_shape_score,
    hair_type_score,
    length_score,
    density_score,
    preference_score,
    maintenance_score
)
from app.ml.recommendation.engine import RecommendationEngine

def test_scoring_functions():
    # Face shape matching
    assert face_shape_score("oval", ["oval", "square"]) == 1.0
    assert face_shape_score("round", ["oval"]) == 0.7
    assert face_shape_score("unknown_shape", ["oval"]) == 0.3

    # Hair type matching
    assert hair_type_score("wavy", ["wavy", "straight"]) == 1.0
    assert hair_type_score("straight", ["wavy"]) == 0.5
    assert hair_type_score("straight", ["coily"]) == 0.1

    # Length matching
    assert length_score("medium", ["medium", "short"]) == 1.0
    assert length_score("long", ["medium"]) == 0.8  # Needs a trim
    assert length_score("very_short", ["long"]) <= 0.5

    # Density & Maintenance
    assert density_score("high", ["high", "medium"]) == 1.0
    assert maintenance_score("high", "low") == 1.0
    assert maintenance_score("low", "high") <= 0.5

def test_engine_ranking():
    engine = RecommendationEngine()
    
    face_analysis = {"face_shape": "oval"}
    hair_analysis = {
        "hair_type": "wavy",
        "hair_length": "medium",
        "hair_density": "high"
    }
    preferences = {
        "style": "modern",
        "maintenance": "medium",
        "haircut_category": "quiff"
    }
    
    hairstyles = [
        {
            "id": "h1",
            "name": "Textured Quiff",
            "category": "quiff",
            "face_shapes": ["oval", "square"],
            "hair_types": ["wavy", "straight"],
            "hair_lengths": ["medium"],
            "hair_density": ["high", "medium"],
            "maintenance_level": "medium",
            "style_tags": ["modern", "textured"],
            "lifestyle_tags": ["casual"]
        },
        {
            "id": "h2",
            "name": "Flat Top",
            "category": "edgy",
            "face_shapes": ["round"],
            "hair_types": ["coily"],
            "hair_lengths": ["short"],
            "hair_density": ["high"],
            "maintenance_level": "high",
            "style_tags": ["retro"],
            "lifestyle_tags": ["sporty"]
        }
    ]
    
    results = engine.recommend(
        face_analysis=face_analysis,
        hair_analysis=hair_analysis,
        preferences=preferences,
        hairstyles=hairstyles,
        top_k=2
    )
    
    assert len(results) == 2
    # Textured Quiff should rank first due to oval face + wavy hair + quiff category match
    assert results[0].hairstyle_id == "h1"
    assert results[0].score > results[1].score
    assert len(results[0].reasons) > 0

def test_explanation_generation():
    engine = RecommendationEngine()
    
    results = engine.recommend(
        face_analysis={"face_shape": "oval"},
        hair_analysis={"hair_type": "straight", "hair_length": "short", "hair_density": "medium"},
        preferences={},
        hairstyles=[{
            "id": "test",
            "name": "Crew Cut",
            "category": "short",
            "face_shapes": ["oval"],
            "hair_types": ["straight"],
            "hair_lengths": ["short"],
            "hair_density": ["medium"],
            "maintenance_level": "low",
            "style_tags": ["clean"],
            "lifestyle_tags": ["everyday"]
        }]
    )
    
    assert len(results) == 1
    exp = results[0].explanation
    assert "summary" in exp
    assert len(results[0].reasons) >= 1
    assert any("oval" in r.lower() for r in results[0].reasons)
