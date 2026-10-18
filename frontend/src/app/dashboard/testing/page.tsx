'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

export interface TestSuiteSummary {
  id: number
  name: string
  test_count: number
  passed: number
  failed: number
  skipped: number
  pass_rate: number | null
  coverage_percentage: number | null
  last_run_at: string | null
}

export interface TestCaseResult {
  id: number
  test_name: string
  status: 'passed' | 'failed' | 'skipped' | null
  duration_ms: number | null
  error_message: string | null
  run_at: string | null
}

type ResultFilter = 'failed' | 'all'

const REPORT_EXAMPLE = `POST /api/v1/test-reports/runs
{
  "suite": "Unit Tests",
  "coverage_percentage": 94.5,
  "results": [
    { "name": "test_login", "status": "passed", "duration_ms": 12.4 },
    { "name": "test_refund", "status": "failed", "duration_ms": 40, "error_message": "expected 200, got 500" }
  ]
}`

function formatTime(value: string | null): string {
  return value ? new Date(value).toLocaleString() : 'Never'
}

function formatPercent(value: number | null): string {
  return value === null ? '—' : `${value.toFixed(1)}%`
}

/** Results uploaded by CI for each test suite, with failures and their messages. */
export default function TestingPage() {
  const [suites, setSuites] = useState<TestSuiteSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState('')
  const [selected, setSelected] = useState<number | null>(null)
  const [filter, setFilter] = useState<ResultFilter>('failed')
  const [results, setResults] = useState<TestCaseResult[]>([])
  const [resultsError, setResultsError] = useState('')
  const [resultsLoading, setResultsLoading] = useState(false)

  useEffect(() => {
    ApiClient.get('/test-reports/suites')
      .then((list: TestSuiteSummary[]) => setSuites(list))
      .catch((err: unknown) => setLoadError(errorMessage(err, 'Test results could not be loaded.')))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (selected === null) return
    let active = true
    setResultsLoading(true)
    setResultsError('')
    const query = filter === 'failed' ? '?status=failed&limit=100' : '?limit=100'
    ApiClient.get(`/test-reports/suites/${selected}${query}`)
      .then((detail: { results: TestCaseResult[] }) => {
        if (active) setResults(detail.results)
      })
      .catch((err: unknown) => {
        if (active) setResultsError(errorMessage(err, 'Results could not be loaded.'))
      })
      .finally(() => {
        if (active) setResultsLoading(false)
      })
    return () => {
      active = false
    }
  }, [selected, filter])

  const totalTests = suites.reduce((sum, suite) => sum + suite.test_count, 0)
  const totalPassed = suites.reduce((sum, suite) => sum + suite.passed, 0)
  const totalFailed = suites.reduce((sum, suite) => sum + suite.failed, 0)
  const passRate = totalPassed + totalFailed > 0 ? (totalPassed / (totalPassed + totalFailed)) * 100 : null
  const coverageValues = suites.map((suite) => suite.coverage_percentage).filter((value): value is number => value !== null)
  const averageCoverage = coverageValues.length > 0
    ? coverageValues.reduce((sum, value) => sum + value, 0) / coverageValues.length
    : null

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Test Suites</h1>
        <p className="mt-1 text-sm text-gray-600">Results recorded by the CI pipeline for each suite.</p>
      </div>

      {loadError && <p role="alert" className="text-sm text-red-700">{loadError}</p>}

      {loading ? (
        <p role="status" className="text-sm text-gray-600">Loading test results...</p>
      ) : suites.length === 0 ? (
        <section className="rounded-lg bg-white p-6 shadow">
          <p className="text-gray-700">No test runs have been recorded yet.</p>
          <p className="mt-2 text-sm text-gray-600">Have CI report each run:</p>
          <pre className="mt-2 overflow-x-auto rounded bg-gray-900 p-3 text-xs text-gray-100">{REPORT_EXAMPLE}</pre>
        </section>
      ) : (
        <>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-lg bg-white p-6 shadow">
              <p className="text-sm text-gray-600">Total tests</p>
              <p className="text-3xl font-bold text-blue-600">{totalTests}</p>
            </div>
            <div className="rounded-lg bg-white p-6 shadow">
              <p className="text-sm text-gray-600">Pass rate</p>
              <p className="text-3xl font-bold text-green-600">{formatPercent(passRate)}</p>
            </div>
            <div className="rounded-lg bg-white p-6 shadow">
              <p className="text-sm text-gray-600">Average coverage</p>
              <p className="text-3xl font-bold text-purple-600">{formatPercent(averageCoverage)}</p>
            </div>
          </div>

          <section className="rounded-lg bg-white p-6 shadow">
            <h2 className="mb-4 text-xl font-semibold">Suites</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead className="text-gray-600">
                  <tr>
                    <th className="py-2 pr-3">Suite</th>
                    <th className="py-2 pr-3">Tests</th>
                    <th className="py-2 pr-3">Passed</th>
                    <th className="py-2 pr-3">Failed</th>
                    <th className="py-2 pr-3">Pass rate</th>
                    <th className="py-2 pr-3">Coverage</th>
                    <th className="py-2 pr-3">Last run</th>
                    <th className="py-2"></th>
                  </tr>
                </thead>
                <tbody>
                  {suites.map((suite) => (
                    <tr key={suite.id} className="border-t">
                      <td className="py-2 pr-3 font-medium">{suite.name}</td>
                      <td className="py-2 pr-3">{suite.test_count}</td>
                      <td className="py-2 pr-3 text-green-700">{suite.passed}</td>
                      <td className="py-2 pr-3 text-red-700">{suite.failed}</td>
                      <td className="py-2 pr-3">{formatPercent(suite.pass_rate)}</td>
                      <td className="py-2 pr-3">{formatPercent(suite.coverage_percentage)}</td>
                      <td className="py-2 pr-3">{formatTime(suite.last_run_at)}</td>
                      <td className="py-2">
                        <button
                          className="rounded border px-3 py-1 hover:bg-gray-50"
                          aria-pressed={selected === suite.id}
                          onClick={() => {
                            setSelected(suite.id)
                            setFilter('failed')
                          }}
                        >
                          View results
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          {selected !== null && (
            <section className="rounded-lg bg-white p-6 shadow">
              <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
                <h2 className="text-xl font-semibold">
                  {suites.find((suite) => suite.id === selected)?.name} results
                </h2>
                <div className="space-x-2 text-sm">
                  <button
                    className={`rounded border px-3 py-1 ${filter === 'failed' ? 'bg-gray-100' : ''}`}
                    onClick={() => setFilter('failed')}
                  >
                    Failures
                  </button>
                  <button
                    className={`rounded border px-3 py-1 ${filter === 'all' ? 'bg-gray-100' : ''}`}
                    onClick={() => setFilter('all')}
                  >
                    All results
                  </button>
                </div>
              </div>
              {resultsError ? (
                <p role="alert" className="text-sm text-red-700">{resultsError}</p>
              ) : resultsLoading ? (
                <p role="status" className="text-sm text-gray-600">Loading results...</p>
              ) : results.length === 0 ? (
                <p className="text-sm text-gray-600">{filter === 'failed' ? 'No failures in the latest runs.' : 'No results recorded.'}</p>
              ) : (
                <ul className="divide-y">
                  {results.map((item) => (
                    <li key={item.id} className="py-3">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <span className="font-mono text-sm">{item.test_name}</span>
                        <span className={`text-xs font-medium ${
                          item.status === 'failed' ? 'text-red-700' : item.status === 'passed' ? 'text-green-700' : 'text-gray-600'
                        }`}>
                          {item.status ?? 'unknown'}
                        </span>
                      </div>
                      {item.error_message && <p className="mt-1 text-sm text-red-800">{item.error_message}</p>}
                      <p className="mt-1 text-xs text-gray-500">
                        {item.duration_ms !== null ? `${item.duration_ms} ms · ` : ''}{formatTime(item.run_at)}
                      </p>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          )}
        </>
      )}
    </div>
  )
}
