# StyleAI REST API Reference

Base URL: `http://localhost:8000/api`

Interactive Documentation (Swagger UI): `http://localhost:8000/docs`

---

## 1. Authentication

### `POST /auth/register`
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "styleuser",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "id": "c1f10927-4a06-4df4-a82f-2db4719601be",
  "email": "user@example.com",
  "username": "styleuser",
  "is_active": true,
  "is_admin": false,
  "avatar_url": null
}
```

---

### `POST /auth/login`
Authenticate and obtain a JWT bearer token.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 2. User Profile

### `GET /users/profile`
Get the authenticated user's profile details.  
*Requires Header: `Authorization: Bearer <token>`*

---

## 3. Analysis Pipeline

### `POST /analysis/upload`
Upload an image for quality validation and session initialization.  
*Content-Type: `multipart/form-data`*

**Form Data:**
- `file`: Image file (JPEG, PNG, WebP)

**Response (200 OK):**
```json
{
  "session_id": "84c8a2ef-91f8-479c-b17f-71ca37cf6e44",
  "message": "Image uploaded and validated successfully"
}
```

---

### `POST /analysis/analyze/{session_id}`
Run MediaPipe face detection, landmark extraction, geometric shape classification, and hair feature analysis.

**Response (200 OK):**
```json
{
  "session_id": "84c8a2ef-91f8-479c-b17f-71ca37cf6e44",
  "status": "completed",
  "original_image_url": "/uploads/84c8a2ef-91f8.jpg",
  "face_analysis": {
    "face_shape": "oval",
    "confidence": 0.93,
    "face_length": 1.45,
    "forehead_width": 1.02,
    "cheekbone_width": 1.15,
    "jaw_width": 0.92,
    "chin_width": 0.48,
    "face_width": 1.15,
    "face_aspect_ratio": 1.26,
    "jaw_ratio": 0.80,
    "forehead_ratio": 0.89,
    "cheekbone_ratio": 1.00,
    "explanation": "Your face appears oval because it is longer than it is wide, with balanced forehead, cheekbones, and jawline."
  },
  "hair_profile": {
    "hair_type": "wavy",
    "hair_type_confidence": 0.88,
    "hair_length": "medium",
    "hair_density": "high",
    "hair_volume": "medium",
    "raw_predictions": {}
  }
}
```

---

## 4. Hairstyle Recommendations

### `POST /recommendations/?session_id={session_id}`
Calculate weighted compatibility scores and return top recommended hairstyles with human-readable explanations.

**Request Body (Optional Preferences):**
```json
{
  "preferred_length": "medium",
  "maintenance": "low",
  "style": "modern",
  "lifestyle": "casual",
  "haircut_category": "quiff"
}
```

**Response (200 OK):**
```json
{
  "session_id": "84c8a2ef-91f8-479c-b17f-71ca37cf6e44",
  "recommendations": [
    {
      "id": "rec-5384-9011",
      "score": 94.2,
      "reasons": [
        "✓ Suitable for your oval face shape",
        "✓ Works well with wavy hair",
        "✓ Suitable for your current hair length",
        "✓ Matches your personal style preferences"
      ],
      "explanation": "Textured Quiff is an excellent match for you!",
      "rank": 1,
      "hairstyle": {
        "id": "hs-quiff-01",
        "name": "Textured Quiff",
        "description": "A modern quiff with textured, tousled styling on top...",
        "category": "quiff",
        "face_shapes": ["oval", "square", "round", "heart"],
        "hair_types": ["straight", "wavy"],
        "hair_lengths": ["medium"],
        "hair_density": ["medium", "high"],
        "maintenance_level": "medium",
        "style_tags": ["modern", "textured", "trendy"],
        "lifestyle_tags": ["casual", "university", "professional"],
        "difficulty": 3,
        "image_url": "/assets/hairstyles/textured-quiff.jpg",
        "thumbnail_url": "/assets/hairstyles/thumbnails/textured-quiff.jpg"
      }
    }
  ]
}
```

---

## 5. Virtual Try-On

### `POST /tryon/generate`
Trigger Generative AI virtual try-on for a selected recommendation.

**Request Body:**
```json
{
  "recommendation_id": "rec-5384-9011"
}
```

**Response (200 OK):**
```json
{
  "id": "tryon-8921-bc34",
  "session_id": "84c8a2ef-91f8-479c-b17f-71ca37cf6e44",
  "recommendation_id": "rec-5384-9011",
  "hairstyle_id": "hs-quiff-01",
  "original_image_url": "/uploads/84c8a2ef-91f8.jpg",
  "generated_image_url": "/generated/tryon_9fbc102a.png",
  "status": "completed",
  "generation_time_ms": 1420
}
```

---

## 6. Hairstyles Catalog & Admin

- `GET /hairstyles/?skip=0&limit=50`: Get paginated hairstyle catalog.
- `GET /hairstyles/{id}`: Get single hairstyle metadata.
- `POST /hairstyles/`: Create new hairstyle *(Admin only)*.
- `PUT /hairstyles/{id}`: Update hairstyle metadata *(Admin only)*.
- `DELETE /hairstyles/{id}`: Delete hairstyle *(Admin only)*.

---

## 7. Favorites

- `GET /favorites/`: Get authenticated user's saved hairstyles.
- `POST /favorites/`: Add a hairstyle / try-on result to favorites.
- `DELETE /favorites/{id}`: Remove from favorites.
