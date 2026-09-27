'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import axios from 'axios';

interface Tenant {
  id: number;
  name: string;
  slug: string;
  description: string;
  logo_url: string;
  website: string;
  plan: string;
  status: string;
  max_users: number;
  created_at: string;
}

export default function TenantDetailPage() {
  const params = useParams();
  const tenantId = params.id as string;
  const [tenant, setTenant] = useState<Tenant | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('details');
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState<Partial<Tenant>>({});
  const router = useRouter();

  useEffect(() => {
    fetchTenant();
  }, [tenantId]);

  const fetchTenant = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/v1/tenants/${tenantId}`);
      setTenant(response.data);
      setFormData(response.data);
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load tenant');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.put(`/api/v1/tenants/${tenantId}`, formData);
      setTenant(response.data);
      setEditMode(false);
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update tenant');
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure? This action cannot be undone.')) {
      try {
        await axios.delete(`/api/v1/tenants/${tenantId}`);
        router.push('/dashboard/tenants');
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to delete tenant');
      }
    }
  };

  if (loading) return <div className="p-8">Loading...</div>;
  if (!tenant) return <div className="p-8">Tenant not found</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <Link href="/dashboard/tenants" className="text-blue-600 hover:text-blue-700">
            ← Back to Tenants
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 mt-4">{tenant.name}</h1>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <div className="bg-white rounded-lg shadow-md">
          <div className="border-b border-gray-200">
            <div className="flex space-x-8 px-6">
              <button
                onClick={() => setActiveTab('details')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'details'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Details
              </button>
              <button
                onClick={() => setActiveTab('members')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'members'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Members
              </button>
              <button
                onClick={() => setActiveTab('settings')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'settings'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Settings
              </button>
            </div>
          </div>

          <div className="p-6">
            {activeTab === 'details' && (
              <div>
                {!editMode ? (
                  <>
                    <div className="grid grid-cols-2 gap-6 mb-6">
                      <div>
                        <label className="text-sm text-gray-500">Name</label>
                        <p className="text-lg font-semibold">{tenant.name}</p>
                      </div>
                      <div>
                        <label className="text-sm text-gray-500">Slug</label>
                        <p className="text-lg font-semibold">{tenant.slug}</p>
                      </div>
                      <div className="col-span-2">
                        <label className="text-sm text-gray-500">Description</label>
                        <p className="text-lg">{tenant.description || '-'}</p>
                      </div>
                      <div>
                        <label className="text-sm text-gray-500">Plan</label>
                        <p className="text-lg font-semibold">{tenant.plan}</p>
                      </div>
                      <div>
                        <label className="text-sm text-gray-500">Max Users</label>
                        <p className="text-lg font-semibold">{tenant.max_users}</p>
                      </div>
                    </div>
                    <div className="flex gap-4">
                      <button
                        onClick={() => setEditMode(true)}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
                      >
                        Edit
                      </button>
                      <button
                        onClick={handleDelete}
                        className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg"
                      >
                        Delete
                      </button>
                    </div>
                  </>
                ) : (
                  <form onSubmit={handleUpdate}>
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      <input
                        type="text"
                        value={formData.name || ''}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        placeholder="Name"
                        className="border rounded-lg px-4 py-2"
                      />
                      <input
                        type="text"
                        value={formData.slug || ''}
                        onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                        placeholder="Slug"
                        className="border rounded-lg px-4 py-2"
                      />
                      <textarea
                        value={formData.description || ''}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        placeholder="Description"
                        className="border rounded-lg px-4 py-2 col-span-2"
                        rows={3}
                      />
                    </div>
                    <div className="flex gap-4">
                      <button
                        type="submit"
                        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
                      >
                        Save
                      </button>
                      <button
                        type="button"
                        onClick={() => setEditMode(false)}
                        className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-2 rounded-lg"
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                )}
              </div>
            )}

            {activeTab === 'members' && (
              <div>
                <Link href={`/dashboard/tenants/${tenantId}/members`} className="text-blue-600 hover:text-blue-700">
                  Manage members →
                </Link>
              </div>
            )}

            {activeTab === 'settings' && (
              <div>
                <Link href={`/dashboard/tenants/${tenantId}/settings`} className="text-blue-600 hover:text-blue-700">
                  Manage settings →
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
