"""
AI Judge Service
Uses LLM to judge battles between player prompts
"""
from typing import List
from app.models.game import PromptSubmission, BattleResult, VisualEffect
from app.providers.llm_provider import LLMProvider, LLMMessage
from app.providers.llm_factory import get_llm_provider
import json


class JudgeService:
    """Service for judging battles using AI"""
    
    # System prompt that defines the judge's role and rules
    SYSTEM_PROMPT = """You are an AI judge for "Prompt Wars," a creative text-based battle game.

Your role is to evaluate two players' creative prompts and determine the winner based on:
1. **Creativity** (0-10): How imaginative and original is the prompt?
2. **Card Adherence** (0-10): How well does the prompt incorporate the required cards?
3. **Battle Impact**: Which prompt would be more effective in a fantasy battle?

RULES:
- Each player submits a prompt using specific cards (elements, actions, materials)
- The prompt MUST use all the cards they selected
- Award higher scores for creative combinations and vivid imagery
- Deduct points if cards are not properly incorporated
- Determine a winner based on overall effectiveness
- Ties are allowed if both prompts are equally matched

OUTPUT FORMAT (JSON):
{
  "winner": "player1" or "player2" or "tie",
  "player1_creativity": 0-10,
  "player1_adherence": 0-10,
  "player2_creativity": 0-10,
  "player2_adherence": 0-10,
  "damage": 0-50 (damage dealt to loser, 0 for tie),
  "reasoning": "Write a SHORT, EXCITING 2-3 sentence story describing what happened in the battle and who won. Make it dramatic and engaging! Example: 'The warrior summons a blazing phoenix that soars through the arena! The opponent's ice shield shatters under the intense heat. Victory goes to the fire wielder!'",
  "visual_effect": "fire" or "ice" or "lightning" or "explosion" or "heal" or "shield"
}

Be fair, creative, and entertaining in your judgments! The reasoning should be a mini-story, not a dry explanation."""
    
    def __init__(self, llm_provider: LLMProvider = None):
        """
        Initialize the judge service
        
        Args:
            llm_provider: LLM provider to use (defaults to singleton)
        """
        self.llm_provider = llm_provider or get_llm_provider()
    
    def _build_battle_prompt(
        self,
        player1_submission: PromptSubmission,
        player2_submission: PromptSubmission,
        player1_name: str = "Player 1",
        player2_name: str = "Player 2"
    ) -> str:
        """
        Build the battle prompt for the LLM
        
        Args:
            player1_submission: Player 1's prompt submission
            player2_submission: Player 2's prompt submission
            player1_name: Player 1's display name
            player2_name: Player 2's display name
            
        Returns:
            Formatted battle prompt
        """
        return f"""BATTLE ROUND

{player1_name}:
- Cards Used: {', '.join(player1_submission.cards_used)}
- Prompt: "{player1_submission.prompt}"

{player2_name}:
- Cards Used: {', '.join(player2_submission.cards_used)}
- Prompt: "{player2_submission.prompt}"

Judge this battle and provide your verdict in JSON format."""
    
    async def judge_battle(
        self,
        player1_submission: PromptSubmission,
        player2_submission: PromptSubmission,
        player1_name: str = "Player 1",
        player2_name: str = "Player 2"
    ) -> BattleResult:
        """
        Judge a battle between two players
        
        Args:
            player1_submission: Player 1's prompt submission
            player2_submission: Player 2's prompt submission
            player1_name: Player 1's display name
            player2_name: Player 2's display name
            
        Returns:
            BattleResult with winner, scores, and reasoning
            
        Raises:
            Exception: If LLM call fails or response is invalid
        """
        # Build the battle prompt
        battle_prompt = self._build_battle_prompt(
            player1_submission,
            player2_submission,
            player1_name,
            player2_name
        )
        
        # Create messages for LLM
        messages = [
            LLMMessage(role="system", content=self.SYSTEM_PROMPT),
            LLMMessage(role="user", content=battle_prompt)
        ]
        
        # Call LLM
        response = await self.llm_provider.generate(
            messages,
            temperature=0.7,
            max_tokens=500
        )
        
        # Parse JSON response
        try:
            # Extract JSON from response (handle markdown code blocks)
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            result_data = json.loads(content)
            
            # Determine winner ID
            winner_id = None
            if result_data["winner"] == "player1":
                winner_id = player1_submission.player_id
            elif result_data["winner"] == "player2":
                winner_id = player2_submission.player_id
            # else: tie (winner_id remains None)
            
            # Calculate average scores
            p1_avg = (result_data["player1_creativity"] + result_data["player1_adherence"]) / 2
            p2_avg = (result_data["player2_creativity"] + result_data["player2_adherence"]) / 2

            # Create visual effect
            visual_effect_type = result_data.get("visual_effect", "explosion")
            visual_effects = [
                VisualEffect(
                    particle_type=visual_effect_type,
                    intensity=1.5 if winner_id else 1.0,
                    color=self._get_effect_color(visual_effect_type),
                    duration_ms=1500
                )
            ]

            # Build battle result
            return BattleResult(
                winner_id=winner_id,
                damage_dealt=result_data["damage"],
                reasoning=result_data["reasoning"],
                creativity_score=p1_avg if winner_id == player1_submission.player_id else p2_avg,
                adherence_score=result_data["player1_adherence"] if winner_id == player1_submission.player_id else result_data["player2_adherence"],
                visual_effects=visual_effects
            )

        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse LLM response as JSON: {str(e)}\nResponse: {response.content}")
        except KeyError as e:
            raise Exception(f"Missing required field in LLM response: {str(e)}\nResponse: {response.content}")

    def _get_effect_color(self, effect_type: str) -> str:
        """
        Get color for visual effect type

        Args:
            effect_type: Type of effect

        Returns:
            Hex color code
        """
        colors = {
            "fire": "#FF4500",
            "ice": "#00BFFF",
            "lightning": "#FFD700",
            "explosion": "#FF6347",
            "heal": "#32CD32",
            "shield": "#4169E1"
        }
        return colors.get(effect_type, "#FFFFFF")

    async def is_available(self) -> bool:
        """
        Check if the judge service is available

        Returns:
            True if LLM provider is available, False otherwise
        """
        return await self.llm_provider.is_available()

