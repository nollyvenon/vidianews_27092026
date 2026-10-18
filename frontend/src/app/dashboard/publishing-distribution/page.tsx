/**
 * Publishing, Distribution & Optimization Dashboard
 * Modules 66-70: Publishing, Distribution, Analytics, A/B Testing, Recommendations
 */

'use client';

import React, { useEffect, useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import PublishingTab from './components/PublishingTab';
import DistributionTab from './components/DistributionTab';
import AnalyticsTab from './components/AnalyticsTab';
import ABTestingTab from './components/ABTestingTab';
import RecommendationsTab from './components/RecommendationsTab';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';

interface PublishingOverview {
  pending_publications: number;
  average_engagement: number | null;
  distribution_reach: number | null;
  click_through_rate: number | null;
  running_ab_tests: number;
}

/** A figure from the overview, or a plain statement when nothing has been recorded for it yet. */
function figure(value: number | null | undefined, format: (value: number) => string) {
  return value === null || value === undefined ? 'No data yet' : format(value);
}

export default function PublishingDistributionPage() {
  const [activeTab, setActiveTab] = useState('publishing');
  const [overview, setOverview] = useState<PublishingOverview | null>(null);
  const [overviewError, setOverviewError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    ApiClient.get('/publishing/overview')
      .then((data: PublishingOverview) => {
        if (active) setOverview(data);
      })
      .catch((err) => {
        if (active) setOverviewError(errorMessage(err, 'Publishing figures could not be loaded.'));
      });
    return () => {
      active = false;
    };
  }, []);

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
      {overviewError && <p role="alert" className="text-sm text-red-700">{overviewError}</p>}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Pending Publications</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview ? overview.pending_publications : '…'}</div>
            <p className="text-xs text-gray-500">Scheduled and not yet published</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Avg Engagement</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview ? figure(overview.average_engagement, (v) => v.toFixed(1)) : '…'}</div>
            <p className="text-xs text-gray-500">Average engagement score across content</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Distribution Reach</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview ? figure(overview.distribution_reach, (v) => v.toLocaleString()) : '…'}</div>
            <p className="text-xs text-gray-500">Total views recorded</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Running A/B Tests</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview ? overview.running_ab_tests : '…'}</div>
            <p className="text-xs text-gray-500">In progress</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Click-Through Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview ? figure(overview.click_through_rate, (v) => `${v.toFixed(2)}%`) : '…'}</div>
            <p className="text-xs text-gray-500">Clicks per view</p>
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
