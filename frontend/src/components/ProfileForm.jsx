import React, { useState } from 'react';
import axios from 'axios';
import LoadingSpinner from './LoadingSpinner';

const API_URL = 'http://localhost:8000';

function ProfileForm({ onRecommendation, sessionId }) {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    lifestyle: '',
    conditions: [],
    income: '',
    city: ''
  });
  const [loading, setLoading] = useState(false);

  const conditionsList = ['Diabetes', 'Hypertension', 'Asthma', 'Cardiac', 'None', 'Other'];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleConditionChange = (condition) => {
    setFormData(prev => {
      const newConditions = prev.conditions.includes(condition)
        ? prev.conditions.filter(c => c !== condition)
        : [...prev.conditions, condition];
      return { ...prev, conditions: newConditions };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const required = ['name', 'age', 'lifestyle', 'income', 'city'];
    for (let field of required) {
      if (!formData[field]) {
        alert(`Please fill ${field}`);
        return;
      }
    }
    
    setLoading(true);
    
    try {
      const response = await axios.post(`${API_URL}/chat/submit-profile`, {
        session_id: sessionId,
        profile: formData
      });
      
      onRecommendation(response.data.recommendation, formData);
    } catch (error) {
      console.error('Error:', error);
      alert('Error getting recommendation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="profile-form-container">
      <h2>Tell us about yourself</h2>
      <p className="subtitle">We'll find the perfect insurance plan for your needs</p>
      
      <form onSubmit={handleSubmit} className="profile-form">
        <div className="form-group">
          <label>Full Name *</label>
          <input type="text" name="name" value={formData.name} onChange={handleChange} required />
        </div>

        <div className="form-group">
          <label>Age *</label>
          <input type="number" name="age" value={formData.age} onChange={handleChange} min="1" max="99" required />
        </div>

        <div className="form-group">
          <label>Lifestyle *</label>
          <select name="lifestyle" value={formData.lifestyle} onChange={handleChange} required>
            <option value="">Select lifestyle</option>
            <option value="Sedentary">Sedentary</option>
            <option value="Moderate">Moderate</option>
            <option value="Active">Active</option>
            <option value="Athlete">Athlete</option>
          </select>
        </div>

        <div className="form-group">
          <label>Pre-existing Conditions</label>
          <div className="checkbox-group">
            {conditionsList.map(condition => (
              <label key={condition} className="checkbox-label">
                <input type="checkbox" checked={formData.conditions.includes(condition)} onChange={() => handleConditionChange(condition)} />
                {condition}
              </label>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Annual Income *</label>
          <select name="income" value={formData.income} onChange={handleChange} required>
            <option value="">Select income range</option>
            <option value="under 3L">Under ₹3 Lakhs</option>
            <option value="3-8L">₹3 - 8 Lakhs</option>
            <option value="8-15L">₹8 - 15 Lakhs</option>
            <option value="15L+">₹15 Lakhs+</option>
          </select>
        </div>

        <div className="form-group">
          <label>City / Tier *</label>
          <select name="city" value={formData.city} onChange={handleChange} required>
            <option value="">Select city type</option>
            <option value="Metro">Metro City</option>
            <option value="Tier-2">Tier-2 City</option>
            <option value="Tier-3">Tier-3 City</option>
          </select>
        </div>

        <button type="submit" disabled={loading} className="submit-btn">
  {loading ? (
    <>
      <div className="loading-spinner" style={{ marginRight: '8px' }}></div>
      Finding best policy...
    </>
  ) : (
    'Get Recommendation →'
  )}
</button>
      </form>
    </div>
  );
}

export default ProfileForm;