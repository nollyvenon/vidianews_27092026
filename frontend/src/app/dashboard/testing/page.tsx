'use client'

import { useState } from 'react'

export default function TestingPage() {
  const [suites] = useState([
    { id: 1, name: 'Unit Tests', tests: 250, passed: 245, failed: 5, coverage: 94.5 },
    { id: 2, name: 'Integration Tests', tests: 85, passed: 83, failed: 2, coverage: 89.2 },
    { id: 3, name: 'E2E Tests', tests: 42, passed: 41, failed: 1, coverage: 92.1 }
  ])

  const totalTests = suites.reduce((sum, s) => sum + s.tests, 0)
  const totalPassed = suites.reduce((sum, s) => sum + s.passed, 0)
  const passRate = ((totalPassed / totalTests) * 100).toFixed(1)

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Test Suites</h1>

      <div className="grid gap-6">
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm">Total Tests</p>
            <p className="text-3xl font-bold text-blue-600">{totalTests}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm">Pass Rate</p>
            <p className="text-3xl font-bold text-green-600">{passRate}%</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm">Avg Coverage</p>
            <p className="text-3xl font-bold text-purple-600">91.9%</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Test Suites</h2>
          <div className="space-y-4">
            {suites.map(suite => (
              <div key={suite.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <p className="font-semibold">{suite.name}</p>
                  <span className="text-sm font-medium text-gray-600">{suite.tests} tests</span>
                </div>
                <div className="grid grid-cols-3 gap-2 text-sm mb-2">
                  <span className="text-green-600">✓ {suite.passed} passed</span>
                  <span className="text-red-600">✗ {suite.failed} failed</span>
                  <span className="text-blue-600">Coverage: {suite.coverage}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Actions</h2>
          <div className="space-y-2">
            <button className="w-full px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50">Run All Tests</button>
            <button className="w-full px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50">Coverage Report</button>
          </div>
        </div>
      </div>
    </div>
  )
}
