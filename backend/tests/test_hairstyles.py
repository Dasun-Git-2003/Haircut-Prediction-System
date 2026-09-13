def test_get_hairstyles(client):
    res = client.get("/api/hairstyles/")
    # Returns 200 list (may be empty initially in test DB)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_hairstyle_not_found(client):
    res = client.get("/api/hairstyles/non-existent-id")
    assert res.status_code == 404

def test_admin_routes_require_auth(client):
    # Protected endpoints should reject unauthenticated requests
    res = client.post("/api/hairstyles/", json={
        "name": "Test Cut",
        "description": "A description",
        "category": "fade",
        "face_shapes": ["oval"],
        "hair_types": ["straight"],
        "hair_lengths": ["short"],
        "hair_density": ["high"],
        "maintenance_level": "low",
        "style_tags": ["modern"],
        "lifestyle_tags": ["casual"],
        "gender_target": "male",
        "difficulty": 1,
        "image_url": "/test.jpg",
        "thumbnail_url": "/thumb.jpg"
    })
    assert res.status_code in (401, 403)
