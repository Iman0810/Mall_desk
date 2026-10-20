import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';

export default function StoreUsers({ storeId }: { storeId: number }) {
  const { data: users, isLoading, isError } = useQuery({
    queryKey: ['users', storeId],
    queryFn: async () => (await api.get(`/stores/${storeId}/users/`)).data,
  });

  if (isLoading) return <div>Loading users...</div>;
  if (isError) return <div className="text-red-500">You do not have permission to view users.</div>;

  return (
    <div className="mt-4">
      <h3 className="text-lg font-bold mb-4">Store Users</h3>
      <ul className="space-y-2">
        {users.map((u: any) => (
          <li key={u.id} className="border p-3 rounded flex justify-between items-center bg-gray-50">
            <span>{u.user.username}</span>
            <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded font-bold">
              {u.role}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}