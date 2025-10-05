from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    firebase_uid: str
    username: Optional[str] = None

class ComplimentCreate(BaseModel):
    content: str
    lat: float
    lng: float
    media_url: Optional[str] = None

class LocationUpdate(BaseModel):
    lat: float
    lng: float

class ComplimentResponse(BaseModel):
    id: str
    content: str
    sender_score: int
    created_at: datetime
    media_url: Optional[str] = None

class UserProfile(BaseModel):
    username: str
    kindness_score: int
    total_sent: int
    total_received: int
    current_streak: int
    badge_count: int

class LeaderboardEntry(BaseModel):
    username: str
    kindness_score: int
    rank: int

class BadgeResponse(BaseModel):
    id: int
    name: str
    description: str
    icon_path: str
    earned_at: Optional[datetime] = None