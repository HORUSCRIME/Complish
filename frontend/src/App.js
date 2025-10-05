import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [compliment, setCompliment] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ sent: 0, received: 0, score: 0 });

  useEffect(() => {
    createParticles();
  }, []);

  const createParticles = () => {
    const particleCount = 20;
    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = `${Math.random() * 100}%`;
      particle.style.animationDelay = `${Math.random() * 20}s`;
      particle.style.animationDuration = `${15 + Math.random() * 10}s`;
      document.querySelector('.app').appendChild(particle);
    }
  };

  const showMessage = (text, type) => {
    setMessage(text);
    setMessageType(type);
    setTimeout(() => setMessage(''), 4000);
  };

  const sendCompliment = async () => {
    if (!compliment.trim()) {
      showMessage('✨ Please write a compliment first!', 'error');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/compliments/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: compliment,
          lat: 40.7128,
          lng: -74.0060
        })
      });
      
      const result = await response.json();
      
      if (response.ok) {
        showMessage('🎉 Compliment sent successfully!', 'success');
        setCompliment('');
        setStats(prev => ({ 
          ...prev, 
          sent: prev.sent + 1, 
          score: prev.score + 5 
        }));
        createSparkles();
      } else {
        showMessage('❌ Failed to send compliment', 'error');
      }
    } catch (error) {
      showMessage('⚠️ Network error. Please try again.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const createSparkles = () => {
    const container = document.querySelector('.container');
    for (let i = 0; i < 10; i++) {
      const sparkle = document.createElement('div');
      sparkle.className = 'sparkle';
      sparkle.style.left = `${Math.random() * 100}%`;
      sparkle.style.top = `${Math.random() * 100}%`;
      sparkle.style.animationDelay = `${Math.random() * 0.5}s`;
      container.appendChild(sparkle);
      setTimeout(() => sparkle.remove(), 1000);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      sendCompliment();
    }
  };

  return (
    <div className="app">
      <div className="container">
        <div className="header">
          <div className="logo">💝</div>
          <h1 className="title">Compliment Generator</h1>
          <p className="subtitle">Spread kindness across the world</p>
        </div>

        <div className="form">
          <div className="input-group">
            <textarea
              className="textarea"
              value={compliment}
              onChange={(e) => setCompliment(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Write something beautiful and uplifting..."
              maxLength={280}
            />
            <div className="char-count">{compliment.length}/280</div>
          </div>

          <button 
            className="send-button"
            onClick={sendCompliment}
            disabled={loading || !compliment.trim()}
          >
            {loading ? '✨ Sending Magic...' : '💫 Send Kindness'}
          </button>

          {message && (
            <div className={`message ${messageType}`}>
              {message}
            </div>
          )}
        </div>

        <div className="stats">
          <div className="stat">
            <span className="stat-number">{stats.sent}</span>
            <span className="stat-label">Sent</span>
          </div>
          <div className="stat">
            <span className="stat-number">{stats.received}</span>
            <span className="stat-label">Received</span>
          </div>
          <div className="stat">
            <span className="stat-number">{stats.score}</span>
            <span className="stat-label">Kindness</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;