"""
Judge API endpoints for testing battle judgments
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from app.logic.judge_service import JudgeService
from app.models.game import PromptSubmission, BattleResult

router = APIRouter()


class BattleRequest(BaseModel):
    """Request model for testing battle judgments"""
    player1_name: str = Field(..., min_length=1, max_length=50)
    player1_prompt: str = Field(..., min_length=10, max_length=500)
    player1_cards: List[str] = Field(..., min_items=1, max_items=10)
    
    player2_name: str = Field(..., min_length=1, max_length=50)
    player2_prompt: str = Field(..., min_length=10, max_length=500)
    player2_cards: List[str] = Field(..., min_items=1, max_items=10)
    
    class Config:
        json_schema_extra = {
            "example": {
                "player1_name": "Alice",
                "player1_prompt": "A blazing phoenix rises from the ashes, wielding a flaming sword to strike down my enemies",
                "player1_cards": ["fire", "summon", "sword"],
                "player2_name": "Bob",
                "player2_prompt": "An ice dragon descends from the frozen peaks, breathing crystalline shards",
                "player2_cards": ["ice", "summon", "crystal"]
            }
        }


@router.post("/judge/battle", response_model=BattleResult)
async def judge_battle(request: BattleRequest):
    """
    Test the AI judge by submitting two prompts for battle
    
    This endpoint allows you to test the AI judge service by providing
    two player prompts with their selected cards. The AI will evaluate
    creativity, card adherence, and determine a winner.
    
    **Note:** This requires a valid LLM provider to be configured.
    Set LLM_PROVIDER, LLM_MODEL, and appropriate API keys in your .env file.
    """
    try:
        # Create judge service
        judge = JudgeService()
        
        # Check if judge is available
        if not await judge.is_available():
            raise HTTPException(
                status_code=503,
                detail="AI Judge service is not available. Please check your LLM provider configuration."
            )
        
        # Create prompt submissions
        player1_submission = PromptSubmission(
            player_id="player_1",
            prompt=request.player1_prompt,
            cards_used=request.player1_cards,
            submitted_at=datetime.utcnow()
        )
        
        player2_submission = PromptSubmission(
            player_id="player_2",
            prompt=request.player2_prompt,
            cards_used=request.player2_cards,
            submitted_at=datetime.utcnow()
        )
        
        # Judge the battle
        result = await judge.judge_battle(
            player1_submission,
            player2_submission,
            request.player1_name,
            request.player2_name
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to judge battle: {str(e)}"
        )


@router.get("/judge/health")
async def judge_health():
    """
    Check if the AI judge service is available
    
    Returns the status of the LLM provider and whether
    the judge service can process battles.
    """
    try:
        judge = JudgeService()
        is_available = await judge.is_available()
        
        return {
            "status": "available" if is_available else "unavailable",
            "provider": judge.llm_provider.get_provider_name(),
            "model": judge.llm_provider.get_model_name(),
            "message": "AI Judge is ready" if is_available else "AI Judge is not configured"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

