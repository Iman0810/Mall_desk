import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import Assistant from './Assistant';
import Products from './Products';
import StoreUsers from './StoreUsers';

export default function Dashboard() {
  const { logout } = useAuth();
  const [activeStoreId, setActiveStoreId] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<'products' | 'users' | 'assistant'>('products');

  const { data: stores, isLoading } = useQuery({
    queryKey: ['stores'],
    queryFn: async () => (await api.get('/stores/')).data,
  });

  if (isLoading) return <div className="p-8 text-center text-xl">Loading stores...</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white p-4 shadow flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-600">MallDesk</h1>
        <button onClick={logout} className="text-red-500 font-bold hover:underline">Logout</button>
      </nav>

      <div className="max-w-4xl mx-auto p-6">
        <h2 className="text-2xl font-bold mb-4">Select a Store</h2>
        <div className="flex gap-4 mb-8">
          {stores?.map((store: any) => (
            <button
              key={store.id}
              onClick={() => setActiveStoreId(store.id)}
              className={`p-4 rounded border font-bold ${activeStoreId === store.id ? 'bg-blue-600 text-white border-blue-600' : 'bg-white hover:bg-gray-100'}`}
            >
              {store.name} ({store.role})
            </button>
          ))}
        </div>

        {activeStoreId ? (
          <div className="bg-white p-6 rounded shadow-md border">
            
            {/* Tabs */}
            <div className="flex gap-4 border-b mb-6 pb-2">
              <button onClick={() => setActiveTab('products')} className={`font-bold pb-2 ${activeTab === 'products' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}>Products</button>
              <button onClick={() => setActiveTab('users')} className={`font-bold pb-2 ${activeTab === 'users' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}>Users</button>
              <button onClick={() => setActiveTab('assistant')} className={`font-bold pb-2 ${activeTab === 'assistant' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}>AI Assistant</button>
            </div>

            {/* Content */}
            {activeTab === 'products' && <Products storeId={activeStoreId} />}
            {activeTab === 'users' && <StoreUsers storeId={activeStoreId} />}
            {activeTab === 'assistant' && <Assistant storeId={activeStoreId} />}
            
          </div>
        ) : (
          <p className="text-gray-500 text-center mt-10">Please select a store to continue.</p>
        )}
      </div>
    </div>
  );
}