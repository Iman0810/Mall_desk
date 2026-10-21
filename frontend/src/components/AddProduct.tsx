import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/client';

export default function AddProduct({ storeId, role }: { storeId: number, role: string }) {
  const [isOpen, setIsOpen] = useState(false);
  const [name, setName] = useState('');
  const [sku, setSku] = useState('');
  const [price, setPrice] = useState('');
  const [stock, setStock] = useState('');
  const [costPrice, setCostPrice] = useState('');
  const [error, setError] = useState('');

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (newProduct: any) => {
      return api.post(`/stores/${storeId}/products/`, newProduct);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products', storeId] });
      setIsOpen(false);
      setName(''); setSku(''); setPrice(''); setStock(''); setCostPrice(''); setError('');
    },
    onError: (err: any) => {
      setError(err.response?.data?.error || JSON.stringify(err.response?.data));
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const payload: any = { name, sku, price: parseFloat(price), stock: parseInt(stock) };
    
    // Only include cost_price if the user is an Admin
    if (role === 'ADMIN' && costPrice) {
      payload.cost_price = parseFloat(costPrice);
    }
    
    mutation.mutate(payload);
  };

  if (!isOpen) {
    return (
      <button onClick={() => setIsOpen(true)} className="mb-4 bg-green-600 text-white px-4 py-2 rounded font-bold hover:bg-green-700">
        + Add New Product
      </button>
    );
  }

  return (
    <div className="mb-6 bg-gray-100 dark:bg-gray-800 p-4 rounded border dark:border-gray-700">
      <h4 className="font-bold mb-3 text-gray-800 dark:text-gray-200">Add Product to Branch</h4>
      {error && <div className="text-red-500 text-sm mb-2">{error}</div>}
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-3">
        <input required placeholder="Product Name" value={name} onChange={e => setName(e.target.value)} className="p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white" />
        <input required placeholder="SKU" value={sku} onChange={e => setSku(e.target.value)} className="p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white" />
        <input required type="number" step="0.01" placeholder="Retail Price ($)" value={price} onChange={e => setPrice(e.target.value)} className="p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white" />
        <input required type="number" placeholder="Initial Stock" value={stock} onChange={e => setStock(e.target.value)} className="p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white" />
        
        {/* Only show Cost Price to Admins */}
        {role === 'ADMIN' && (
          <input type="number" step="0.01" placeholder="Cost Price ($) (Admin Only)" value={costPrice} onChange={e => setCostPrice(e.target.value)} className="p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white" />
        )}
        
        <div className="col-span-2 flex gap-2 mt-2">
          <button type="submit" disabled={mutation.isPending} className="bg-blue-600 text-white px-4 py-2 rounded font-bold hover:bg-blue-700">
            {mutation.isPending ? 'Saving...' : 'Save Product'}
          </button>
          <button type="button" onClick={() => setIsOpen(false)} className="bg-gray-400 text-white px-4 py-2 rounded font-bold hover:bg-gray-500">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}