'use client'

import { useState } from 'react'

export default function DocsPage() {
  const [docs] = useState([
    { id: 1, title: 'Getting Started', slug: 'getting-started', type: 'guide', published: true, views: 1250 },
    { id: 2, title: 'API Reference', slug: 'api-reference', type: 'reference', published: true, views: 3420 },
    { id: 3, title: 'Authentication', slug: 'authentication', type: 'guide', published: true, views: 890 }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Documentation</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Published Docs</h2>
            <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm">+ New Doc</button>
          </div>

          <div className="space-y-3">
            {docs.map(doc => (
              <div key={doc.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-semibold">{doc.title}</p>
                    <p className="text-sm text-gray-600 mt-1">Type: {doc.type}</p>
                  </div>
                  <div className="text-right">
                    <span className="inline-block px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium mb-2">
                      Published
                    </span>
                    <p className="text-sm text-gray-600">{doc.views.toLocaleString()} views</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">API Documentation</h2>
          <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 text-sm">
            View All API Docs
          </button>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Documentation Stats</h2>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold">12</p>
              <p className="text-xs text-gray-600">Total Docs</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-blue-600">5.6K</p>
              <p className="text-xs text-gray-600">Total Views</p>
            </div>
            <div>
              <p className="text-2xl font-bold">24</p>
              <p className="text-xs text-gray-600">API Endpoints</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
