"""
Card API Endpoints
Provides access to card registry and card operations
"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.game import Card, CardType
from app.services.card_service import get_card_service

router = APIRouter()


@router.get("/cards", response_model=List[Card])
async def get_all_cards():
    """
    Get all available cards
    
    Returns:
        List of all cards in the registry
    """
    card_service = get_card_service()
    return card_service.get_all_cards()


@router.get("/cards/{card_id}", response_model=Card)
async def get_card(card_id: str):
    """
    Get a specific card by ID
    
    Args:
        card_id: The card identifier
        
    Returns:
        Card object
        
    Raises:
        HTTPException: If card not found
    """
    card_service = get_card_service()
    card = card_service.get_card(card_id)
    
    if card is None:
        raise HTTPException(status_code=404, detail=f"Card '{card_id}' not found")
    
    return card


@router.get("/cards/type/{card_type}", response_model=List[Card])
async def get_cards_by_type(card_type: CardType):
    """
    Get all cards of a specific type
    
    Args:
        card_type: The card type (element, action, material)
        
    Returns:
        List of cards matching the type
    """
    card_service = get_card_service()
    return card_service.get_cards_by_type(card_type)


@router.get("/cards/draw/hand", response_model=List[Card])
async def draw_random_hand(hand_size: int = 3):
    """
    Draw a random hand of cards
    
    Args:
        hand_size: Number of cards to draw (default: 3, minimum: 3)
        
    Returns:
        List of randomly drawn cards
        
    Raises:
        HTTPException: If hand_size is invalid
    """
    if hand_size < 3:
        raise HTTPException(
            status_code=400, 
            detail="Hand size must be at least 3 to include all card types"
        )
    
    if hand_size > 20:
        raise HTTPException(
            status_code=400,
            detail="Hand size cannot exceed 20 (total number of cards)"
        )
    
    card_service = get_card_service()
    return card_service.draw_random_hand(hand_size)


@router.get("/cards/stats/summary")
async def get_card_stats():
    """
    Get statistics about the card registry
    
    Returns:
        Dictionary with card statistics
    """
    card_service = get_card_service()
    
    return {
        "total_cards": card_service.get_card_count(),
        "elements": len(card_service.get_cards_by_type(CardType.ELEMENT)),
        "actions": len(card_service.get_cards_by_type(CardType.ACTION)),
        "materials": len(card_service.get_cards_by_type(CardType.MATERIAL))
    }

