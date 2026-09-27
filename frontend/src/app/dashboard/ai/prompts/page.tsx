'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'

interface Prompt {
  id: number
  name: string
  category: string
  usage_count: number
  rating: number
  created_at: string
}

export default function PromptsPage() {
  const [prompts, setPrompts] = useState<Prompt[]>([])
  const [loading, setLoading] = useState(true)
  const [newPromptName, setNewPromptName] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('general')

  useEffect(() => {
    fetchPrompts()
  }, [selectedCategory])

  const fetchPrompts = async () => {
    try {
      const data = await ApiClient.get(`/ai/templates?category=${selectedCategory}`)
      setPrompts(data)
    } catch (err) {
      console.error('Failed to fetch prompts', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Prompt Library</h1>

      <div className="mb-6 flex gap-4">
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-md"
        >
          <option value="general">General</option>
          <option value="content">Content</option>
          <option value="analysis">Analysis</option>
          <option value="creative">Creative</option>
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {prompts.map((prompt) => (
          <div key={prompt.id} className="bg-white rounded-lg shadow p-4">
            <h3 className="font-semibold">{prompt.name}</h3>
            <p className="text-sm text-gray-600 mb-2">{prompt.category}</p>
            <div className="flex justify-between text-xs text-gray-500">
              <span>Used {prompt.usage_count} times</span>
              <span>⭐ {prompt.rating.toFixed(1)}</span>
            </div>
          </div>
        ))}
      </div>

      {prompts.length === 0 && (
        <div className="text-center text-gray-600 py-8">
          No prompts in this category yet.
        </div>
      )}
    </div>
  )
}
