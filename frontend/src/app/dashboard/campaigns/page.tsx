'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface Campaign {
  id: number
  name: string
  subject: string
  body: string
  status?: string | null
}

/** Email campaigns owned by the signed-in creator: create them and send them. */
export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  const [name, setName] = useState('')
  const [subject, setSubject] = useState('')
  const [body, setBody] = useState('')

  const load = () =>
    ApiClient.get('/monetization/campaigns')
      .then((data: Campaign[]) => setCampaigns(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Campaigns could not be loaded.')))

  useEffect(() => {
    load();
  }, []);

  const create = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    try {
      await ApiClient.post('/monetization/campaigns', { name: name.trim(), subject: subject.trim(), body: body.trim() });
      setName('');
      setSubject('');
      setBody('');
      setNotice('Campaign created.');
      await load();
    } catch (err) {
      setError(errorMessage(err, 'The campaign could not be created.'));
    }
  };

  const send = async (campaign: Campaign) => {
    setError(null);
    try {
      await ApiClient.post(`/monetization/campaigns/${campaign.id}/send`, {});
      setNotice(`"${campaign.name}" was sent.`);
      await load();
    } catch (err) {
      setError(errorMessage(err, 'The campaign could not be sent.'));
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Campaigns</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}
      {notice && <p role="status" className="text-green-700">{notice}</p>}

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Your campaigns</h2>
        {campaigns === null ? (
          <p className="text-gray-500">Loading campaigns…</p>
        ) : campaigns.length === 0 ? (
          <p className="text-gray-500">No campaigns yet.</p>
        ) : (
          <ul className="space-y-3">
            {campaigns.map((campaign) => (
              <li key={campaign.id} className="border rounded p-4 flex justify-between items-start gap-4">
                <div>
                  <p className="font-medium">{campaign.name}</p>
                  <p className="text-sm text-gray-600">Subject: {campaign.subject}</p>
                  {campaign.status && <p className="text-xs text-gray-500">Status: {campaign.status}</p>}
                </div>
                <button type="button" onClick={() => send(campaign)} className="px-3 py-1 text-sm border border-blue-600 text-blue-600 rounded">
                  Send
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <form onSubmit={create} className="bg-white rounded-lg shadow p-6 space-y-3">
        <h2 className="text-xl font-semibold">New campaign</h2>
        <input className="w-full border rounded px-3 py-2" placeholder="Campaign name" value={name} onChange={(e) => setName(e.target.value)} required />
        <input className="w-full border rounded px-3 py-2" placeholder="Subject line" value={subject} onChange={(e) => setSubject(e.target.value)} required />
        <textarea className="w-full border rounded px-3 py-2" rows={5} placeholder="Message body" value={body} onChange={(e) => setBody(e.target.value)} required />
        <button type="submit" disabled={!name.trim() || !subject.trim() || !body.trim()} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">
          Create campaign
        </button>
      </form>
    </div>
  );
}
