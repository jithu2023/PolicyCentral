import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

function ChatBox({ sessionId, userProfile }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Add welcome message
    setMessages([
      {
        type: 'bot',
        content: `Hello ${userProfile?.name || 'there'}! 👋\n\nI'm your insurance explainer. Ask me anything about your policy, insurance terms, or how coverage works for your specific health conditions.\n\nFor example:\n• "What is a waiting period?"\n• "How does co-pay work?"\n• "Are my diabetes treatments covered?"`
      }
    ]);
  }, [userProfile]);

  useEffect(() => {
    // Scroll to bottom when messages update
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setMessages(prev => [...prev, { type: 'user', content: userMessage }]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat/ask`, {
        session_id: sessionId,
        message: userMessage
      });

      const botMessage = response.data.answer;
      setMessages(prev => [...prev, { type: 'bot', content: botMessage }]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, { 
        type: 'bot', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <h3>💬 Ask about your policy</h3>
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.type}`}>
            <div>{msg.content}</div>
          </div>
        ))}
        {loading && (
  <div className="message bot">
    <div className="typing-indicator">
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>
)}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={sendMessage} className="chat-input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about waiting periods, co-pay, coverage..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatBox;