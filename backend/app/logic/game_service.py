"""
Game Service
Manages game lifecycle, turn processing, and state management
"""
from typing import Optional, Tuple
from datetime import datetime
import uuid
from app.models.game import (
    GameState, GameStatus, PlayerState, Card, PromptSubmission,
    TurnState, BattleResult
)
from app.services.redis_service import RedisService
from app.services.card_service import get_card_service
from app.logic.judge_service import JudgeService


class GameService:
    """Service for managing game state and turn processing"""
    
    def __init__(
        self,
        redis_service: Optional[RedisService] = None,
        judge_service: Optional[JudgeService] = None
    ):
        """
        Initialize game service
        
        Args:
            redis_service: Redis service for state persistence
            judge_service: Judge service for battle resolution
        """
        self.redis = redis_service or RedisService()
        self.judge = judge_service or JudgeService()
        self.card_service = get_card_service()
    
    def create_game(
        self,
        player1_id: str,
        player1_username: str,
        player2_id: str,
        player2_username: str
    ) -> GameState:
        """
        Create a new game between two players
        
        Args:
            player1_id: Player 1's ID
            player1_username: Player 1's username
            player2_id: Player 2's ID
            player2_username: Player 2's username
            
        Returns:
            New GameState
        """
        # Generate game ID
        game_id = str(uuid.uuid4())
        
        # Draw starting hands for both players
        player1_hand = self.card_service.draw_random_hand(hand_size=3)
        player2_hand = self.card_service.draw_random_hand(hand_size=3)
        
        # Get player ratings from Redis
        player1_rating = self.redis.get_player_rating(player1_id)
        player2_rating = self.redis.get_player_rating(player2_id)
        
        # Create player states
        player1 = PlayerState(
            player_id=player1_id,
            username=player1_username,
            hp=100,
            hand=player1_hand,
            elo_rating=player1_rating
        )
        
        player2 = PlayerState(
            player_id=player2_id,
            username=player2_username,
            hp=100,
            hand=player2_hand,
            elo_rating=player2_rating
        )
        
        # Create game state
        game = GameState(
            game_id=game_id,
            status=GameStatus.WAITING,
            player1=player1,
            player2=player2,
            current_turn=1,
            turn_history=[],
            winner_id=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Save to Redis
        self._save_game(game)
        
        return game
    
    def start_game(self, game_id: str) -> GameState:
        """
        Start a game (transition from WAITING to IN_PROGRESS)
        
        Args:
            game_id: Game ID
            
        Returns:
            Updated GameState
            
        Raises:
            ValueError: If game not found or already started
        """
        game = self._load_game(game_id)
        
        if game.status != GameStatus.WAITING:
            raise ValueError(f"Game {game_id} is not in WAITING status")

        game.status = GameStatus.ACTIVE
        game.updated_at = datetime.utcnow()
        
        self._save_game(game)
        
        return game
    
    async def submit_prompt(
        self,
        game_id: str,
        player_id: str,
        prompt: str,
        card_ids: list[str]
    ) -> Tuple[GameState, Optional[BattleResult]]:
        """
        Submit a player's prompt for the current turn
        
        Args:
            game_id: Game ID
            player_id: Player ID
            prompt: Player's creative prompt
            card_ids: List of card IDs used
            
        Returns:
            Tuple of (updated GameState, BattleResult if turn complete)

        Raises:
            ValueError: If game not found, not in progress, or invalid cards
        """
        game = self._load_game(game_id)

        if game.status != GameStatus.ACTIVE:
            raise ValueError(f"Game {game_id} is not in progress")

        # Validate cards
        if not self.card_service.validate_cards(card_ids):
            raise ValueError("Invalid card IDs provided")

        # Get cards
        cards = [self.card_service.get_card(card_id) for card_id in card_ids]

        # Create submission
        submission = PromptSubmission(
            player_id=player_id,
            prompt=prompt,
            cards_used=card_ids,
            submitted_at=datetime.utcnow()
        )

        # Determine which player submitted
        is_player1 = (player_id == game.player1.player_id)

        # Check if this is the first or second submission for this turn
        current_turn_state = None
        if game.turn_history and game.turn_history[-1].turn_number == game.current_turn:
            current_turn_state = game.turn_history[-1]

        # If no turn state exists, create one with this submission
        if not current_turn_state:
            turn_state = TurnState(
                turn_number=game.current_turn,
                player1_submission=submission if is_player1 else None,
                player2_submission=None if is_player1 else submission,
                battle_result=None,
                completed_at=None
            )
            game.turn_history.append(turn_state)
            game.updated_at = datetime.utcnow()
            self._save_game(game)
            return game, None

        # Both players have submitted - resolve the turn
        if is_player1:
            current_turn_state.player1_submission = submission
        else:
            current_turn_state.player2_submission = submission

        # Judge the battle
        battle_result = await self.judge.judge_battle(
            current_turn_state.player1_submission,
            current_turn_state.player2_submission,
            game.player1.username,
            game.player2.username
        )

        # Update turn state
        current_turn_state.battle_result = battle_result
        current_turn_state.completed_at = datetime.utcnow()

        # Apply damage
        if battle_result.winner_id == game.player1.player_id:
            game.player2.hp = max(0, game.player2.hp - battle_result.damage_dealt)
        elif battle_result.winner_id == game.player2.player_id:
            game.player1.hp = max(0, game.player1.hp - battle_result.damage_dealt)
        # Tie: no damage

        # Draw new cards for both players
        game.player1.hand = self.card_service.draw_random_hand(hand_size=3)
        game.player2.hand = self.card_service.draw_random_hand(hand_size=3)

        # Check for game over
        if game.player1.hp <= 0:
            game.status = GameStatus.FINISHED
            game.winner_id = game.player2.player_id
            await self._update_ratings(game)
        elif game.player2.hp <= 0:
            game.status = GameStatus.FINISHED
            game.winner_id = game.player1.player_id
            await self._update_ratings(game)
        else:
            # Continue to next turn
            game.current_turn += 1

        game.updated_at = datetime.utcnow()
        self._save_game(game)

        return game, battle_result

    async def _update_ratings(self, game: GameState):
        """Update Elo ratings for both players"""
        # Simple Elo calculation (K-factor = 32)
        K = 32

        # Expected scores
        expected_p1 = 1 / (1 + 10 ** ((game.player2.elo_rating - game.player1.elo_rating) / 400))
        expected_p2 = 1 - expected_p1

        # Actual scores
        if game.winner_id == game.player1.player_id:
            actual_p1, actual_p2 = 1, 0
        elif game.winner_id == game.player2.player_id:
            actual_p1, actual_p2 = 0, 1
        else:
            actual_p1, actual_p2 = 0.5, 0.5

        # New ratings
        new_rating_p1 = game.player1.elo_rating + K * (actual_p1 - expected_p1)
        new_rating_p2 = game.player2.elo_rating + K * (actual_p2 - expected_p2)

        # Update in Redis
        self.redis.update_player_rating(game.player1.player_id, new_rating_p1)
        self.redis.update_player_rating(game.player2.player_id, new_rating_p2)

    def get_game(self, game_id: str) -> GameState:
        """Get game state by ID"""
        return self._load_game(game_id)

    def _save_game(self, game: GameState):
        """Save game state to Redis"""
        self.redis.save_game_state(game.game_id, game.model_dump(), ttl=7200)

    def _load_game(self, game_id: str) -> GameState:
        """Load game state from Redis"""
        state_dict = self.redis.get_game_state(game_id)
        if not state_dict:
            raise ValueError(f"Game {game_id} not found")
        return GameState(**state_dict)

