import React, { useEffect, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calendar, Send } from 'lucide-react';
import { format } from 'date-fns';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';
import { ContentPicker, ContentOption } from '@/components/content/content-picker';

interface PublishingJob {
  id: number;
  title: string | null;
  status: string;
  scheduled_publish_time: string;
  distribution_channels: string[];
}

const CHANNELS = ['website', 'email', 'social', 'rss'];

export default function PublishingTab() {
  const queryClient = useQueryClient();
  const [selected, setSelected] = useState<ContentOption | null>(null);
  const [title, setTitle] = useState('');
  const [publishTime, setPublishTime] = useState('');
  const [selectedChannels, setSelectedChannels] = useState<string[]>(['website']);

  useEffect(() => {
    if (selected) setTitle(selected.title);
  }, [selected]);

  const jobsQuery = useQuery({
    queryKey: ['publishing-jobs'],
    queryFn: () => ApiClient.get('/publishing/jobs/pending') as Promise<PublishingJob[]>,
  });
  const jobs = Array.isArray(jobsQuery.data) ? jobsQuery.data : [];

  const createJobMutation = useMutation({
    mutationFn: () =>
      ApiClient.post('/publishing/jobs', {
        content_id: selected?.id,
        title,
        // datetime-local has no zone; the browser's local time is converted to an absolute instant.
        scheduled_publish_time: new Date(publishTime).toISOString(),
        distribution_channels: selectedChannels,
        auto_promote: true,
      }),
    onSuccess: () => {
      setPublishTime('');
      setSelected(null);
      setTitle('');
      queryClient.invalidateQueries({ queryKey: ['publishing-jobs'] });
    },
  });

  const toggleChannel = (channel: string) =>
    setSelectedChannels((prev) =>
      prev.includes(channel) ? prev.filter((item) => item !== channel) : [...prev, channel]
    );

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Schedule Publication</CardTitle>
          <CardDescription>Choose content, a publish time and the channels to publish to</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <ContentPicker value={selected?.id ?? null} onChange={setSelected} label="Content to publish" />
          <Input placeholder="Publication title" value={title} onChange={(e) => setTitle(e.target.value)} />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="block">
              <span className="text-sm font-medium">Publish time</span>
              <Input type="datetime-local" value={publishTime} onChange={(e) => setPublishTime(e.target.value)} />
            </label>
            <div>
              <span className="text-sm font-medium">Distribution channels</span>
              <div className="flex gap-2 flex-wrap mt-2">
                {CHANNELS.map((channel) => (
                  <Badge
                    key={channel}
                    variant={selectedChannels.includes(channel) ? 'default' : 'outline'}
                    className="cursor-pointer"
                    onClick={() => toggleChannel(channel)}
                  >
                    {channel.charAt(0).toUpperCase() + channel.slice(1)}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
          {createJobMutation.isError && (
            <p role="alert" className="text-sm text-red-700">
              {errorMessage(createJobMutation.error, 'The publication could not be scheduled.')}
            </p>
          )}
          <Button
            onClick={() => createJobMutation.mutate()}
            disabled={!selected || !title || !publishTime || selectedChannels.length === 0 || createJobMutation.isPending}
            className="w-full"
          >
            <Send className="mr-2 h-4 w-4" />
            {createJobMutation.isPending ? 'Scheduling…' : 'Schedule Publication'}
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
                  <h4 className="font-semibold">{job.title ?? `Publication ${job.id}`}</h4>
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
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
