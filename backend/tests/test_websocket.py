"""
Tests for WebSocket connection manager
"""
import pytest
from app.api.websockets import ConnectionManager


@pytest.fixture
def manager():
    """Create a fresh ConnectionManager for each test"""
    return ConnectionManager()


def test_manager_initialization(manager):
    """Test that manager initializes with empty connections"""
    assert len(manager.active_connections) == 0
    assert len(manager.rooms) == 0


def test_join_room(manager):
    """Test joining a room"""
    connection_id = "test_client_1"
    room_id = "test_room"
    
    manager.join_room(connection_id, room_id)
    
    assert room_id in manager.rooms
    assert connection_id in manager.rooms[room_id]


def test_join_multiple_rooms(manager):
    """Test that a client can join multiple rooms"""
    connection_id = "test_client_1"
    room_1 = "room_1"
    room_2 = "room_2"
    
    manager.join_room(connection_id, room_1)
    manager.join_room(connection_id, room_2)
    
    assert connection_id in manager.rooms[room_1]
    assert connection_id in manager.rooms[room_2]


def test_leave_room(manager):
    """Test leaving a room"""
    connection_id = "test_client_1"
    room_id = "test_room"
    
    # Join then leave
    manager.join_room(connection_id, room_id)
    manager.leave_room(connection_id, room_id)
    
    # Room should be deleted if empty
    assert room_id not in manager.rooms


def test_leave_room_with_multiple_clients(manager):
    """Test leaving a room when other clients are present"""
    client_1 = "test_client_1"
    client_2 = "test_client_2"
    room_id = "test_room"
    
    # Both join
    manager.join_room(client_1, room_id)
    manager.join_room(client_2, room_id)
    
    # One leaves
    manager.leave_room(client_1, room_id)
    
    # Room should still exist with client_2
    assert room_id in manager.rooms
    assert client_1 not in manager.rooms[room_id]
    assert client_2 in manager.rooms[room_id]


def test_disconnect_removes_from_all_rooms(manager):
    """Test that disconnect removes client from all rooms"""
    connection_id = "test_client_1"
    room_1 = "room_1"
    room_2 = "room_2"
    
    # Join multiple rooms
    manager.join_room(connection_id, room_1)
    manager.join_room(connection_id, room_2)
    
    # Disconnect
    manager.disconnect(connection_id)
    
    # Should be removed from all rooms
    assert room_1 not in manager.rooms
    assert room_2 not in manager.rooms


def test_disconnect_nonexistent_client(manager):
    """Test that disconnecting non-existent client doesn't raise error"""
    # Should not raise any exception
    manager.disconnect("nonexistent_client")


def test_leave_nonexistent_room(manager):
    """Test leaving a room that doesn't exist"""
    # Should not raise any exception
    manager.leave_room("test_client", "nonexistent_room")


def test_multiple_clients_in_room(manager):
    """Test multiple clients in the same room"""
    room_id = "test_room"
    clients = ["client_1", "client_2", "client_3"]
    
    for client in clients:
        manager.join_room(client, room_id)
    
    assert len(manager.rooms[room_id]) == 3
    for client in clients:
        assert client in manager.rooms[room_id]


def test_room_cleanup_on_last_client_leave(manager):
    """Test that room is deleted when last client leaves"""
    connection_id = "test_client_1"
    room_id = "test_room"
    
    manager.join_room(connection_id, room_id)
    assert room_id in manager.rooms
    
    manager.leave_room(connection_id, room_id)
    assert room_id not in manager.rooms


def test_disconnect_with_active_connection(manager):
    """Test disconnect removes from active connections"""
    connection_id = "test_client_1"
    
    # Simulate adding to active connections
    manager.active_connections[connection_id] = "mock_websocket"
    
    manager.disconnect(connection_id)
    
    assert connection_id not in manager.active_connections

