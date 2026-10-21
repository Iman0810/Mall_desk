import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/client';

export default function EditProduct({ product, storeId, role }: { product: any, storeId: number, role: string }) {
  const [isOpen, setIsOpen] = useState(false);
  const [name, setName] = useState(product.name);
  const [price, setPrice] = useState(product.price);
  const [stock, setStock] = useState(product.stock);
  const [costPrice, setCostPrice] = useState(product.cost_price || '');
  const [error, setError] = useState('');

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (updatedProduct: any) => {
      return api.patch(`/stores/${storeId}/products/${product.id}/`, updatedProduct);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products', storeId] });
      setIsOpen(false);
      setError('');
    },
    onError: (err: any) => {
      setError(err.response?.data?.error || JSON.stringify(err.response?.data));
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const payload: any = { 
      name, 
      price: parseFloat(price), 
      stock: parseInt(stock) 
    };
    
    if (role === 'ADMIN' && costPrice) {
      payload.cost_price = parseFloat(costPrice);
    }
    
    mutation.mutate(payload);
  };

  if (!isOpen) {
    return (
      <button 
        onClick={() => setIsOpen(true)}
        className="mt-2 w-full text-xs bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 py-1 rounded hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      >
        Edit
      </button>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl w-96">
        <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Edit {product.name}</h3>
        {error && <div className="text-red-500 text-sm mb-2">{error}</div>}
        
        <form onSubmit={handleSubmit} className="space-y-3">
          <input required value={name} onChange={e => setName(e.target.value)} className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="Name" />
          <input required type="number" step="0.01" value={price} onChange={e => setPrice(e.target.value)} className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="Price" />
          <input required type="number" value={stock} onChange={e => setStock(e.target.value)} className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="Stock" />
          
          {role === 'ADMIN' && (
            <input type="number" step="0.01" value={costPrice} onChange={e => setCostPrice(e.target.value)} className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="Cost Price" />
          )}
          
          <div className="flex gap-2 pt-2">
            <button type="submit" disabled={mutation.isPending} className="flex-1 bg-blue-600 text-white py-2 rounded font-bold hover:bg-blue-700">
              {mutation.isPending ? 'Saving...' : 'Save'}
            </button>
            <button type="button" onClick={() => setIsOpen(false)} className="flex-1 bg-gray-400 text-white py-2 rounded font-bold hover:bg-gray-500">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}