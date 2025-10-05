from fastapi import WebSocket
from typing import Dict, List
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_locations: Dict[str, tuple] = {}  

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"User {user_id} connected via WebSocket")

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_locations:
            del self.user_locations[user_id]
        print(f"User {user_id} disconnected")

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            try:
                websocket = self.active_connections[user_id]
                await websocket.send_text(json.dumps(message))
                return True
            except Exception as e:
                print(f"Error sending message to {user_id}: {e}")
                self.disconnect(user_id)
                return False
        return False

    async def broadcast_to_nearby(self, user_ids: List[str], message: dict):
        successful_sends = 0
        
        for user_id in user_ids:
            success = await self.send_personal_message(message, user_id)
            if success:
                successful_sends += 1
        
        print(f"Broadcast sent to {successful_sends}/{len(user_ids)} users")
        return successful_sends

    async def broadcast_to_all(self, message: dict):
        if not self.active_connections:
            return 0
        
        user_ids = list(self.active_connections.keys())
        return await self.broadcast_to_nearby(user_ids, message)

    def update_user_location(self, user_id: str, lat: float, lng: float):
        self.user_locations[user_id] = (lat, lng)

    def get_nearby_connected_users(self, lat: float, lng: float, radius_km: float = 5.0) -> List[str]:
        nearby_users = []
        
        for user_id, (user_lat, user_lng) in self.user_locations.items():
            if user_id in self.active_connections:
                lat_diff = abs(lat - user_lat)
                lng_diff = abs(lng - user_lng)
                
                distance_km = ((lat_diff ** 2 + lng_diff ** 2) ** 0.5) * 111
                
                if distance_km <= radius_km:
                    nearby_users.append(user_id)
        
        return nearby_users

    async def send_notification(self, user_id: str, notification_type: str, data: dict):
        message = {
            "type": "notification",
            "notification_type": notification_type,
            "data": data,
            "timestamp": data.get("timestamp", "")
        }
        
        return await self.send_personal_message(message, user_id)

    async def send_badge_notification(self, user_id: str, badge_data: dict):
        return await self.send_notification(user_id, "badge_earned", {
            "badge_name": badge_data["name"],
            "badge_id": badge_data["id"],
            "message": f"Congratulations! You earned the '{badge_data['name']}' badge!"
        })

    async def send_compliment_notification(self, user_id: str, compliment_data: dict):
        return await self.send_notification(user_id, "new_compliment", {
            "content": compliment_data["content"],
            "sender_score": compliment_data.get("sender_score", 0),
            "media_url": compliment_data.get("media_url"),
            "message": "You received a new compliment!"
        })

    def get_connection_stats(self) -> dict:
        return {
            "total_connections": len(self.active_connections),
            "users_with_location": len(self.user_locations),
            "connected_users": list(self.active_connections.keys())
        }