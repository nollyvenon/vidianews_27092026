'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface ActiveStream {
  id: number
  title: string
  viewers: number
}

interface CreatedStream {
  id: number
  stream_key: string
  status: string
}

/** Live streams: create one, start or end it, and see who is live now. */
export default function LivestreamPage() {
  const [active, setActive] = useState<ActiveStream[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [created, setCreated] = useState<CreatedStream | null>(null)
  const [streamId, setStreamId] = useState('')

  const load = () =>
    ApiClient.get('/livestream/active')
      .then((data: ActiveStream[]) => setActive(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Live streams could not be loaded.')))

  useEffect(() => {
    load();
  }, []);

  const create = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    try {
      const query = new URLSearchParams({ title: title.trim(), description: description.trim() }).toString();
      const stream: CreatedStream = await ApiClient.post(`/livestream?${query}`, {});
      setCreated(stream);
      setTitle('');
      setDescription('');
    } catch (err) {
      setError(errorMessage(err, 'The stream could not be created.'));
    }
  };

  const change = async (action: 'start' | 'end') => {
    setError(null);
    try {
      await ApiClient.put(`/livestream/${Number(streamId)}/${action}`, {});
      await load();
    } catch (err) {
      setError(errorMessage(err, `The stream could not be ${action === 'start' ? 'started' : 'ended'}.`));
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Live Streams</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Live now</h2>
        {active === null ? (
          <p className="text-gray-500">Loading streams…</p>
        ) : active.length === 0 ? (
          <p className="text-gray-500">Nobody is live right now.</p>
        ) : (
          <ul className="space-y-2">
            {active.map((stream) => (
              <li key={stream.id} className="border rounded p-3 flex justify-between">
                <span className="font-medium">{stream.title}</span>
                <span className="text-sm text-gray-600">{stream.viewers} viewers</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="bg-white rounded-lg shadow p-6 space-y-3">
        <h2 className="text-xl font-semibold">Start a new stream</h2>
        <form onSubmit={create} className="space-y-3">
          <input className="w-full border rounded px-3 py-2" placeholder="Stream title" value={title} onChange={(e) => setTitle(e.target.value)} required />
          <input className="w-full border rounded px-3 py-2" placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
          <button type="submit" disabled={!title.trim()} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">Create stream</button>
        </form>
        {created && (
          <div className="border rounded p-3 text-sm space-y-1">
            <p>Stream #{created.id} is {created.status}.</p>
            <p>Stream key: <code className="font-mono">{created.stream_key}</code></p>
          </div>
        )}
      </div>

      <div className="bg-white rounded-lg shadow p-6 space-y-3">
        <h2 className="text-xl font-semibold">Go live or end a stream</h2>
        <div className="flex gap-2 items-end">
          <label className="text-sm">
            <span className="block text-xs text-gray-600">Stream ID</span>
            <input type="number" min={1} className="border rounded px-2 py-1" value={streamId} onChange={(e) => setStreamId(e.target.value)} />
          </label>
          <button type="button" disabled={!streamId} onClick={() => change('start')} className="px-3 py-1 bg-green-600 text-white rounded disabled:opacity-50">Start</button>
          <button type="button" disabled={!streamId} onClick={() => change('end')} className="px-3 py-1 bg-gray-700 text-white rounded disabled:opacity-50">End</button>
        </div>
      </div>
    </div>
  );
}
