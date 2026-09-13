def test_404_not_found(client):
    response = client.get("/api/nonexistent-route")
    assert response.status_code == 404

def test_422_validation_error(client):
    # Missing required body fields
    response = client.post("/api/auth/register", json={"email": "incomplete@example.com"})
    assert response.status_code == 422
    assert "detail" in response.json()

def test_tryon_missing_id_404(client):
    response = client.get("/api/tryon/invalid-nonexistent-id")
    assert response.status_code == 404
