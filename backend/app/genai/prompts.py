def build_hairstyle_prompt(hairstyle_name: str, hairstyle_description: str, hair_type: str = "", high_quality: bool = False) -> str:
    """Builds a robust prompt for genAI image generation/editing."""
    
    quality_prefix = ""
    if high_quality:
        quality_prefix = "Professional photography, 8k resolution, highly detailed, photorealistic. "
        
    hair_type_context = f"natural {hair_type} hair texture" if hair_type and hair_type != "unknown" else "natural hair texture"
    
    prompt = (
        f"{quality_prefix}Edit the person's hair in the image to be a '{hairstyle_name}'. "
        f"Description: {hairstyle_description}. "
        f"Important: Ensure the new hair has a {hair_type_context}. "
        f"CRITICAL: Preserve the person's exact facial structure, identity, skin tone, eye color, and clothing. "
        f"Only modify the hair and seamlessly blend it with the face and background."
    )
    
    return prompt
