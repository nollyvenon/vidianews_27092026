'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface Recommendation {
  id: number
  content_id: number
  score: number
  title: string
  creator: string | null
  views: number
  reason: string | null
}

interface TrendingTopic {
  id: number
  topic: string
  score: number
  mention_count: number
}

/** Content recommended for the signed-in user, and the topics trending across the platform. */
export default function DiscoverPage() {
  const [recommendations, setRecommendations] = useState<Recommendation[] | null>(null)
  const [recommendationsError, setRecommendationsError] = useState<string | null>(null)
  const [trending, setTrending] = useState<TrendingTopic[] | null>(null)
  const [trendingError, setTrendingError] = useState<string | null>(null)

  useEffect(() => {
    ApiClient.get('/recommendations?limit=10')
      .then((data: Recommendation[]) => setRecommendations(Array.isArray(data) ? data : []))
      .catch((err) => setRecommendationsError(errorMessage(err, 'Recommendations could not be loaded.')));
    ApiClient.get('/trending?limit=10')
      .then((data: TrendingTopic[]) => setTrending(Array.isArray(data) ? data : []))
      .catch((err) => setTrendingError(errorMessage(err, 'Trending topics could not be loaded.')));
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Discover</h1>
      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Recommended</h2>
          {recommendationsError && <p role="alert" className="text-red-700">{recommendationsError}</p>}
          {recommendations === null && !recommendationsError ? (
            <p className="text-gray-500">Loading recommendations…</p>
          ) : recommendations && recommendations.length === 0 ? (
            <p className="text-gray-500">No recommendations yet.</p>
          ) : recommendations ? (
            <div className="space-y-3">
              {recommendations.map((item) => (
                <div key={item.id} className="border rounded-lg p-4">
                  <p className="font-semibold">{item.title}</p>
                  <p className="text-xs text-gray-600">
                    {item.creator ?? 'Unknown creator'} - {item.views.toLocaleString()} views
                  </p>
                  {item.reason && <p className="text-xs text-gray-500 mt-1">{item.reason}</p>}
                </div>
              ))}
            </div>
          ) : null}
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Trending</h2>
          {trendingError && <p role="alert" className="text-red-700">{trendingError}</p>}
          {trending === null && !trendingError ? (
            <p className="text-gray-500">Loading trending topics…</p>
          ) : trending && trending.length === 0 ? (
            <p className="text-gray-500">No trending topics yet.</p>
          ) : trending ? (
            <div className="space-y-2">
              {trending.map((item) => (
                <div key={item.id} className="flex justify-between">
                  <span>#{item.topic}</span>
                  <span className="text-sm text-gray-600">{item.mention_count.toLocaleString()} mentions</span>
                </div>
              ))}
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
