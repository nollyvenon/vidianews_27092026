'use client';

import React, { useEffect, useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';
import {
  AlertCircle,
  Shield,
  Eye,
  AlertTriangle,
  FileText,
  Users,
  Bell,
  BarChart3,
} from 'lucide-react';

interface AuditLog {
  id: number;
  user_id: number;
  action: string;
  severity: string | null;
  created_at: string;
}

interface ModerationItem {
  id: number;
  content_id: number;
  content_type: string;
  status: string;
  confidence_score: number;
  created_at: string;
}

interface Alert {
  id: number;
  notification_type: string;
  title: string;
  message: string;
  read: boolean;
}

interface Report {
  id: number;
  name: string;
  report_type: string;
  status: string;
  generated_at: string | null;
  created_at: string;
}

interface RateLimit {
  id: number;
  endpoint: string;
  requests_per_minute: number;
  requests_per_hour: number;
  requests_per_day: number;
  burst_limit: number;
}

interface Overview {
  total_subscribers: number;
}

const SEVERITY_CLASSES: Record<string, string> = {
  critical: 'bg-red-100 text-red-800',
  high: 'bg-red-100 text-red-800',
  medium: 'bg-yellow-100 text-yellow-800',
  low: 'bg-green-100 text-green-800',
  info: 'bg-green-100 text-green-800',
};

const MODERATION_CLASSES: Record<string, string> = {
  pending: 'bg-yellow-100 text-yellow-800',
  flagged: 'bg-red-100 text-red-800',
  appealed: 'bg-orange-100 text-orange-800',
};

const REPORT_CLASSES: Record<string, string> = {
  completed: 'bg-green-100 text-green-800',
  processing: 'bg-blue-100 text-blue-800',
};

const ALERT_ICONS: Record<string, React.ReactNode> = {
  alert: <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />,
  error: <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />,
  warning: <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />,
  info: <Bell className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />,
};

const ERROR_CLASS = 'bg-red-50 border border-red-200 text-red-700 rounded-md p-3';

/** Security audit trail, moderation queue, system alerts, generated reports and rate limits. */
export default function EnterprisePage() {
  const [activeTab, setActiveTab] = useState('security');
  const [overview, setOverview] = useState<Overview | null>(null);
  const [auditLogs, setAuditLogs] = useState<AuditLog[] | null>(null);
  const [auditError, setAuditError] = useState<string | null>(null);
  const [moderation, setModeration] = useState<ModerationItem[] | null>(null);
  const [moderationError, setModerationError] = useState<string | null>(null);
  const [alerts, setAlerts] = useState<Alert[] | null>(null);
  const [alertsError, setAlertsError] = useState<string | null>(null);
  const [unreadCount, setUnreadCount] = useState<number | null>(null);
  const [reports, setReports] = useState<Report[] | null>(null);
  const [reportsError, setReportsError] = useState<string | null>(null);
  const [limits, setLimits] = useState<RateLimit[] | null>(null);
  const [limitsError, setLimitsError] = useState<string | null>(null);

  useEffect(() => {
    const list = <T,>(path: string, setItems: (rows: T[]) => void, setFailure: (message: string) => void, fallback: string) =>
      ApiClient.get(path)
        .then((data: T[]) => setItems(Array.isArray(data) ? data : []))
        .catch((err) => setFailure(errorMessage(err, fallback)));

    ApiClient.get('/subscribers/overview')
      .then((data: Overview) => setOverview(data))
      .catch(() => setOverview(null));
    list<AuditLog>('/security/audit-logs?days=30&limit=500', setAuditLogs, setAuditError, 'Audit logs could not be loaded.');
    list<ModerationItem>('/moderation/queue/pending?limit=50', setModeration, setModerationError, 'The moderation queue could not be loaded.');
    list<Alert>('/enterprise/notifications/?limit=50', setAlerts, setAlertsError, 'Alerts could not be loaded.');
    list<Report>('/reports/?limit=50', setReports, setReportsError, 'Reports could not be loaded.');
    list<RateLimit>('/rate-limits/configs', setLimits, setLimitsError, 'Rate limits could not be loaded.');
    ApiClient.get('/enterprise/notifications/?unread_only=true&limit=500')
      .then((data: Alert[]) => setUnreadCount(Array.isArray(data) ? data.length : 0))
      .catch(() => setUnreadCount(null));
  }, []);

  const stats = [
    { label: 'Subscribers', value: overview ? overview.total_subscribers.toLocaleString() : '—', icon: Users, color: 'bg-blue-100' },
    { label: 'Pending Moderation', value: moderation ? moderation.length.toLocaleString() : '—', icon: AlertCircle, color: 'bg-orange-100' },
    { label: 'Security Events', value: auditLogs ? auditLogs.length.toLocaleString() : '—', icon: Shield, color: 'bg-red-100' },
    { label: 'Unread Alerts', value: unreadCount !== null ? unreadCount.toLocaleString() : '—', icon: Bell, color: 'bg-yellow-100' },
  ];

  return (
    <div className="space-y-6 p-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Enterprise Dashboard</h1>
          <p className="text-gray-600 mt-2">Security, Compliance & Operations</p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.label}>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">{stat.label}</p>
                    <p className="text-2xl font-bold mt-1">{stat.value}</p>
                  </div>
                  <div className={`${stat.color} p-3 rounded-lg`}>
                    <Icon className="w-6 h-6" />
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="security" className="flex items-center gap-2">
            <Shield className="w-4 h-4" />
            <span className="hidden sm:inline">Security</span>
          </TabsTrigger>
          <TabsTrigger value="moderation" className="flex items-center gap-2">
            <Eye className="w-4 h-4" />
            <span className="hidden sm:inline">Moderation</span>
          </TabsTrigger>
          <TabsTrigger value="notifications" className="flex items-center gap-2">
            <Bell className="w-4 h-4" />
            <span className="hidden sm:inline">Alerts</span>
          </TabsTrigger>
          <TabsTrigger value="reports" className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            <span className="hidden sm:inline">Reports</span>
          </TabsTrigger>
          <TabsTrigger value="rateLimits" className="flex items-center gap-2">
            <BarChart3 className="w-4 h-4" />
            <span className="hidden sm:inline">Limits</span>
          </TabsTrigger>
        </TabsList>

        {/* Security Tab */}
        <TabsContent value="security" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Security Audit Logs</CardTitle>
              <CardDescription>Recent user actions and security events</CardDescription>
            </CardHeader>
            <CardContent>
              {auditError && <p role="alert" className={ERROR_CLASS}>{auditError}</p>}
              {auditLogs === null && !auditError ? (
                <p className="text-gray-500">Loading audit logs…</p>
              ) : auditLogs && auditLogs.length === 0 ? (
                <p className="text-gray-500">No security events in the last 30 days.</p>
              ) : auditLogs ? (
                <div className="space-y-2">
                  {auditLogs.map((log) => (
                    <div key={log.id} className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <p className="font-medium">{log.action}</p>
                        <p className="text-sm text-gray-600">User: {log.user_id}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-600">{new Date(log.created_at).toLocaleString()}</p>
                        <span className={`inline-block px-2 py-1 text-xs rounded mt-1 ${SEVERITY_CLASSES[log.severity ?? ''] ?? 'bg-gray-100 text-gray-800'}`}>
                          {log.severity ?? 'unrated'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : null}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Moderation Tab */}
        <TabsContent value="moderation" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Content Moderation Queue</CardTitle>
              <CardDescription>Items pending review and compliance checks</CardDescription>
            </CardHeader>
            <CardContent>
              {moderationError && <p role="alert" className={ERROR_CLASS}>{moderationError}</p>}
              {moderation === null && !moderationError ? (
                <p className="text-gray-500">Loading the queue…</p>
              ) : moderation && moderation.length === 0 ? (
                <p className="text-gray-500">The moderation queue is empty.</p>
              ) : moderation ? (
                <div className="space-y-2">
                  {moderation.map((item) => {
                    const percent = Math.round(item.confidence_score * 100);
                    return (
                      <div key={item.id} className="flex items-center justify-between p-3 border rounded-lg">
                        <div className="flex-1">
                          <p className="font-medium">{`${item.content_type} #${item.content_id}`}</p>
                          <p className="text-sm text-gray-600">{item.content_type}</p>
                        </div>
                        <div className="text-right">
                          <div className="mb-2">
                            <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
                              <div className="h-full bg-blue-600" style={{ width: `${percent}%` }} />
                            </div>
                            <p className="text-xs text-gray-600 mt-1">{percent}%</p>
                          </div>
                          <span className={`inline-block px-2 py-1 text-xs rounded ${MODERATION_CLASSES[item.status] ?? 'bg-gray-100 text-gray-800'}`}>
                            {item.status}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : null}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Notifications Tab */}
        <TabsContent value="notifications" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>System Alerts</CardTitle>
              <CardDescription>Active alerts and notifications</CardDescription>
            </CardHeader>
            <CardContent>
              {alertsError && <p role="alert" className={ERROR_CLASS}>{alertsError}</p>}
              {alerts === null && !alertsError ? (
                <p className="text-gray-500">Loading alerts…</p>
              ) : alerts && alerts.length === 0 ? (
                <p className="text-gray-500">No alerts.</p>
              ) : alerts ? (
                <div className="space-y-2">
                  {alerts.map((notif) => (
                    <div key={notif.id} className={`p-3 border rounded-lg ${notif.read ? 'bg-gray-50' : 'bg-blue-50'}`}>
                      <div className="flex items-start gap-3">
                        {ALERT_ICONS[notif.notification_type] ?? <Bell className="w-5 h-5 text-gray-500 flex-shrink-0 mt-0.5" />}
                        <div className="flex-1">
                          <p className="font-medium">{notif.title}</p>
                          <p className="text-sm text-gray-600">{notif.message}</p>
                        </div>
                        {!notif.read && <div className="w-2 h-2 bg-blue-600 rounded-full flex-shrink-0 mt-2" />}
                      </div>
                    </div>
                  ))}
                </div>
              ) : null}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Reports Tab */}
        <TabsContent value="reports" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Generated Reports</CardTitle>
              <CardDescription>Recent reports and exports</CardDescription>
            </CardHeader>
            <CardContent>
              {reportsError && <p role="alert" className={ERROR_CLASS}>{reportsError}</p>}
              {reports === null && !reportsError ? (
                <p className="text-gray-500">Loading reports…</p>
              ) : reports && reports.length === 0 ? (
                <p className="text-gray-500">You have not generated any reports.</p>
              ) : reports ? (
                <div className="space-y-2">
                  {reports.map((report) => (
                    <div key={report.id} className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <p className="font-medium">{report.name}</p>
                        <p className="text-sm text-gray-600">{report.report_type}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-600">
                          {new Date(report.generated_at ?? report.created_at).toLocaleDateString()}
                        </p>
                        <span className={`inline-block px-2 py-1 text-xs rounded mt-1 ${REPORT_CLASSES[report.status] ?? 'bg-gray-100 text-gray-800'}`}>
                          {report.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : null}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Rate Limits Tab */}
        <TabsContent value="rateLimits" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>API Rate Limits</CardTitle>
              <CardDescription>Configured limits for each endpoint. Live usage is not recorded yet.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {limitsError && <p role="alert" className={ERROR_CLASS}>{limitsError}</p>}
              {limits === null && !limitsError ? (
                <p className="text-gray-500">Loading limits…</p>
              ) : limits && limits.length === 0 ? (
                <p className="text-gray-500">No rate limits are configured.</p>
              ) : limits ? (
                limits.map((limit) => (
                  <div key={limit.id} className="border rounded-lg p-3">
                    <p className="font-medium text-sm">{limit.endpoint}</p>
                    <p className="text-sm text-gray-600">
                      {limit.requests_per_minute} per minute · {limit.requests_per_hour.toLocaleString()} per hour · {limit.requests_per_day.toLocaleString()} per day · burst {limit.burst_limit}
                    </p>
                  </div>
                ))
              ) : null}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
