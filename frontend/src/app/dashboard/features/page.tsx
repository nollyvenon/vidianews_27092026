'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface FeatureFlag {
  id: number
  name: string
  description: string | null
  enabled: boolean
  rollout_percentage: number
  target_segments: string[]
  created_at: string
}

interface AbTest {
  id: number
  name: string
  status: string
  metric_a: number
  metric_b: number
  confidence: number
  winner: string | null
}

/** Status shown on a flag: enabled for everyone, partly rolled out, or disabled. */
function statusOf(flag: FeatureFlag): 'enabled' | 'rollout' | 'disabled' {
  if (flag.enabled) return 'enabled'
  return flag.rollout_percentage > 0 ? 'rollout' : 'disabled'
}

const STATUS_CLASSES = {
  enabled: 'bg-green-100 text-green-800',
  rollout: 'bg-blue-100 text-blue-800',
  disabled: 'bg-gray-100 text-gray-800',
}

export default function FeaturesPage() {
  const [flags, setFlags] = useState<FeatureFlag[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [busyId, setBusyId] = useState<number | null>(null)
  const [creating, setCreating] = useState(false)
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [rollout, setRollout] = useState(0)
  const [tests, setTests] = useState<AbTest[] | null>(null)
  const [testsError, setTestsError] = useState<string | null>(null)
  const [testName, setTestName] = useState('')
  const [hypothesis, setHypothesis] = useState('')
  const [metric, setMetric] = useState('')

  const load = () =>
    ApiClient.get('/feature-flags')
      .then((data: FeatureFlag[]) => setFlags(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Feature flags could not be loaded.')))
      .finally(() => setLoading(false))

  const loadTests = () =>
    ApiClient.get('/ab-tests')
      .then((data: AbTest[]) => {
        setTests(Array.isArray(data) ? data : [])
        setTestsError(null)
      })
      .catch((err) => setTestsError(errorMessage(err, 'A/B tests could not be loaded.')))

  useEffect(() => {
    load()
    loadTests()
  }, [])

  const toggle = async (flag: FeatureFlag) => {
    setBusyId(flag.id)
    setError(null)
    try {
      const updated: FeatureFlag = await ApiClient.patch(`/feature-flags/${flag.id}`, {
        name: flag.name,
        description: flag.description,
        enabled: !flag.enabled,
        rollout_percentage: flag.rollout_percentage,
        target_segments: flag.target_segments,
      })
      setFlags((current) => current.map((item) => (item.id === flag.id ? updated : item)))
    } catch (err) {
      setError(errorMessage(err, 'The flag could not be changed.'))
    } finally {
      setBusyId(null)
    }
  }

  const create = async (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    try {
      await ApiClient.post('/feature-flags', {
        name: name.trim(),
        description: description.trim() || null,
        enabled: false,
        rollout_percentage: rollout,
        target_segments: [],
      })
      setName('')
      setDescription('')
      setRollout(0)
      setCreating(false)
      setLoading(true)
      await load()
    } catch (err) {
      setError(errorMessage(err, 'The flag could not be created.'))
    }
  }

  const createTest = async (event: FormEvent) => {
    event.preventDefault()
    setTestsError(null)
    try {
      await ApiClient.post('/ab-tests', { name: testName.trim(), hypothesis: hypothesis.trim(), metric_to_optimize: metric.trim() })
      setTestName('')
      setHypothesis('')
      setMetric('')
      await loadTests()
    } catch (err) {
      setTestsError(errorMessage(err, 'The A/B test could not be created.'))
    }
  }

  const changeTest = async (test: AbTest, action: 'start' | 'end') => {
    setTestsError(null)
    try {
      await ApiClient.post(`/ab-tests/${test.id}/${action}`, {})
      await loadTests()
    } catch (err) {
      setTestsError(errorMessage(err, 'The A/B test could not be changed.'))
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Feature Flags</h1>
      {error && <p role="alert" className="mb-4 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Active Flags</h2>
            <button
              type="button"
              onClick={() => setCreating((open) => !open)}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
            >
              + New Flag
            </button>
          </div>

          {creating && (
            <form onSubmit={create} className="mb-6 border rounded-lg p-4 space-y-3">
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Flag name (for example new_checkout)"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
              <label className="block text-sm">
                <span className="block mb-1">Rollout percentage</span>
                <input
                  type="number"
                  min={0}
                  max={100}
                  className="w-full border rounded px-3 py-2"
                  value={rollout}
                  onChange={(e) => setRollout(Number(e.target.value))}
                />
              </label>
              <button type="submit" disabled={!name.trim()} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">
                Create flag
              </button>
            </form>
          )}

          {loading ? (
            <p className="text-gray-500">Loading flags…</p>
          ) : flags.length === 0 ? (
            <p className="text-gray-500">No feature flags yet.</p>
          ) : (
            <div className="space-y-3">
              {flags.map((flag) => {
                const status = statusOf(flag)
                return (
                  <div key={flag.id} className="border rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <p className="font-semibold">{flag.name}</p>
                      <span className={`px-3 py-1 rounded text-sm font-medium ${STATUS_CLASSES[status]}`}>{status}</span>
                    </div>
                    {flag.description && <p className="text-sm text-gray-600 mb-2">{flag.description}</p>}
                    {flag.rollout_percentage > 0 && (
                      <div className="text-sm text-gray-600 mb-2">Rollout: {flag.rollout_percentage}%</div>
                    )}
                    <button
                      type="button"
                      disabled={busyId === flag.id}
                      onClick={() => toggle(flag)}
                      className="px-3 py-1 text-sm border border-blue-600 text-blue-600 rounded hover:bg-blue-50 disabled:opacity-50"
                    >
                      {flag.enabled ? 'Disable' : 'Enable'}
                    </button>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">A/B Tests</h2>
          {testsError && <p role="alert" className="mb-3 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{testsError}</p>}
          {tests === null ? (
            <p className="text-gray-500">Loading A/B tests…</p>
          ) : tests.length === 0 ? (
            <p className="text-gray-500 mb-4">No A/B tests yet.</p>
          ) : (
            <div className="space-y-3 mb-6">
              {tests.map((test) => (
                <div key={test.id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-center">
                    <p className="font-medium">{test.name}</p>
                    <span className="text-sm text-gray-600">{test.status}</span>
                  </div>
                  <p className="text-sm text-gray-600">
                    Variant A {test.metric_a.toFixed(2)} · Variant B {test.metric_b.toFixed(2)} · Confidence {test.confidence.toFixed(1)}%
                    {test.winner ? ` · Winner: ${test.winner}` : ''}
                  </p>
                  <div className="mt-2 flex gap-2">
                    {test.status !== 'running' && test.status !== 'completed' && (
                      <button type="button" onClick={() => changeTest(test, 'start')} className="px-3 py-1 text-sm border border-blue-600 text-blue-600 rounded">
                        Start
                      </button>
                    )}
                    {test.status === 'running' && (
                      <button type="button" onClick={() => changeTest(test, 'end')} className="px-3 py-1 text-sm border border-gray-600 text-gray-700 rounded">
                        End
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}

          <form onSubmit={createTest} className="grid grid-cols-1 md:grid-cols-4 gap-2 items-end">
            <input className="border rounded px-2 py-1" placeholder="Test name" value={testName} onChange={(e) => setTestName(e.target.value)} required />
            <input className="border rounded px-2 py-1" placeholder="Hypothesis" value={hypothesis} onChange={(e) => setHypothesis(e.target.value)} required />
            <input className="border rounded px-2 py-1" placeholder="Metric to optimize" value={metric} onChange={(e) => setMetric(e.target.value)} required />
            <button type="submit" disabled={!testName.trim() || !hypothesis.trim() || !metric.trim()} className="px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50">
              Create A/B test
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
