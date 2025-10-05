import sqlite3
import os
import sys

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def init_database():
    conn = sqlite3.connect('compliment_app.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            firebase_uid TEXT UNIQUE NOT NULL,
            username TEXT,
            kindness_score INTEGER DEFAULT 0,
            total_sent INTEGER DEFAULT 0,
            total_received INTEGER DEFAULT 0,
            current_streak INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compliments (
            id TEXT PRIMARY KEY,
            sender_id TEXT,
            recipient_id TEXT,
            content TEXT NOT NULL,
            sender_lat REAL,
            sender_lng REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_locations (
            user_id TEXT PRIMARY KEY,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized!")

if __name__ == "__main__":
    init_database()
    
    print("🚀 Starting Compliment Generator Backend...")
    print("📍 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)