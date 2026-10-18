/**
 * Module 65: Brand Voice Consistency Checking
 * Ensure content aligns with brand guidelines
 */

'use client';

import React, { useEffect, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { ContentPicker, ContentOption } from '@/components/content/content-picker';

interface BrandGuide {
  id: number;
  name: string;
  tone: Record<string, unknown>;
  personality_traits: string[];
  is_active: boolean;
}

interface BrandVoiceResult {
  id: number;
  content_id: number;
  check_result: string;
  overall_score: number;
  compliance_score: number;
  tone_match_score: number;
  consistency_score: number;
  recommendations: string[];
}

const RESULT_LABELS: Record<string, string> = {
  compliant: 'Compliant',
  partial: 'Partially compliant',
  non_compliant: 'Not compliant',
  needs_review: 'Needs review',
};

function GuideForm({ onCreated }: { onCreated: () => void }) {
  const [name, setName] = useState('');
  const [tone, setTone] = useState('');
  const [traits, setTraits] = useState('');
  const [vocabulary, setVocabulary] = useState('Moderate');
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setSaving(true);
    try {
      await ApiClient.post('/brand-voice/guide', {
        name: name.trim(),
        tone: Object.fromEntries(tone.split(',').map((item) => item.trim()).filter(Boolean).map((item) => [item, true])),
        personality_traits: traits.split(',').map((item) => item.trim()).filter(Boolean),
        vocabulary_level: vocabulary,
      });
      onCreated();
    } catch (err) {
      setError(errorMessage(err, 'The brand guide could not be created.'));
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <p className="text-sm text-gray-600">
        Your organization has no brand voice guide yet. Create one to check content against.
      </p>
      {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
      <label className="block">
        <span className="block text-sm font-medium mb-1">Guide name</span>
        <Input value={name} onChange={(e) => setName(e.target.value)} required />
      </label>
      <label className="block">
        <span className="block text-sm font-medium mb-1">Tone keywords (comma separated)</span>
        <Input value={tone} onChange={(e) => setTone(e.target.value)} placeholder="authoritative, warm" />
      </label>
      <label className="block">
        <span className="block text-sm font-medium mb-1">Personality traits (comma separated)</span>
        <Input value={traits} onChange={(e) => setTraits(e.target.value)} placeholder="curious, direct" />
      </label>
      <label className="block">
        <span className="block text-sm font-medium mb-1">Vocabulary level</span>
        <select className="w-full border rounded-md px-3 py-2" value={vocabulary} onChange={(e) => setVocabulary(e.target.value)}>
          <option>Simple</option>
          <option>Moderate</option>
          <option>Advanced</option>
        </select>
      </label>
      <Button type="submit" disabled={saving || !name.trim()}>
        {saving ? 'Saving…' : 'Create brand guide'}
      </Button>
    </form>
  );
}

export default function BrandVoiceTab() {
  const queryClient = useQueryClient();
  const [content, setContent] = useState('');
  const [selected, setSelected] = useState<ContentOption | null>(null);
  const [result, setResult] = useState<BrandVoiceResult | null>(null);

  const guidesQuery = useQuery({
    queryKey: ['brand-voice-guides'],
    queryFn: () => ApiClient.get('/brand-voice/guide') as Promise<BrandGuide[]>,
  });
  const guides = Array.isArray(guidesQuery.data) ? guidesQuery.data : [];
  const activeGuide = guides.find((guide) => guide.is_active) ?? guides[0];

  useEffect(() => {
    if (selected?.body !== undefined) setContent(selected.body ?? '');
  }, [selected]);

  const checkMutation = useMutation({
    mutationFn: () =>
      ApiClient.post('/brand-voice/check', {
        content_id: selected?.id,
        text: content,
        guide_id: activeGuide?.id,
      }),
    onSuccess: (data: BrandVoiceResult) => setResult(data),
  });

  const percent = (value: number) => `${Number(value).toFixed(1)}%`;

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Brand Guide</CardTitle>
          <CardDescription>Content is checked against your organization&apos;s active guide</CardDescription>
        </CardHeader>
        <CardContent>
          {guidesQuery.isLoading && <p className="text-sm text-gray-500">Loading guides…</p>}
          {!guidesQuery.isLoading && !activeGuide && (
            <GuideForm onCreated={() => queryClient.invalidateQueries({ queryKey: ['brand-voice-guides'] })} />
          )}
          {activeGuide && <p className="text-sm">Active guide: <strong>{activeGuide.name}</strong></p>}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Check Brand Voice</CardTitle>
          <CardDescription>Choose the content to check; its text loads here and can be edited.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <ContentPicker value={selected?.id ?? null} onChange={setSelected} />
          <Textarea
            placeholder="Choose content above to load its text…"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="min-h-48"
          />
          {checkMutation.isError && (
            <p role="alert" className="text-sm text-red-700">
              {errorMessage(checkMutation.error, 'The brand voice check failed.')}
            </p>
          )}
          <Button
            onClick={() => checkMutation.mutate()}
            disabled={!selected || !content.trim() || !activeGuide || checkMutation.isPending}
            className="w-full"
          >
            {checkMutation.isPending ? 'Analyzing…' : 'Check Brand Voice'}
          </Button>
        </CardContent>
      </Card>

      {result && (
        <Card>
          <CardHeader>
            <CardTitle>Result: {RESULT_LABELS[result.check_result] ?? result.check_result}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {[
              ['Compliance', result.compliance_score],
              ['Tone match', result.tone_match_score],
              ['Consistency', result.consistency_score],
            ].map(([label, value]) => (
              <div key={label as string}>
                <div className="flex justify-between text-sm mb-1">
                  <span>{label}</span>
                  <span>{percent(value as number)}</span>
                </div>
                <Progress value={value as number} className="h-2" />
              </div>
            ))}
            {result.recommendations.length > 0 && (
              <div>
                <p className="text-sm font-semibold mb-2">Recommendations</p>
                <ul className="list-disc pl-5 text-sm space-y-1">
                  {result.recommendations.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
