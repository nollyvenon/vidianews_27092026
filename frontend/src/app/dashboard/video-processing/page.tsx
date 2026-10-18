'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface VideoJob {
  video_id: number
  content_id: number
  title: string
  status: string
  progress: number
  qualities: { quality: string; status: string }[]
}

const STATUS_LABELS: Record<string, { label: string; color: string }> = {
  completed: { label: 'completed', color: 'bg-green-100 text-green-800' },
  in_progress: { label: 'processing', color: 'bg-blue-100 text-blue-800' },
  pending: { label: 'pending', color: 'bg-gray-100 text-gray-800' },
  failed: { label: 'failed', color: 'bg-red-100 text-red-800' },
}

/** Encoding progress for the videos you have published. */
export default function VideoProcessingPage() {
  const [videos, setVideos] = useState<VideoJob[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    ApiClient.get('/content/videos/processing')
      .then((data: VideoJob[]) => setVideos(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Videos could not be loaded.')));
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Video Processing</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3 mb-6">{error}</p>}

      {videos === null && !error ? (
        <p className="text-gray-500">Loading videos…</p>
      ) : videos && videos.length === 0 ? (
        <p className="text-gray-500">You have no videos yet.</p>
      ) : videos ? (
        <div className="space-y-4">
          {videos.map((video) => {
            const status = STATUS_LABELS[video.status] ?? { label: video.status, color: 'bg-red-100 text-red-800' }
            return (
              <div key={video.video_id} className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="font-semibold">{video.title}</h3>
                  <span className={`px-3 py-1 rounded text-sm ${status.color}`}>{status.label}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full transition-all" style={{ width: `${video.progress}%` }} />
                </div>
                <p className="text-sm text-gray-600 mt-2">{video.progress}% complete</p>
                {video.qualities.length > 0 && (
                  <p className="text-xs text-gray-500 mt-1">
                    {video.qualities.map((item) => `${item.quality}: ${item.status}`).join(' · ')}
                  </p>
                )}
              </div>
            )
          })}
        </div>
      ) : null}
    </div>
  );
}
