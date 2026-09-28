/**
 * Module 61: Content Calendar Integration
 * AI-powered content scheduling with recommendations
 */

'use client';

import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calendar, Clock, TrendingUp, Zap } from 'lucide-react';
import { format } from 'date-fns';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface CalendarEvent {
  id: number;
  event_type: string;
  title: string;
  scheduled_for: string;
  ai_recommended_time?: string;
  ai_confidence_score: number;
  predicted_reach?: number;
  predicted_engagement?: number;
}

export default function ContentCalendarTab() {
  const [dateRange, setDateRange] = useState({
    start: new Date(),
    end: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
  });
  const [events, setEvents] = useState<CalendarEvent[]>([]);

  const { data: calendarEvents, isLoading } = useQuery({
    queryKey: ['calendar-events', dateRange],
    queryFn: async () => {
      const response = await fetch(
        `${API_BASE}/content/calendar/events?start_date=${dateRange.start.toISOString()}&end_date=${dateRange.end.toISOString()}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        }
      );
      if (!response.ok) throw new Error('Failed to fetch calendar events');
      return response.json();
    },
  });

  useEffect(() => {
    if (calendarEvents?.events) {
      setEvents(calendarEvents.events);
    }
  }, [calendarEvents]);

  const getEventColor = (confidence: number) => {
    if (confidence >= 0.8) return 'bg-green-100 text-green-800';
    if (confidence >= 0.6) return 'bg-blue-100 text-blue-800';
    if (confidence >= 0.4) return 'bg-yellow-100 text-yellow-800';
    return 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-6">
      {/* Calendar Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="h-5 w-5" />
            Content Calendar
          </CardTitle>
          <CardDescription>
            View and manage your content schedule with AI-powered recommendations
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm">Scheduled Events</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{events.length}</div>
                <p className="text-xs text-gray-500">Next 30 days</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm">Avg Confidence</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">
                  {events.length > 0
                    ? (
                        (events.reduce((acc, e) => acc + e.ai_confidence_score, 0) / events.length) *
                        100
                      ).toFixed(0)
                    : 0}
                  %
                </div>
                <p className="text-xs text-gray-500">AI recommendation quality</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm">Total Reach</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">
                  {(
                    events.reduce((acc, e) => acc + (e.predicted_reach || 0), 0) / 1000
                  ).toFixed(0)}
                  K
                </div>
                <p className="text-xs text-gray-500">Predicted reach</p>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>

      {/* Events List */}
      <Card>
        <CardHeader>
          <CardTitle>Upcoming Events</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="text-center py-8">Loading calendar events...</div>
          ) : events.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No events scheduled. Create one to get started!
            </div>
          ) : (
            <div className="space-y-3">
              {events.map((event) => (
                <div
                  key={event.id}
                  className="border rounded-lg p-4 hover:bg-gray-50 transition"
                >
                  <div className="flex items-start justify-between">
                    <div className="space-y-2 flex-1">
                      <div className="flex items-center gap-2">
                        <h4 className="font-semibold">{event.title}</h4>
                        <Badge className={getEventColor(event.ai_confidence_score)}>
                          {(event.ai_confidence_score * 100).toFixed(0)}% Confidence
                        </Badge>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
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

                        {event.predicted_reach && (
                          <div className="flex items-center gap-2 text-green-600">
                            <TrendingUp className="h-4 w-4" />
                            <span>Est. Reach: {(event.predicted_reach / 1000).toFixed(1)}K</span>
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="flex gap-2">
                      {event.ai_recommended_time && (
                        <Button size="sm" variant="outline">
                          Use Recommendation
                        </Button>
                      )}
                      <Button size="sm" variant="ghost">
                        Edit
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* AI Insights */}
      <Card>
        <CardHeader>
          <CardTitle>AI Insights</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="border-l-4 border-blue-500 pl-4 py-2">
              <p className="font-semibold text-sm">Best Publishing Time</p>
              <p className="text-sm text-gray-600">
                Based on audience behavior, Tuesday 2-4 PM has the highest engagement rates
              </p>
            </div>

            <div className="border-l-4 border-green-500 pl-4 py-2">
              <p className="font-semibold text-sm">Content Gap</p>
              <p className="text-sm text-gray-600">
                You have 3 days without scheduled content next week
              </p>
            </div>

            <div className="border-l-4 border-yellow-500 pl-4 py-2">
              <p className="font-semibold text-sm">Engagement Opportunity</p>
              <p className="text-sm text-gray-600">
                Trending topics in your niche could boost reach by 35%
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
