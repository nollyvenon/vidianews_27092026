'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import axios from 'axios';
import { useRouter } from 'next/navigation';

interface Tenant {
  id: number;
  name: string;
  slug: string;
  description: string;
  plan: string;
  status: string;
  max_users: number;
  created_at: string;
}

export default function TenantsPage() {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newTenant, setNewTenant] = useState({
    name: '',
    slug: '',
    description: '',
    plan: 'free',
  });
  const router = useRouter();

  useEffect(() => {
    fetchTenants();
  }, []);

  const fetchTenants = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/v1/tenants');
      setTenants(response.data.data);
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load tenants');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTenant = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/v1/tenants', newTenant);
      setTenants([...tenants, response.data]);
      setNewTenant({ name: '', slug: '', description: '', plan: 'free' });
      setShowCreateForm(false);
      router.push(`/dashboard/tenants/${response.data.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create tenant');
    }
  };

  if (loading) return <div className="p-8">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Tenants</h1>
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
          >
            + Create Tenant
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {showCreateForm && (
          <form onSubmit={handleCreateTenant} className="bg-white p-6 rounded-lg shadow-md mb-8">
            <h2 className="text-xl font-semibold mb-4">Create New Tenant</h2>
            <div className="grid grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Tenant Name"
                required
                className="border rounded-lg px-4 py-2"
                value={newTenant.name}
                onChange={(e) => setNewTenant({ ...newTenant, name: e.target.value })}
              />
              <input
                type="text"
                placeholder="Slug (url-friendly)"
                required
                className="border rounded-lg px-4 py-2"
                value={newTenant.slug}
                onChange={(e) => setNewTenant({ ...newTenant, slug: e.target.value })}
              />
              <textarea
                placeholder="Description"
                className="border rounded-lg px-4 py-2 col-span-2"
                rows={3}
                value={newTenant.description}
                onChange={(e) => setNewTenant({ ...newTenant, description: e.target.value })}
              />
              <select
                className="border rounded-lg px-4 py-2"
                value={newTenant.plan}
                onChange={(e) => setNewTenant({ ...newTenant, plan: e.target.value })}
              >
                <option value="free">Free</option>
                <option value="pro">Pro</option>
                <option value="enterprise">Enterprise</option>
              </select>
            </div>
            <div className="flex gap-4 mt-4">
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
              >
                Create
              </button>
              <button
                type="button"
                onClick={() => setShowCreateForm(false)}
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-2 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        {tenants.length === 0 ? (
          <div className="bg-white p-8 rounded-lg shadow-md text-center">
            <p className="text-gray-500">No tenants yet. Create your first tenant to get started.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tenants.map((tenant) => (
              <Link key={tenant.id} href={`/dashboard/tenants/${tenant.id}`}>
                <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition cursor-pointer">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{tenant.name}</h3>
                  <p className="text-gray-500 text-sm mb-4">{tenant.description}</p>
                  <div className="flex justify-between items-center">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      tenant.plan === 'pro' ? 'bg-blue-100 text-blue-800' :
                      tenant.plan === 'enterprise' ? 'bg-purple-100 text-purple-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {tenant.plan}
                    </span>
                    <span className="text-gray-400 text-sm">{tenant.max_users} users</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
