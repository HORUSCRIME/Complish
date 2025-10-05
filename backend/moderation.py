import google.generativeai as genai
import os
import re
from typing import bool

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

INAPPROPRIATE_WORDS = [
    "spam", "advertisement", "buy now", "click here", 
]

async def moderate_content(content: str) -> bool:
    if not content or len(content.strip()) < 2:
        return False
    
    if len(content) > 500:  
        return False
    
    if any(word.lower() in content.lower() for word in INAPPROPRIATE_WORDS):
        return False
    
    if has_excessive_repetition(content):
        return False
    
    try:
        return await gemini_moderate(content)
    except Exception as e:
        print(f"Gemini API error: {e}")
        return basic_content_filter(content)

async def gemini_moderate(content: str) -> bool:
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Analyze this message for a compliment/kindness app. 
        Message: "{content}"
        
        Check for:
        - Offensive or inappropriate language
        - Personal information (phone, email, address)
        - Spam or promotional content
        - Harassment or bullying
        - Content not suitable for a positive compliment app
        
        Respond with only "SAFE" or "UNSAFE"
        """
        
        response = model.generate_content(prompt)
        result = response.text.strip().upper()
        
        return "SAFE" in result
        
    except Exception as e:
        print(f"Gemini moderation error: {e}")
        return True  

def basic_content_filter(content: str) -> bool:
    
    content_lower = content.lower()
    
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    if re.search(url_pattern, content):
        return False
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.search(email_pattern, content):
        return False
    
    phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    if re.search(phone_pattern, content):
        return False
    
    positive_words = [
        "beautiful", "amazing", "wonderful", "great", "awesome", "fantastic",
        "lovely", "brilliant", "incredible", "outstanding", "excellent",
        "kind", "sweet", "nice", "good", "perfect", "smile", "happy",
        "joy", "love", "care", "help", "support", "encourage", "inspire"
    ]
    
    has_positive = any(word in content_lower for word in positive_words)
    
    return has_positive and len(content.split()) >= 2

def has_excessive_repetition(content: str) -> bool:
    
    if re.search(r'(.)\1{3,}', content):
        return True
    
    words = content.lower().split()
    if len(words) > 1:
        repeated_count = sum(1 for word in set(words) if words.count(word) > 2)
        if repeated_count > 0:
            return True
    
    return False

def get_content_sentiment_score(content: str) -> float:

    
    positive_words = [
        "amazing", "wonderful", "beautiful", "fantastic", "incredible",
        "outstanding", "brilliant", "excellent", "perfect", "awesome",
        "love", "adore", "cherish", "treasure", "appreciate"
    ]
    
    very_positive_words = [
        "extraordinary", "phenomenal", "magnificent", "spectacular",
        "breathtaking", "inspiring", "uplifting", "heartwarming"
    ]
    
    content_lower = content.lower()
    words = content_lower.split()
    
    score = 0.0
    for word in words:
        if word in very_positive_words:
            score += 0.3
        elif word in positive_words:
            score += 0.2
    
    return min(score / max(len(words), 1), 1.0)