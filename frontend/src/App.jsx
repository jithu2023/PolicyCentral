import React, { useState } from 'react';
import ProfileForm from './components/ProfileForm';
import Recommendation from './components/Recommendation';
import ChatBox from './components/ChatBox';
import AdminPanel from './components/AdminPanel';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('user');
  const [recommendation, setRecommendation] = useState(null);
  const [sessionId, setSessionId] = useState(() => {
    return localStorage.getItem('sessionId') || `user_${Date.now()}`;
  });
  const [userProfile, setUserProfile] = useState(null);

  const handleRecommendation = (recData, profile) => {
    setRecommendation(recData);
    setUserProfile(profile);
    localStorage.setItem('sessionId', sessionId);
  };

  const handleReset = () => {
    setRecommendation(null);
    setUserProfile(null);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🛡️ AarogyaAid</h1>
        <p>Your empathetic health insurance advisor</p>
        <div className="tabs">
          <button 
            className={activeTab === 'user' ? 'active' : ''} 
            onClick={() => setActiveTab('user')}
          >
            👤 Find Insurance
          </button>
          <button 
            className={activeTab === 'admin' ? 'active' : ''} 
            onClick={() => setActiveTab('admin')}
          >
            🔧 Admin Panel
          </button>
        </div>
      </header>

      <main className="main">
        {activeTab === 'user' ? (
          <>
            {!recommendation ? (
              <ProfileForm onRecommendation={handleRecommendation} sessionId={sessionId} />
            ) : (
              <>
                <button 
                  onClick={handleReset}
                  style={{ marginBottom: '20px', padding: '8px 16px', background: '#e2e8f0', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
                >
                  ← Start Over
                </button>
                <div className="result-container">
                  <Recommendation recommendation={recommendation} />
                  <ChatBox sessionId={sessionId} userProfile={userProfile} />
                </div>
              </>
            )}
          </>
        ) : (
          <AdminPanel />
        )}
      </main>
    </div>
  );
}

export default App;