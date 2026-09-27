'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'

interface Report {
  id: number
  report_type: string
  title: string
  created_at: string
}

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)
  const [newTitle, setNewTitle] = useState('')
  const [selectedType, setSelectedType] = useState('performance')

  useEffect(() => {
    fetchReports()
  }, [])

  const fetchReports = async () => {
    try {
      const data = await ApiClient.get('/system/reports')
      setReports(data)
    } catch (err) {
      console.error('Failed to fetch reports', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateReport = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newTitle) return

    try {
      const report = await ApiClient.post('/system/reports', {
        report_type: selectedType,
        title: newTitle,
        data: {},
      })
      setReports([...reports, report])
      setNewTitle('')
    } catch (err) {
      console.error('Failed to create report', err)
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Reports</h1>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Create Report</h2>
        <form onSubmit={handleCreateReport} className="flex gap-2 mb-4">
          <input
            type="text"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="Report title"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md"
          />
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md"
          >
            <option value="performance">Performance</option>
            <option value="engagement">Engagement</option>
            <option value="revenue">Revenue</option>
            <option value="compliance">Compliance</option>
          </select>
          <button
            type="submit"
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Create
          </button>
        </form>
      </div>

      {loading ? (
        <div className="text-gray-600">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {reports.map((report) => (
            <div key={report.id} className="bg-white rounded-lg shadow p-4">
              <h3 className="font-semibold">{report.title}</h3>
              <p className="text-sm text-gray-600">{report.report_type}</p>
              <p className="text-xs text-gray-500 mt-2">
                {new Date(report.created_at).toLocaleDateString()}
              </p>
              <button className="mt-3 text-blue-600 hover:underline text-sm">
                Download
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
