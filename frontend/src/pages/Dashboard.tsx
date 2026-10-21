import { useState, useEffect } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import Assistant from './Assistant';
import Products from './Products';
import StoreUsers from './StoreUsers';
import ThemeToggle from '../components/ThemeToggle';

export default function Dashboard() {
  const { logout } = useAuth();
  const queryClient = useQueryClient();
  const [activeStoreId, setActiveStoreId] = useState<number | null>(null);
  const [activeRole, setActiveRole] = useState<string>(''); // <-- Added to track role
  const [activeTab, setActiveTab] = useState<'products' | 'users' | 'assistant'>('products');

  const { data: stores, isLoading, isError } = useQuery({
    queryKey: ['stores'],
    queryFn: async () => (await api.get('/stores/')).data,
  });

  useEffect(() => {
    if (isError) {
      queryClient.clear();
      logout();
    }
  }, [isError, logout, queryClient]);

  if (isLoading) return <div className="p-8 text-center text-xl dark:text-white dark:bg-gray-900 min-h-screen">Loading stores...</div>;
  if (isError) return <div className="p-8 text-center text-red-500 min-h-screen dark:bg-gray-900">Session expired. Redirecting...</div>;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      <nav className="bg-white dark:bg-gray-800 p-4 shadow flex justify-between items-center transition-colors duration-300">
        <h1 className="text-xl font-bold text-blue-600 dark:text-blue-400">MallDesk</h1>
        <div className="flex items-center gap-4">
          <ThemeToggle />
          <button onClick={logout} className="text-red-500 font-bold hover:underline">Logout</button>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto p-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-100">Select a Branch</h2>
        <div className="flex gap-4 mb-8">
          {stores?.map((store: any) => (
            <button
              key={store.id}
              onClick={() => {
                setActiveStoreId(store.id);
                setActiveRole(store.role); // <-- Set the role
                setActiveTab('products');  
              }}
              className={`p-4 rounded border font-bold transition-all ${
                activeStoreId === store.id 
                  ? 'bg-blue-600 text-white border-blue-600 shadow-lg scale-105' 
                  : 'bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              {store.name} ({store.role})
            </button>
          ))}
        </div>

        {activeStoreId ? (
          <div className="bg-white dark:bg-gray-800 p-6 rounded shadow-md border dark:border-gray-700 transition-colors duration-300">
            
            {/* Tabs */}
            <div className="flex gap-4 border-b dark:border-gray-700 mb-6 pb-2">
              {['products', 'users', 'assistant'].map((tab) => (
                <button 
                  key={tab}
                  onClick={() => setActiveTab(tab as any)} 
                  className={`font-bold pb-2 capitalize transition-colors ${
                    activeTab === tab 
                      ? 'border-b-2 border-blue-600 text-blue-600 dark:text-blue-400 dark:border-blue-400' 
                      : 'text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
                  }`}
                >
                  {tab === 'assistant' ? 'AI Assistant' : tab}
                </button>
              ))}
            </div>

            {/* Content */}
            {activeTab === 'products' && <Products storeId={activeStoreId} role={activeRole} />}
            {activeTab === 'users' && <StoreUsers storeId={activeStoreId} role={activeRole} />}
            {activeTab === 'assistant' && <Assistant storeId={activeStoreId} />}
            
          </div>
        ) : (
          <p className="text-gray-500 dark:text-gray-400 text-center mt-10">Please select a branch to continue.</p>
        )}
      </div>
    </div>
  );
}