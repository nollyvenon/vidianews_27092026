/**
 * Module 63: Plagiarism Detection
 * Originality and source matching
 */

'use client';

import React, { useEffect, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertCircle } from 'lucide-react';
import { ContentPicker, ContentOption } from '@/components/content/content-picker';

/**
 * Plagiarism checks compare text against published sources, which needs an external
 * similarity-search provider. The server refuses the check until one is configured, and this
 * tab shows that refusal instead of inventing a result.
 */
export default function PlagiarismTab() {
  const [content, setContent] = useState('');
  const [selected, setSelected] = useState<ContentOption | null>(null);

  useEffect(() => {
    if (selected?.body !== undefined) setContent(selected.body ?? '');
  }, [selected]);

  const checkMutation = useMutation({
    mutationFn: () => ApiClient.post('/plagiarism/check', { content_id: selected?.id, text: content }),
  });

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Check Plagiarism</CardTitle>
          <CardDescription>Analyze your content for plagiarism and originality</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div role="note" className="flex items-start gap-2 rounded-md bg-yellow-50 p-3 text-sm text-yellow-900">
            <AlertCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
            <span>
              Plagiarism matching needs a similarity-search provider. Checks run only on servers where one is configured.
            </span>
          </div>
          <ContentPicker value={selected?.id ?? null} onChange={setSelected} />
          <Textarea
            placeholder="Choose content above to load its text…"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="min-h-48"
          />
          {checkMutation.isError && (
            <p role="alert" className="text-sm text-red-700">
              {errorMessage(checkMutation.error, 'The plagiarism check could not run.')}
            </p>
          )}
          <Button
            onClick={() => checkMutation.mutate()}
            disabled={!selected || !content.trim() || checkMutation.isPending}
            className="w-full"
          >
            {checkMutation.isPending ? 'Checking…' : 'Check Plagiarism'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
