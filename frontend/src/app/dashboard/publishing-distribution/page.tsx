/**
 * Publishing, Distribution & Optimization Dashboard
 * Modules 66-70: Publishing, Distribution, Analytics, A/B Testing, Recommendations
 */

'use client';

import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import PublishingTab from './components/PublishingTab';
import DistributionTab from './components/DistributionTab';
import AnalyticsTab from './components/AnalyticsTab';
import ABTestingTab from './components/ABTestingTab';
import RecommendationsTab from './components/RecommendationsTab';

export default function PublishingDistributionPage() {
  const [activeTab, setActiveTab] = useState('publishing');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Publishing & Distribution</h1>
        <p className="text-gray-500">
          Manage publishing schedules, track distribution performance, and optimize content delivery
        </p>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Published Today</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-gray-500">Scheduled publications</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Avg Engagement</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">72.5%</div>
            <Badge className="mt-2 bg-green-100 text-green-800">Up 8%</Badge>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Distribution Reach</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">245K</div>
            <p className="text-xs text-gray-500">Total impressions</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Active A/B Tests</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-gray-500">In progress</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Click-Through Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">4.2%</div>
            <p className="text-xs text-gray-500">Average CTR</p>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Card>
        <CardHeader>
          <CardTitle>Management Tools</CardTitle>
          <CardDescription>
            Publishing, distribution, analytics, and content optimization
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="publishing">Publishing</TabsTrigger>
              <TabsTrigger value="distribution">Distribution</TabsTrigger>
              <TabsTrigger value="analytics">Analytics</TabsTrigger>
              <TabsTrigger value="ab-testing">A/B Testing</TabsTrigger>
              <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
            </TabsList>

            <TabsContent value="publishing" className="space-y-4">
              <PublishingTab />
            </TabsContent>

            <TabsContent value="distribution" className="space-y-4">
              <DistributionTab />
            </TabsContent>

            <TabsContent value="analytics" className="space-y-4">
              <AnalyticsTab />
            </TabsContent>

            <TabsContent value="ab-testing" className="space-y-4">
              <ABTestingTab />
            </TabsContent>

            <TabsContent value="recommendations" className="space-y-4">
              <RecommendationsTab />
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}
