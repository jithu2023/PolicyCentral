import React from 'react';

function LoadingSpinner() {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '40px'
    }}>
      <div className="loading-spinner"></div>
      <span style={{ marginLeft: '12px', color: 'var(--gray)' }}>Loading...</span>
    </div>
  );
}

export default LoadingSpinner;