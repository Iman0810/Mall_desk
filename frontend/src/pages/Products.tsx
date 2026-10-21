import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import AddProduct from '../components/AddProduct';

export default function Products({ storeId, role }: { storeId: number, role: string }) {
  const { data: products, isLoading, isError } = useQuery({
    queryKey: ['products', storeId],
    queryFn: async () => (await api.get(`/stores/${storeId}/products/`)).data,
  });

  if (isLoading) return <div className="text-gray-500 dark:text-gray-400">Loading products...</div>;
  if (isError) return <div className="text-red-500">Failed to load products.</div>;

  return (
    <div className="mt-4">
      {(role === 'ADMIN' || role === 'MANAGER') && (
        <AddProduct storeId={storeId} role={role} />
      )}

      {products?.length === 0 ? (
        <div className="text-gray-500 dark:text-gray-400">No products in this branch yet.</div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {products?.map((p: any) => (
            <div key={p.id} className="border dark:border-gray-700 p-4 rounded bg-gray-50 dark:bg-gray-800/50 relative overflow-hidden">
              {p.stock === 0 && (
                <div className="absolute top-2 right-2 bg-red-100 text-red-700 text-xs px-2 py-1 rounded font-bold uppercase tracking-wider">
                  Sold Out
                </div>
              )}
              <h4 className="font-bold text-gray-800 dark:text-gray-100 truncate pr-16">{p.name}</h4>
              <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">SKU: {p.sku}</p>
              <p className="text-lg font-bold text-blue-600 dark:text-blue-400">${p.price}</p>
              
              {/* Show Cost Price ONLY to Admin */}
              {role === 'ADMIN' && p.cost_price && (
                <p className="text-xs text-green-600 dark:text-green-400 font-semibold">
                  Cost: ${p.cost_price}
                </p>
              )}
              
              <p className={`text-sm mt-1 ${p.stock > 0 && p.stock < 5 ? 'text-orange-500 font-bold' : 'text-gray-500 dark:text-gray-400'}`}>
                Stock: {p.stock}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}