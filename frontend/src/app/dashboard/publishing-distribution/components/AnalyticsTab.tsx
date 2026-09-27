import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, Eye, Click, Share2 } from 'lucide-react';

export default function AnalyticsTab() {
  const mockMetrics = {
    views: 45230,
    clicks: 2150,
    shares: 890,
    engagement_score: 72.5,
    trend: 'increasing',
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Eye className="h-4 w-4" />
              Total Views
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{(mockMetrics.views / 1000).toFixed(1)}K</div>
            <p className="text-xs text-gray-500">Last 30 days</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Click className="h-4 w-4" />
              Click-Through Rate
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {((mockMetrics.clicks / mockMetrics.views) * 100).toFixed(1)}%
            </div>
            <p className="text-xs text-gray-500">Avg CTR</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Share2 className="h-4 w-4" />
              Shares
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockMetrics.shares}</div>
            <p className="text-xs text-gray-500">Social shares</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <TrendingUp className="h-4 w-4" />
              Engagement
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockMetrics.engagement_score.toFixed(1)}</div>
            <Badge className="mt-2 bg-green-100 text-green-800">Up 12%</Badge>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Performance Trends</CardTitle>
          <CardDescription>Engagement metrics over time</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm font-medium">Views</span>
              <span className="text-sm text-gray-600">45K</span>
            </div>
            <Progress value={85} className="h-2" />
          </div>
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm font-medium">Engagement Rate</span>
              <span className="text-sm text-gray-600">72.5%</span>
            </div>
            <Progress value={72.5} className="h-2" />
          </div>
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm font-medium">Share Rate</span>
              <span className="text-sm text-gray-600">2.0%</span>
            </div>
            <Progress value={40} className="h-2" />
          </div>
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm font-medium">Conversion</span>
              <span className="text-sm text-gray-600">3.5%</span>
            </div>
            <Progress value={35} className="h-2" />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Top Performing Content</CardTitle>
          <CardDescription>Best engagement this week</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              { title: 'AI Advances in 2026', engagement: 89.5 },
              { title: 'Cloud Security Tips', engagement: 78.2 },
              { title: 'DevOps Best Practices', engagement: 72.1 },
            ].map((item, idx) => (
              <div key={idx} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-sm font-medium">{item.title}</span>
                <Badge>{item.engagement}% engagement</Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
