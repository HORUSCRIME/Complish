import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Heart, Send, Trophy, Zap } from 'lucide-react';

const Dashboard = () => {
  const { userProfile } = useAuth();
  const [nearbyUsers, setNearbyUsers] = useState(12);

  return (
    <div className="dashboard">
      <div className="welcome-section">
        <h1>Welcome back, {userProfile?.username}!</h1>
        <p>Spread kindness in your community</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <Heart className="icon" />
          </div>
          <div className="stat-content">
            <h3>{userProfile?.kindness_score || 0}</h3>
            <p>Kindness Score</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Send className="icon" />
          </div>
          <div className="stat-content">
            <h3>{userProfile?.total_sent || 0}</h3>
            <p>Compliments Sent</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Trophy className="icon" />
          </div>
          <div className="stat-content">
            <h3>{userProfile?.total_received || 0}</h3>
            <p>Compliments Received</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Zap className="icon" />
          </div>
          <div className="stat-content">
            <h3>{userProfile?.current_streak || 0}</h3>
            <p>Day Streak</p>
          </div>
        </div>
      </div>

      <div className="dashboard-sections">
        <div className="section">
          <h2>Community</h2>
          <div className="community-stats">
            <div className="community-item">
              <span className="community-number">{nearbyUsers}</span>
              <span className="community-label">People nearby</span>
            </div>
            <button className="cta-button" onClick={() => window.location.href = '/send'}>
              Send a Compliment
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;