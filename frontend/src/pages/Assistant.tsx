import { useState } from 'react';
import { api } from '../api/client';

export default function Assistant({ storeId }: { storeId: number }) {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState<{ role: 'user' | 'ai', text: string }[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    setChat(prev => [...prev, { role: 'user', text: message }]);
    setMessage('');
    setLoading(true);

    try {
      const res = await api.post(`/stores/${storeId}/assistant/`, { message });
      setChat(prev => [...prev, { role: 'ai', text: res.data.reply }]);
    } catch (err) {
      setChat(prev => [...prev, { role: 'ai', text: "Error connecting to assistant." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3 className="text-lg font-bold mb-4">Store AI Assistant</h3>
      <div className="h-64 overflow-y-auto border p-4 mb-4 bg-gray-50 rounded">
        {chat.length === 0 && <p className="text-gray-400 text-center mt-10">Ask me about products or stock!</p>}
        {chat.map((c, i) => (
          <div key={i} className={`mb-2 ${c.role === 'user' ? 'text-right' : 'text-left'}`}>
            <span className={`inline-block p-2 rounded ${c.role === 'user' ? 'bg-blue-100' : 'bg-gray-200'}`}>
              {c.text}
            </span>
          </div>
        ))}
        {loading && <div className="text-gray-400 text-sm">Assistant is typing...</div>}
      </div>
      <form onSubmit={sendMessage} className="flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="flex-1 border p-2 rounded"
          placeholder="Ask a question..."
        />
        <button type="submit" disabled={loading} className="bg-green-600 text-white px-4 py-2 rounded">
          Send
        </button>
      </form>
    </div>
  );
}