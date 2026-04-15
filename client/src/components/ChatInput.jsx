import React, { useState, useRef } from 'react';

export default function ChatInput({ onSend, onVoice, listening, disabled }) {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  function submit() {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText('');
  }

  return (
    <div style={{
      display: 'flex',
      alignItems: 'flex-end',
      gap: '10px',
      padding: '12px 16px',
      borderTop: '1px solid #1e1e2e',
      background: '#0a0a0f',
    }}>
      <textarea
        ref={textareaRef}
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask Pragya anything..."
        rows={1}
        disabled={disabled}
        style={{
          flex: 1,
          background: '#12121a',
          border: '1px solid #1e1e2e',
          borderRadius: '12px',
          color: '#e2e2f0',
          padding: '10px 14px',
          fontSize: '14px',
          resize: 'none',
          outline: 'none',
          fontFamily: 'Inter, sans-serif',
          lineHeight: '1.5',
          maxHeight: '120px',
          overflowY: 'auto',
        }}
      />
      <button
        onClick={onVoice}
        title={listening ? 'Stop listening' : 'Voice input'}
        style={{
          width: '40px', height: '40px',
          borderRadius: '50%',
          border: `1px solid ${listening ? '#7c6af7' : '#1e1e2e'}`,
          background: listening ? '#1e1b4b' : '#12121a',
          color: listening ? '#a78bfa' : '#6b6b8a',
          cursor: 'pointer',
          fontSize: '18px',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0,
          transition: 'all 0.2s',
        }}
      >
        🎙
      </button>
      <button
        onClick={submit}
        disabled={!text.trim() || disabled}
        style={{
          width: '40px', height: '40px',
          borderRadius: '50%',
          border: 'none',
          background: text.trim() && !disabled ? '#7c6af7' : '#1e1e2e',
          color: '#fff',
          cursor: text.trim() && !disabled ? 'pointer' : 'default',
          fontSize: '16px',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0,
          transition: 'background 0.2s',
        }}
      >
        ↑
      </button>
    </div>
  );
}
