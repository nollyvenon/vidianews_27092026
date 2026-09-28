'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function AdvancedFeaturesPage() {
  const [activeTab, setActiveTab] = useState('recommendations');

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Advanced Features</h1>
        <p className="text-gray-500 mt-2">Personalization, recommendations, retention, and predictions</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4 lg:grid-cols-8">
          <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
          <TabsTrigger value="retention">Retention</TabsTrigger>
          <TabsTrigger value="abtest">A/B Tests</TabsTrigger>
          <TabsTrigger value="insights">Insights</TabsTrigger>
          <TabsTrigger value="cohorts">Cohorts</TabsTrigger>
          <TabsTrigger value="personalization">Personalization</TabsTrigger>
          <TabsTrigger value="predictions">Predictions</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
        </TabsList>

        <TabsContent value="recommendations" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Total Recommendations</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">2,847</div>
                <p className="text-xs text-gray-500 mt-2">+12% from last week</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Click-Through Rate</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">28.4%</div>
                <p className="text-xs text-gray-500 mt-2">+3.2% improvement</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">12.7%</div>
                <p className="text-xs text-gray-500 mt-2">+1.5% from baseline</p>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Recommendation Performance by Type</CardTitle>
              <CardDescription>CTR and conversion rates by recommendation type</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Collaborative Filtering</p>
                    <p className="text-sm text-gray-500">850 recommendations</p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold">32.1% CTR</p>
                    <p className="text-sm text-gray-500">14.2% conversion</p>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Content-Based</p>
                    <p className="text-sm text-gray-500">920 recommendations</p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold">26.3% CTR</p>
                    <p className="text-sm text-gray-500">11.5% conversion</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="retention" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">At-Risk Users</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">347</div>
                <p className="text-xs text-gray-500 mt-2">12.3% of active users</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Avg Churn Probability</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">0.68</div>
                <p className="text-xs text-gray-500 mt-2">68% estimated churn risk</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Campaign ROI</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">3.2x</div>
                <p className="text-xs text-gray-500 mt-2">Return on retention spend</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="abtest" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Active Tests</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">3</div>
                <p className="text-xs text-gray-500 mt-2">2 reaching significance</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Completed Tests</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">18</div>
                <p className="text-xs text-gray-500 mt-2">12 with positive results</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Test Success Rate</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">66.7%</div>
                <p className="text-xs text-gray-500 mt-2">Winning vs baseline</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="insights" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Key Insights</CardTitle>
              <CardDescription>Actionable insights from advanced analytics</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-l-4 border-red-500 bg-red-50 p-4 rounded">
                <p className="font-semibold text-red-900">Anomaly Detected</p>
                <p className="text-sm text-red-800 mt-1">Unusual spike in 404 errors (342% increase)</p>
                <p className="text-xs text-red-700 mt-2">Confidence: 94%</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="cohorts" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>User Cohorts</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between items-center p-3 border rounded-lg">
                <div>
                  <p className="font-medium">High-Value Users</p>
                  <p className="text-sm text-gray-500">LTV > $1000</p>
                </div>
                <div className="text-right">
                  <p className="font-semibold">1,247 users</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="personalization" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Avg Personalization Score</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">0.72</div>
                <p className="text-xs text-gray-500 mt-2">72% profile completion</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Users with Preferences</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">8,234</div>
                <p className="text-xs text-gray-500 mt-2">87.4% of active users</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="predictions" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Active Models</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">4</div>
                <p className="text-xs text-gray-500 mt-2">All deployed</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Avg Model Accuracy</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">0.894</div>
                <p className="text-xs text-gray-500 mt-2">89.4% accuracy</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Predictions This Month</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">24.3k</div>
                <p className="text-xs text-gray-500 mt-2">+18.2% from last month</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="performance" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-4">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Recommendations/sec</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">1,240</div>
                <p className="text-xs text-gray-500 mt-2">Avg throughput</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">P95 Latency</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">142ms</div>
                <p className="text-xs text-gray-500 mt-2">95th percentile</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Cache Hit Rate</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">94.2%</div>
                <p className="text-xs text-gray-500 mt-2">Advanced features cache</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">System Uptime</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">99.98%</div>
                <p className="text-xs text-gray-500 mt-2">This month</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
