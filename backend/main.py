from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(title="Compliment Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    firebase_uid: str
    username: Optional[str] = None

class ComplimentCreate(BaseModel):
    content: str
    lat: float
    lng: float

class LocationUpdate(BaseModel):
    lat: float
    lng: float

def get_db():
    return sqlite3.connect('compliment_app.db')

@app.post("/api/users/register")
async def register_user(user_data: UserCreate):
    conn = get_db()
    cursor = conn.cursor()
    
    user_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO users (id, firebase_uid, username, kindness_score)
        VALUES (?, ?, ?, 0)
    """, (user_id, user_data.firebase_uid, user_data.username))
    
    conn.commit()
    conn.close()
    
    return {"user_id": user_id, "kindness_score": 0}

@app.post("/api/compliments/send")
async def send_compliment(compliment: ComplimentCreate):
    conn = get_db()
    cursor = conn.cursor()
    
    compliment_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO compliments (id, content, sender_lat, sender_lng, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (compliment_id, compliment.content, compliment.lat, compliment.lng, datetime.now()))
    
    conn.commit()
    conn.close()
    
    return {"success": True, "message": "Compliment sent!"}

@app.get("/api/compliments/recent")
async def get_recent_compliments():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT content, created_at FROM compliments 
        ORDER BY created_at DESC LIMIT 10
    """)
    
    compliments = [{"content": row[0], "created_at": row[1]} for row in cursor.fetchall()]
    conn.close()
    
    return compliments

@app.get("/")
async def root():
    return {"message": "Compliment Generator API is running!"}