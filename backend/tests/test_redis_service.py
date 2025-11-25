"""
Tests for Redis service
"""
import pytest
from app.services.redis_service import redis_service


def test_redis_connection(fake_redis):
    """Test Redis connection"""
    assert redis_service.is_connected()


def test_save_and_get_game_state(fake_redis, sample_game_state):
    """Test saving and retrieving game state"""
    game_id = sample_game_state["game_id"]
    
    # Save game state
    result = redis_service.save_game_state(game_id, sample_game_state)
    assert result is True
    
    # Retrieve game state
    retrieved = redis_service.get_game_state(game_id)
    assert retrieved == sample_game_state


def test_get_nonexistent_game_state(fake_redis):
    """Test retrieving non-existent game state"""
    result = redis_service.get_game_state("nonexistent_game")
    assert result is None


def test_delete_game_state(fake_redis, sample_game_state):
    """Test deleting game state"""
    game_id = sample_game_state["game_id"]
    
    # Save game state
    redis_service.save_game_state(game_id, sample_game_state)
    
    # Delete game state
    result = redis_service.delete_game_state(game_id)
    assert result is True
    
    # Verify it's deleted
    retrieved = redis_service.get_game_state(game_id)
    assert retrieved is None


def test_update_player_rating(fake_redis):
    """Test updating player rating"""
    player_id = "test_player"
    rating = 1500.0
    
    result = redis_service.update_player_rating(player_id, rating)
    assert result is True
    
    # Verify rating was saved
    retrieved_rating = redis_service.get_player_rating(player_id)
    assert retrieved_rating == rating


def test_get_nonexistent_player_rating(fake_redis):
    """Test getting rating for non-existent player"""
    result = redis_service.get_player_rating("nonexistent_player")
    assert result is None


def test_leaderboard_ordering(fake_redis):
    """Test that leaderboard returns players in correct order"""
    # Add players with different ratings
    players = [
        ("player_1", 1200.0),
        ("player_2", 1600.0),
        ("player_3", 1400.0),
        ("player_4", 1800.0),
    ]
    
    for player_id, rating in players:
        redis_service.update_player_rating(player_id, rating)
    
    # Get leaderboard
    leaderboard = redis_service.get_leaderboard(limit=10)
    
    # Verify order (highest rating first)
    assert len(leaderboard) == 4
    assert leaderboard[0]["player_id"] == "player_4"
    assert leaderboard[0]["rating"] == 1800.0
    assert leaderboard[0]["rank"] == 1
    
    assert leaderboard[1]["player_id"] == "player_2"
    assert leaderboard[1]["rating"] == 1600.0
    assert leaderboard[1]["rank"] == 2
    
    assert leaderboard[3]["player_id"] == "player_1"
    assert leaderboard[3]["rating"] == 1200.0
    assert leaderboard[3]["rank"] == 4


def test_leaderboard_limit(fake_redis):
    """Test that leaderboard respects limit parameter"""
    # Add 5 players
    for i in range(5):
        redis_service.update_player_rating(f"player_{i}", 1000.0 + i * 100)
    
    # Get top 3
    leaderboard = redis_service.get_leaderboard(limit=3)
    
    assert len(leaderboard) == 3


def test_add_to_matchmaking_queue(fake_redis):
    """Test adding player to matchmaking queue"""
    player_id = "test_player"
    rating = 1500.0
    
    result = redis_service.add_to_queue(player_id, rating)
    assert result is True


def test_remove_from_matchmaking_queue(fake_redis):
    """Test removing player from matchmaking queue"""
    player_id = "test_player"
    rating = 1500.0
    
    # Add to queue
    redis_service.add_to_queue(player_id, rating)
    
    # Remove from queue
    result = redis_service.remove_from_queue(player_id)
    assert result is True


def test_game_state_with_ttl(fake_redis, sample_game_state):
    """Test that game state is saved with TTL"""
    game_id = sample_game_state["game_id"]
    ttl = 60
    
    # Save with TTL
    redis_service.save_game_state(game_id, sample_game_state, ttl=ttl)
    
    # Verify it exists
    retrieved = redis_service.get_game_state(game_id)
    assert retrieved == sample_game_state
    
    # Check TTL is set (FakeRedis supports TTL)
    key = f"game:{game_id}"
    remaining_ttl = fake_redis.ttl(key)
    assert remaining_ttl > 0
    assert remaining_ttl <= ttl

