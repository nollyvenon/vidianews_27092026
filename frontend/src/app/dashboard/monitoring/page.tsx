'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface HealthMetrics {
  cpu_percent: number
  memory_percent: number
  disk_percent: number
  database_latency_ms: number
}

interface HealthCheck {
  name: string
  status: string
  latency_ms?: number
  pending?: number
  running?: number
  failed?: number
}

interface HealthReport {
  metrics: HealthMetrics
  checks: HealthCheck[]
}

interface SystemAlert {
  id: number
  alert_type: string
  severity: string
  message: string
  created_at: string
}

const HIGH_SEVERITIES = ['high', 'critical']

/** Live figures for this server; a value over its threshold is flagged as a warning. */
function metricsFrom(metrics: HealthMetrics) {
  return [
    { type: 'CPU Usage', value: `${metrics.cpu_percent.toFixed(0)}%`, warn: metrics.cpu_percent > 80 },
    { type: 'Memory Usage', value: `${metrics.memory_percent.toFixed(0)}%`, warn: metrics.memory_percent > 80 },
    { type: 'Disk Usage', value: `${metrics.disk_percent.toFixed(0)}%`, warn: metrics.disk_percent > 90 },
    { type: 'Database Latency', value: `${metrics.database_latency_ms.toFixed(1)}ms`, warn: metrics.database_latency_ms > 200 },
  ]
}

export default function MonitoringPage() {
  const [report, setReport] = useState<HealthReport | null>(null)
  const [reportError, setReportError] = useState<string | null>(null)
  const [alerts, setAlerts] = useState<SystemAlert[]>([])
  const [alertsError, setAlertsError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let active = true
    Promise.allSettled([ApiClient.get('/system/health/checks'), ApiClient.get('/system/alerts')]).then(
      ([reportResult, alertsResult]) => {
        if (!active) return
        if (reportResult.status === 'fulfilled') setReport(reportResult.value as HealthReport)
        else setReportError(errorMessage(reportResult.reason, 'System health could not be loaded.'))
        if (alertsResult.status === 'fulfilled') setAlerts(Array.isArray(alertsResult.value) ? alertsResult.value : [])
        else setAlertsError(errorMessage(alertsResult.reason, 'Alerts could not be loaded.'))
        setLoading(false)
      },
    )
    return () => {
      active = false
    }
  }, [])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">System Monitoring</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Key Metrics</h2>
          {loading ? (
            <p className="text-gray-500">Loading metrics…</p>
          ) : report ? (
            <div className="grid grid-cols-2 gap-4">
              {metricsFrom(report.metrics).map((m) => (
                <div key={m.type} className="border rounded-lg p-4">
                  <p className="text-sm text-gray-600">{m.type}</p>
                  <p className="text-2xl font-bold mt-1">{m.value}</p>
                  <span className={`inline-block mt-2 px-2 py-1 rounded text-xs ${m.warn ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}`}>
                    {m.warn ? 'warning' : 'good'}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p role="alert" className="text-red-700">{reportError}</p>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Active Alerts</h2>
          {alertsError && <p role="alert" className="mb-3 text-red-700">{alertsError}</p>}
          {!loading && !alertsError && alerts.length === 0 && <p className="text-gray-500">No active alerts.</p>}
          <div className="space-y-3">
            {alerts.map((a) => (
              <div
                key={a.id}
                className={`border-l-4 pl-4 py-2 ${HIGH_SEVERITIES.includes(a.severity) ? 'border-red-500 bg-red-50' : 'border-yellow-500 bg-yellow-50'}`}
              >
                <div className="flex justify-between items-start">
                  <p className="font-medium text-sm">{a.message}</p>
                  <span className="text-xs text-gray-500 whitespace-nowrap ml-4">{new Date(a.created_at).toLocaleString()}</span>
                </div>
                <p className="text-xs text-gray-600">{a.alert_type} · {a.severity}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Health Checks</h2>
          {report && (
            <div className="space-y-2 text-sm">
              {report.checks.map((check) => (
                <div key={check.name} className="flex justify-between items-center">
                  <span>{check.name}</span>
                  <span className={check.status === 'healthy' ? 'text-green-600' : 'text-yellow-700'}>
                    {check.status === 'healthy' ? '✓ Healthy' : '⚠ Degraded'}
                    {check.name === 'Background jobs'
                      ? ` · ${check.pending ?? 0} pending · ${check.running ?? 0} running · ${check.failed ?? 0} failed`
                      : check.latency_ms !== undefined
                        ? ` · ${check.latency_ms.toFixed(1)}ms`
                        : ''}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
