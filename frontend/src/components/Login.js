import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Heart, Sparkles } from 'lucide-react';

const Login = () => {
  const { signInAnonymous, loading } = useAuth();
  const [isSigningIn, setIsSigningIn] = useState(false);

  const handleAnonymousSignIn = async () => {
    try {
      setIsSigningIn(true);
      await signInAnonymous();
    } catch (error) {
      console.error('Sign in failed:', error);
    } finally {
      setIsSigningIn(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-content">
        <div className="login-header">
          <div className="app-logo">
            <Heart className="logo-icon" />
            <Sparkles className="sparkle-icon" />
          </div>
          <h1>Compliment Generator</h1>
          <p className="app-tagline">Spread kindness in your community</p>
        </div>

        <div className="login-features">
          <div className="feature">
            <Heart size={24} />
            <span>Send anonymous compliments to nearby people</span>
          </div>
          <div className="feature">
            <Sparkles size={24} />
            <span>Earn kindness points and badges</span>
          </div>
          <div className="feature">
            <Heart size={24} />
            <span>Build positive communities</span>
          </div>
        </div>

        <div className="login-actions">
          <button 
            className="anonymous-login-btn"
            onClick={handleAnonymousSignIn}
            disabled={loading || isSigningIn}
          >
            {isSigningIn ? 'Getting Started...' : 'Start Spreading Kindness'}
          </button>
          
          <p className="privacy-note">
            Anonymous login - no personal information required
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;