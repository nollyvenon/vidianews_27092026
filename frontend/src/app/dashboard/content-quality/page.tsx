/**
 * Content Quality Dashboard
 * Modules 61-65: Content Quality & Processing
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import ContentCalendarTab from './components/ContentCalendarTab';
import ProofreadingTab from './components/ProofreadingTab';
import PlagiarismTab from './components/PlagiarismTab';
import ReadabilityTab from './components/ReadabilityTab';
import BrandVoiceTab from './components/BrandVoiceTab';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';

const DAY_MS = 24 * 60 * 60 * 1000;

interface QualityOverview {
  proofreading: { checks: number; average_score: number | null };
  readability: { checks: number; average_grade: number | null };
  brand_voice: { checks: number; average_compliance: number | null };
  plagiarism: { checks: number; average_similarity: number | null };
}

/** The value shown on an overview card, or a plain statement when no check has been run yet. */
function figure(value: number | null | undefined, format: (value: number) => string, emptyText: string) {
  return value === null || value === undefined ? emptyText : format(value);
}

export default function ContentQualityPage() {
  const [activeTab, setActiveTab] = useState('calendar');
  const [upcomingEvents, setUpcomingEvents] = useState<number | 'loading' | 'unavailable'>('loading');
  const [overview, setOverview] = useState<QualityOverview | null>(null);
  const [overviewError, setOverviewError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const start = new Date();
    const end = new Date(start.getTime() + 30 * DAY_MS);
    ApiClient.get(
      `/calendar/events?start_date=${encodeURIComponent(start.toISOString())}&end_date=${encodeURIComponent(end.toISOString())}`,
    )
      .then((data: { count: number }) => {
        if (active) setUpcomingEvents(data.count);
      })
      .catch(() => {
        if (active) setUpcomingEvents('unavailable');
      });
    ApiClient.get('/content-quality/overview')
      .then((data: QualityOverview) => {
        if (active) setOverview(data);
      })
      .catch((err) => {
        if (active) setOverviewError(errorMessage(err, 'Quality figures could not be loaded.'));
      });
    return () => {
      active = false;
    };
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Content Quality</h1>
        <p className="text-gray-500">
          Analyze, optimize, and ensure quality across all your content
        </p>
      </div>

      {/* Quality Overview Cards */}
      {overviewError && <p role="alert" className="text-sm text-red-700">{overviewError}</p>}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Calendar Events</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {upcomingEvents === 'loading' ? '…' : upcomingEvents === 'unavailable' ? 'Unavailable' : upcomingEvents}
            </div>
            <p className="text-xs text-gray-500">Scheduled in the next 30 days</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Avg Proofreading Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {overview ? figure(overview.proofreading.average_score, (v) => v.toFixed(1), 'No checks yet') : '…'}
            </div>
            <p className="text-xs text-gray-500">{overview ? `${overview.proofreading.checks} checks run` : 'Across all proofreading checks'}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Avg Similarity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {overview ? figure(overview.plagiarism.average_similarity, (v) => `${v.toFixed(1)}%`, 'No checks yet') : '…'}
            </div>
            <p className="text-xs text-gray-500">{overview ? `${overview.plagiarism.checks} plagiarism checks` : 'Across all plagiarism checks'}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Avg Reading Grade</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {overview ? figure(overview.readability.average_grade, (v) => `Grade ${v.toFixed(1)}`, 'No checks yet') : '…'}
            </div>
            <p className="text-xs text-gray-500">{overview ? `${overview.readability.checks} readability checks` : 'Flesch-Kincaid grade level'}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Avg Brand Compliance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {overview ? figure(overview.brand_voice.average_compliance, (v) => `${v.toFixed(0)}%`, 'No checks yet') : '…'}
            </div>
            <p className="text-xs text-gray-500">{overview ? `${overview.brand_voice.checks} brand voice checks` : 'Against your brand guide'}</p>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Card>
        <CardHeader>
          <CardTitle>Analysis Tools</CardTitle>
          <CardDescription>
            Comprehensive content quality analysis and optimization
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="calendar">Calendar</TabsTrigger>
              <TabsTrigger value="proofreading">Proofreading</TabsTrigger>
              <TabsTrigger value="plagiarism">Plagiarism</TabsTrigger>
              <TabsTrigger value="readability">Readability</TabsTrigger>
              <TabsTrigger value="brand-voice">Brand Voice</TabsTrigger>
            </TabsList>

            <TabsContent value="calendar" className="space-y-4">
              <ContentCalendarTab />
            </TabsContent>

            <TabsContent value="proofreading" className="space-y-4">
              <ProofreadingTab />
            </TabsContent>

            <TabsContent value="plagiarism" className="space-y-4">
              <PlagiarismTab />
            </TabsContent>

            <TabsContent value="readability" className="space-y-4">
              <ReadabilityTab />
            </TabsContent>

            <TabsContent value="brand-voice" className="space-y-4">
              <BrandVoiceTab />
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}
