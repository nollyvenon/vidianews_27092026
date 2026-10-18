'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface EndpointVersion {
  id: number
  endpoint: string
  version: string
  deprecated: boolean
  sunset_date: string | null
}

interface Migration {
  id: number
  old_version: string
  new_version: string
  status: string
  executed_at: string | null
}

/** Registered API endpoint versions, their deprecation state, and the migrations between versions. */
export default function APIVersionsPage() {
  const [versions, setVersions] = useState<EndpointVersion[] | null>(null)
  const [versionsError, setVersionsError] = useState<string | null>(null)
  const [migrations, setMigrations] = useState<Migration[] | null>(null)
  const [migrationsError, setMigrationsError] = useState<string | null>(null)
  const [showMigrations, setShowMigrations] = useState(false)

  useEffect(() => {
    ApiClient.get('/versions')
      .then((data: EndpointVersion[]) => setVersions(Array.isArray(data) ? data : []))
      .catch((err) => setVersionsError(errorMessage(err, 'API versions could not be loaded.')));
    ApiClient.get('/versions/migrations')
      .then((data: Migration[]) => setMigrations(Array.isArray(data) ? data : []))
      .catch((err) => setMigrationsError(errorMessage(err, 'Migrations could not be loaded.')));
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">API Versions</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Active Versions</h2>
          {versionsError && <p role="alert" className="text-red-700 mb-3">{versionsError}</p>}
          {versions === null && !versionsError ? (
            <p className="text-gray-500">Loading versions…</p>
          ) : versions && versions.length === 0 ? (
            <p className="text-gray-500">No endpoint versions are registered yet.</p>
          ) : versions ? (
            <div className="space-y-3">
              {versions.map((item) => (
                <div key={item.id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <p className="font-semibold text-lg">{item.endpoint}</p>
                      <p className="text-sm text-gray-600">Version {item.version}</p>
                    </div>
                    <span className={`px-3 py-1 rounded text-sm font-medium ${
                      item.deprecated ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                    }`}>
                      {item.deprecated ? 'Deprecated' : 'Active'}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">Usage: not tracked yet</p>
                  {item.deprecated && item.sunset_date && (
                    <p className="text-xs text-red-600 mt-2">Sunset: {new Date(item.sunset_date).toLocaleDateString()}</p>
                  )}
                </div>
              ))}
            </div>
          ) : null}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Migration Path</h2>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-900">
              Move between versions to get the latest features and performance improvements.
            </p>
            <button
              type="button"
              onClick={() => setShowMigrations((open) => !open)}
              className="mt-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
            >
              {showMigrations ? 'Hide migrations' : 'View migrations'}
            </button>
            {showMigrations && (
              <div className="mt-4 space-y-2">
                {migrationsError && <p role="alert" className="text-red-700">{migrationsError}</p>}
                {migrations === null && !migrationsError ? (
                  <p className="text-sm text-blue-900">Loading migrations…</p>
                ) : migrations && migrations.length === 0 ? (
                  <p className="text-sm text-blue-900">No migrations are planned.</p>
                ) : migrations ? (
                  migrations.map((item) => (
                    <p key={item.id} className="text-sm text-blue-900">
                      {item.old_version} → {item.new_version} · {item.status}
                      {item.executed_at && ` · ${new Date(item.executed_at).toLocaleDateString()}`}
                    </p>
                  ))
                ) : null}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
