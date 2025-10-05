import React, { createContext, useContext, useState, useEffect } from 'react';
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, onAuthStateChanged } from 'firebase/auth';
import { getAnalytics, logEvent } from 'firebase/analytics';
import axios from 'axios';

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const analytics = getAnalytics(app);

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [userProfile, setUserProfile] = useState(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        try {
          const token = await firebaseUser.getIdToken();
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          
          const profile = await getUserProfile(firebaseUser.uid);
          setUser(firebaseUser);
          setUserProfile(profile);
          
          logEvent(analytics, 'user_login', { method: 'anonymous' });
        } catch (error) {
          console.error('Error setting up user:', error);
        }
      } else {
        setUser(null);
        setUserProfile(null);
        delete axios.defaults.headers.common['Authorization'];
      }
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const signInAnonymous = async () => {
    try {
      setLoading(true);
      const result = await signInAnonymously(auth);
      await registerUser(result.user.uid);
      logEvent(analytics, 'sign_up', { method: 'anonymous' });
      return result.user;
    } catch (error) {
      console.error('Anonymous sign-in error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const registerUser = async (firebaseUid) => {
    try {
      const response = await axios.post('/api/users/register', {
        firebase_uid: firebaseUid,
        username: `User${Math.floor(Math.random() * 10000)}`
      });
      return response.data;
    } catch (error) {
      console.error('User registration error:', error);
      throw error;
    }
  };

  const getUserProfile = async (firebaseUid) => {
    try {
      const response = await axios.get('/api/user/profile');
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) {
        return await registerUser(firebaseUid);
      }
      throw error;
    }
  };

  const value = {
    user,
    userProfile,
    loading,
    signInAnonymous,
    analytics
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};