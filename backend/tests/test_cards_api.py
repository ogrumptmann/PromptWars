"""
Tests for Cards API Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestCardsAPI:
    """Tests for /api/cards endpoints"""
    
    def test_get_all_cards(self):
        """Test GET /api/cards - get all cards"""
        response = client.get("/api/cards")
        assert response.status_code == 200
        
        cards = response.json()
        assert len(cards) == 20
        assert all('id' in card for card in cards)
        assert all('name' in card for card in cards)
        assert all('type' in card for card in cards)
        assert all('description' in card for card in cards)
    
    def test_get_card_by_id_success(self):
        """Test GET /api/cards/{card_id} - get specific card"""
        response = client.get("/api/cards/fire")
        assert response.status_code == 200
        
        card = response.json()
        assert card['id'] == 'fire'
        assert card['name'] == 'Fire'
        assert card['type'] == 'element'
    
    def test_get_card_by_id_not_found(self):
        """Test GET /api/cards/{card_id} - card not found"""
        response = client.get("/api/cards/nonexistent")
        assert response.status_code == 404
        assert 'not found' in response.json()['detail'].lower()
    
    def test_get_cards_by_type_element(self):
        """Test GET /api/cards/type/element"""
        response = client.get("/api/cards/type/element")
        assert response.status_code == 200
        
        cards = response.json()
        assert len(cards) == 7
        assert all(card['type'] == 'element' for card in cards)
    
    def test_get_cards_by_type_action(self):
        """Test GET /api/cards/type/action"""
        response = client.get("/api/cards/type/action")
        assert response.status_code == 200
        
        cards = response.json()
        assert len(cards) == 6
        assert all(card['type'] == 'action' for card in cards)
    
    def test_get_cards_by_type_material(self):
        """Test GET /api/cards/type/material"""
        response = client.get("/api/cards/type/material")
        assert response.status_code == 200
        
        cards = response.json()
        assert len(cards) == 7
        assert all(card['type'] == 'material' for card in cards)
    
    def test_draw_random_hand_default(self):
        """Test GET /api/cards/draw/hand - default hand size"""
        response = client.get("/api/cards/draw/hand")
        assert response.status_code == 200
        
        hand = response.json()
        assert len(hand) == 3
        
        # Should have one of each type
        types = [card['type'] for card in hand]
        assert 'element' in types
        assert 'action' in types
        assert 'material' in types
    
    def test_draw_random_hand_custom_size(self):
        """Test GET /api/cards/draw/hand?hand_size=5"""
        response = client.get("/api/cards/draw/hand?hand_size=5")
        assert response.status_code == 200
        
        hand = response.json()
        assert len(hand) == 5
        
        # Cards should be unique
        card_ids = [card['id'] for card in hand]
        assert len(card_ids) == len(set(card_ids))
    
    def test_draw_random_hand_invalid_size_too_small(self):
        """Test GET /api/cards/draw/hand?hand_size=2 - invalid size"""
        response = client.get("/api/cards/draw/hand?hand_size=2")
        assert response.status_code == 400
        assert 'at least 3' in response.json()['detail'].lower()
    
    def test_draw_random_hand_invalid_size_too_large(self):
        """Test GET /api/cards/draw/hand?hand_size=25 - invalid size"""
        response = client.get("/api/cards/draw/hand?hand_size=25")
        assert response.status_code == 400
        assert 'cannot exceed' in response.json()['detail'].lower()
    
    def test_get_card_stats(self):
        """Test GET /api/cards/stats/summary"""
        response = client.get("/api/cards/stats/summary")
        assert response.status_code == 200
        
        stats = response.json()
        assert stats['total_cards'] == 20
        assert stats['elements'] == 7
        assert stats['actions'] == 6
        assert stats['materials'] == 7
        assert stats['total_cards'] == stats['elements'] + stats['actions'] + stats['materials']


class TestCardsAPIIntegration:
    """Integration tests for cards API"""
    
    def test_draw_multiple_hands_are_different(self):
        """Test that drawing multiple hands produces different results"""
        response1 = client.get("/api/cards/draw/hand?hand_size=5")
        response2 = client.get("/api/cards/draw/hand?hand_size=5")
        
        hand1 = response1.json()
        hand2 = response2.json()
        
        # Hands should be different (with very high probability)
        hand1_ids = sorted([card['id'] for card in hand1])
        hand2_ids = sorted([card['id'] for card in hand2])
        
        # At least one card should be different
        assert hand1_ids != hand2_ids or len(hand1_ids) < 5

