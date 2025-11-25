"""
Tests for Game Data Models
"""
import pytest
from datetime import datetime
from app.models.game import (
    Card, CardType, PlayerState, PromptSubmission,
    VisualEffect, BattleResult, TurnState, GameState, GameStatus
)


class TestCard:
    """Tests for Card model"""
    
    def test_card_creation(self):
        """Test creating a valid card"""
        card = Card(
            id="fire",
            name="Fire",
            type=CardType.ELEMENT,
            description="Harness the power of flames"
        )
        assert card.id == "fire"
        assert card.name == "Fire"
        assert card.type == CardType.ELEMENT
        assert card.description == "Harness the power of flames"
    
    def test_card_types(self):
        """Test all card types are valid"""
        element_card = Card(id="fire", name="Fire", type=CardType.ELEMENT, description="Test")
        action_card = Card(id="attack", name="Attack", type=CardType.ACTION, description="Test")
        material_card = Card(id="sword", name="Sword", type=CardType.MATERIAL, description="Test")
        
        assert element_card.type == CardType.ELEMENT
        assert action_card.type == CardType.ACTION
        assert material_card.type == CardType.MATERIAL


class TestPlayerState:
    """Tests for PlayerState model"""
    
    def test_player_creation(self):
        """Test creating a player state"""
        player = PlayerState(
            player_id="player_123",
            username="TestPlayer",
            hp=100,
            hand=[],
            elo_rating=1200
        )
        assert player.player_id == "player_123"
        assert player.username == "TestPlayer"
        assert player.hp == 100
        assert player.elo_rating == 1200
    
    def test_player_default_values(self):
        """Test player default values"""
        player = PlayerState(player_id="p1", username="Player1")
        assert player.hp == 100
        assert player.hand == []
        assert player.elo_rating == 1200
    
    def test_player_hp_validation(self):
        """Test HP validation (0-100)"""
        # Valid HP
        player = PlayerState(player_id="p1", username="Player1", hp=50)
        assert player.hp == 50
        
        # Invalid HP should raise validation error
        with pytest.raises(Exception):
            PlayerState(player_id="p1", username="Player1", hp=150)
        
        with pytest.raises(Exception):
            PlayerState(player_id="p1", username="Player1", hp=-10)


class TestPromptSubmission:
    """Tests for PromptSubmission model"""
    
    def test_prompt_submission(self):
        """Test creating a prompt submission"""
        submission = PromptSubmission(
            player_id="player_123",
            prompt="A blazing phoenix rises from the ashes",
            cards_used=["fire", "summon"]
        )
        assert submission.player_id == "player_123"
        assert submission.prompt == "A blazing phoenix rises from the ashes"
        assert submission.cards_used == ["fire", "summon"]
        assert isinstance(submission.submitted_at, datetime)
    
    def test_prompt_length_validation(self):
        """Test prompt length constraints"""
        # Valid prompt
        submission = PromptSubmission(
            player_id="p1",
            prompt="Valid prompt",
            cards_used=["fire"]
        )
        assert len(submission.prompt) > 0
        
        # Empty prompt should fail
        with pytest.raises(Exception):
            PromptSubmission(
                player_id="p1",
                prompt="",
                cards_used=["fire"]
            )


class TestBattleResult:
    """Tests for BattleResult model"""
    
    def test_battle_result_with_winner(self):
        """Test battle result with a winner"""
        result = BattleResult(
            winner_id="player_123",
            damage_dealt=25,
            reasoning="Player 1's attack was more creative",
            creativity_score=8.5,
            adherence_score=9.0
        )
        assert result.winner_id == "player_123"
        assert result.damage_dealt == 25
        assert result.creativity_score == 8.5
        assert result.adherence_score == 9.0
    
    def test_battle_result_tie(self):
        """Test battle result with no winner (tie)"""
        result = BattleResult(
            winner_id=None,
            damage_dealt=0,
            reasoning="Both prompts were equally matched",
            creativity_score=7.0,
            adherence_score=7.0
        )
        assert result.winner_id is None
        assert result.damage_dealt == 0
    
    def test_score_validation(self):
        """Test score validation (0-10)"""
        # Valid scores
        result = BattleResult(
            reasoning="Test",
            creativity_score=5.0,
            adherence_score=5.0
        )
        assert 0 <= result.creativity_score <= 10
        assert 0 <= result.adherence_score <= 10


class TestGameState:
    """Tests for GameState model"""

    def test_game_creation(self):
        """Test creating a new game"""
        player1 = PlayerState(player_id="p1", username="Player1")
        game = GameState(
            game_id="game_123",
            player1=player1
        )
        assert game.game_id == "game_123"
        assert game.status == GameStatus.WAITING
        assert game.player1.player_id == "p1"
        assert game.player2 is None
        assert game.current_turn == 1

    def test_game_with_two_players(self):
        """Test game with both players"""
        player1 = PlayerState(player_id="p1", username="Player1")
        player2 = PlayerState(player_id="p2", username="Player2")
        game = GameState(
            game_id="game_123",
            status=GameStatus.ACTIVE,
            player1=player1,
            player2=player2
        )
        assert game.status == GameStatus.ACTIVE
        assert game.player1.player_id == "p1"
        assert game.player2.player_id == "p2"

    def test_game_status_transitions(self):
        """Test game status values"""
        player1 = PlayerState(player_id="p1", username="Player1")

        # Waiting status
        game = GameState(game_id="g1", player1=player1, status=GameStatus.WAITING)
        assert game.status == GameStatus.WAITING

        # Active status
        game.status = GameStatus.ACTIVE
        assert game.status == GameStatus.ACTIVE

        # Finished status
        game.status = GameStatus.FINISHED
        assert game.status == GameStatus.FINISHED

