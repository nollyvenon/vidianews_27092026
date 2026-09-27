'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import axios from 'axios';

interface Organization {
  id: number;
  tenant_id: number;
  name: string;
  slug: string;
  org_type: string;
  status: string;
  created_at: string;
}

export default function OrganizationsPage() {
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [tenantId, setTenantId] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newOrg, setNewOrg] = useState({ name: '', slug: '', org_type: 'department' });

  useEffect(() => {
    if (tenantId) fetchOrganizations();
  }, [tenantId]);

  const fetchOrganizations = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/v1/organizations?tenant_id=${tenantId}`);
      setOrganizations(response.data.data);
    } catch (error) {
      console.error('Error loading organizations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('/api/v1/organizations', {
        tenant_id: parseInt(tenantId),
        ...newOrg,
      });
      setNewOrg({ name: '', slug: '', org_type: 'department' });
      setShowCreateForm(false);
      await fetchOrganizations();
    } catch (error) {
      console.error('Error creating organization:', error);
    }
  };

  if (!tenantId) {
    return (
      <div className="p-8 bg-gray-50 min-h-screen">
        <h1 className="text-3xl font-bold mb-8">Organizations</h1>
        <input
          type="number"
          placeholder="Enter Tenant ID"
          value={tenantId}
          onChange={(e) => setTenantId(e.target.value)}
          className="border rounded-lg px-4 py-2 mb-8"
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Organizations</h1>
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
          >
            + Create Organization
          </button>
        </div>

        {showCreateForm && (
          <form onSubmit={handleCreate} className="bg-white p-6 rounded-lg shadow-md mb-8">
            <input
              type="text"
              placeholder="Name"
              value={newOrg.name}
              onChange={(e) => setNewOrg({ ...newOrg, name: e.target.value })}
              className="border rounded-lg px-4 py-2 w-full mb-4"
              required
            />
            <input
              type="text"
              placeholder="Slug"
              value={newOrg.slug}
              onChange={(e) => setNewOrg({ ...newOrg, slug: e.target.value })}
              className="border rounded-lg px-4 py-2 w-full mb-4"
              required
            />
            <select
              value={newOrg.org_type}
              onChange={(e) => setNewOrg({ ...newOrg, org_type: e.target.value })}
              className="border rounded-lg px-4 py-2 w-full mb-4"
            >
              <option value="department">Department</option>
              <option value="team">Team</option>
              <option value="project">Project</option>
            </select>
            <div className="flex gap-4">
              <button type="submit" className="bg-blue-600 text-white px-6 py-2 rounded-lg">
                Create
              </button>
              <button
                type="button"
                onClick={() => setShowCreateForm(false)}
                className="bg-gray-200 text-gray-800 px-6 py-2 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        {loading ? (
          <div>Loading...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {organizations.map((org) => (
              <Link key={org.id} href={`/dashboard/organizations/${org.id}`}>
                <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg cursor-pointer">
                  <h3 className="text-lg font-semibold mb-2">{org.name}</h3>
                  <p className="text-gray-500 text-sm mb-4">{org.slug}</p>
                  <div className="flex justify-between items-center">
                    <span className="text-xs bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                      {org.org_type}
                    </span>
                    <span className="text-gray-400 text-sm">{org.status}</span>
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
