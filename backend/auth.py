import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from database import get_db

def init_firebase():
    try:
        firebase_admin.get_app()
    except ValueError:
        cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY", "serviceAccountKey.json")
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            print("Warning: Firebase service account key not found. Using default credentials.")
            firebase_admin.initialize_app()

init_firebase()

security = HTTPBearer()

async def verify_firebase_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        firebase_uid = decoded_token['uid']
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE firebase_uid = ?", (firebase_uid,))
        user_row = cursor.fetchone()
        
        conn.close()
        
        if not user_row:
            raise HTTPException(status_code=404, detail="User not found in database")
        
        return {
            "id": user_row[0],
            "firebase_uid": user_row[1],
            "username": user_row[2],
            "kindness_score": user_row[3],
            "total_sent": user_row[4],
            "total_received": user_row[5],
            "current_streak": user_row[6]
        }
        
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Expired authentication token")
    except Exception as e:
        print(f"Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:

    try:
        return await verify_firebase_token(credentials)
    except HTTPException:
        return None

def create_anonymous_user(firebase_uid: str, username: str = None) -> dict:

    conn = get_db()
    cursor = conn.cursor()
    
    import uuid
    user_id = str(uuid.uuid4())
    
    cursor.execute("""
        INSERT INTO users (id, firebase_uid, username, kindness_score)
        VALUES (?, ?, ?, 0)
    """, (user_id, firebase_uid, username))
    
    conn.commit()
    conn.close()
    
    return {
        "id": user_id,
        "firebase_uid": firebase_uid,
        "username": username,
        "kindness_score": 0
    }

def validate_user_permissions(current_user: dict, required_permission: str = None) -> bool:

    if not current_user:
        return False
    
    if not current_user.get("is_active", True):
        return False
    
    if required_permission == "send_compliment":
        return True
    
    return True