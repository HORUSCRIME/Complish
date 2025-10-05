# Setup Guide

## Quick Start (No Credentials Needed)

The app works **without any API keys** for basic functionality:

```bash
# 1. Start Backend
cd compliment_app
python run_backend.py

# 2. Start Frontend (new terminal)
cd compliment_app/frontend
npm install
npm start
```

Visit: http://localhost:3000

---

## Optional: Add Firebase & Gemini (Advanced Features)

### 1. Firebase Setup (Optional - for Auth & Analytics)

**Get Firebase Credentials:**
1. Go to https://console.firebase.google.com
2. Create a new project
3. Go to Project Settings > General
4. Scroll to "Your apps" > Add web app
5. Copy the config values

**Frontend Setup:**
```bash
cd frontend
cp .env.example .env
# Edit .env with your Firebase values
```

**Backend Setup (Service Account):**
1. Firebase Console > Project Settings > Service Accounts
2. Click "Generate new private key"
3. Save as `serviceAccountKey.json` in backend folder

---

### 2. Gemini API Setup (Optional - for AI Moderation)

**Get Gemini API Key:**
1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Copy the key

**Backend Setup:**
```bash
cd backend
cp .env.example .env
# Add: GEMINI_API_KEY=your_key_here
```

---

## What Works Without Credentials?

✅ Send/receive compliments
✅ Kindness score tracking
✅ Local database storage
✅ Real-time updates
✅ All UI features

## What Needs Credentials?

❌ Firebase Authentication (uses mock auth)
❌ Firebase Analytics (disabled)
❌ AI Content Moderation (uses basic filtering)

---

## Troubleshooting

**Backend won't start:**
- Make sure Python 3.8+ is installed
- Run: `pip install -r backend/requirements.txt`

**Frontend won't start:**
- Make sure Node.js 16+ is installed
- Delete `node_modules` and run `npm install` again

**Database errors:**
- Delete `compliment_app.db` and restart backend