'use client'

import { useState, useEffect } from 'react'
import { ApiClient } from '@/lib/api-client'

interface Organization {
  id: number
  tenant_id: number
  name: string
  slug: string
  org_type: string
  status: string
  created_at: string
}

interface OrganizationListResponse {
  data: Organization[]
}

const ORG_TYPES = [
  { value: 'department', label: 'Department' },
  { value: 'team', label: 'Team' },
  { value: 'project', label: 'Project' },
]

export default function OrganizationsPage() {
  const [tenantId, setTenantId] = useState('')
  const [orgs, setOrgs] = useState<Organization[]>([])
  const [loading, setLoading] = useState(false)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newOrg, setNewOrg] = useState({ name: '', slug: '', org_type: 'department' })
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!tenantId) {
      setOrgs([])
      return
    }
    const fetchOrganizations = async () => {
      setLoading(true)
      setError(null)
      try {
        const response: OrganizationListResponse = await ApiClient.get(
          `/organizations?tenant_id=${encodeURIComponent(tenantId)}`
        )
        setOrgs(response.data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load organizations')
      } finally {
        setLoading(false)
      }
    }
    fetchOrganizations()
  }, [tenantId])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!tenantId) return

    setCreating(true)
    setError(null)
    try {
      const org: Organization = await ApiClient.post('/organizations', {
        tenant_id: parseInt(tenantId, 10),
        ...newOrg,
      })
      setOrgs([...orgs, org])
      setNewOrg({ name: '', slug: '', org_type: 'department' })
      setShowCreateForm(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create organization')
    } finally {
      setCreating(false)
    }
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Organizations</h1>
        {tenantId && (
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
          >
            + Create Organization
          </button>
        )}
      </div>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="tenant-id">
          Tenant ID
        </label>
        <input
          id="tenant-id"
          type="number"
          min={1}
          placeholder="Enter Tenant ID"
          value={tenantId}
          onChange={(e) => setTenantId(e.target.value)}
          className="border rounded-lg px-4 py-2 w-full max-w-xs"
        />
      </div>

      {error && (
        <div role="alert" className="bg-red-50 text-red-700 rounded-lg p-4 mb-6">
          {error}
        </div>
      )}

      {tenantId && showCreateForm && (
        <form onSubmit={handleCreate} className="bg-white p-6 rounded-lg shadow mb-6">
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
            aria-label="Organization type"
            value={newOrg.org_type}
            onChange={(e) => setNewOrg({ ...newOrg, org_type: e.target.value })}
            className="border rounded-lg px-4 py-2 w-full mb-4"
          >
            {ORG_TYPES.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
          <div className="flex gap-4">
            <button
              type="submit"
              disabled={creating}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg disabled:opacity-50"
            >
              {creating ? 'Creating...' : 'Create'}
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

      {!tenantId ? (
        <p className="text-center text-gray-600 py-8">Enter a tenant ID to view its organizations.</p>
      ) : loading ? (
        <div className="text-gray-600">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {orgs.map((org) => (
            <div key={org.id} className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold">{org.name}</h3>
              <p className="text-gray-600 text-sm mb-2">{org.slug}</p>
              <div className="flex justify-between items-center text-sm">
                <span className="text-xs bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                  {org.org_type}
                </span>
                <span className="text-gray-400">{org.status}</span>
              </div>
            </div>
          ))}
          {orgs.length === 0 && (
            <p className="text-center text-gray-600 py-8 col-span-full">
              No organizations yet. Create one to get started!
            </p>
          )}
        </div>
      )}
    </div>
  )
}
