from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: str
    firebase_uid: str
    username: Optional[str]
    kindness_score: int = 0
    total_sent: int = 0
    total_received: int = 0
    current_streak: int = 0

@dataclass
class Compliment:
    id: str
    sender_id: str
    recipient_id: str
    content: str
    sender_lat: float
    sender_lng: float

@dataclass
class UserLocation:
    user_id: str
    latitude: float
    longitude: float