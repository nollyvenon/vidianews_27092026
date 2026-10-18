'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface CacheStats {
  total_entries: number
  hot_entries: number
  warm_entries: number
  cold_entries: number
  total_hits: number
  avg_hits_per_entry: number
  hit_rate: number
}

interface CachePolicy {
  resource_type: string
  cache_type: string
  ttl_seconds: number
  max_size_mb: number
  is_active: boolean
  hits: number
  misses: number
  hit_rate: number
}

const CACHE_TYPES = ['redis', 'cloudflare', 'local']

/** Cache statistics, per-resource policies, and the administrator's flush and optimize actions. */
export default function CachePage() {
  const [stats, setStats] = useState<CacheStats | null>(null)
  const [statsError, setStatsError] = useState<string | null>(null)
  const [policies, setPolicies] = useState<CachePolicy[] | null>(null)
  const [policiesError, setPoliciesError] = useState<string | null>(null)
  const [editing, setEditing] = useState<CachePolicy | null>(null)
  const [actionMessage, setActionMessage] = useState<string | null>(null)
  const [actionError, setActionError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  const loadPolicies = () =>
    ApiClient.get('/cache/policies')
      .then((data: CachePolicy[]) => {
        setPolicies(Array.isArray(data) ? data : [])
        setPoliciesError(null)
      })
      .catch((err) => setPoliciesError(errorMessage(err, 'Cache policies could not be loaded.')))

  useEffect(() => {
    ApiClient.get('/cache/stats/summary')
      .then((data: CacheStats) => setStats(data))
      .catch((err) => setStatsError(errorMessage(err, 'Cache statistics could not be loaded.')))
    loadPolicies()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const savePolicy = async () => {
    if (!editing) return
    setBusy(true)
    setPoliciesError(null)
    try {
      await ApiClient.put(`/cache/policies/${editing.resource_type}`, {
        cache_type: editing.cache_type,
        ttl_seconds: Number(editing.ttl_seconds),
        max_size_mb: Number(editing.max_size_mb),
        is_active: editing.is_active,
      })
      setEditing(null)
      await loadPolicies()
    } catch (err) {
      setPoliciesError(errorMessage(err, 'The policy could not be saved.'))
    } finally {
      setBusy(false)
    }
  }

  const runAction = async (path: '/cache/flush' | '/cache/optimize') => {
    setBusy(true)
    setActionError(null)
    setActionMessage(null)
    try {
      const result: { removed: number; remaining?: number } = await ApiClient.post(path, {})
      setActionMessage(
        path === '/cache/flush'
          ? `Removed ${result.removed} cache entries.`
          : `Removed ${result.removed} expired entries; ${result.remaining} remain.`,
      )
      const refreshed: CacheStats = await ApiClient.get('/cache/stats/summary')
      setStats(refreshed)
    } catch (err) {
      setActionError(errorMessage(err, 'The cache action could not be completed.'))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Cache Configuration</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Cache Statistics</h2>
          {statsError && <p role="alert" className="mb-3 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{statsError}</p>}
          {!stats && !statsError && <p className="text-gray-500">Loading cache statistics…</p>}
          {stats && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <p className="text-3xl font-bold text-blue-600">{stats.total_entries}</p>
                <p className="text-sm text-gray-600">Entries</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-green-600">{(stats.hit_rate * 100).toFixed(1)}%</p>
                <p className="text-sm text-gray-600">Entries with hits</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-purple-600">{stats.total_hits}</p>
                <p className="text-sm text-gray-600">Total Hits</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold">{stats.avg_hits_per_entry.toFixed(1)}</p>
                <p className="text-sm text-gray-600">Avg Hits per Entry</p>
              </div>
              <div className="text-center">
                <p className="text-xl font-semibold">{stats.hot_entries}</p>
                <p className="text-sm text-gray-600">Hot</p>
              </div>
              <div className="text-center">
                <p className="text-xl font-semibold">{stats.warm_entries}</p>
                <p className="text-sm text-gray-600">Warm</p>
              </div>
              <div className="text-center">
                <p className="text-xl font-semibold">{stats.cold_entries}</p>
                <p className="text-sm text-gray-600">Cold</p>
              </div>
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Cache Policies</h2>
          {policiesError && <p role="alert" className="mb-3 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{policiesError}</p>}
          {policies && policies.length === 0 && <p className="text-gray-500">No cache policies are defined yet.</p>}
          {policies && policies.length > 0 && (
            <div className="space-y-4">
              {policies.map((policy) => (
                <div key={policy.resource_type} className="border rounded p-4">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <p className="font-semibold text-lg">{policy.resource_type}</p>
                      <p className="text-sm text-gray-600">
                        Type: {policy.cache_type} | TTL: {policy.ttl_seconds}s | Max: {policy.max_size_mb} MB | {policy.is_active ? 'Active' : 'Inactive'}
                      </p>
                    </div>
                    <span className="text-2xl font-bold text-blue-600">{policy.hit_rate.toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>{policy.hits} hits</span>
                    <span>{policy.misses} misses</span>
                  </div>
                  <button type="button" onClick={() => setEditing({ ...policy })} className="mt-3 text-sm text-blue-600 hover:underline">
                    Edit policy
                  </button>
                </div>
              ))}
            </div>
          )}

          {editing && (
            <form
              className="mt-6 border-t pt-4 grid grid-cols-1 md:grid-cols-4 gap-3 items-end"
              onSubmit={(e) => {
                e.preventDefault()
                savePolicy()
              }}
            >
              <label className="text-sm">
                <span className="block text-xs text-gray-600">Cache type</span>
                <select className="border rounded px-2 py-1 w-full" value={editing.cache_type} onChange={(e) => setEditing({ ...editing, cache_type: e.target.value })}>
                  {CACHE_TYPES.map((type) => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </label>
              <label className="text-sm">
                <span className="block text-xs text-gray-600">TTL (seconds)</span>
                <input type="number" min={1} className="border rounded px-2 py-1 w-full" value={editing.ttl_seconds} onChange={(e) => setEditing({ ...editing, ttl_seconds: Number(e.target.value) })} required />
              </label>
              <label className="text-sm">
                <span className="block text-xs text-gray-600">Max size (MB)</span>
                <input type="number" min={1} className="border rounded px-2 py-1 w-full" value={editing.max_size_mb} onChange={(e) => setEditing({ ...editing, max_size_mb: Number(e.target.value) })} required />
              </label>
              <label className="flex items-center gap-2 text-sm">
                <input type="checkbox" checked={editing.is_active} onChange={(e) => setEditing({ ...editing, is_active: e.target.checked })} />
                Active
              </label>
              <div className="flex gap-2 md:col-span-4">
                <button type="submit" disabled={busy} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">Save policy</button>
                <button type="button" onClick={() => setEditing(null)} className="px-4 py-2 border rounded">Cancel</button>
              </div>
            </form>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Cache Management</h2>
          {actionMessage && <p role="status" className="mb-3 text-green-700">{actionMessage}</p>}
          {actionError && <p role="alert" className="mb-3 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{actionError}</p>}
          <div className="space-y-2">
            <button type="button" disabled={busy} onClick={() => runAction('/cache/flush')} className="w-full px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 disabled:opacity-50">
              Flush All Cache
            </button>
            <button type="button" disabled={busy} onClick={() => runAction('/cache/optimize')} className="w-full px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 disabled:opacity-50">
              Optimize Cache
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
