from datetime import datetime, timedelta
import sqlite3

def update_user_score(cursor, user_id: str, action: str) -> int:

    cursor.execute("SELECT kindness_score, total_sent, total_received, current_streak, last_activity FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    
    if not user_data:
        return 0
    
    current_score, total_sent, total_received, current_streak, last_activity = user_data
    
    points = 0
    if action == "send":
        points = 5
        total_sent += 1
    elif action == "receive":
        points = 3
        total_received += 1
    
    last_activity_date = datetime.fromisoformat(last_activity) if last_activity else datetime.now()
    today = datetime.now().date()
    
    if last_activity_date.date() == today - timedelta(days=1):
        current_streak += 1
        points += 2  
    elif last_activity_date.date() != today:
        current_streak = 1
    
    streak_multiplier = min(1 + (current_streak * 0.1), 2.0)
    points = int(points * streak_multiplier)
    
    new_score = current_score + points
    
    cursor.execute("""
        UPDATE users 
        SET kindness_score = ?, total_sent = ?, total_received = ?, 
            current_streak = ?, last_activity = ?
        WHERE id = ?
    """, (new_score, total_sent, total_received, current_streak, datetime.now(), user_id))
    
    return new_score

def check_badge_eligibility(cursor, user_id: str) -> list:

    
    cursor.execute("""
        SELECT kindness_score, total_sent, total_received, current_streak
        FROM users WHERE id = ?
    """, (user_id,))
    
    user_stats = cursor.fetchone()
    if not user_stats:
        return []
    
    score, sent, received, streak = user_stats
    
    cursor.execute("""
        SELECT b.id, b.name, b.requirement_type, b.requirement_value
        FROM badges b
        WHERE b.id NOT IN (
            SELECT badge_id FROM user_badges WHERE user_id = ?
        )
    """, (user_id,))
    
    available_badges = cursor.fetchall()
    new_badges = []
    
    for badge_id, name, req_type, req_value in available_badges:
        earned = False
        
        if req_type == "score" and score >= req_value:
            earned = True
        elif req_type == "count" and sent >= req_value:
            earned = True
        elif req_type == "streak" and streak >= req_value:
            earned = True
        elif req_type == "special":
            earned = check_special_badge(cursor, user_id, name)
        
        if earned:
            cursor.execute("""
                INSERT INTO user_badges (user_id, badge_id)
                VALUES (?, ?)
            """, (user_id, badge_id))
            
            new_badges.append({"id": badge_id, "name": name})
            
            cursor.execute("""
                UPDATE users SET kindness_score = kindness_score + 15
                WHERE id = ?
            """, (user_id,))
    
    return new_badges

def check_special_badge(cursor, user_id: str, badge_name: str) -> bool:
    
    if badge_name == "Local Hero":

        return False
    
    return False

def calculate_leaderboard_rank(cursor, user_id: str, leaderboard_type: str = "global") -> int:
    
    if leaderboard_type == "global":
        cursor.execute("""
            SELECT COUNT(*) + 1 as rank
            FROM users 
            WHERE kindness_score > (
                SELECT kindness_score FROM users WHERE id = ?
            ) AND is_active = 1
        """, (user_id,))
    
    result = cursor.fetchone()
    return result[0] if result else 0