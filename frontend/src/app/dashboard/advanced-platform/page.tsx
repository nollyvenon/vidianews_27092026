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
import { Zap, Clock, Layers, Database } from 'lucide-react';

interface Presence {
  online: number;
  idle: number;
}

interface HealthReport {
  metrics: { cpu_percent: number; memory_percent: number; disk_percent: number; database_latency_ms: number };
  checks: { name: string; status: string; pending?: number; running?: number; failed?: number }[];
}

interface BackgroundJob {
  id: number;
  job_type: string;
  status: string;
  priority: number;
  created_at: string;
}

interface Pipeline {
  id: number;
  name: string;
  source_type: string;
  destination_type: string;
  status: string;
  is_active: boolean;
  failure_count: number;
  last_run: string | null;
}

interface CacheSummary {
  entries: number;
  total_hits: number;
  memory_usage_mb: number;
}

interface ApiUsage {
  id: number;
  endpoint: string;
  method: string;
  call_count: number;
  error_count: number;
  average_response_time_ms: number;
}

const CHECK_CLASSES: Record<string, string> = {
  healthy: 'bg-green-100 text-green-800',
  degraded: 'bg-yellow-100 text-yellow-800',
};

/** WebSocket presence, background jobs, data pipelines, cache and API usage, all read from the live platform. */
export default function AdvancedPlatformPage() {
  const [activeTab, setActiveTab] = useState('overview');
  const [presence, setPresence] = useState<Presence | null>(null);
  const [health, setHealth] = useState<HealthReport | null>(null);
  const [jobs, setJobs] = useState<BackgroundJob[] | null>(null);
  const [jobsError, setJobsError] = useState<string | null>(null);
  const [pipelines, setPipelines] = useState<Pipeline[] | null>(null);
  const [pipelinesError, setPipelinesError] = useState<string | null>(null);
  const [cache, setCache] = useState<CacheSummary | null>(null);
  const [cacheError, setCacheError] = useState<string | null>(null);
  const [usage, setUsage] = useState<ApiUsage[] | null>(null);
  const [usageError, setUsageError] = useState<string | null>(null);
  const [presenceError, setPresenceError] = useState<string | null>(null);
  const [healthError, setHealthError] = useState<string | null>(null);

  useEffect(() => {
    ApiClient.get('/websocket/presence')
      .then((data: Presence) => setPresence(data))
      .catch((err) => setPresenceError(errorMessage(err, 'Connection figures could not be loaded.')));
    ApiClient.get('/system/health/checks')
      .then((data: HealthReport) => setHealth(data))
      .catch((err) => setHealthError(errorMessage(err, 'Health figures could not be loaded.')));
    ApiClient.get('/jobs/pending')
      .then((data: BackgroundJob[]) => setJobs(Array.isArray(data) ? data : []))
      .catch((err) => setJobsError(errorMessage(err, 'Pending jobs could not be loaded.')));
    ApiClient.get('/pipelines/')
      .then((data: Pipeline[]) => setPipelines(Array.isArray(data) ? data : []))
      .catch((err) => setPipelinesError(errorMessage(err, 'Pipelines could not be loaded.')));
    ApiClient.get('/cache-summary')
      .then((data: CacheSummary) => setCache(data))
      .catch((err) => setCacheError(errorMessage(err, 'Cache figures could not be loaded.')));
    ApiClient.get('/api-docs/usage')
      .then((data: ApiUsage[]) => setUsage(Array.isArray(data) ? data : []))
      .catch((err) => setUsageError(errorMessage(err, 'API usage could not be loaded.')));
  }, []);

  const activePipelines = pipelines ? pipelines.filter((pipeline) => pipeline.is_active).length : null;

  const stats = [
    { label: 'Active WebSockets', value: presence ? presence.online.toLocaleString() : '—', icon: Zap, color: 'bg-blue-100' },
    { label: 'Pending Jobs', value: jobs ? jobs.length.toLocaleString() : '—', icon: Clock, color: 'bg-orange-100' },
    { label: 'Active Pipelines', value: activePipelines !== null ? activePipelines.toLocaleString() : '—', icon: Layers, color: 'bg-green-100' },
    { label: 'Cached Entries', value: cache ? cache.entries.toLocaleString() : '—', icon: Database, color: 'bg-purple-100' },
  ];

  return (
    <div className="space-y-6 p-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Advanced Platform</h1>
        <p className="text-gray-600 mt-2">WebSockets, Jobs, Pipelines & Performance</p>
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
              <CardDescription>Live figures from this server</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {presenceError && <p role="alert" className="text-red-700">{presenceError}</p>}
              {healthError && <p role="alert" className="text-red-700">{healthError}</p>}
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 border rounded-lg">
                  <p className="text-sm text-gray-600">CPU Usage</p>
                  <p className="text-2xl font-bold mt-2">{health ? `${health.metrics.cpu_percent}%` : '—'}</p>
                </div>
                <div className="p-4 border rounded-lg">
                  <p className="text-sm text-gray-600">Database Latency</p>
                  <p className="text-2xl font-bold mt-2">{health ? `${health.metrics.database_latency_ms}ms` : '—'}</p>
                </div>
              </div>
              {health && (
                <div className="space-y-2">
                  {health.checks.map((check) => (
                    <div key={check.name} className="flex items-center justify-between p-3 border rounded-lg">
                      <span className="font-medium">{check.name}</span>
                      <span className={`px-2 py-1 text-xs rounded ${CHECK_CLASSES[check.status] ?? 'bg-gray-100 text-gray-800'}`}>
                        {check.status}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="jobs">
          <Card>
            <CardHeader>
              <CardTitle>Background Jobs</CardTitle>
              <CardDescription>Jobs waiting to run</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              {jobsError && <p role="alert" className="text-red-700">{jobsError}</p>}
              {jobs === null && !jobsError ? (
                <p className="text-gray-500">Loading jobs…</p>
              ) : jobs && jobs.length === 0 ? (
                <p className="text-gray-500">No jobs are waiting.</p>
              ) : jobs ? (
                jobs.map((job) => (
                  <div key={job.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <p className="font-medium">{job.job_type}</p>
                      <p className="text-xs text-gray-600">Priority {job.priority} · queued {new Date(job.created_at).toLocaleString()}</p>
                    </div>
                    <span className="px-2 py-1 text-xs rounded bg-yellow-100 text-yellow-800">{job.status}</span>
                  </div>
                ))
              ) : null}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="pipelines">
          <Card>
            <CardHeader>
              <CardTitle>Data Pipelines</CardTitle>
              <CardDescription>Sources, destinations and recent runs</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              {pipelinesError && <p role="alert" className="text-red-700">{pipelinesError}</p>}
              {pipelines === null && !pipelinesError ? (
                <p className="text-gray-500">Loading pipelines…</p>
              ) : pipelines && pipelines.length === 0 ? (
                <p className="text-gray-500">No pipelines have been created.</p>
              ) : pipelines ? (
                pipelines.map((pipeline) => (
                  <div key={pipeline.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <p className="font-medium">{pipeline.name}</p>
                      <p className="text-xs text-gray-600">
                        {pipeline.source_type} → {pipeline.destination_type}
                        {pipeline.last_run ? ` · last run ${new Date(pipeline.last_run).toLocaleString()}` : ' · never run'}
                        {pipeline.failure_count > 0 ? ` · ${pipeline.failure_count} failures` : ''}
                      </p>
                    </div>
                    <span className={`text-xs px-2 py-1 rounded ${pipeline.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                      {pipeline.is_active ? 'active' : pipeline.status}
                    </span>
                  </div>
                ))
              ) : null}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="cache">
          <Card>
            <CardHeader>
              <CardTitle>Cache Performance</CardTitle>
              <CardDescription>Cached entries and the hits they have served</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              {cacheError && <p role="alert" className="text-red-700">{cacheError}</p>}
              {cache && (
                <>
                  <div className="flex justify-between p-3 border rounded-lg">
                    <span>Cached Entries</span>
                    <span className="font-bold">{cache.entries.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between p-3 border rounded-lg">
                    <span>Hits Served</span>
                    <span className="font-bold">{cache.total_hits.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between p-3 border rounded-lg">
                    <span>Memory Usage</span>
                    <span className="font-bold">{cache.memory_usage_mb.toFixed(2)}MB</span>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="api">
          <Card>
            <CardHeader>
              <CardTitle>API Usage</CardTitle>
              <CardDescription>Measured calls per endpoint</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              {usageError && <p role="alert" className="text-red-700">{usageError}</p>}
              {usage === null && !usageError ? (
                <p className="text-gray-500">Loading usage…</p>
              ) : usage && usage.length === 0 ? (
                <p className="text-gray-500">No API calls have been measured yet.</p>
              ) : usage ? (
                usage.map((item) => (
                  <div key={item.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <span className="font-medium">{item.method} {item.endpoint}</span>
                    <span className="text-sm text-gray-600">
                      {item.call_count.toLocaleString()} calls · {item.error_count.toLocaleString()} errors · {item.average_response_time_ms}ms avg
                    </span>
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
