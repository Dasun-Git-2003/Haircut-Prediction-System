import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import init_db, async_session_maker
from app.database.seed_hairstyles import seed_database

@pytest.fixture(scope="session", autouse=True)
def initialize_test_database():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_db())
    
    async def seed():
        async with async_session_maker() as session:
            await seed_database(session)
            
    loop.run_until_complete(seed())
    loop.close()

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def test_user():
    return {"id": "test-uuid", "email": "test@example.com", "username": "testuser"}
