'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface PremiumStatus {
  is_premium: boolean
  features?: string[]
}

/** The signed-in user's premium streaming access, and the option to subscribe to it. */
export default function PremiumPage() {
  const [status, setStatus] = useState<PremiumStatus | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)

  const load = () =>
    ApiClient.get('/premium/status')
      .then((data: PremiumStatus) => setStatus(data))
      .catch((err) => setError(errorMessage(err, 'Premium status could not be loaded.')))

  useEffect(() => {
    load();
  }, []);

  const subscribe = async () => {
    setError(null);
    setNotice(null);
    try {
      await ApiClient.post('/premium/subscribe', {});
      setNotice('Premium access is on.');
      await load();
    } catch (err) {
      setError(errorMessage(err, 'Premium could not be activated.'));
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Premium</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}
      {notice && <p role="status" className="text-green-700">{notice}</p>}

      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        {status === null && !error ? (
          <p className="text-gray-500">Loading premium status…</p>
        ) : status ? (
          <>
            <p>Status: <strong>{status.is_premium ? 'Premium' : 'Free'}</strong></p>
            {status.features && status.features.length > 0 && (
              <ul className="list-disc pl-6 text-sm text-gray-700">
                {status.features.map((feature) => (
                  <li key={feature}>{feature.replace(/_/g, ' ')}</li>
                ))}
              </ul>
            )}
            {!status.is_premium && (
              <button type="button" onClick={subscribe} className="px-4 py-2 bg-blue-600 text-white rounded">
                Turn on premium access
              </button>
            )}
          </>
        ) : null}
      </div>
    </div>
  );
}
