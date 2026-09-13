import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_db_session():
    # Mocking DB session for tests
    pass

@pytest.fixture
def test_user():
    return {"id": "test-uuid", "email": "test@example.com", "username": "testuser"}
