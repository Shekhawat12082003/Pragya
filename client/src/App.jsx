import React, { useEffect, useRef, useState } from 'react';
import Orb from './components/Orb';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import StatusBar from './components/StatusBar';
import { useChat } from './hooks/useChat';
import { useVoice } from './hooks/useVoice';

export default function App() {
  const [mode, setMode] = useState('normal');
  const { messages, loading, sendMessage } = useChat();
  const messagesEndRef = useRef(null);

  const orbState = loading ? 'thinking' : 'idle';

  async function handleSend(text) {
    await sendMessage(text, mode);
  }

  const { listening, startListening, stopListening } = useVoice({
    onResult: (transcript) => handleSend(transcript),
  });

  function handleVoiceToggle() {
    listening ? stopListening() : startListening();
  }

  const status = loading ? 'thinking' : listening ? 'listening' : 'idle';

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', background: '#0a0a0f' }}>
      {/* Header */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: '14px',
        padding: '16px 20px',
        borderBottom: '1px solid #1e1e2e',
        background: '#0d0d15',
      }}>
        <Orb state={listening ? 'listening' : orbState} />
        <div>
          <div style={{ fontSize: '20px', fontWeight: 600, color: '#e2e2f0', letterSpacing: '0.5px' }}>
            Pragya
          </div>
          <div style={{ fontSize: '12px', color: '#6b6b8a' }}>
            Your personal AI assistant
          </div>
        </div>
      </div>

      <StatusBar status={status} mode={mode} onModeChange={setMode} />

      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', paddingTop: '16px' }}>
        {messages.length === 0 && (
          <div style={{
            display: 'flex', flexDirection: 'column', alignItems: 'center',
            justifyContent: 'center', height: '100%', color: '#6b6b8a', gap: '8px',
          }}>
            <div style={{ fontSize: '32px' }}>🔮</div>
            <div style={{ fontSize: '14px' }}>Say "Pragya" or type to begin</div>
          </div>
        )}
        {messages.map(msg => <ChatMessage key={msg.id} message={msg} />)}
        {loading && (
          <div style={{ padding: '0 16px 12px', color: '#6b6b8a', fontSize: '13px' }}>
            <span style={{ animation: 'blink 1s infinite' }}>Pragya is thinking...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <ChatInput
        onSend={handleSend}
        onVoice={handleVoiceToggle}
        listening={listening}
        disabled={loading}
      />

      <style>{`
        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      `}</style>
    </div>
  );
}
