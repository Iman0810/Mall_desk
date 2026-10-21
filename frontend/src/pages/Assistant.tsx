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
    <div className="mt-4 flex flex-col h-[400px]">
      <div className="flex-1 overflow-y-auto border dark:border-gray-700 p-4 mb-4 bg-gray-50 dark:bg-gray-900 rounded">
        {chat.length === 0 && <p className="text-gray-400 dark:text-gray-500 text-center mt-10">Ask me about products or stock!</p>}
        {chat.map((c, i) => (
          <div key={i} className={`mb-3 flex ${c.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <span className={`inline-block px-4 py-2 rounded-lg max-w-[80%] ${
              c.role === 'user' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100'
            }`}>
              {c.text}
            </span>
          </div>
        ))}
        {loading && <div className="text-gray-400 dark:text-gray-500 text-sm animate-pulse">Assistant is typing...</div>}
      </div>
      <form onSubmit={sendMessage} className="flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="flex-1 border dark:border-gray-600 p-3 rounded bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Ask a question..."
        />
        <button type="submit" disabled={loading} className="bg-green-600 text-white px-6 py-3 rounded font-bold hover:bg-green-700 disabled:opacity-50">
          Send
        </button>
      </form>
    </div>
  );
}