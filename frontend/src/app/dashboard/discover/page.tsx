'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'

export default function DiscoverPage() {
  const [recommendations, setRecommendations] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchRecommendations()
  }, [])

  const fetchRecommendations = async () => {
    try {
      const data = await ApiClient.get('/resources/recommendations')
      setRecommendations(data)
    } catch (err) {
      console.error('Failed to fetch', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Discover</h1>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recommendations.map((rec) => (
            <div key={rec.id} className="bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer">
              <div className="p-4">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold">Recommendation</h3>
                  <span className="text-lg font-bold text-blue-600">{(rec.score * 100).toFixed(0)}%</span>
                </div>
                <p className="text-sm text-gray-600 mb-3">{rec.reason}</p>
                <button className="w-full px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm">
                  View
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
