"""
Game Data Models
Pydantic models for Prompt Wars game state
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum


class CardType(str, Enum):
    """Card category types"""
    ELEMENT = "element"
    ACTION = "action"
    MATERIAL = "material"


class Card(BaseModel):
    """
    Card model representing a constraint card
    """
    id: str = Field(..., description="Unique card identifier (e.g., 'fire', 'sword')")
    name: str = Field(..., description="Display name of the card")
    type: CardType = Field(..., description="Card category")
    description: str = Field(..., description="Flavor text for the card")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "fire",
                "name": "Fire",
                "type": "element",
                "description": "Harness the power of flames"
            }
        }


class PlayerState(BaseModel):
    """
    Player state within a game
    """
    player_id: str = Field(..., description="Unique player identifier")
    username: str = Field(..., description="Player display name")
    hp: int = Field(default=100, ge=0, le=100, description="Current hit points")
    hand: List[Card] = Field(default_factory=list, description="Cards in player's hand")
    elo_rating: int = Field(default=1200, description="Player's Elo rating")
    
    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "player_123",
                "username": "PromptMaster",
                "hp": 100,
                "hand": [],
                "elo_rating": 1200
            }
        }


class PromptSubmission(BaseModel):
    """
    Player's prompt submission for a turn
    """
    player_id: str = Field(..., description="Player who submitted the prompt")
    prompt: str = Field(..., min_length=1, max_length=500, description="The creative prompt text")
    cards_used: List[str] = Field(..., description="List of card IDs used in this prompt")
    submitted_at: datetime = Field(default_factory=datetime.utcnow, description="Submission timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "player_123",
                "prompt": "A blazing phoenix rises from the ashes",
                "cards_used": ["fire", "phoenix"],
                "submitted_at": "2024-01-01T12:00:00Z"
            }
        }


class VisualEffect(BaseModel):
    """
    Visual effect configuration for PixiJS rendering
    """
    particle_type: Literal["fire", "ice", "lightning", "explosion", "heal", "shield"] = Field(
        ..., description="Type of particle effect"
    )
    intensity: float = Field(default=1.0, ge=0.0, le=2.0, description="Effect intensity multiplier")
    color: str = Field(default="#FFFFFF", description="Primary color in hex format")
    duration_ms: int = Field(default=1000, ge=100, le=5000, description="Effect duration in milliseconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "particle_type": "fire",
                "intensity": 1.5,
                "color": "#FF4500",
                "duration_ms": 1500
            }
        }


class BattleResult(BaseModel):
    """
    Result of a turn battle judged by AI
    """
    winner_id: Optional[str] = Field(None, description="Player ID of the winner, None for tie")
    damage_dealt: int = Field(default=0, ge=0, le=50, description="Damage dealt to loser")
    reasoning: str = Field(..., description="AI judge's explanation of the decision")
    creativity_score: float = Field(default=0.0, ge=0.0, le=10.0, description="Creativity rating (0-10)")
    adherence_score: float = Field(default=0.0, ge=0.0, le=10.0, description="Card adherence rating (0-10)")
    visual_effects: List[VisualEffect] = Field(default_factory=list, description="Visual effects to render")
    
    class Config:
        json_schema_extra = {
            "example": {
                "winner_id": "player_123",
                "damage_dealt": 25,
                "reasoning": "Player 1's fiery phoenix overwhelmed the opponent with creative imagery",
                "creativity_score": 8.5,
                "adherence_score": 9.0,
                "visual_effects": []
            }
        }


class TurnState(BaseModel):
    """
    State of a single turn in the game
    """
    turn_number: int = Field(..., ge=1, description="Turn sequence number")
    player1_submission: Optional[PromptSubmission] = Field(None, description="Player 1's prompt submission")
    player2_submission: Optional[PromptSubmission] = Field(None, description="Player 2's prompt submission")
    battle_result: Optional[BattleResult] = Field(None, description="AI judge's battle result")
    completed_at: Optional[datetime] = Field(None, description="Turn completion timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "turn_number": 1,
                "player1_submission": None,
                "player2_submission": None,
                "battle_result": None,
                "completed_at": None
            }
        }


class GameStatus(str, Enum):
    """Game state status"""
    WAITING = "waiting"  # Waiting for second player
    ACTIVE = "active"    # Game in progress
    FINISHED = "finished"  # Game completed


class GameState(BaseModel):
    """
    Complete game state
    """
    game_id: str = Field(..., description="Unique game identifier")
    status: GameStatus = Field(default=GameStatus.WAITING, description="Current game status")
    player1: PlayerState = Field(..., description="Player 1 state")
    player2: Optional[PlayerState] = Field(None, description="Player 2 state")
    current_turn: int = Field(default=1, ge=1, description="Current turn number")
    turn_history: List[TurnState] = Field(default_factory=list, description="History of completed turns")
    winner_id: Optional[str] = Field(None, description="Winner player ID when game is finished")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Game creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "game_id": "game_abc123",
                "status": "active",
                "player1": {
                    "player_id": "player_123",
                    "username": "PromptMaster",
                    "hp": 75,
                    "hand": [],
                    "elo_rating": 1200
                },
                "player2": {
                    "player_id": "player_456",
                    "username": "AIWarrior",
                    "hp": 80,
                    "hand": [],
                    "elo_rating": 1250
                },
                "current_turn": 3,
                "turn_history": [],
                "winner_id": None,
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:05:00Z"
            }
        }

