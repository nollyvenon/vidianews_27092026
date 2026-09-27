'use client'
import { useState, useEffect } from 'react'

export default function CompliancePage() {
  const [complianceStatus, setComplianceStatus] = useState(null)
  const [auditLogs, setAuditLogs] = useState([])

  useEffect(() => {
    fetchCompliance()
    fetchAuditLogs()
  }, [])

  const fetchCompliance = async () => {
    try {
      const res = await fetch('/api/v1/compliance/status')
      if (res.ok) {
        const data = await res.json()
        setComplianceStatus(data)
      }
    } catch (err) {
      console.error('Failed to fetch compliance:', err)
    }
  }

  const fetchAuditLogs = async () => {
    try {
      const res = await fetch('/api/v1/audit/logs')
      if (res.ok) {
        const data = await res.json()
        setAuditLogs(data)
      }
    } catch (err) {
      console.error('Failed to fetch audit logs:', err)
    }
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Compliance & Legal</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-2">GDPR</h3>
          <p className={`text-2xl font-bold ${complianceStatus?.gdpr ? 'text-green-600' : 'text-red-600'}`}>
            {complianceStatus?.gdpr ? '✓ Compliant' : '✗ Non-compliant'}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-2">CCPA</h3>
          <p className={`text-2xl font-bold ${complianceStatus?.ccpa ? 'text-green-600' : 'text-red-600'}`}>
            {complianceStatus?.ccpa ? '✓ Compliant' : '✗ Non-compliant'}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-2">Overall Status</h3>
          <p className={`text-2xl font-bold ${complianceStatus?.compliant ? 'text-green-600' : 'text-yellow-600'}`}>
            {complianceStatus?.compliant ? 'Good' : 'Review Required'}
          </p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">Audit Trail</h2>
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {auditLogs.map(log => (
            <div key={log.id} className="py-2 border-b last:border-b-0">
              <p className="font-semibold">{log.action}</p>
              <p className="text-sm text-gray-600">{log.resource} • {new Date(log.created_at).toLocaleString()}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
