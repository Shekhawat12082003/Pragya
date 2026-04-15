import React from 'react';

export default function StatusBar({ status, mode, onModeChange }) {
  const modes = ['normal', 'focus', 'conversational'];
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '8px 16px',
      borderBottom: '1px solid #1e1e2e',
      background: '#0d0d15',
      fontSize: '12px',
      color: '#6b6b8a',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
        <span style={{
          width: '6px', height: '6px', borderRadius: '50%',
          background: status === 'idle' ? '#22c55e' : status === 'listening' ? '#7c6af7' : '#f59e0b',
          display: 'inline-block',
        }} />
        {status === 'idle' ? 'Ready' : status === 'listening' ? 'Listening...' : 'Thinking...'}
      </div>
      <div style={{ display: 'flex', gap: '6px' }}>
        {modes.map(m => (
          <button key={m} onClick={() => onModeChange(m)} style={{
            padding: '2px 8px',
            borderRadius: '10px',
            border: `1px solid ${mode === m ? '#7c6af7' : '#1e1e2e'}`,
            background: mode === m ? '#1e1b4b' : 'transparent',
            color: mode === m ? '#a78bfa' : '#6b6b8a',
            cursor: 'pointer',
            fontSize: '11px',
            textTransform: 'capitalize',
          }}>
            {m}
          </button>
        ))}
      </div>
    </div>
  );
}
