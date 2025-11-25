"""
Tests for Game Service
"""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime
from app.logic.game_service import GameService
from app.models.game import GameState, GameStatus, PlayerState, Card, CardType, BattleResult, VisualEffect
from app.services.redis_service import RedisService
from app.logic.judge_service import JudgeService
from app.providers.llm_provider import LLMResponse


@pytest.fixture
def mock_redis():
    """Create a mock Redis service"""
    redis = MagicMock(spec=RedisService)
    redis.get_player_rating.return_value = 1500
    redis.save_game_state.return_value = True
    redis.get_game_state.return_value = None
    redis.update_player_rating.return_value = True
    return redis


@pytest.fixture
def mock_judge():
    """Create a mock Judge service"""
    judge = MagicMock(spec=JudgeService)

    # Create a mock battle result
    async def mock_judge_battle(*args, **kwargs):
        return BattleResult(
            winner_id="p1",  # Use the actual player ID from tests
            damage_dealt=25,
            reasoning="Player 1 had a more creative prompt",
            creativity_score=9.0,
            adherence_score=8.5,
            visual_effects=[
                VisualEffect(
                    particle_type="fire",
                    intensity=1.5,
                    color="#FF4500",
                    duration_ms=1500
                )
            ]
        )

    judge.judge_battle = AsyncMock(side_effect=mock_judge_battle)
    return judge


@pytest.fixture
def game_service(mock_redis, mock_judge):
    """Create a game service with mocked dependencies"""
    return GameService(redis_service=mock_redis, judge_service=mock_judge)


