import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calendar, Clock, Send } from 'lucide-react';
import { format } from 'date-fns';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface PublishingJob {
  id: number;
  title: string;
  status: string;
  scheduled_publish_time: string;
  actual_publish_time?: string;
  distribution_channels: string[];
}

export default function PublishingTab() {
  const [jobs, setJobs] = useState<PublishingJob[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [publishTime, setPublishTime] = useState('');
  const [selectedChannels, setSelectedChannels] = useState<string[]>(['website']);

  const createJobMutation = useMutation({
    mutationFn: async () => {
      const response = await fetch(`${API_BASE}/publishing/jobs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          content_id: 1,
          title,
          scheduled_publish_time: publishTime,
          distribution_channels: selectedChannels,
          auto_promote: true,
        }),
      });
      if (!response.ok) throw new Error('Failed to create job');
      return response.json();
    },
    onSuccess: (data) => {
      setJobs([...jobs, data]);
      setTitle('');
      setDescription('');
      setPublishTime('');
    },
  });

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Schedule Publication</CardTitle>
          <CardDescription>Create a new publishing job with automatic distribution</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input
            placeholder="Publication title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <Textarea
            placeholder="Description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="min-h-24"
          />
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Publish Time</label>
              <Input
                type="datetime-local"
                value={publishTime}
                onChange={(e) => setPublishTime(e.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Distribution Channels</label>
              <div className="flex gap-2 flex-wrap mt-2">
                {['website', 'email', 'social', 'rss'].map((channel) => (
                  <Badge
                    key={channel}
                    variant={selectedChannels.includes(channel) ? 'default' : 'outline'}
                    className="cursor-pointer"
                    onClick={() =>
                      setSelectedChannels((prev) =>
                        prev.includes(channel)
                          ? prev.filter((c) => c !== channel)
                          : [...prev, channel]
                      )
                    }
                  >
                    {channel.charAt(0).toUpperCase() + channel.slice(1)}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
          <Button
            onClick={() => createJobMutation.mutate()}
            disabled={!title || !publishTime || createJobMutation.isPending}
            className="w-full"
          >
            <Send className="mr-2 h-4 w-4" />
            {createJobMutation.isPending ? 'Scheduling...' : 'Schedule Publication'}
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Scheduled Publications</CardTitle>
          <CardDescription>{jobs.length} publications scheduled</CardDescription>
        </CardHeader>
        <CardContent>
          {jobs.length === 0 ? (
            <p className="text-center text-gray-500 py-8">No scheduled publications</p>
          ) : (
            <div className="space-y-3">
              {jobs.map((job) => (
                <div key={job.id} className="border rounded-lg p-4 hover:bg-gray-50 transition">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h4 className="font-semibold">{job.title}</h4>
                      <div className="flex gap-4 text-sm text-gray-600 mt-2">
                        <span className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          {format(new Date(job.scheduled_publish_time), 'MMM d, HH:mm')}
                        </span>
                        <Badge variant="outline">{job.status}</Badge>
                      </div>
                      <div className="flex gap-1 mt-2">
                        {job.distribution_channels.map((channel) => (
                          <Badge key={channel} className="bg-blue-100 text-blue-800">
                            {channel}
                          </Badge>
                        ))}
                      </div>
                    </div>
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
