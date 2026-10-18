/**
 * Module 61: Content Calendar Integration
 * AI-powered content scheduling with recommendations
 */

'use client';

import React, { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calendar, Clock, TrendingUp, Zap } from 'lucide-react';
import { format } from 'date-fns';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';

interface CalendarEvent {
  id: number;
  event_type: string;
  title: string;
  scheduled_for: string;
  ai_recommended_time?: string | null;
  ai_confidence_score: number;
  predicted_reach?: number | null;
  predicted_engagement?: number | null;
}

interface CalendarResponse {
  count: number;
  events: CalendarEvent[];
}

const DAY_MS = 24 * 60 * 60 * 1000;

/** Badge colour for an AI confidence score between 0 and 1. */
export function confidenceClass(confidence: number): string {
  if (confidence >= 0.8) return 'bg-green-100 text-green-800';
  if (confidence >= 0.6) return 'bg-blue-100 text-blue-800';
  if (confidence >= 0.4) return 'bg-yellow-100 text-yellow-800';
  return 'bg-gray-100 text-gray-800';
}

export default function ContentCalendarTab() {
  // The window is fixed for each mount: the next 30 days from now.
  const range = useMemo(() => {
    const start = new Date();
    return { start, end: new Date(start.getTime() + 30 * DAY_MS) };
  }, []);

  const { data, isLoading, error } = useQuery({
    queryKey: ['calendar-events', range.start.toISOString()],
    queryFn: () => {
      const params = new URLSearchParams({
        start_date: range.start.toISOString(),
        end_date: range.end.toISOString(),
      });
      return ApiClient.get(`/calendar/events?${params.toString()}`) as Promise<CalendarResponse>;
    },
  });

  const events = Array.isArray(data?.events) ? data.events : [];
  const averageConfidence = events.length
    ? (events.reduce((sum, event) => sum + event.ai_confidence_score, 0) / events.length) * 100
    : 0;
  const totalReach = events.reduce((sum, event) => sum + (event.predicted_reach ?? 0), 0);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="h-5 w-5" />
            Content Calendar
          </CardTitle>
          <CardDescription>Scheduled content for the next 30 days, with AI timing recommendations</CardDescription>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <p className="text-sm font-semibold text-gray-600">Scheduled events</p>
            <p className="text-3xl font-bold">{events.length}</p>
          </div>
          <div>
            <p className="text-sm font-semibold text-gray-600">Average confidence</p>
            <p className="text-3xl font-bold">{averageConfidence.toFixed(0)}%</p>
          </div>
          <div>
            <p className="text-sm font-semibold text-gray-600">Predicted reach</p>
            <p className="text-3xl font-bold">{(totalReach / 1000).toFixed(0)}K</p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Upcoming Events</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <p className="text-center py-8">Loading calendar events…</p>
          ) : error ? (
            <p role="alert" className="text-center py-8 text-red-700">
              {errorMessage(error, 'The calendar could not be loaded.')}
            </p>
          ) : events.length === 0 ? (
            <p className="text-center py-8 text-gray-500">No events scheduled in the next 30 days.</p>
          ) : (
            <div className="space-y-3">
              {events.map((event) => (
                <div key={event.id} className="border rounded-lg p-4 hover:bg-gray-50 transition">
                  <div className="flex items-center gap-2">
                    <h4 className="font-semibold">{event.title}</h4>
                    <Badge className={confidenceClass(event.ai_confidence_score)}>
                      {(event.ai_confidence_score * 100).toFixed(0)}% Confidence
                    </Badge>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm mt-2">
                    <div className="flex items-center gap-2 text-gray-600">
                      <Clock className="h-4 w-4" />
                      <span>Scheduled: {format(new Date(event.scheduled_for), 'MMM d, HH:mm')}</span>
                    </div>
                    {event.ai_recommended_time && (
                      <div className="flex items-center gap-2 text-blue-600">
                        <Zap className="h-4 w-4" />
                        <span>Recommended: {format(new Date(event.ai_recommended_time), 'MMM d, HH:mm')}</span>
                      </div>
                    )}
                    {event.predicted_reach ? (
                      <div className="flex items-center gap-2 text-green-600">
                        <TrendingUp className="h-4 w-4" />
                        <span>Est. Reach: {(event.predicted_reach / 1000).toFixed(1)}K</span>
                      </div>
                    ) : null}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
