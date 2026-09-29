'use client';

import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface AdminLog {
  id: number;
  admin_id: number;
  action: string;
  resource_type: string;
  created_at: string;
}

interface SystemAlert {
  id: number;
  alert_type: string;
  message: string;
  severity: string;
}

export default function AdminPage() {
  const [logs, setLogs] = useState<AdminLog[]>([]);
  const [alerts, setAlerts] = useState<SystemAlert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('/api/v1/admin/logs').then(r => r.json().catch(() => [])),
      fetch('/api/v1/system/alerts').then(r => r.json().catch(() => [])),
    ]).then(([logsData, alertsData]) => {
      setLogs(Array.isArray(logsData) ? logsData : []);
      setAlerts(Array.isArray(alertsData) ? alertsData : []);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-6">Loading admin dashboard...</div>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>

      {alerts.length > 0 && (
        <Card className="p-4 mb-6 bg-red-50 border-red-200">
          <h2 className="text-lg font-bold text-red-900 mb-4">System Alerts</h2>
          {alerts.map(alert => (
            <div key={alert.id} className="mb-2 p-2 bg-white rounded border-l-4 border-red-500">
              <p className="font-semibold">{alert.alert_type}</p>
              <p className="text-sm text-gray-600">{alert.message}</p>
              <span className={`text-xs font-bold ${
                alert.severity === 'critical' ? 'text-red-600' : 'text-yellow-600'
              }`}>
                {alert.severity.toUpperCase()}
              </span>
            </div>
          ))}
        </Card>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <Card className="p-6">
          <h2 className="text-lg font-bold mb-4">Quick Actions</h2>
          <div className="space-y-2">
            <Button className="w-full" variant="outline">Suspend User</Button>
            <Button className="w-full" variant="outline">Moderate Content</Button>
            <Button className="w-full" variant="outline">Export Data</Button>
            <Button className="w-full" variant="outline">Generate Report</Button>
          </div>
        </Card>

        <Card className="p-6">
          <h2 className="text-lg font-bold mb-4">System Status</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span>CPU Usage</span>
              <span className="font-bold">45.5%</span>
            </div>
            <div className="flex justify-between">
              <span>Memory Usage</span>
              <span className="font-bold">62.3%</span>
            </div>
            <div className="flex justify-between">
              <span>Disk Usage</span>
              <span className="font-bold">75.0%</span>
            </div>
            <div className="flex justify-between">
              <span>Uptime</span>
              <span className="font-bold text-green-600">99.8%</span>
            </div>
          </div>
        </Card>
      </div>

      <Card className="p-6">
        <h2 className="text-lg font-bold mb-4">Recent Admin Activity</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b">
                <th className="text-left p-2">Action</th>
                <th className="text-left p-2">Resource</th>
                <th className="text-left p-2">Date</th>
              </tr>
            </thead>
            <tbody>
              {logs.slice(0, 10).map(log => (
                <tr key={log.id} className="border-b hover:bg-gray-50">
                  <td className="p-2 font-semibold">{log.action}</td>
                  <td className="p-2">{log.resource_type}</td>
                  <td className="p-2 text-gray-600">
                    {new Date(log.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
