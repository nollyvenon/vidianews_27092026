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
  Zap,
  Database,
  BarChart3,
  Layers,
  Clock,
  TrendingUp,
} from 'lucide-react';

export default function AdvancedPlatformPage() {
  const [activeTab, setActiveTab] = useState('overview');

  const stats = [
    { label: 'Active WebSockets', value: '234', icon: Zap, color: 'bg-blue-100' },
    { label: 'Pending Jobs', value: '12', icon: Clock, color: 'bg-orange-100' },
    { label: 'Running Pipelines', value: '5', icon: Layers, color: 'bg-green-100' },
    { label: 'Cache Hit Rate', value: '87.3%', icon: TrendingUp, color: 'bg-purple-100' },
  ];

  const backgroundJobs = [
    { id: 1, type: 'email_notification', status: 'running', priority: 2, retries: 0 },
    { id: 2, type: 'data_export', status: 'pending', priority: 1, retries: 1 },
    { id: 3, type: 'report_generation', status: 'pending', priority: 3, retries: 0 },
  ];

  const pipelines = [
    { id: 1, name: 'User Sync', source: 'database', dest: 'warehouse', status: 'active', records: 5234 },
    { id: 2, name: 'Event Pipeline', source: 'events', dest: 'analytics', status: 'active', records: 12456 },
  ];

  const cacheMetrics = [
    { metric: 'Total Requests', value: '1,234,567' },
    { metric: 'Cache Hits', value: '1,078,890' },
    { metric: 'Avg Response Time', value: '45.2ms' },
    { metric: 'Memory Usage', value: '512.5MB' },
  ];

  const apiEndpoints = [
    { path: '/users', method: 'GET', calls: 12345, errors: 23 },
    { path: '/content', method: 'GET', calls: 54321, errors: 12 },
  ];

  return (
    <div className="space-y-6 p-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Advanced Platform</h1>
        <p className="text-gray-600 mt-2">WebSockets, Jobs, Pipelines & Performance</p>
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

      {/* Main Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="jobs">Jobs</TabsTrigger>
          <TabsTrigger value="pipelines">Pipelines</TabsTrigger>
          <TabsTrigger value="cache">Cache</TabsTrigger>
          <TabsTrigger value="api">API</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <Card>
            <CardHeader>
              <CardTitle>Platform Overview</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-2 gap-4">
              <div className="p-4 border rounded-lg">
                <p className="text-sm text-gray-600">Uptime</p>
                <p className="text-2xl font-bold mt-2">99.99%</p>
              </div>
              <div className="p-4 border rounded-lg">
                <p className="text-sm text-gray-600">Avg Latency</p>
                <p className="text-2xl font-bold mt-2">45ms</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="jobs">
          <Card>
            <CardHeader>
              <CardTitle>Background Jobs</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {backgroundJobs.map((job) => (
                <div key={job.id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <p className="font-medium">{job.type}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded ${
                    job.status === 'running' ? 'bg-blue-100 text-blue-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {job.status}
                  </span>
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="pipelines">
          <Card>
            <CardHeader>
              <CardTitle>Data Pipelines</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {pipelines.map((pipeline) => (
                <div key={pipeline.id} className="flex items-center justify-between p-3 border rounded-lg">
                  <p className="font-medium">{pipeline.name}</p>
                  <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                    {pipeline.status}
                  </span>
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="cache">
          <Card>
            <CardHeader>
              <CardTitle>Cache Performance</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {cacheMetrics.map((item, idx) => (
                <div key={idx} className="flex justify-between p-3 border rounded-lg">
                  <span>{item.metric}</span>
                  <span className="font-bold">{item.value}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="api">
          <Card>
            <CardHeader>
              <CardTitle>API Usage</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {apiEndpoints.map((endpoint, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 border rounded-lg">
                  <span className="font-medium">{endpoint.method} {endpoint.path}</span>
                  <span className="text-sm text-gray-600">{endpoint.calls.toLocaleString()} calls</span>
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
