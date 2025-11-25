"""
WebSocket Connection Manager
Handles real-time communication between clients and server
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections for real-time game communication"""
    
    def __init__(self):
        # Active connections: {connection_id: websocket}
        self.active_connections: Dict[str, WebSocket] = {}
        # Room memberships: {room_id: set of connection_ids}
        self.rooms: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, connection_id: str):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        logger.info(f"Client {connection_id} connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, connection_id: str):
        """Remove a WebSocket connection"""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
            logger.info(f"Client {connection_id} disconnected. Total connections: {len(self.active_connections)}")
        
        # Remove from all rooms
        for room_id in list(self.rooms.keys()):
            if connection_id in self.rooms[room_id]:
                self.rooms[room_id].remove(connection_id)
                if not self.rooms[room_id]:
                    del self.rooms[room_id]
    
    def join_room(self, connection_id: str, room_id: str):
        """Add a connection to a room"""
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        self.rooms[room_id].add(connection_id)
        logger.info(f"Client {connection_id} joined room {room_id}")
    
    def leave_room(self, connection_id: str, room_id: str):
        """Remove a connection from a room"""
        if room_id in self.rooms and connection_id in self.rooms[room_id]:
            self.rooms[room_id].remove(connection_id)
            if not self.rooms[room_id]:
                del self.rooms[room_id]
            logger.info(f"Client {connection_id} left room {room_id}")
    
    async def send_personal_message(self, message: dict, connection_id: str):
        """Send a message to a specific connection"""
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            await websocket.send_json(message)
    
    async def broadcast_to_room(self, message: dict, room_id: str, exclude: str = None):
        """Broadcast a message to all connections in a room"""
        if room_id in self.rooms:
            for connection_id in self.rooms[room_id]:
                if connection_id != exclude:
                    await self.send_personal_message(message, connection_id)
    
    async def broadcast_to_all(self, message: dict):
        """Broadcast a message to all active connections"""
        for connection_id in list(self.active_connections.keys()):
            await self.send_personal_message(message, connection_id)


# Global connection manager instance
manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for real-time communication
    
    Message format:
    {
        "type": "MESSAGE_TYPE",
        "data": {...}
    }
    """
    await manager.connect(websocket, client_id)
    
    try:
        # Send welcome message
        await manager.send_personal_message({
            "type": "CONNECTED",
            "data": {
                "client_id": client_id,
                "message": "Connected to Prompt Wars server"
            }
        }, client_id)
        
        # Listen for messages
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type", "UNKNOWN")
            message_data = data.get("data", {})
            
            logger.info(f"Received {message_type} from {client_id}: {message_data}")
            
            # Echo the message back (for testing)
            await manager.send_personal_message({
                "type": "ECHO",
                "data": {
                    "original_type": message_type,
                    "original_data": message_data,
                    "message": f"Server received your {message_type} message"
                }
            }, client_id)
            
            # Broadcast to all other clients
            await manager.broadcast_to_all({
                "type": "BROADCAST",
                "data": {
                    "from": client_id,
                    "message_type": message_type,
                    "message": f"Client {client_id} sent a {message_type} message"
                }
            })
    
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info(f"Client {client_id} disconnected")
    except Exception as e:
        logger.error(f"Error in WebSocket connection {client_id}: {e}")
        manager.disconnect(client_id)

