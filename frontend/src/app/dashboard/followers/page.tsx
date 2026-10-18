'use client'

import { useEffect, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface FollowRow {
  id: number
  follower_id: number
  following_id: number
  created_at: string
  follower_name: string | null
}

export default function FollowersPage() {
  const { user } = useAuth()
  const [followers, setFollowers] = useState<FollowRow[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!user) return
    let active = true
    ApiClient.get(`/platform/followers/${user.id}`)
      .then((data: FollowRow[]) => {
        if (active) setFollowers(Array.isArray(data) ? data : [])
      })
      .catch((err) => {
        if (active) setError(errorMessage(err, 'Followers could not be loaded.'))
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [user])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">My Network</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Followers</h2>
        {error && <p role="alert" className="mb-3 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}
        {loading ? (
          <p className="text-gray-500">Loading followers…</p>
        ) : followers.length === 0 ? (
          <p className="text-gray-500">You have no followers yet.</p>
        ) : (
          <div className="space-y-3">
            {followers.map((follow) => (
              <div key={follow.id} className="border rounded-lg p-4">
                <p className="font-semibold">{follow.follower_name ?? `User #${follow.follower_id}`}</p>
                <p className="text-sm text-gray-600">Following since {new Date(follow.created_at).toLocaleDateString()}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
