/**
 * Content Quality Dashboard
 * Modules 61-65: Content Quality & Processing
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import ContentCalendarTab from './components/ContentCalendarTab';
import ProofreadingTab from './components/ProofreadingTab';
import PlagiarismTab from './components/PlagiarismTab';
import ReadabilityTab from './components/ReadabilityTab';
import BrandVoiceTab from './components/BrandVoiceTab';

export default function ContentQualityPage() {
  const [activeTab, setActiveTab] = useState('calendar');

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
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Calendar Events</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">24</div>
            <p className="text-xs text-gray-500">Next 30 days</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Avg Quality Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">87.5</div>
            <Badge className="mt-2 bg-green-100 text-green-800">Good</Badge>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Plagiarism Risk</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Low</div>
            <p className="text-xs text-gray-500">5.2% avg similarity</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Readability</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Moderate</div>
            <p className="text-xs text-gray-500">Grade 8-9</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Brand Voice</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">92%</div>
            <p className="text-xs text-gray-500">Compliance</p>
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
