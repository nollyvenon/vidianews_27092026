import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, Eye, MousePointerClick, Share2 } from 'lucide-react';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';
import { ContentPicker, ContentOption } from '@/components/content/content-picker';

interface EngagementMetrics {
  content_id: number;
  total_views: number;
  total_clicks: number;
  total_shares: number;
  engagement_score: number;
  engagement_trend: string | null;
}

/** Engagement recorded for one content item, chosen by the author. */
export default function AnalyticsTab() {
  const [selected, setSelected] = useState<ContentOption | null>(null);
  const [metrics, setMetrics] = useState<EngagementMetrics | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!selected) {
      setMetrics(null);
      setError(null);
      return;
    }
    let active = true;
    setLoading(true);
    setError(null);
    ApiClient.get(`/analytics/metrics/${selected.id}`)
      .then((data: EngagementMetrics) => {
        if (active) setMetrics(data);
      })
      .catch((err) => {
        if (active) {
          setMetrics(null);
          setError(errorMessage(err, 'Engagement could not be loaded for this content.'));
        }
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [selected]);

  const clickRate = metrics && metrics.total_views > 0 ? (metrics.total_clicks / metrics.total_views) * 100 : 0;

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Content Engagement</CardTitle>
          <CardDescription>Choose a content item to see the engagement recorded for it</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <ContentPicker value={selected?.id ?? null} onChange={setSelected} />
          {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
          {!selected && <p className="text-sm text-gray-500">Select content to see its engagement.</p>}
          {selected && loading && <p className="text-sm text-gray-500">Loading engagement…</p>}
          {selected && metrics && (
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
                    <div className="text-2xl font-bold">{metrics.total_views.toLocaleString()}</div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="flex items-center gap-2 text-sm">
                      <MousePointerClick className="h-4 w-4" />
                      Click-Through Rate
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{clickRate.toFixed(1)}%</div>
                    <p className="text-xs text-gray-500">{metrics.total_clicks.toLocaleString()} clicks</p>
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
                    <div className="text-2xl font-bold">{metrics.total_shares.toLocaleString()}</div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="flex items-center gap-2 text-sm">
                      <TrendingUp className="h-4 w-4" />
                      Engagement Score
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{metrics.engagement_score.toFixed(1)}</div>
                    {metrics.engagement_trend && (
                      <Badge className="mt-2">{metrics.engagement_trend}</Badge>
                    )}
                  </CardContent>
                </Card>
              </div>

              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">Engagement score</span>
                  <span className="text-sm text-gray-600">{metrics.engagement_score.toFixed(1)} / 100</span>
                </div>
                <Progress value={Math.min(100, Math.max(0, metrics.engagement_score))} className="h-2" />
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
