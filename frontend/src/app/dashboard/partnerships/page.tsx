'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface Partnership {
  id: number
  type: string
  status: string
}

const PARTNERSHIP_TYPES = ['sponsorship', 'revenue_share', 'collaboration', 'affiliate']

/** Partnerships the signed-in creator has with other members. */
export default function PartnershipsPage() {
  const [partnerships, setPartnerships] = useState<Partnership[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  const [partnerId, setPartnerId] = useState('')
  const [type, setType] = useState(PARTNERSHIP_TYPES[0])

  const load = () =>
    ApiClient.get('/partnerships')
      .then((data: Partnership[]) => setPartnerships(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Partnerships could not be loaded.')))

  useEffect(() => {
    load();
  }, []);

  const propose = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setNotice(null);
    try {
      const query = new URLSearchParams({ partner_id: partnerId, partnership_type: type }).toString();
      await ApiClient.post(`/partnerships?${query}`, {});
      setNotice('Partnership proposed.');
      setPartnerId('');
      await load();
    } catch (err) {
      setError(errorMessage(err, 'The partnership could not be proposed.'));
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Partnerships</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}
      {notice && <p role="status" className="text-green-700">{notice}</p>}

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Your partnerships</h2>
        {partnerships === null ? (
          <p className="text-gray-500">Loading partnerships…</p>
        ) : partnerships.length === 0 ? (
          <p className="text-gray-500">No partnerships yet.</p>
        ) : (
          <ul className="space-y-2">
            {partnerships.map((partnership) => (
              <li key={partnership.id} className="border rounded p-3 flex justify-between">
                <span className="font-medium">{partnership.type.replace(/_/g, ' ')}</span>
                <span className="text-sm text-gray-600">{partnership.status}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <form onSubmit={propose} className="bg-white rounded-lg shadow p-6 flex flex-wrap gap-2 items-end">
        <label className="text-sm">
          <span className="block text-xs text-gray-600">Partner user ID</span>
          <input type="number" min={1} className="border rounded px-2 py-1" value={partnerId} onChange={(e) => setPartnerId(e.target.value)} required />
        </label>
        <label className="text-sm">
          <span className="block text-xs text-gray-600">Type</span>
          <select aria-label="Partnership type" className="border rounded px-2 py-1" value={type} onChange={(e) => setType(e.target.value)}>
            {PARTNERSHIP_TYPES.map((option) => (
              <option key={option} value={option}>{option.replace(/_/g, ' ')}</option>
            ))}
          </select>
        </label>
        <button type="submit" disabled={!partnerId} className="px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50">Propose partnership</button>
      </form>
    </div>
  );
}
