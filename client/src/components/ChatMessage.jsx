import React from 'react';

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user';
  return (
    <div style={{
      display: 'flex',
      justifyContent: isUser ? 'flex-end' : 'flex-start',
      marginBottom: '12px',
      padding: '0 16px',
    }}>
      <div style={{
        maxWidth: '72%',
        padding: '10px 14px',
        borderRadius: isUser ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
        background: isUser ? '#1e1b4b' : '#13131f',
        border: `1px solid ${isUser ? '#3730a3' : '#1e1e2e'}`,
        color: '#e2e2f0',
        fontSize: '14px',
        lineHeight: '1.6',
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-word',
      }}>
        {!isUser && (
          <span style={{ fontSize: '11px', color: '#7c6af7', fontWeight: 600, display: 'block', marginBottom: '4px' }}>
            PRAGYA
          </span>
        )}
        {message.content}
      </div>
    </div>
  );
}
