"""
Tests for Card Service
"""
import pytest
from app.services.card_service import CardService, get_card_service
from app.models.game import CardType


class TestCardService:
    """Tests for CardService"""
    
    @pytest.fixture
    def card_service(self):
        """Create a fresh CardService instance for each test"""
        return CardService()
    
    def test_card_service_initialization(self, card_service):
        """Test that card service loads cards on initialization"""
        assert card_service.get_card_count() > 0
    
    def test_get_all_cards(self, card_service):
        """Test getting all cards"""
        cards = card_service.get_all_cards()
        assert len(cards) == 20  # We have 20 cards in cards.json
        assert all(hasattr(card, 'id') for card in cards)
        assert all(hasattr(card, 'name') for card in cards)
        assert all(hasattr(card, 'type') for card in cards)
    
    def test_get_card_by_id(self, card_service):
        """Test getting a specific card by ID"""
        fire_card = card_service.get_card("fire")
        assert fire_card is not None
        assert fire_card.id == "fire"
        assert fire_card.name == "Fire"
        assert fire_card.type == CardType.ELEMENT
    
    def test_get_nonexistent_card(self, card_service):
        """Test getting a card that doesn't exist"""
        card = card_service.get_card("nonexistent")
        assert card is None
    
    def test_get_cards_by_type_element(self, card_service):
        """Test getting all element cards"""
        elements = card_service.get_cards_by_type(CardType.ELEMENT)
        assert len(elements) == 7  # fire, water, earth, air, lightning, ice, shadow
        assert all(card.type == CardType.ELEMENT for card in elements)
    
    def test_get_cards_by_type_action(self, card_service):
        """Test getting all action cards"""
        actions = card_service.get_cards_by_type(CardType.ACTION)
        assert len(actions) == 6  # attack, defend, heal, summon, transform, enchant
        assert all(card.type == CardType.ACTION for card in actions)
    
    def test_get_cards_by_type_material(self, card_service):
        """Test getting all material cards"""
        materials = card_service.get_cards_by_type(CardType.MATERIAL)
        assert len(materials) == 7  # sword, shield, crystal, book, potion, armor, staff
        assert all(card.type == CardType.MATERIAL for card in materials)
    
    def test_draw_random_hand_default_size(self, card_service):
        """Test drawing a random hand with default size (3)"""
        hand = card_service.draw_random_hand()
        assert len(hand) == 3
        
        # Should have one of each type
        types = [card.type for card in hand]
        assert CardType.ELEMENT in types
        assert CardType.ACTION in types
        assert CardType.MATERIAL in types
    
    def test_draw_random_hand_custom_size(self, card_service):
        """Test drawing a random hand with custom size"""
        hand = card_service.draw_random_hand(hand_size=5)
        assert len(hand) == 5
        
        # Should still have at least one of each type
        types = [card.type for card in hand]
        assert CardType.ELEMENT in types
        assert CardType.ACTION in types
        assert CardType.MATERIAL in types
    
    def test_draw_random_hand_invalid_size(self, card_service):
        """Test that drawing a hand with size < 3 raises error"""
        with pytest.raises(ValueError):
            card_service.draw_random_hand(hand_size=2)
    
    def test_draw_random_hand_uniqueness(self, card_service):
        """Test that drawn cards are unique (no duplicates)"""
        hand = card_service.draw_random_hand(hand_size=5)
        card_ids = [card.id for card in hand]
        assert len(card_ids) == len(set(card_ids))  # All IDs should be unique
    
    def test_validate_cards_valid(self, card_service):
        """Test validating a list of valid card IDs"""
        valid_ids = ["fire", "attack", "sword"]
        assert card_service.validate_cards(valid_ids) is True
    
    def test_validate_cards_invalid(self, card_service):
        """Test validating a list with invalid card IDs"""
        invalid_ids = ["fire", "nonexistent", "sword"]
        assert card_service.validate_cards(invalid_ids) is False
    
    def test_validate_cards_empty(self, card_service):
        """Test validating an empty list"""
        assert card_service.validate_cards([]) is True
    
    def test_get_card_count(self, card_service):
        """Test getting the total card count"""
        count = card_service.get_card_count()
        assert count == 20


class TestCardServiceSingleton:
    """Tests for CardService singleton pattern"""
    
    def test_get_card_service_singleton(self):
        """Test that get_card_service returns the same instance"""
        service1 = get_card_service()
        service2 = get_card_service()
        assert service1 is service2
    
    def test_singleton_has_cards_loaded(self):
        """Test that singleton instance has cards loaded"""
        service = get_card_service()
        assert service.get_card_count() == 20

