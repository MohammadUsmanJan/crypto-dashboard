import React, { useState } from 'react';
import API from '../services/api';

export default function ChatAssistant({ onShowTrend }) {
  const [text, setText] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!text.trim()) return;

    const q = text.trim();
    setMessages((m) => [...m, { from: 'user', text: q }]);
    setText('');
    setLoading(true);

    try {
        const res = await API.get('/qa/', { params: { q: q } });
        const data = res.data;

      // Handle responses based on backend format
      if (data.type === 'price') {
        setMessages((m) => [
          ...m,
          { from: 'bot', text: `${data.coin} price is $${data.price}` },
        ]);
      } else if (data.type === 'trend') {
        setMessages((m) => [
          ...m,
          { from: 'bot', text: `Showing ${data.days}-day trend for ${data.coin}` },
        ]);
        if (onShowTrend) onShowTrend(data.coin, data.days);
      } else {
        setMessages((m) => [
          ...m,
          { from: 'bot', text: JSON.stringify(data) },
        ]);
      }
    } catch (err) {
      console.error(err);
      setMessages((m) => [
        ...m,
        { from: 'bot', text: 'Sorry, I could not process that.' },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat">
      <h3>Chat Assistant</h3>

      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.from}`}>
            {m.text}
          </div>
        ))}
      </div>

      <div className="composer">
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Ask: price of bitcoin or show 7-day trend of ethereum"
        />
        <button onClick={send} disabled={loading}>
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
}
