import { useState, useCallback } from 'react';
import axios from 'axios';

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const sessionId = 'session_' + Math.random().toString(36).slice(2, 8);

  const sendMessage = useCallback(async (text, mode = 'normal') => {
    const userMsg = { role: 'user', content: text, id: Date.now() };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await axios.post('/api/chat', { message: text, sessionId, mode });
      const aiMsg = { role: 'assistant', content: res.data.reply, id: Date.now() + 1 };
      setMessages(prev => [...prev, aiMsg]);
      return res.data.reply;
    } catch (err) {
      const errMsg = { role: 'assistant', content: 'Something went wrong. Check server logs.', id: Date.now() + 1 };
      setMessages(prev => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  return { messages, loading, sendMessage };
}
