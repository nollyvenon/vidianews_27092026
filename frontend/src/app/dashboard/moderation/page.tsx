'use client'

import { useState } from 'react'

export default function ModerationPage() {
  const [reports] = useState([
    { id: 1, content: 'Inappropriate video', reason: 'Offensive language', status: 'pending', reportedAt: '5 min ago' },
    { id: 2, content: 'Spam comment', reason: 'Promotional link', status: 'pending', reportedAt: '10 min ago' }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Content Moderation</h1>
      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Pending Reports</h2>
          <div className="space-y-3">
            {reports.map(report => (
              <div key={report.id} className="border rounded-lg p-4">
                <p className="font-semibold">{report.content}</p>
                <p className="text-sm text-gray-600">Reason: {report.reason}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
