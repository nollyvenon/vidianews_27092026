'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'

interface Workflow {
  id: number
  name: string
  description?: string
  status: string
  created_at: string
}

export default function WorkflowsPage() {
  const [workflows, setWorkflows] = useState<Workflow[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchWorkflows()
  }, [])

  const fetchWorkflows = async () => {
    try {
      const data = await ApiClient.get('/ai/workflows')
      setWorkflows(data)
    } catch (err) {
      console.error('Failed to fetch workflows', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">AI Workflows</h1>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
          Create Workflow
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {workflows.map((workflow) => (
          <div key={workflow.id} className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold">{workflow.name}</h3>
            {workflow.description && (
              <p className="text-gray-600 text-sm mt-2">{workflow.description}</p>
            )}
            <div className="mt-4 flex justify-between items-center">
              <span className={`px-3 py-1 rounded text-sm ${
                workflow.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100'
              }`}>
                {workflow.status}
              </span>
              <button className="text-blue-600 hover:underline">Edit</button>
            </div>
          </div>
        ))}
      </div>

      {workflows.length === 0 && (
        <div className="text-center text-gray-600 py-12">
          No workflows yet. Create one to automate your tasks.
        </div>
      )}
    </div>
  )
}
