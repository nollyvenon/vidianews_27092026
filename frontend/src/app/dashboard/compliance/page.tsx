'use client'

import { useState } from 'react'

export default function CompliancePage() {
  const [reports] = useState([
    { id: 1, type: 'GDPR', period: 'Q3 2026', status: 'completed', date: '2026-09-27' },
    { id: 2, type: 'SOC 2', period: 'Q2 2026', status: 'completed', date: '2026-06-30' },
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Compliance</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-green-600">2</div>
          <div className="text-gray-600">Reports Completed</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-blue-600">0</div>
          <div className="text-gray-600">Findings</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-green-600">100%</div>
          <div className="text-gray-600">Compliance</div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow">
        <table className="w-full">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold">Type</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Period</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Status</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Date</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {reports.map((r) => (
              <tr key={r.id}>
                <td className="px-6 py-3 text-sm font-medium">{r.type}</td>
                <td className="px-6 py-3 text-sm">{r.period}</td>
                <td className="px-6 py-3 text-sm">
                  <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                    {r.status}
                  </span>
                </td>
                <td className="px-6 py-3 text-sm text-gray-600">{r.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
