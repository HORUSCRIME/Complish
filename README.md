# Compliment Generator - Social Good App

A mobile/web application that allows users to anonymously send compliments to nearby people based on geolocation, featuring gamification with kindness scores, badges, and leaderboards.

## Architecture Overview

### Tech Stack
- **Frontend**: React (Web) / React Native (Mobile)
- **Backend**: FastAPI (Python)
- **Database**: SQLite (self-hosted)
- **Authentication**: Firebase Anonymous Auth
- **Real-time**: WebSockets
- **AI Moderation**: Gemini API
- **Analytics**: Firebase Analytics

### System Components
```
React Frontend ↔ FastAPI Backend ↔ SQLite Database
     ↓              ↓                    ↓
Firebase Auth   WebSockets         Geolocation Data
     ↓              ↓                    ↓
Analytics      Real-time Notifications  Gamification
```

## Quick Start

### Backend Setup
```bash
cd backend
pip install fastapi uvicorn sqlite3 firebase-admin google-generativeai
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Environment Variables
Create `.env` files:

**Backend (.env)**:
```
GEMINI_API_KEY=your_gemini_api_key
FIREBASE_SERVICE_ACCOUNT_KEY=path/to/serviceAccountKey.json
DATABASE_URL=sqlite:///compliment_app.db
```

**Frontend (.env)**:
```
REACT_APP_FIREBASE_API_KEY=your_firebase_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your_project_id
REACT_APP_API_URL=http://localhost:8000
```

## Features

### Phase 1: Core MVP
- ✅ Anonymous Firebase authentication
- ✅ SQLite database with user/compliment tables
- ✅ Basic compliment sending/receiving
- ✅ Geolocation-based user discovery
- ✅ Real-time WebSocket notifications
- ✅ Kindness score tracking

### Phase 2: Gamification
- ✅ Badge system with achievements
- ✅ Daily streak tracking
- ✅ Local/global leaderboards
- ✅ Score multipliers and bonuses

### Phase 3: Advanced Features
- ✅ Gemini AI content moderation
- ✅ Media attachment support
- ✅ Firebase Analytics integration
- ✅ Advanced gamification mechanics

## API Endpoints

### Authentication
- `POST /api/users/register` - Register new user
- `GET /api/user/profile` - Get user profile

### Compliments
- `POST /api/compliments/send` - Send compliment
- `GET /api/compliments/recent` - Get recent compliments

### Gamification
- `GET /api/leaderboard/{type}` - Get leaderboards
- `GET /api/badges` - Get available badges

### Real-time
- `WebSocket /ws/{user_id}` - Real-time notifications

## Database Schema

### Core Tables
- **users**: User profiles and scores
- **compliments**: Sent/received messages
- **user_locations**: Geolocation data
- **badges**: Achievement definitions
- **user_badges**: Earned achievements

## Gamification System

### Scoring Algorithm
```python
SEND_COMPLIMENT = 5 points
RECEIVE_COMPLIMENT = 3 points
DAILY_STREAK_BONUS = 2 points per day
BADGE_EARNED_BONUS = 15 points
STREAK_MULTIPLIER = 1.1x per day (max 2x)
```

### Badge Categories
- **Starter**: First compliment, first week
- **Progress**: 10, 50, 100 compliments
- **Achievement**: Score milestones, streaks
- **Special**: Local leader, community contributor

## Security Features

### AI Content Moderation
- Gemini API integration for advanced filtering
- Fallback local word filtering
- Pattern detection (URLs, emails, phone numbers)
- Sentiment analysis for quality scoring

### Data Protection
- Anonymous authentication only
- No personal information storage
- Geolocation data anonymization
- Content moderation before storage

## Deployment

### Self-Hosted Setup
1. **Backend**: Deploy FastAPI with Uvicorn
2. **Database**: SQLite file on server
3. **Frontend**: Build and serve static files
4. **WebSockets**: Configure reverse proxy for WS support

### Production Considerations
- Use PostgreSQL for better concurrent access
- Implement Redis for WebSocket scaling
- Add rate limiting and DDoS protection
- Set up automated backups
- Configure SSL/TLS certificates

## Development Roadmap

### Immediate (Week 1-2)
- Complete core MVP features
- Basic UI/UX implementation
- WebSocket real-time system

### Short-term (Week 3-4)
- Advanced gamification
- AI moderation integration
- Media attachment support

### Long-term (Month 2+)
- Mobile app (React Native)
- Advanced analytics dashboard
- Community features (groups, events)
- Internationalization support

## Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Submit pull request

## License

MIT License - See LICENSE file for details