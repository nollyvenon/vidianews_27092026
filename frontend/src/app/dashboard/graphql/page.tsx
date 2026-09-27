'use client'

import { useState } from 'react'

export default function GraphQLPage() {
  const [queries] = useState([
    { id: 1, name: 'GetUser', executions: 12540, avgTime: 25.3 },
    { id: 2, name: 'GetPosts', executions: 8420, avgTime: 45.7 },
    { id: 3, name: 'GetComments', executions: 5230, avgTime: 18.9 }
  ])
  const [queryInput, setQueryInput] = useState('')

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">GraphQL Explorer</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Query Editor</h2>
          <textarea
            value={queryInput}
            onChange={(e) => setQueryInput(e.target.value)}
            placeholder="query GetUser { user { id name email } }"
            className="w-full h-40 p-3 border border-gray-300 rounded font-mono text-sm focus:outline-none"
          />
          <div className="flex gap-2 mt-3">
            <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Execute</button>
            <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50">Save Query</button>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Popular Queries</h2>
          <div className="space-y-3">
            {queries.map(q => (
              <div key={q.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <p className="font-semibold">{q.name}</p>
                  <span className="text-sm text-gray-600">{q.executions.toLocaleString()} executions</span>
                </div>
                <p className="text-sm text-gray-600">Avg Response: {q.avgTime.toFixed(1)}ms</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Schema Documentation</h2>
          <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50">
            View Full Schema
          </button>
        </div>
      </div>
    </div>
  )
}
