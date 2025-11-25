"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from fakeredis import FakeRedis
from app.main import app
from app.services.redis_service import redis_service


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def fake_redis():
    """Fake Redis client for testing"""
    fake_client = FakeRedis(decode_responses=True)
    # Replace the real Redis client with fake one
    original_client = redis_service.client
    redis_service.client = fake_client
    
    yield fake_client
    
    # Cleanup
    fake_client.flushall()
    redis_service.client = original_client


@pytest.fixture
def sample_game_state():
    """Sample game state for testing"""
    return {
        "game_id": "test_game_123",
        "player1": {
            "id": "player_1",
            "hp": 100,
            "cards": ["fireball", "shield", "lightning"]
        },
        "player2": {
            "id": "player_2",
            "hp": 100,
            "cards": ["ice", "heal", "wind"]
        },
        "turn": 1,
        "status": "active"
    }

