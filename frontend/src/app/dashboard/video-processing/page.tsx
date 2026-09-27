'use client'

import { useState } from 'react'

export default function VideoProcessingPage() {
  const [videos, setVideos] = useState([
    { id: 1, name: 'Tutorial.mp4', status: 'completed', progress: 100 },
    { id: 2, name: 'Guide.mp4', status: 'processing', progress: 65 },
    { id: 3, name: 'Demo.mp4', status: 'pending', progress: 0 },
  ])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800'
      case 'processing': return 'bg-blue-100 text-blue-800'
      case 'pending': return 'bg-gray-100'
      default: return 'bg-red-100 text-red-800'
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Video Processing</h1>

      <div className="space-y-4">
        {videos.map((video) => (
          <div key={video.id} className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-start mb-4">
              <h3 className="font-semibold">{video.name}</h3>
              <span className={`px-3 py-1 rounded text-sm ${getStatusColor(video.status)}`}>
                {video.status}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all"
                style={{ width: `${video.progress}%` }}
              />
            </div>
            <p className="text-sm text-gray-600 mt-2">{video.progress}% complete</p>
          </div>
        ))}
      </div>
    </div>
  )
}
