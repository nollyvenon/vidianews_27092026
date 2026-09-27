'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface DailyAnalytics {
  date: string;
  pageviews: number;
  sessions: number;
  uniqueVisitors: number;
  bounceRate: number;
}

interface TopContent {
  contentId: number;
  pageviews: number;
  uniqueVisitors: number;
  avgTimeOnPage: number;
  conversionCount: number;
}

interface PerformanceMetrics {
  endpoint: string;
  avgResponseTime: number;
  p95ResponseTime: number;
  errorRate: number;
  requestCount: number;
}

interface SystemHealth {
  overallStatus: string;
  services: ServiceHealth[];
  totalUptime: number;
}

interface ServiceHealth {
  serviceName: string;
  status: string;
  uptime: number;
  responseTime?: number;
}

export default function AnalyticsDashboard() {
  const [dailyAnalytics, setDailyAnalytics] = useState<DailyAnalytics[]>([]);
  const [topContent, setTopContent] = useState<TopContent[]>([]);
  const [performanceMetrics, setPerformanceMetrics] = useState<PerformanceMetrics[]>([]);
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const mockDailyAnalytics: DailyAnalytics[] = [
        {
          date: new Date().toISOString().split('T')[0],
          pageviews: 5200,
          sessions: 1400,
          uniqueVisitors: 950,
          bounceRate: 0.32,
        },
        {
          date: new Date(Date.now() - 86400000).toISOString().split('T')[0],
          pageviews: 4800,
          sessions: 1300,
          uniqueVisitors: 900,
          bounceRate: 0.35,
        },
      ];

      const mockTopContent: TopContent[] = [
        {
          contentId: 1,
          pageviews: 2500,
          uniqueVisitors: 1800,
          avgTimeOnPage: 4.2,
          conversionCount: 125,
        },
        {
          contentId: 2,
          pageviews: 2200,
          uniqueVisitors: 1600,
          avgTimeOnPage: 3.8,
          conversionCount: 110,
        },
      ];

      const mockPerformanceMetrics: PerformanceMetrics[] = [
        {
          endpoint: '/api/articles',
          avgResponseTime: 125,
          p95ResponseTime: 250,
          errorRate: 0.002,
          requestCount: 15000,
        },
        {
          endpoint: '/api/users',
          avgResponseTime: 100,
          p95ResponseTime: 200,
          errorRate: 0.001,
          requestCount: 12000,
        },
      ];

      const mockSystemHealth: SystemHealth = {
        overallStatus: 'healthy',
        services: [
          {
            serviceName: 'API Server',
            status: 'healthy',
            uptime: 99.95,
            responseTime: 125,
          },
          {
            serviceName: 'Database',
            status: 'healthy',
            uptime: 99.98,
            responseTime: 50,
          },
          {
            serviceName: 'Cache Service',
            status: 'healthy',
            uptime: 99.9,
            responseTime: 10,
          },
        ],
        totalUptime: 99.94,
      };

      setDailyAnalytics(mockDailyAnalytics);
      setTopContent(mockTopContent);
      setPerformanceMetrics(mockPerformanceMetrics);
      setSystemHealth(mockSystemHealth);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'healthy':
        return 'bg-green-100 text-green-800';
      case 'degraded':
        return 'bg-yellow-100 text-yellow-800';
      case 'unhealthy':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-lg text-gray-600">Loading analytics...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Analytics & Reporting</h1>
        <p className="text-gray-600 mt-2">Monitor system performance and content metrics</p>
      </div>

      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="content">Content</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="health">Health</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">
                  Today's Pageviews
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">5.2K</div>
                <p className="text-xs text-gray-500 mt-1">↑ 8% from yesterday</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">
                  Sessions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">1.4K</div>
                <p className="text-xs text-gray-500 mt-1">↑ 8% from yesterday</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">
                  Unique Visitors
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">950</div>
                <p className="text-xs text-gray-500 mt-1">↑ 5% from yesterday</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">
                  Bounce Rate
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">32%</div>
                <p className="text-xs text-gray-500 mt-1">↓ 3% from yesterday</p>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Daily Analytics (Last 7 Days)</CardTitle>
              <CardDescription>Pageviews and session trends</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {dailyAnalytics.map((day, idx) => (
                  <div key={idx} className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="font-medium">{day.date}</span>
                      <span className="text-gray-600">
                        {day.pageviews} pageviews, {day.sessions} sessions
                      </span>
                    </div>
                    <Progress value={(day.pageviews / 6000) * 100} className="h-2" />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="content" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Top Content by Pageviews</CardTitle>
              <CardDescription>Most viewed articles and pages</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {topContent.map((content) => (
                  <div key={content.contentId} className="border-b pb-4 last:border-0">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium">Article #{content.contentId}</h4>
                      <Badge variant="outline">{content.pageviews} views</Badge>
                    </div>
                    <div className="grid grid-cols-3 gap-4 text-sm text-gray-600">
                      <div>
                        <div className="font-medium text-gray-900">
                          {content.uniqueVisitors}
                        </div>
                        <div className="text-xs">Unique Visitors</div>
                      </div>
                      <div>
                        <div className="font-medium text-gray-900">
                          {content.avgTimeOnPage.toFixed(1)}s
                        </div>
                        <div className="text-xs">Avg. Time on Page</div>
                      </div>
                      <div>
                        <div className="font-medium text-gray-900">
                          {content.conversionCount}
                        </div>
                        <div className="text-xs">Conversions</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="performance" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {performanceMetrics.map((metric) => (
              <Card key={metric.endpoint}>
                <CardHeader>
                  <CardTitle className="text-sm font-medium">
                    {metric.endpoint}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-600">Avg Response Time</span>
                      <span className="font-medium">{metric.avgResponseTime}ms</span>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-600">P95 Latency</span>
                      <span className="font-medium">{metric.p95ResponseTime}ms</span>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-600">Error Rate</span>
                      <span className={`font-medium ${metric.errorRate > 0.01 ? 'text-red-600' : 'text-green-600'}`}>
                        {(metric.errorRate * 100).toFixed(2)}%
                      </span>
                    </div>
                  </div>
                  <div className="pt-2 border-t">
                    <div className="text-xs text-gray-500">
                      {metric.requestCount.toLocaleString()} requests
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="health" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>System Health Status</CardTitle>
              <CardDescription>Overall system and service health metrics</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {systemHealth && (
                <>
                  <div className="flex items-center justify-between">
                    <span className="text-lg font-medium">Overall Status</span>
                    <Badge className={getStatusColor(systemHealth.overallStatus)}>
                      {systemHealth.overallStatus.toUpperCase()}
                    </Badge>
                  </div>

                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>Total Uptime</span>
                      <span className="font-medium">
                        {systemHealth.totalUptime.toFixed(2)}%
                      </span>
                    </div>
                    <Progress
                      value={systemHealth.totalUptime}
                      className="h-2"
                    />
                  </div>

                  <div className="mt-6 space-y-4">
                    <h4 className="font-medium text-sm">Services</h4>
                    {systemHealth.services.map((service) => (
                      <div key={service.serviceName} className="border-l-4 pl-4 border-gray-200">
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-medium text-sm">{service.serviceName}</span>
                          <Badge className={getStatusColor(service.status)}>
                            {service.status}
                          </Badge>
                        </div>
                        <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                          <div>Uptime: {service.uptime.toFixed(2)}%</div>
                          {service.responseTime && (
                            <div>Response: {service.responseTime}ms</div>
                          )}
                        </div>
                        <Progress
                          value={service.uptime}
                          className="h-1 mt-2"
                        />
                      </div>
                    ))}
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