class TestGameService:
    """Tests for GameService"""
    
    def test_create_game(self, game_service, mock_redis):
        """Test creating a new game"""
        game = game_service.create_game(
            player1_id="player_1",
            player1_username="Alice",
            player2_id="player_2",
            player2_username="Bob"
        )
        
        assert game.game_id is not None
        assert game.status == GameStatus.WAITING
        assert game.player1.player_id == "player_1"
        assert game.player1.username == "Alice"
        assert game.player1.hp == 100
        assert len(game.player1.hand) == 3
        assert game.player2.player_id == "player_2"
        assert game.player2.username == "Bob"
        assert game.player2.hp == 100
        assert len(game.player2.hand) == 3
        assert game.current_turn == 1
        assert len(game.turn_history) == 0
        
        # Verify Redis was called
        mock_redis.save_game_state.assert_called_once()
        mock_redis.get_player_rating.assert_called()
    
    def test_start_game(self, game_service, mock_redis):
        """Test starting a game"""
        # Create a game first
        game = game_service.create_game("p1", "Alice", "p2", "Bob")

        # Mock the load to return the created game
        mock_redis.get_game_state.return_value = game.model_dump()

        # Start the game
        started_game = game_service.start_game(game.game_id)

        assert started_game.status == GameStatus.ACTIVE
        assert started_game.current_turn == 1
    
    def test_start_game_already_started(self, game_service, mock_redis):
        """Test starting a game that's already in progress"""
        game = game_service.create_game("p1", "Alice", "p2", "Bob")
        game.status = GameStatus.ACTIVE
        mock_redis.get_game_state.return_value = game.model_dump()

        with pytest.raises(ValueError, match="not in WAITING status"):
            game_service.start_game(game.game_id)
    
    @pytest.mark.asyncio
    async def test_submit_prompt_first_player(self, game_service, mock_redis):
        """Test submitting a prompt as the first player"""
        # Create and start a game
        game = game_service.create_game("p1", "Alice", "p2", "Bob")
        game.status = GameStatus.ACTIVE
        game.current_turn = 1
        mock_redis.get_game_state.return_value = game.model_dump()

        # Submit prompt for player 1
        updated_game, battle_result = await game_service.submit_prompt(
            game.game_id,
            "p1",
            "A blazing phoenix rises with a flaming sword",
            ["fire", "summon", "sword"]
        )

        assert updated_game.status == GameStatus.ACTIVE
        assert len(updated_game.turn_history) == 1
        assert updated_game.turn_history[0].player1_submission is not None
        assert updated_game.turn_history[0].player2_submission is None
        assert battle_result is None  # Battle not resolved yet
    
    @pytest.mark.asyncio
    async def test_submit_prompt_both_players(self, game_service, mock_redis, mock_judge):
        """Test submitting prompts from both players and resolving battle"""
        # Create and start a game
        game = game_service.create_game("p1", "Alice", "p2", "Bob")
        game.status = GameStatus.ACTIVE
        game.current_turn = 1

        # Mock the load to return the created game
        mock_redis.get_game_state.return_value = game.model_dump()

        # First submission
        updated_game_1, _ = await game_service.submit_prompt(
            game.game_id,
            "p1",
            "A blazing phoenix rises with a flaming sword",
            ["fire", "summon", "sword"]
        )

        # Update mock to return the game with first submission
        mock_redis.get_game_state.return_value = updated_game_1.model_dump()

        # Second submission
        updated_game, battle_result = await game_service.submit_prompt(
            game.game_id,
            "p2",
            "An ice dragon descends with frozen crystals",
            ["ice", "summon", "crystal"]
        )

        assert updated_game.status == GameStatus.ACTIVE
        assert len(updated_game.turn_history) == 1
        assert updated_game.turn_history[0].player1_submission is not None
        assert updated_game.turn_history[0].player2_submission is not None
        assert updated_game.turn_history[0].battle_result is not None
        assert battle_result is not None
        assert battle_result.winner_id == "p1"  # Mock judge returns player_1 as winner
        assert battle_result.damage_dealt == 25
        assert updated_game.player2.hp == 75  # 100 - 25
        assert updated_game.current_turn == 2  # Advanced to next turn

        # Verify judge was called
        mock_judge.judge_battle.assert_called_once()

    @pytest.mark.asyncio
    async def test_game_over_player1_wins(self, game_service, mock_redis, mock_judge):
        """Test game ending when player 2's HP reaches 0"""
        # Create game with player 2 at low HP
        game = game_service.create_game("p1", "Alice", "p2", "Bob")
        game.status = GameStatus.ACTIVE
        game.current_turn = 1
        game.player2.hp = 20  # Low HP

        # Mock the load to return the created game
        mock_redis.get_game_state.return_value = game.model_dump()

        # First submission
        updated_game_1, _ = await game_service.submit_prompt(
            game.game_id,
            "p1",
            "A blazing phoenix rises with a flaming sword",
            ["fire", "summon", "sword"]
        )

        # Update mock to return the game with first submission
        mock_redis.get_game_state.return_value = updated_game_1.model_dump()

        # Second submission (will deal 25 damage, killing player 2)
        updated_game, battle_result = await game_service.submit_prompt(
            game.game_id,
            "p2",
            "An ice dragon descends with frozen crystals",
            ["ice", "summon", "crystal"]
        )

        assert updated_game.status == GameStatus.FINISHED
        assert updated_game.winner_id == "p1"  # Player 1 wins (mock returns p1 as winner, so player_2 takes damage and dies)
        assert updated_game.player2.hp == 0  # HP can't go below 0

        # Verify ratings were updated
        mock_redis.update_player_rating.assert_called()

    @pytest.mark.asyncio
    async def test_submit_prompt_invalid_cards(self, game_service, mock_redis):
        """Test submitting with invalid card IDs"""
        game = game_service.create_game("p1", "Alice", "p2", "Bob")
        game.status = GameStatus.ACTIVE
        game.current_turn = 1
        mock_redis.get_game_state.return_value = game.model_dump()

        with pytest.raises(ValueError, match="Invalid card IDs"):
            await game_service.submit_prompt(
                game.game_id,
                "p1",
                "A prompt",
                ["invalid_card_1", "invalid_card_2"]
            )

    @pytest.mark.asyncio
    async def test_submit_prompt_game_not_in_progress(self, game_service, mock_redis):
        """Test submitting when game is not in progress"""
        game = game_service.create_game("p1", "Alice", "p2", "Bob")
        game.status = GameStatus.WAITING
        mock_redis.get_game_state.return_value = game.model_dump()

        with pytest.raises(ValueError, match="not in progress"):
            await game_service.submit_prompt(
                game.game_id,
                "p1",
                "A prompt",
                ["fire", "summon", "sword"]
            )

    def test_get_game(self, game_service, mock_redis):
        """Test getting a game by ID"""
        game = game_service.create_game("p1", "Alice", "p2", "Bob")
        mock_redis.get_game_state.return_value = game.model_dump()

        retrieved_game = game_service.get_game(game.game_id)

        assert retrieved_game.game_id == game.game_id
        assert retrieved_game.player1.username == "Alice"
        assert retrieved_game.player2.username == "Bob"

    def test_get_game_not_found(self, game_service, mock_redis):
        """Test getting a non-existent game"""
        mock_redis.get_game_state.return_value = None

        with pytest.raises(ValueError, match="not found"):
            game_service.get_game("nonexistent_game_id")

    @pytest.mark.asyncio
    async def test_elo_rating_update(self, game_service, mock_redis, mock_judge):
        """Test that Elo ratings are updated correctly"""
        # Create game
        game = game_service.create_game("p1", "Alice", "p2", "Bob")
        game.status = GameStatus.ACTIVE
        game.current_turn = 1
        game.player1.elo_rating = 1500
        game.player2.elo_rating = 1500
        game.player2.hp = 20  # Low HP to end game

        # Mock the load to return the created game
        mock_redis.get_game_state.return_value = game.model_dump()

        # Submit both prompts
        updated_game_1, _ = await game_service.submit_prompt(
            game.game_id,
            "p1",
            "A blazing phoenix rises with a flaming sword",
            ["fire", "summon", "sword"]
        )

        # Update mock to return the game with first submission
        mock_redis.get_game_state.return_value = updated_game_1.model_dump()

        await game_service.submit_prompt(
            game.game_id,
            "p2",
            "An ice dragon descends with frozen crystals",
            ["ice", "summon", "crystal"]
        )

        # Verify update_player_rating was called for both players
        assert mock_redis.update_player_rating.call_count == 2

