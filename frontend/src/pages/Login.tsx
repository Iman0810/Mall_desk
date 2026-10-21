import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import ThemeToggle from '../components/ThemeToggle';

export default function Login() {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('password123');
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.post('/login/', { username, password });
      login(res.data.token);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Login failed');
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-gray-100 dark:bg-gray-900 transition-colors duration-300 relative">
      <div className="absolute top-6 right-6">
        <ThemeToggle />
      </div>
      
      <form onSubmit={handleLogin} className="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-2xl w-96 border dark:border-gray-700">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-extrabold text-blue-600 dark:text-blue-400">MallDesk</h2>
          <p className="text-gray-500 dark:text-gray-400 mt-2 text-sm">Retail Management Portal</p>
        </div>
        
        {error && <div className="bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 p-3 rounded mb-4 text-sm text-center">{error}</div>}
        
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full p-3 border dark:border-gray-600 rounded bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-3 border dark:border-gray-600 rounded bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <button type="submit" className="w-full bg-blue-600 text-white mt-6 p-3 rounded font-bold hover:bg-blue-700 transition-colors">
          Sign In
        </button>
      </form>
    </div>
  );
}