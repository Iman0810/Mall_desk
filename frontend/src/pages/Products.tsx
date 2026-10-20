import {useQuery} from '@tanstack/react-query';
import { api } from '../api/client';

export default function Products({ storeId }: { storeId: number }) {
  

  const { data: products, isLoading, isError } = useQuery({
    queryKey: ['products', storeId],
    queryFn: async () => (await api.get(`/stores/${storeId}/products/`)).data,
  });

  if (isLoading) return <div>Loading products...</div>;
  if (isError) return <div className="text-red-500">Failed to load products.</div>;
  if (products?.length === 0) return <div>No products in this store yet.</div>;

  return (
    <div className="mt-4">
      <h3 className="text-lg font-bold mb-4">Products</h3>
      <div className="grid grid-cols-2 gap-4">
        {products.map((p: any) => (
          <div key={p.id} className="border p-4 rounded bg-gray-50">
            <h4 className="font-bold">{p.name}</h4>
            <p className="text-sm text-gray-500">SKU: {p.sku}</p>
            <p className="text-sm">Price: ${p.price}</p>
            <p className="text-sm">Stock: {p.stock}</p>
          </div>
        ))}
      </div>
    </div>
  );
}