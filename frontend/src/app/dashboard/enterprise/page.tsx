'use client';

import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  AlertCircle,
  Shield,
  Eye,
  AlertTriangle,
  FileText,
  Users,
  Bell,
  Lock,
  BarChart3,
} from 'lucide-react';

export default function EnterprisePage() {
  const [activeTab, setActiveTab] = useState('security');

  const auditLogs = [
    { id: 1, user: 'user123', action: 'login', timestamp: '2024-01-15 10:30', severity: 'info' },
    { id: 2, user: 'admin456', action: 'user_delete', timestamp: '2024-01-15 10:25', severity: 'high' },
    { id: 3, user: 'user789', action: 'content_edit', timestamp: '2024-01-15 10:20', severity: 'medium' },
  ];

  const moderationQueue = [
    { id: 1, content: 'Article #123', type: 'article', status: 'pending', confidence: 0.92 },
    { id: 2, content: 'Comment #456', type: 'comment', status: 'flagged', confidence: 0.78 },
    { id: 3, content: 'Video #789', type: 'video', status: 'appealed', confidence: 0.65 },
  ];

  const notifications = [
    { id: 1, type: 'alert', title: 'High CPU Usage', message: 'Server load exceeded 80%', read: false },
    { id: 2, type: 'warning', title: 'Rate Limit Warning', message: 'API rate limit at 95%', read: false },
    { id: 3, type: 'info', title: 'Backup Complete', message: 'Daily backup finished successfully', read: true },
  ];

  const reports = [
    { id: 1, name: 'Monthly Analytics', type: 'analytics', status: 'completed', date: '2024-01-15' },
    { id: 2, name: 'Compliance Report', type: 'compliance', status: 'processing', date: '2024-01-15' },
    { id: 3, name: 'Performance Report', type: 'performance', status: 'pending', date: '2024-01-14' },
  ];

  const stats = [
    { label: 'Active Users', value: '2,543', icon: Users, color: 'bg-blue-100' },
    { label: 'Pending Moderation', value: '12', icon: AlertCircle, color: 'bg-orange-100' },
    { label: 'Security Events', value: '156', icon: Shield, color: 'bg-red-100' },
    { label: 'Unread Alerts', value: '5', icon: Bell, color: 'bg-yellow-100' },
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
        {stats.map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <Card key={idx}>
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
              <div className="space-y-2">
                {auditLogs.map((log) => (
                  <div key={log.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <p className="font-medium">{log.action}</p>
                      <p className="text-sm text-gray-600">User: {log.user}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-600">{log.timestamp}</p>
                      <span className={`inline-block px-2 py-1 text-xs rounded mt-1 ${
                        log.severity === 'high' ? 'bg-red-100 text-red-800' :
                        log.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {log.severity}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
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
              <div className="space-y-2">
                {moderationQueue.map((item) => (
                  <div key={item.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex-1">
                      <p className="font-medium">{item.content}</p>
                      <p className="text-sm text-gray-600">{item.type}</p>
                    </div>
                    <div className="text-right">
                      <div className="mb-2">
                        <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-blue-600"
                            style={{ width: `${item.confidence * 100}%` }}
                          />
                        </div>
                        <p className="text-xs text-gray-600 mt-1">{(item.confidence * 100).toFixed(0)}%</p>
                      </div>
                      <span className={`inline-block px-2 py-1 text-xs rounded ${
                        item.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        item.status === 'flagged' ? 'bg-red-100 text-red-800' :
                        'bg-orange-100 text-orange-800'
                      }`}>
                        {item.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
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
              <div className="space-y-2">
                {notifications.map((notif) => (
                  <div key={notif.id} className={`p-3 border rounded-lg ${notif.read ? 'bg-gray-50' : 'bg-blue-50'}`}>
                    <div className="flex items-start gap-3">
                      {notif.type === 'alert' && <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />}
                      {notif.type === 'warning' && <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />}
                      {notif.type === 'info' && <Bell className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />}
                      <div className="flex-1">
                        <p className="font-medium">{notif.title}</p>
                        <p className="text-sm text-gray-600">{notif.message}</p>
                      </div>
                      {!notif.read && <div className="w-2 h-2 bg-blue-600 rounded-full flex-shrink-0 mt-2" />}
                    </div>
                  </div>
                ))}
              </div>
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
              <div className="space-y-2">
                {reports.map((report) => (
                  <div key={report.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <p className="font-medium">{report.name}</p>
                      <p className="text-sm text-gray-600">{report.type}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-600">{report.date}</p>
                      <span className={`inline-block px-2 py-1 text-xs rounded mt-1 ${
                        report.status === 'completed' ? 'bg-green-100 text-green-800' :
                        report.status === 'processing' ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {report.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Rate Limits Tab */}
        <TabsContent value="rateLimits" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>API Rate Limits</CardTitle>
              <CardDescription>Current usage and throttling status</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">Requests per Minute</span>
                  <span className="text-sm text-gray-600">45 / 60</span>
                </div>
                <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-green-600" style={{ width: '75%' }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">Requests per Hour</span>
                  <span className="text-sm text-gray-600">850 / 1000</span>
                </div>
                <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-600" style={{ width: '85%' }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">Requests per Day</span>
                  <span className="text-sm text-gray-600">8,500 / 10,000</span>
                </div>
                <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-orange-600" style={{ width: '85%' }} />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
