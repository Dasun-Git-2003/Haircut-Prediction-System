from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token

def test_password_hashing():
    raw = "MySecurePassword123!"
    hashed = get_password_hash(raw)
    assert hashed != raw
    assert verify_password(raw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_flow():
    user_id = "test-user-uuid-123"
    token = create_access_token(subject=user_id)
    assert isinstance(token, str)
    assert len(token) > 20
    
    decoded = decode_access_token(token)
    assert decoded["sub"] == user_id
    assert "exp" in decoded

def test_auth_api_routes(client):
    # Test register validation
    res = client.post("/api/auth/register", json={
        "email": "not-an-email",
        "username": "u",
        "password": "p"
    })
    assert res.status_code == 422

    # Test login validation
    res = client.post("/api/auth/login", json={})
    assert res.status_code == 422
