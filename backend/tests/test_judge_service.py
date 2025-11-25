"""
Tests for AI Judge Service
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from app.logic.judge_service import JudgeService
from app.models.game import PromptSubmission
from app.providers.llm_provider import LLMProvider, LLMResponse


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing"""
    
    def __init__(self, mock_response: str):
        super().__init__(model_name="mock-model")
        self.mock_response = mock_response
        self.generate_called = False
        self.last_messages = None
    
    async def generate(self, messages, temperature=0.7, max_tokens=500, **kwargs):
        self.generate_called = True
        self.last_messages = messages
        return LLMResponse(
            content=self.mock_response,
            model="mock-model"
        )
    
    async def is_available(self):
        return True


class TestJudgeService:
    """Tests for JudgeService"""
    
    @pytest.fixture
    def player1_submission(self):
        """Create a sample player 1 submission"""
        return PromptSubmission(
            player_id="player_1",
            prompt="A blazing phoenix rises from the ashes, wielding a flaming sword",
            cards_used=["fire", "summon", "sword"],
            submitted_at=datetime.utcnow()
        )
    
    @pytest.fixture
    def player2_submission(self):
        """Create a sample player 2 submission"""
        return PromptSubmission(
            player_id="player_2",
            prompt="An ice dragon descends, breathing frozen crystals",
            cards_used=["ice", "summon", "crystal"],
            submitted_at=datetime.utcnow()
        )
    
    @pytest.fixture
    def mock_judge_response_player1_wins(self):
        """Mock LLM response where player 1 wins"""
        return """{
            "winner": "player1",
            "player1_creativity": 9.0,
            "player1_adherence": 8.5,
            "player2_creativity": 7.0,
            "player2_adherence": 7.5,
            "damage": 25,
            "reasoning": "Player 1's phoenix imagery was more vivid and creative",
            "visual_effect": "fire"
        }"""
    
    @pytest.fixture
    def mock_judge_response_tie(self):
        """Mock LLM response for a tie"""
        return """{
            "winner": "tie",
            "player1_creativity": 8.0,
            "player1_adherence": 8.0,
            "player2_creativity": 8.0,
            "player2_adherence": 8.0,
            "damage": 0,
            "reasoning": "Both prompts were equally creative and well-executed",
            "visual_effect": "explosion"
        }"""
    
    def test_initialization(self):
        """Test judge service initialization"""
        mock_provider = MockLLMProvider("test")
        judge = JudgeService(llm_provider=mock_provider)
        assert judge.llm_provider is mock_provider
    
    def test_system_prompt_exists(self):
        """Test that system prompt is defined"""
        assert JudgeService.SYSTEM_PROMPT is not None
        assert len(JudgeService.SYSTEM_PROMPT) > 100
        assert "Prompt Wars" in JudgeService.SYSTEM_PROMPT
        assert "creativity" in JudgeService.SYSTEM_PROMPT.lower()
    
    def test_build_battle_prompt(self, player1_submission, player2_submission):
        """Test building battle prompt"""
        mock_provider = MockLLMProvider("test")
        judge = JudgeService(llm_provider=mock_provider)
        
        prompt = judge._build_battle_prompt(
            player1_submission,
            player2_submission,
            "Alice",
            "Bob"
        )
        
        assert "Alice" in prompt
        assert "Bob" in prompt
        assert player1_submission.prompt in prompt
        assert player2_submission.prompt in prompt
        assert "fire" in prompt
        assert "ice" in prompt
    
    @pytest.mark.asyncio
    async def test_judge_battle_player1_wins(
        self,
        player1_submission,
        player2_submission,
        mock_judge_response_player1_wins
    ):
        """Test judging a battle where player 1 wins"""
        mock_provider = MockLLMProvider(mock_judge_response_player1_wins)
        judge = JudgeService(llm_provider=mock_provider)
        
        result = await judge.judge_battle(
            player1_submission,
            player2_submission,
            "Alice",
            "Bob"
        )
        
        assert result.winner_id == "player_1"
        assert result.damage_dealt == 25
        assert "phoenix" in result.reasoning.lower() or "vivid" in result.reasoning.lower()
        assert result.creativity_score > 0
        assert result.adherence_score > 0
        assert len(result.visual_effects) > 0
        assert result.visual_effects[0].particle_type == "fire"
    
    @pytest.mark.asyncio
    async def test_judge_battle_tie(
        self,
        player1_submission,
        player2_submission,
        mock_judge_response_tie
    ):
        """Test judging a battle that results in a tie"""
        mock_provider = MockLLMProvider(mock_judge_response_tie)
        judge = JudgeService(llm_provider=mock_provider)
        
        result = await judge.judge_battle(
            player1_submission,
            player2_submission
        )
        
        assert result.winner_id is None
        assert result.damage_dealt == 0
        assert "equally" in result.reasoning.lower() or "tie" in result.reasoning.lower()

    @pytest.mark.asyncio
    async def test_judge_battle_with_markdown_json(
        self,
        player1_submission,
        player2_submission
    ):
        """Test handling LLM response wrapped in markdown code blocks"""
        markdown_response = """```json
{
    "winner": "player2",
    "player1_creativity": 7.0,
    "player1_adherence": 7.0,
    "player2_creativity": 9.0,
    "player2_adherence": 9.0,
    "damage": 30,
    "reasoning": "Player 2's ice dragon was more impressive",
    "visual_effect": "ice"
}
```"""
        mock_provider = MockLLMProvider(markdown_response)
        judge = JudgeService(llm_provider=mock_provider)

        result = await judge.judge_battle(
            player1_submission,
            player2_submission
        )

        assert result.winner_id == "player_2"
        assert result.damage_dealt == 30
        assert result.visual_effects[0].particle_type == "ice"

    @pytest.mark.asyncio
    async def test_judge_battle_llm_called_correctly(
        self,
        player1_submission,
        player2_submission,
        mock_judge_response_player1_wins
    ):
        """Test that LLM is called with correct parameters"""
        mock_provider = MockLLMProvider(mock_judge_response_player1_wins)
        judge = JudgeService(llm_provider=mock_provider)

        await judge.judge_battle(
            player1_submission,
            player2_submission
        )

        assert mock_provider.generate_called
        assert len(mock_provider.last_messages) == 2
        assert mock_provider.last_messages[0].role == "system"
        assert mock_provider.last_messages[1].role == "user"
        assert "Alice" not in mock_provider.last_messages[1].content  # Default names
        assert "Player 1" in mock_provider.last_messages[1].content

    @pytest.mark.asyncio
    async def test_judge_battle_invalid_json(
        self,
        player1_submission,
        player2_submission
    ):
        """Test handling invalid JSON response"""
        mock_provider = MockLLMProvider("This is not valid JSON")
        judge = JudgeService(llm_provider=mock_provider)

        with pytest.raises(Exception, match="Failed to parse"):
            await judge.judge_battle(
                player1_submission,
                player2_submission
            )

    @pytest.mark.asyncio
    async def test_judge_battle_missing_fields(
        self,
        player1_submission,
        player2_submission
    ):
        """Test handling response with missing required fields"""
        incomplete_response = '{"winner": "player1"}'
        mock_provider = MockLLMProvider(incomplete_response)
        judge = JudgeService(llm_provider=mock_provider)

        with pytest.raises(Exception, match="Missing required field"):
            await judge.judge_battle(
                player1_submission,
                player2_submission
            )

    def test_get_effect_color(self):
        """Test getting colors for different effect types"""
        mock_provider = MockLLMProvider("test")
        judge = JudgeService(llm_provider=mock_provider)

        assert judge._get_effect_color("fire") == "#FF4500"
        assert judge._get_effect_color("ice") == "#00BFFF"
        assert judge._get_effect_color("lightning") == "#FFD700"
        assert judge._get_effect_color("explosion") == "#FF6347"
        assert judge._get_effect_color("heal") == "#32CD32"
        assert judge._get_effect_color("shield") == "#4169E1"
        assert judge._get_effect_color("unknown") == "#FFFFFF"

    @pytest.mark.asyncio
    async def test_is_available(self):
        """Test checking if judge service is available"""
        mock_provider = MockLLMProvider("test")
        judge = JudgeService(llm_provider=mock_provider)

        assert await judge.is_available() is True

