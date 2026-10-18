'use client'

import { FormEvent, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

const lines = (value: string) => value.split('\n').map((item) => item.trim()).filter(Boolean)

export default function CreateCoursePage() {
  const router = useRouter()
  const [form, setForm] = useState({
    title: '',
    description: '',
    category: 'general',
    price: '0',
    difficulty_level: 'beginner',
    language: 'en',
    prerequisites: '',
    learning_objectives: '',
  })
  const [error, setError] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)

  const update = (field: keyof typeof form, value: string) => setForm((prev) => ({ ...prev, [field]: value }))

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    setSaving(true)
    try {
      const course = await ApiClient.post('/courses', {
        title: form.title.trim(),
        description: form.description.trim() || null,
        category: form.category.trim() || 'general',
        price: Number(form.price) || 0,
        difficulty_level: form.difficulty_level,
        language: form.language.trim() || 'en',
        prerequisites: lines(form.prerequisites),
        learning_objectives: lines(form.learning_objectives),
      })
      router.push(`/dashboard/courses/${course.id}`)
    } catch (err) {
      setError(errorMessage(err, 'The course could not be created.'))
    } finally {
      setSaving(false)
    }
  }

  const input = 'w-full border rounded-md px-3 py-2'

  return (
    <div className="p-6 space-y-6 max-w-3xl">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Create course</h1>
        <Link href="/dashboard/courses" className="text-blue-600 hover:underline">Back to courses</Link>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
        {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

        <label className="block">
          <span className="block text-sm font-medium mb-1">Title</span>
          <input className={input} value={form.title} onChange={(e) => update('title', e.target.value)} required />
        </label>
        <label className="block">
          <span className="block text-sm font-medium mb-1">Description</span>
          <textarea className={input} rows={3} value={form.description} onChange={(e) => update('description', e.target.value)} />
        </label>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <label className="block">
            <span className="block text-sm font-medium mb-1">Category</span>
            <input className={input} value={form.category} onChange={(e) => update('category', e.target.value)} />
          </label>
          <label className="block">
            <span className="block text-sm font-medium mb-1">Price (USD)</span>
            <input className={input} type="number" min="0" step="0.01" value={form.price} onChange={(e) => update('price', e.target.value)} />
          </label>
          <label className="block">
            <span className="block text-sm font-medium mb-1">Level</span>
            <select className={input} value={form.difficulty_level} onChange={(e) => update('difficulty_level', e.target.value)}>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </label>
        </div>
        <label className="block">
          <span className="block text-sm font-medium mb-1">Learning objectives (one per line)</span>
          <textarea className={input} rows={3} value={form.learning_objectives} onChange={(e) => update('learning_objectives', e.target.value)} />
        </label>
        <label className="block">
          <span className="block text-sm font-medium mb-1">Prerequisites (one per line)</span>
          <textarea className={input} rows={2} value={form.prerequisites} onChange={(e) => update('prerequisites', e.target.value)} />
        </label>

        <button type="submit" disabled={saving} className="px-6 py-2 bg-blue-600 text-white rounded-md disabled:opacity-50">
          {saving ? 'Creating…' : 'Create course'}
        </button>
      </form>
    </div>
  )
}
