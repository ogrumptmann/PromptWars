"""
Redis Test Endpoints
Comprehensive tests for Redis functionality
"""
from fastapi import APIRouter, HTTPException
from app.services.redis_service import redis_service
import time

router = APIRouter()


@router.get("/redis/test")
async def test_redis():
    """
    Comprehensive Redis test
    Tests all major Redis operations
    """
    results = {
        "connection": False,
        "game_state": False,
        "leaderboard": False,
        "queue": False,
        "errors": []
    }
    
    # Test 1: Connection
    try:
        if redis_service.is_connected():
            results["connection"] = True
        else:
            results["errors"].append("Redis connection failed")
    except Exception as e:
        results["errors"].append(f"Connection test error: {str(e)}")
    
    # Test 2: Game State Operations
    try:
        test_game_id = f"test_game_{int(time.time())}"
        test_state = {
            "player1": "alice",
            "player2": "bob",
            "turn": 1,
            "status": "active"
        }
        
        # Save
        if not redis_service.save_game_state(test_game_id, test_state, ttl=60):
            results["errors"].append("Failed to save game state")
        else:
            # Retrieve
            retrieved = redis_service.get_game_state(test_game_id)
            if retrieved == test_state:
                # Delete
                if redis_service.delete_game_state(test_game_id):
                    results["game_state"] = True
                else:
                    results["errors"].append("Failed to delete game state")
            else:
                results["errors"].append(f"Game state mismatch: {retrieved} != {test_state}")
    except Exception as e:
        results["errors"].append(f"Game state test error: {str(e)}")
    
    # Test 3: Leaderboard Operations
    try:
        test_players = [
            ("test_player_1", 1500.0),
            ("test_player_2", 1600.0),
            ("test_player_3", 1400.0)
        ]
        
        # Add players
        for player_id, rating in test_players:
            if not redis_service.update_player_rating(player_id, rating):
                results["errors"].append(f"Failed to update rating for {player_id}")
                break
        else:
            # Get leaderboard
            leaderboard = redis_service.get_leaderboard(limit=10)
            
            # Verify top player
            if leaderboard and leaderboard[0]["player_id"] == "test_player_2":
                # Get specific rating
                rating = redis_service.get_player_rating("test_player_1")
                if rating == 1500.0:
                    results["leaderboard"] = True
                else:
                    results["errors"].append(f"Rating mismatch: {rating} != 1500.0")
            else:
                results["errors"].append("Leaderboard order incorrect")
    except Exception as e:
        results["errors"].append(f"Leaderboard test error: {str(e)}")
    
    # Test 4: Matchmaking Queue Operations
    try:
        test_player = "test_queue_player"
        
        # Add to queue
        if not redis_service.add_to_queue(test_player, 1500.0):
            results["errors"].append("Failed to add to queue")
        else:
            # Remove from queue
            if redis_service.remove_from_queue(test_player):
                results["queue"] = True
            else:
                results["errors"].append("Failed to remove from queue")
    except Exception as e:
        results["errors"].append(f"Queue test error: {str(e)}")
    
    # Overall status
    all_passed = all([
        results["connection"],
        results["game_state"],
        results["leaderboard"],
        results["queue"]
    ])
    
    return {
        "status": "passed" if all_passed else "failed",
        "tests": results,
        "summary": {
            "total": 4,
            "passed": sum([
                results["connection"],
                results["game_state"],
                results["leaderboard"],
                results["queue"]
            ]),
            "failed": sum([
                not results["connection"],
                not results["game_state"],
                not results["leaderboard"],
                not results["queue"]
            ])
        }
    }


@router.get("/redis/leaderboard")
async def get_leaderboard(limit: int = 10):
    """Get current leaderboard"""
    if not redis_service.is_connected():
        raise HTTPException(status_code=503, detail="Redis not connected")
    
    leaderboard = redis_service.get_leaderboard(limit)
    return {
        "leaderboard": leaderboard,
        "count": len(leaderboard)
    }

