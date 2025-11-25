"""
Card Service
Manages the card registry and card-related operations
"""
import json
import random
from pathlib import Path
from typing import List, Dict, Optional
from app.models.game import Card, CardType


class CardService:
    """Service for managing game cards"""
    
    def __init__(self):
        """Initialize card service and load cards from JSON"""
        self._cards: Dict[str, Card] = {}
        self._load_cards()
    
    def _load_cards(self) -> None:
        """Load cards from cards.json file"""
        cards_file = Path(__file__).parent.parent / "data" / "cards.json"
        
        with open(cards_file, 'r') as f:
            data = json.load(f)
        
        for card_data in data['cards']:
            card = Card(**card_data)
            self._cards[card.id] = card
    
    def get_card(self, card_id: str) -> Optional[Card]:
        """
        Get a card by its ID
        
        Args:
            card_id: The card identifier
            
        Returns:
            Card object or None if not found
        """
        return self._cards.get(card_id)
    
    def get_all_cards(self) -> List[Card]:
        """
        Get all available cards
        
        Returns:
            List of all Card objects
        """
        return list(self._cards.values())
    
    def get_cards_by_type(self, card_type: CardType) -> List[Card]:
        """
        Get all cards of a specific type
        
        Args:
            card_type: The type of cards to retrieve
            
        Returns:
            List of Card objects matching the type
        """
        return [card for card in self._cards.values() if card.type == card_type]
    
    def draw_random_hand(self, hand_size: int = 3) -> List[Card]:
        """
        Draw a random hand of cards
        Ensures one card from each type (element, action, material)
        
        Args:
            hand_size: Number of cards to draw (default: 3)
            
        Returns:
            List of Card objects
        """
        if hand_size < 3:
            raise ValueError("Hand size must be at least 3 to include all card types")
        
        hand = []
        
        # Draw one card from each type
        for card_type in CardType:
            type_cards = self.get_cards_by_type(card_type)
            hand.append(random.choice(type_cards))
        
        # Fill remaining slots with random cards
        remaining_slots = hand_size - 3
        if remaining_slots > 0:
            all_cards = self.get_all_cards()
            # Exclude already drawn cards
            available_cards = [c for c in all_cards if c not in hand]
            hand.extend(random.sample(available_cards, min(remaining_slots, len(available_cards))))
        
        return hand
    
    def validate_cards(self, card_ids: List[str]) -> bool:
        """
        Validate that all card IDs exist in the registry
        
        Args:
            card_ids: List of card IDs to validate
            
        Returns:
            True if all cards exist, False otherwise
        """
        return all(card_id in self._cards for card_id in card_ids)
    
    def get_card_count(self) -> int:
        """
        Get total number of cards in registry
        
        Returns:
            Number of cards
        """
        return len(self._cards)


# Singleton instance
_card_service_instance: Optional[CardService] = None


def get_card_service() -> CardService:
    """
    Get the singleton CardService instance
    
    Returns:
        CardService instance
    """
    global _card_service_instance
    if _card_service_instance is None:
        _card_service_instance = CardService()
    return _card_service_instance

