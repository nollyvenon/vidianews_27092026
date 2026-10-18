'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface ErrorReport {
  id: number
  error_type: string
  message: string
  severity: string | null
  occurrence_count: number
  first_seen: string | null
  last_seen: string | null
}

/** Application errors that have not been resolved, most frequent first. */
export default function ErrorsPage() {
  const [errors, setErrors] = useState<ErrorReport[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    ApiClient.get('/errors/unresolved')
      .then((data: ErrorReport[]) => {
        const rows = Array.isArray(data) ? data : [];
        setErrors([...rows].sort((a, b) => b.occurrence_count - a.occurrence_count));
      })
      .catch((err) => setError(errorMessage(err, 'Errors could not be loaded.')));
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Errors</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

      <div className="bg-white rounded-lg shadow p-6">
        {errors === null && !error ? (
          <p className="text-gray-500">Loading errors…</p>
        ) : errors && errors.length === 0 ? (
          <p className="text-gray-500">No unresolved errors.</p>
        ) : errors ? (
          <ul className="space-y-3">
            {errors.map((item) => (
              <li key={item.id} className="border rounded p-4">
                <div className="flex justify-between">
                  <span className="font-medium">{item.error_type}</span>
                  <span className="text-sm text-gray-600">{item.occurrence_count} occurrences{item.severity ? ` · ${item.severity}` : ''}</span>
                </div>
                <p className="text-sm text-gray-700">{item.message}</p>
                {item.last_seen && <p className="text-xs text-gray-500">Last seen {new Date(item.last_seen).toLocaleString()}</p>}
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    </div>
  );
}
