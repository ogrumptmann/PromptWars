"""
Redis Service
Handles all Redis operations for game state and leaderboards
"""
from redis import Redis
from typing import Optional, Dict, List
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisService:
    """Service for managing Redis operations"""
    
    def __init__(self):
        self.client: Optional[Redis] = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Redis"""
        try:
            self.client = Redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5
            )
            self.client.ping()
            logger.info("Successfully connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = None
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        if not self.client:
            return False
        try:
            self.client.ping()
            return True
        except:
            return False
    
    # Game State Operations
    
    def save_game_state(self, game_id: str, state: Dict, ttl: int = 3600) -> bool:
        """
        Save game state to Redis with TTL
        
        Args:
            game_id: Unique game identifier
            state: Game state dictionary
            ttl: Time to live in seconds (default: 1 hour)
        """
        try:
            key = f"game:{game_id}"
            self.client.setex(key, ttl, json.dumps(state))
            logger.info(f"Saved game state for {game_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save game state: {e}")
            return False
    
    def get_game_state(self, game_id: str) -> Optional[Dict]:
        """Get game state from Redis"""
        try:
            key = f"game:{game_id}"
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Failed to get game state: {e}")
            return None
    
    def delete_game_state(self, game_id: str) -> bool:
        """Delete game state from Redis"""
        try:
            key = f"game:{game_id}"
            self.client.delete(key)
            logger.info(f"Deleted game state for {game_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete game state: {e}")
            return False
    
    # Leaderboard Operations (using Sorted Sets)
    
    def update_player_rating(self, player_id: str, rating: float) -> bool:
        """Update player rating in leaderboard"""
        try:
            self.client.zadd("leaderboard", {player_id: rating})
            logger.info(f"Updated rating for {player_id}: {rating}")
            return True
        except Exception as e:
            logger.error(f"Failed to update player rating: {e}")
            return False
    
    def get_player_rating(self, player_id: str) -> Optional[float]:
        """Get player rating from leaderboard"""
        try:
            rating = self.client.zscore("leaderboard", player_id)
            return rating
        except Exception as e:
            logger.error(f"Failed to get player rating: {e}")
            return None
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """
        Get top players from leaderboard
        
        Returns:
            List of dicts with 'player_id', 'rating', and 'rank'
        """
        try:
            # Get top players with scores (descending order)
            results = self.client.zrevrange("leaderboard", 0, limit - 1, withscores=True)
            
            leaderboard = []
            for rank, (player_id, rating) in enumerate(results, start=1):
                leaderboard.append({
                    "rank": rank,
                    "player_id": player_id,
                    "rating": rating
                })
            
            return leaderboard
        except Exception as e:
            logger.error(f"Failed to get leaderboard: {e}")
            return []
    
    # Matchmaking Queue Operations
    
    def add_to_queue(self, player_id: str, rating: float) -> bool:
        """Add player to matchmaking queue"""
        try:
            self.client.zadd("matchmaking_queue", {player_id: rating})
            logger.info(f"Added {player_id} to matchmaking queue")
            return True
        except Exception as e:
            logger.error(f"Failed to add to queue: {e}")
            return False
    
    def remove_from_queue(self, player_id: str) -> bool:
        """Remove player from matchmaking queue"""
        try:
            self.client.zrem("matchmaking_queue", player_id)
            logger.info(f"Removed {player_id} from matchmaking queue")
            return True
        except Exception as e:
            logger.error(f"Failed to remove from queue: {e}")
            return False


# Global Redis service instance
redis_service = RedisService()

