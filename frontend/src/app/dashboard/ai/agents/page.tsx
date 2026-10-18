'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'
import { slugify } from '@/components/content/content-form'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

interface Agent {
  id: number
  name: string
  slug: string
  description: string | null
  status: string
  execution_count: number
  success_rate: number
  created_at: string
}

const STATUS_CLASSES: Record<string, string> = {
  active: 'bg-green-100 text-green-800',
  paused: 'bg-yellow-100 text-yellow-800',
  draft: 'bg-gray-100 text-gray-800',
}

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [name, setName] = useState('')
  const [slug, setSlug] = useState('')
  const [slugEdited, setSlugEdited] = useState(false)
  const [description, setDescription] = useState('')
  const [systemPrompt, setSystemPrompt] = useState('')

  const load = () =>
    ApiClient.get('/ai/agents')
      .then((data: Agent[]) => setAgents(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Agents could not be loaded.')))
      .finally(() => setLoading(false))

  useEffect(() => {
    load()
  }, [])

  const create = async (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    try {
      await ApiClient.post('/ai/agents', {
        name: name.trim(),
        slug: slug.trim(),
        description: description.trim() || null,
        system_prompt: systemPrompt.trim() || null,
      })
      setName('')
      setSlug('')
      setSlugEdited(false)
      setDescription('')
      setSystemPrompt('')
      await load()
    } catch (err) {
      setError(errorMessage(err, 'The agent could not be created.'))
    }
  }

  const setStatus = async (agent: Agent, action: 'activate' | 'pause') => {
    setError(null)
    try {
      await ApiClient.post(`/ai/agents/${agent.id}/${action}`, {})
      await load()
    } catch (err) {
      setError(errorMessage(err, 'The agent status could not be changed.'))
    }
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">AI Agents</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

      <Card>
        <CardHeader>
          <CardTitle>New agent</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={create} className="space-y-3">
            <Input
              placeholder="Name"
              value={name}
              onChange={(e) => {
                setName(e.target.value)
                if (!slugEdited) setSlug(slugify(e.target.value))
              }}
              required
            />
            <Input
              placeholder="Slug"
              value={slug}
              onChange={(e) => {
                setSlugEdited(true)
                setSlug(e.target.value)
              }}
              required
            />
            <Input placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
            <Textarea placeholder="System prompt" rows={3} value={systemPrompt} onChange={(e) => setSystemPrompt(e.target.value)} />
            <Button type="submit" disabled={!name.trim() || !slug.trim()}>Create agent</Button>
          </form>
        </CardContent>
      </Card>

      {loading ? (
        <p className="text-gray-500">Loading agents…</p>
      ) : agents.length === 0 ? (
        <p className="text-gray-500">No agents yet. Create one above.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {agents.map((agent) => (
            <Card key={agent.id}>
              <CardContent className="p-4 space-y-2">
                <div className="flex justify-between items-center">
                  <h2 className="font-semibold">{agent.name}</h2>
                  <span className={`px-2 py-1 rounded text-xs ${STATUS_CLASSES[agent.status] ?? 'bg-gray-100'}`}>{agent.status}</span>
                </div>
                {agent.description && <p className="text-sm text-gray-600">{agent.description}</p>}
                <p className="text-xs text-gray-500">{agent.execution_count} runs · {agent.success_rate}% success</p>
                <div className="flex gap-2">
                  {agent.status !== 'active' && (
                    <Button size="sm" variant="outline" onClick={() => setStatus(agent, 'activate')}>Activate</Button>
                  )}
                  {agent.status === 'active' && (
                    <Button size="sm" variant="outline" onClick={() => setStatus(agent, 'pause')}>Pause</Button>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
