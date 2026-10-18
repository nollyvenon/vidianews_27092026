'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface CreatorProfile {
  id: number
  user_id: number
  bio: string | null
  followers: number
  is_verified: boolean
}

/** The signed-in member's creator profile, and the directory of creators on the platform. */
export default function CreatorPage() {
  const [profile, setProfile] = useState<CreatorProfile | null | undefined>(undefined)
  const [creators, setCreators] = useState<CreatorProfile[] | null>(null)
  const [verifiedOnly, setVerifiedOnly] = useState(false)
  const [bio, setBio] = useState('')
  const [error, setError] = useState<string | null>(null)

  const loadProfile = () =>
    ApiClient.get('/monetization/creator-profile')
      .then((data: CreatorProfile | null) => setProfile(data ?? null))
      .catch((err) => {
        setProfile(null);
        // A member without a creator profile is not an error; anything else is shown.
        if (!(err instanceof Error) || !/not found/i.test(err.message)) setError(errorMessage(err, 'The creator profile could not be loaded.'));
      });

  const loadCreators = (onlyVerified: boolean) =>
    ApiClient.get(`/monetization/creators?verified_only=${onlyVerified}`)
      .then((data: CreatorProfile[]) => setCreators(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Creators could not be loaded.')));

  useEffect(() => {
    loadProfile();
  }, []);

  useEffect(() => {
    loadCreators(verifiedOnly);
  }, [verifiedOnly]);

  const create = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    try {
      await ApiClient.post(`/monetization/creator-profile?bio=${encodeURIComponent(bio.trim())}`, {});
      setBio('');
      await loadProfile();
      await loadCreators(verifiedOnly);
    } catch (err) {
      setError(errorMessage(err, 'The creator profile could not be created.'));
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Creator</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

      <div className="bg-white rounded-lg shadow p-6 space-y-3">
        <h2 className="text-xl font-semibold">Your creator profile</h2>
        {profile === undefined ? (
          <p className="text-gray-500">Loading profile…</p>
        ) : profile ? (
          <div className="text-sm space-y-1">
            <p>{profile.bio || 'No bio yet.'}</p>
            <p>{profile.followers} followers · {profile.is_verified ? 'Verified' : 'Not verified'}</p>
          </div>
        ) : (
          <form onSubmit={create} className="space-y-3">
            <p className="text-gray-500">You have no creator profile yet.</p>
            <textarea className="w-full border rounded px-3 py-2" rows={3} placeholder="Tell viewers about your work" value={bio} onChange={(e) => setBio(e.target.value)} />
            <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">Create creator profile</button>
          </form>
        )}
      </div>

      <div className="bg-white rounded-lg shadow p-6 space-y-3">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-semibold">Creator directory</h2>
          <label className="text-sm flex items-center gap-2">
            <input type="checkbox" checked={verifiedOnly} onChange={(e) => setVerifiedOnly(e.target.checked)} />
            Verified only
          </label>
        </div>
        {creators === null ? (
          <p className="text-gray-500">Loading creators…</p>
        ) : creators.length === 0 ? (
          <p className="text-gray-500">No creators to show.</p>
        ) : (
          <ul className="space-y-2">
            {creators.map((creator) => (
              <li key={creator.id} className="border rounded p-3">
                <span className="font-medium">Creator #{creator.user_id}</span>
                {creator.is_verified && <span className="ml-2 text-xs text-green-700">Verified</span>}
                <p className="text-sm text-gray-600">{creator.bio || 'No bio yet.'} · {creator.followers} followers</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
