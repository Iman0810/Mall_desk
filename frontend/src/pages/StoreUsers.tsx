import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function StoreUsers({ storeId, role }: { storeId: number, role: string }) {
  const queryClient = useQueryClient();
  const [username, setUsername] = useState('');
  const [newRole, setNewRole] = useState('STAFF');
  const [error, setError] = useState('');

  const { data: users, isLoading, isError } = useQuery({
    queryKey: ['users', storeId],
    queryFn: async () => (await api.get(`/stores/${storeId}/users/`)).data,
  });

  const assignMutation = useMutation({
    mutationFn: async (data: { username: string, role: string }) => {
      return api.post(`/stores/${storeId}/users/assign/`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users', storeId] });
      setUsername('');
      setError('');
    },
    onError: (err: any) => {
      setError(err.response?.data?.error || 'Failed to assign user. Check if username exists.');
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim()) return;
    assignMutation.mutate({ username, role: newRole });
  };

  if (isLoading) return <div className="text-gray-500 dark:text-gray-400">Loading directory...</div>;
  if (isError) return <div className="text-red-500">You do not have permission to view this directory.</div>;

  return (
    <div className="mt-4 flex flex-col gap-8">

      {/* Add User Form (Only visible to Admins and Managers) */}
      {(role === 'ADMIN' || role === 'MANAGER') && (
        <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg border dark:border-gray-700">
          <h4 className="font-bold text-gray-800 dark:text-gray-200 mb-3">Assign Staff to Branch</h4>
          {error && <div className="text-red-500 text-sm mb-2">{error}</div>}
          <form onSubmit={handleSubmit} className="flex gap-3">
            <input
              type="text"
              placeholder="Username (e.g., staff)"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="flex-1 p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
            <select
              value={newRole}
              onChange={(e) => setNewRole(e.target.value)}
              className="p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            >
              <option value="STAFF">Staff</option>
              <option value="MANAGER">Manager</option>
              {role === 'ADMIN' && <option value="ADMIN">Admin</option>}
            </select>
            <button
              type="submit"
              disabled={assignMutation.isPending}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 font-bold"
            >
              {assignMutation.isPending ? 'Adding...' : 'Assign'}
            </button>
          </form>
        </div>
      )}

      {/* User List */}
      <ul className="space-y-3">
        {users.map((u: any) => (
          <li key={u.id} className="border dark:border-gray-700 p-4 rounded-lg flex justify-between items-center bg-white dark:bg-gray-800/50 shadow-sm">
            <div className="flex flex-col">
              <span className="text-gray-900 dark:text-white font-bold text-lg">
                {u.user.first_name} {u.user.last_name}
              </span>
              <span className="text-gray-500 dark:text-gray-400 text-sm">{u.user.email}</span>
              <span className="text-gray-400 dark:text-gray-500 text-xs mt-1">@{u.user.username}</span>
            </div>
            <span className="bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-300 text-xs px-3 py-1.5 rounded-full font-bold tracking-wider">
              {u.role}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}