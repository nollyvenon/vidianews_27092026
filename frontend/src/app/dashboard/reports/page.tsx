'use client'
import { useState, useEffect } from 'react'

export default function ReportsPage() {
  const [reports, setReports] = useState([])
  const [reportType, setReportType] = useState('views')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchReports()
  }, [])

  const fetchReports = async () => {
    try {
      const res = await fetch('/api/v1/reports')
      if (res.ok) {
        const data = await res.json()
        setReports(data)
      }
    } catch (err) {
      console.error('Failed to fetch reports:', err)
    }
  }

  const handleGenerateReport = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/v1/reports', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ report_type: reportType })
      })
      if (res.ok) {
        fetchReports()
      }
    } catch (err) {
      console.error('Failed to generate report:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async () => {
    try {
      const res = await fetch('/api/v1/data-export', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ export_type: 'csv' })
      })
      if (res.ok) {
        const data = await res.json()
        console.log('Export requested:', data.id)
      }
    } catch (err) {
      console.error('Failed to request export:', err)
    }
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Reports & Analytics</h1>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Generate New Report</h2>
        <div className="flex gap-4">
          <select 
            value={reportType}
            onChange={(e) => setReportType(e.target.value)}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="views">View Analytics</option>
            <option value="engagement">Engagement</option>
            <option value="revenue">Revenue</option>
            <option value="growth">Growth</option>
          </select>
          <button 
            onClick={handleGenerateReport}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Generating...' : 'Generate Report'}
          </button>
          <button 
            onClick={handleExport}
            className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
          >
            Export Data
          </button>
        </div>
      </div>

      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Recent Reports</h2>
        {reports.map(report => (
          <div key={report.id} className="bg-white rounded-lg shadow p-4">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-semibold text-lg">{report.type} Report</h3>
                <p className="text-sm text-gray-600">Generated: {new Date(report.generated).toLocaleDateString()}</p>
              </div>
              <button className="text-blue-600 hover:underline">Download</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
