'use client'

import { useState, useEffect } from 'react'
import { ApiClient } from '@/lib/api-client'

interface Organization {
  id: number
  name: string
  slug: string
  logo_url?: string
  subscription_tier: string
  created_at: string
}

export default function OrganizationsPage() {
  const [orgs, setOrgs] = useState<Organization[]>([])
  const [loading, setLoading] = useState(true)
  const [newOrgName, setNewOrgName] = useState('')
  const [creating, setCreating] = useState(false)

  useEffect(() => {
    fetchOrganizations()
  }, [])

  const fetchOrganizations = async () => {
    try {
      const data = await ApiClient.get('/organizations')
      setOrgs(data)
    } catch (err) {
      console.error('Failed to fetch organizations', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateOrg = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newOrgName) return

    setCreating(true)
    try {
      const org = await ApiClient.post('/organizations', { name: newOrgName })
      setOrgs([...orgs, org])
      setNewOrgName('')
    } catch (err) {
      console.error('Failed to create organization', err)
    } finally {
      setCreating(false)
    }
  }

  if (loading) {
    return <div className="text-gray-600">Loading...</div>
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Organizations</h1>
      </div>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Create Organization</h2>
        <form onSubmit={handleCreateOrg} className="flex gap-2">
          <input
            type="text"
            value={newOrgName}
            onChange={(e) => setNewOrgName(e.target.value)}
            placeholder="Organization name"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={creating}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {creating ? 'Creating...' : 'Create'}
          </button>
        </form>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {orgs.map((org) => (
          <div key={org.id} className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold">{org.name}</h3>
            <p className="text-gray-600 text-sm mb-2">{org.slug}</p>
            <div className="flex justify-between items-center text-sm">
              <span className="text-blue-600">{org.subscription_tier}</span>
              <button className="text-blue-600 hover:underline">Manage</button>
            </div>
          </div>
        ))}
      </div>

      {orgs.length === 0 && (
        <div className="text-center text-gray-600 py-8">
          No organizations yet. Create one to get started!
        </div>
      )}
    </div>
  )
}
