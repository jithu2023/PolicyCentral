import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

function AdminPanel() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // Edit state
  const [editingPolicy, setEditingPolicy] = useState(null);
  const [editName, setEditName] = useState('');
  const [editInsurer, setEditInsurer] = useState('');

  // ✅ FIXED: Backend validates credentials, not frontend
  const handleLogin = async (e) => {
    e.preventDefault();
    
    setLoading(true);
    
    try {
      // Try to fetch policies with provided credentials
      const response = await axios.get(`${API_URL}/admin/policies`, {
        auth: { username, password }
      });
      
      // If successful, credentials are correct
      setIsAuthenticated(true);
      setPolicies(response.data.policies || []);
      setUploadStatus('✅ Login successful');
      
    } catch (error) {
      console.error('Login failed:', error);
      alert('Invalid credentials');
      setUsername('');
      setPassword('');
    } finally {
      setLoading(false);
    }
  };

  const loadPolicies = async () => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/admin/policies`, {
        auth: { username, password }
      });
      console.log('Policies loaded:', response.data);
      setPolicies(response.data.policies || []);
    } catch (error) {
      console.error('Error loading policies:', error);
      // If auth fails, log out
      if (error.response?.status === 401) {
        setIsAuthenticated(false);
        setUploadStatus('❌ Session expired. Please login again.');
      } else {
        setUploadStatus('❌ Failed to load policies');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      alert('Please select a file');
      return;
    }

    setUploading(true);
    setUploadStatus('Uploading...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/admin/upload-policy`, formData, {
        auth: { username, password },
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.success) {
        setUploadStatus(`✅ ${response.data.message}`);
      } else {
        setUploadStatus(`⚠️ ${response.data.message || 'Upload completed'}`);
      }
      
      setFile(null);
      document.getElementById('file-input').value = '';
      
      // Reload policies list
      await loadPolicies();
      
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus(`❌ Error: ${error.response?.data?.detail || error.message}`);
      // If auth fails, log out
      if (error.response?.status === 401) {
        setIsAuthenticated(false);
      }
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (policyId) => {
    if (!confirm(`Are you sure you want to delete "${policyId}"? This cannot be undone.`)) return;

    setUploadStatus(`Deleting ${policyId}...`);
    
    try {
      const encodedId = encodeURIComponent(policyId);
      
      const response = await axios.delete(`${API_URL}/admin/policy/${encodedId}`, {
        auth: { username, password }
      });
      
      if (response.data.success) {
        setUploadStatus(`✅ ${response.data.message}`);
        await loadPolicies();
      } else {
        setUploadStatus(`⚠️ ${response.data.message}`);
      }
      
    } catch (error) {
      console.error('Delete error:', error);
      setUploadStatus(`❌ Error deleting: ${error.response?.data?.detail || error.message}`);
      if (error.response?.status === 401) {
        setIsAuthenticated(false);
      }
    }
  };

  const handleEdit = async (policy) => {
    if (!editName.trim()) {
      alert('Please enter a policy name');
      return;
    }
    
    setUploadStatus(`Updating ${policy.source}...`);
    
    try {
      const encodedId = encodeURIComponent(policy.source);
      
      const response = await axios.put(
        `${API_URL}/admin/policy/${encodedId}`,
        {
          policy_name: editName,
          insurer: editInsurer || 'Not specified'
        },
        {
          auth: { username, password }
        }
      );
      
      if (response.data.success) {
        setUploadStatus(`✅ ${response.data.message}`);
        setEditingPolicy(null);
        setEditName('');
        setEditInsurer('');
        await loadPolicies();
      } else {
        setUploadStatus(`⚠️ ${response.data.message}`);
      }
      
    } catch (error) {
      console.error('Edit error:', error);
      setUploadStatus(`❌ Error editing: ${error.response?.data?.detail || error.message}`);
      if (error.response?.status === 401) {
        setIsAuthenticated(false);
      }
    }
  };

  const startEditing = (policy) => {
    setEditingPolicy(policy.source);
    setEditName(policy.name || '');
    setEditInsurer(policy.insurer || '');
  };

  const cancelEditing = () => {
    setEditingPolicy(null);
    setEditName('');
    setEditInsurer('');
  };

  // Auto-refresh policies every 30 seconds
  useEffect(() => {
    if (isAuthenticated) {
      loadPolicies();
      const interval = setInterval(loadPolicies, 30000);
      return () => clearInterval(interval);
    }
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return (
      <div className="admin-panel">
        <div className="admin-login">
          <h2>🔐 Admin Login</h2>
          <form onSubmit={handleLogin}>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Checking...' : 'Login'}
            </button>
          </form>
          <p style={{ marginTop: '20px', fontSize: '0.9rem', color: '#718096' }}>
            Default credentials are set in backend/.env
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-panel">
      <h2>📄 Policy Knowledge Base Management</h2>
      
      <div className="upload-section">
        <h3>📤 Upload New Policy Document</h3>
        <form onSubmit={handleFileUpload}>
          <input
            id="file-input"
            type="file"
            accept=".pdf,.txt,.json"
            onChange={(e) => setFile(e.target.files[0])}
            required
          />
          <button type="submit" disabled={uploading} className="submit-btn">
            {uploading ? 'Uploading...' : 'Upload Policy'}
          </button>
        </form>
        {uploadStatus && (
          <p style={{ marginTop: '10px', padding: '10px', background: '#f0f0f0', borderRadius: '5px' }}>
            {uploadStatus}
          </p>
        )}
        <p style={{ marginTop: '10px', fontSize: '0.85rem', color: '#718096' }}>
          Supported formats: PDF, TXT, JSON
        </p>
      </div>

      <div className="policies-section">
        <h3>📚 Uploaded Policies ({policies.length})</h3>
        {loading ? (
          <p>Loading policies...</p>
        ) : policies.length === 0 ? (
          <p>No policies uploaded yet. Upload a policy document to get started.</p>
        ) : (
          <ul className="policies-list">
            {policies.map((policy, idx) => (
              <li key={idx}>
                {editingPolicy === policy.source ? (
                  <div style={{ width: '100%' }}>
                    <div style={{ marginBottom: '10px' }}>
                      <input
                        type="text"
                        value={editName}
                        onChange={(e) => setEditName(e.target.value)}
                        placeholder="Policy Name"
                        style={{
                          width: '100%',
                          padding: '8px',
                          marginBottom: '8px',
                          border: '1px solid #ccc',
                          borderRadius: '4px'
                        }}
                      />
                      <input
                        type="text"
                        value={editInsurer}
                        onChange={(e) => setEditInsurer(e.target.value)}
                        placeholder="Insurer Name"
                        style={{
                          width: '100%',
                          padding: '8px',
                          marginBottom: '8px',
                          border: '1px solid #ccc',
                          borderRadius: '4px'
                        }}
                      />
                    </div>
                    <div>
                      <button
                        onClick={() => handleEdit(policy)}
                        style={{
                          background: '#48bb78',
                          color: 'white',
                          border: 'none',
                          padding: '6px 12px',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          marginRight: '8px'
                        }}
                      >
                        💾 Save
                      </button>
                      <button
                        onClick={cancelEditing}
                        style={{
                          background: '#a0aec0',
                          color: 'white',
                          border: 'none',
                          padding: '6px 12px',
                          borderRadius: '4px',
                          cursor: 'pointer'
                        }}
                      >
                        ❌ Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div style={{ width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <strong style={{ fontSize: '1rem' }}>{policy.name || policy.source}</strong>
                      <br />
                      <small>
                        Insurer: {policy.insurer || 'Not specified'} | 
                        File: {policy.source} | 
                        Type: {policy.file_type || 'Unknown'} | 
                        Chunks: {policy.chunks || 1}
                      </small>
                    </div>
                    <div>
                      <button
                        onClick={() => startEditing(policy)}
                        style={{
                          background: '#4299e1',
                          color: 'white',
                          border: 'none',
                          padding: '6px 12px',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          marginRight: '8px'
                        }}
                      >
                        ✏️ Edit
                      </button>
                      <button
                        onClick={() => handleDelete(policy.id || policy.source)}
                        style={{
                          background: '#e53e3e',
                          color: 'white',
                          border: 'none',
                          padding: '6px 12px',
                          borderRadius: '4px',
                          cursor: 'pointer'
                        }}
                      >
                        🗑️ Delete
                      </button>
                    </div>
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="upload-section">
        <h3>ℹ️ How it works</h3>
        <p>When you upload a policy document:</p>
        <ol style={{ marginLeft: '20px', marginTop: '10px' }}>
          <li>The document is processed and split into chunks</li>
          <li>Text is converted to vector embeddings</li>
          <li>Stored in the knowledge base for RAG retrieval</li>
          <li>AI agent uses this information for recommendations</li>
          <li><strong>Delete removes the policy completely from the knowledge base</strong></li>
          <li><strong>Edit updates the policy name and insurer for all chunks</strong></li>
        </ol>
        <p style={{ marginTop: '10px', fontSize: '0.85rem', color: '#718096' }}>
          Admin credentials are stored in backend/.env file (ADMIN_USER and ADMIN_PASS)
        </p>
      </div>
    </div>
  );
}

export default AdminPanel;