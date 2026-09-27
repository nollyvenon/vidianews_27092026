'use client'

import { useState } from 'react'
import { ApiClient } from '@/lib/api-client'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<any[]>([])
  const [searching, setSearching] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setSearching(true)
    try {
      const data = await ApiClient.get(`/system/search?q=${encodeURIComponent(query)}`)
      setResults(data)
    } catch (err) {
      console.error('Search failed', err)
    } finally {
      setSearching(false)
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Search & Discover</h1>

      <form onSubmit={handleSearch} className="mb-8">
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search content, videos, articles..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={searching}
            className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {searching ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {results.map((result) => (
          <div key={result.id} className="bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer p-4">
            <h3 className="font-semibold mb-2">{result.title}</h3>
            <p className="text-sm text-gray-600 mb-3">{result.content?.substring(0, 100)}...</p>
            <div className="flex justify-between items-center text-sm">
              <span className="text-blue-600">{result.resource_type}</span>
              <button className="text-blue-600 hover:underline">View</button>
            </div>
          </div>
        ))}
      </div>

      {results.length === 0 && !searching && (
        <div className="text-center text-gray-600 py-12">
          {query ? 'No results found' : 'Search to discover content'}
        </div>
      )}
    </div>
  )
}
