'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface TestSuite {
  id: number
  name: string
  test_count: number
  passed: number
  failed: number
  skipped: number
  coverage_percentage: number
  last_run_at: string | null
}

/** Recorded results for each test suite, with totals across the suites. */
export default function TestingPage() {
  const [suites, setSuites] = useState<TestSuite[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    ApiClient.get('/testing/suites')
      .then((data: TestSuite[]) => setSuites(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Test results could not be loaded.')));
  }, []);

  const totalTests = (suites ?? []).reduce((sum, suite) => sum + suite.test_count, 0);
  const totalPassed = (suites ?? []).reduce((sum, suite) => sum + suite.passed, 0);
  const passRate = totalTests > 0 ? ((totalPassed / totalTests) * 100).toFixed(1) : '0.0';
  const averageCoverage = suites && suites.length > 0
    ? (suites.reduce((sum, suite) => sum + suite.coverage_percentage, 0) / suites.length).toFixed(1)
    : '0.0';

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Test Suites</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3 mb-6">{error}</p>}

      <div className="grid gap-6">
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm">Total Tests</p>
            <p className="text-3xl font-bold text-blue-600">{totalTests.toLocaleString()}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm">Pass Rate</p>
            <p className="text-3xl font-bold text-green-600">{passRate}%</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm">Avg Coverage</p>
            <p className="text-3xl font-bold text-purple-600">{averageCoverage}%</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Test Suites</h2>
          {suites === null && !error ? (
            <p className="text-gray-500">Loading test suites…</p>
          ) : suites && suites.length === 0 ? (
            <p className="text-gray-500">No test suites have been recorded yet.</p>
          ) : suites ? (
            <div className="space-y-4">
              {suites.map((suite) => (
                <div key={suite.id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <p className="font-semibold">{suite.name}</p>
                    <span className="text-sm font-medium text-gray-600">{suite.test_count.toLocaleString()} tests</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 text-sm mb-2">
                    <span className="text-green-600">✓ {suite.passed} passed</span>
                    <span className="text-red-600">✗ {suite.failed} failed</span>
                    <span className="text-blue-600">Coverage: {suite.coverage_percentage}%</span>
                  </div>
                  <p className="text-xs text-gray-500">
                    {suite.last_run_at ? `Last run ${new Date(suite.last_run_at).toLocaleString()}` : 'Not run yet'}
                  </p>
                </div>
              ))}
            </div>
          ) : null}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Actions</h2>
          <p className="text-sm text-gray-600 mb-3">
            This page shows results recorded through the testing API. Starting a test run from here is not available.
          </p>
          <div className="space-y-2">
            <button type="button" disabled className="w-full px-4 py-2 border border-gray-300 text-gray-400 rounded">Run All Tests</button>
            <button type="button" disabled className="w-full px-4 py-2 border border-gray-300 text-gray-400 rounded">Coverage Report</button>
          </div>
        </div>
      </div>
    </div>
  );
}
