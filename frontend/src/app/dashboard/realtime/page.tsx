'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface FeedEvent {
  id: number
  event_type: string
  event_source: string
  payload: Record<string, unknown>
  created_at: string | null
}

interface Presence {
  online: number
  idle: number
}

const REFRESH_INTERVAL_MS = 15_000

/** The platform's live event feed, with a box to broadcast a message and the number of connected users. */
export default function RealtimePage() {
  const [events, setEvents] = useState<FeedEvent[] | null>(null)
  const [presence, setPresence] = useState<Presence | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [newMessage, setNewMessage] = useState('')

  const refresh = async () => {
    try {
      const [feed, counts] = await Promise.all([
        ApiClient.get('/websocket/events?limit=50'),
        ApiClient.get('/websocket/presence'),
      ]);
      setEvents(Array.isArray(feed) ? feed : []);
      setPresence(counts);
      setError(null);
    } catch (err) {
      setError(errorMessage(err, 'The live feed could not be loaded.'));
    }
  };

  useEffect(() => {
    refresh();
    const timer = setInterval(refresh, REFRESH_INTERVAL_MS);
    return () => clearInterval(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const send = async (event: FormEvent) => {
    event.preventDefault();
    const message = newMessage.trim();
    if (!message) return;
    try {
      await ApiClient.post('/websocket/broadcast', {
        event_type: 'message',
        event_source: 'live-feed',
        user_ids: [],
        payload: { message },
        priority: 0,
      });
      setNewMessage('');
      await refresh();
    } catch (err) {
      setError(errorMessage(err, 'The message could not be sent.'));
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Live Feed</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3 mb-6">{error}</p>}

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center mb-4">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2 animate-pulse"></div>
            <span className="font-semibold">Live Updates</span>
          </div>

          <div className="space-y-4 mb-6 max-h-96 overflow-y-auto">
            {events === null && !error ? (
              <p className="text-gray-500">Loading events…</p>
            ) : events && events.length === 0 ? (
              <p className="text-gray-500">No events yet.</p>
            ) : events ? (
              events.map((item) => (
                <div key={item.id} className="border-l-4 border-blue-500 pl-4 py-2">
                  <div className="flex justify-between items-start">
                    <p className="font-semibold text-sm">{item.event_source}</p>
                    <p className="text-xs text-gray-500">
                      {item.created_at ? new Date(item.created_at).toLocaleTimeString() : ''}
                    </p>
                  </div>
                  <p className="text-gray-700 text-sm mt-1">
                    {typeof item.payload.message === 'string' ? item.payload.message : JSON.stringify(item.payload)}
                  </p>
                </div>
              ))
            ) : null}
          </div>

          <form onSubmit={send} className="flex gap-2">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type a message..."
              aria-label="Message"
              className="flex-1 px-3 py-2 border border-gray-300 rounded focus:outline-none"
            />
            <button
              type="submit"
              disabled={!newMessage.trim()}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              Send
            </button>
          </form>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Connected Users</h2>
          <div className="space-y-2">
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              <span>{presence ? `${presence.online.toLocaleString()} users online` : 'Loading…'}</span>
            </div>
            <div className="flex items-center">
              <div className="w-2 h-2 bg-yellow-500 rounded-full mr-2"></div>
              <span>{presence ? `${presence.idle.toLocaleString()} users idle` : 'Loading…'}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
