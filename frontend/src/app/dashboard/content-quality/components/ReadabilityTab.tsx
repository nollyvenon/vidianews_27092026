/**
 * Module 64: Content Readability Analysis
 * Flesch, Gunning Fog, SMOG, and more
 */

'use client';

import React, { useEffect, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, BarChart3, Target } from 'lucide-react';
import { ContentPicker, ContentOption } from '@/components/content/content-picker';

interface ReadabilityResult {
  id: number;
  content_id: number;
  word_count: number;
  sentence_count: number;
  paragraph_count: number;
  flesch_reading_ease: number;
  flesch_kincaid_grade: number;
  gunning_fog_index: number;
  smog_index: number;
  readability_level: string;
  target_audience_grade_level: string;
  complexity_score: number;
  avg_word_length: number;
  avg_sentence_length: number;
  recommendations: string[];
}

const LEVEL_CLASSES: Record<string, string> = {
  Easy: 'text-green-600 bg-green-50',
  Moderate: 'text-blue-600 bg-blue-50',
  Difficult: 'text-orange-600 bg-orange-50',
  'Very Difficult': 'text-red-600 bg-red-50',
};

/** Plain-language band for a Flesch Reading Ease score. */
export function describeReadingEase(score: number): string {
  if (score >= 90) return 'Very Easy - 5th grade level';
  if (score >= 80) return 'Easy - 6th grade level';
  if (score >= 70) return 'Fairly Easy - 7th grade level';
  if (score >= 60) return 'Standard - 8th-9th grade level';
  if (score >= 50) return 'Fairly Difficult - 10th-12th grade level';
  if (score >= 30) return 'Difficult - College level';
  return 'Very Difficult - College graduate level';
}

export default function ReadabilityTab() {
  const [content, setContent] = useState('');
  const [selected, setSelected] = useState<ContentOption | null>(null);
  const [result, setResult] = useState<ReadabilityResult | null>(null);

  useEffect(() => {
    if (selected?.body !== undefined) setContent(selected.body ?? '');
  }, [selected]);

  const checkMutation = useMutation({
    mutationFn: () => ApiClient.post('/readability/check', { content_id: selected?.id, text: content }),
    onSuccess: (data: ReadabilityResult) => setResult(data),
  });

  const fixed = (value: number, digits = 1) => Number(value).toFixed(digits);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Analyze Readability</CardTitle>
          <CardDescription>Choose the content to analyse; its text loads here and can be edited.</CardDescription>
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
              {errorMessage(checkMutation.error, 'The readability check failed.')}
            </p>
          )}
          <Button
            onClick={() => checkMutation.mutate()}
            disabled={!selected || !content.trim() || checkMutation.isPending}
            className="w-full"
          >
            {checkMutation.isPending ? 'Analyzing...' : 'Check Readability'}
          </Button>
        </CardContent>
      </Card>

      {result && (
        <>
          <Card className={LEVEL_CLASSES[result.readability_level] ?? 'bg-gray-50 text-gray-600'}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5" />
                Readability Level
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm font-semibold mb-2">Reading Level</p>
                <p className="text-3xl font-bold">{result.readability_level}</p>
                <p className="text-sm text-gray-600 mt-1">{result.target_audience_grade_level}</p>
              </div>
              <div>
                <p className="text-sm font-semibold mb-2">Complexity Score</p>
                <div className="text-3xl font-bold">{fixed(result.complexity_score, 0)}</div>
                <p className="text-xs text-gray-600 mt-1">
                  {result.complexity_score > 70 ? 'High complexity' : result.complexity_score > 40 ? 'Moderate complexity' : 'Low complexity'}
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Readability Metrics
              </CardTitle>
              <CardDescription>Multiple readability indexes for comprehensive analysis</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="border rounded-lg p-4">
                  <p className="font-semibold text-sm mb-3">Flesch Reading Ease</p>
                  <span className="text-2xl font-bold">{fixed(result.flesch_reading_ease)}</span>
                  <p className="text-xs text-gray-600 mt-2">{describeReadingEase(result.flesch_reading_ease)}</p>
                </div>
                <div className="border rounded-lg p-4">
                  <p className="font-semibold text-sm mb-3">Flesch-Kincaid Grade</p>
                  <span className="text-2xl font-bold">{fixed(result.flesch_kincaid_grade)}</span>
                  <p className="text-xs text-gray-600 mt-2">Requires grade {Math.round(result.flesch_kincaid_grade)} level education</p>
                </div>
                <div className="border rounded-lg p-4">
                  <p className="font-semibold text-sm mb-3">Gunning Fog Index</p>
                  <span className="text-2xl font-bold">{fixed(result.gunning_fog_index)}</span>
                  <p className="text-xs text-gray-600 mt-2">Years of education needed to understand</p>
                </div>
                <div className="border rounded-lg p-4">
                  <p className="font-semibold text-sm mb-3">SMOG Index</p>
                  <span className="text-2xl font-bold">{fixed(result.smog_index)}</span>
                  <p className="text-xs text-gray-600 mt-2">Based on polysyllabic word count</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5" />
                Content Statistics
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div>
                  <p className="text-sm font-semibold text-gray-600">Words</p>
                  <p className="text-2xl font-bold">{result.word_count}</p>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-600">Sentences</p>
                  <p className="text-2xl font-bold">{result.sentence_count}</p>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-600">Paragraphs</p>
                  <p className="text-2xl font-bold">{result.paragraph_count}</p>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-600">Avg Sentence</p>
                  <p className="text-2xl font-bold">{fixed(result.avg_sentence_length)} words</p>
                </div>
              </div>
              <p className="text-sm text-gray-600">
                Average word length: {fixed(result.avg_word_length)} characters per word
              </p>
              {result.recommendations.length > 0 && (
                <div>
                  <p className="text-sm font-semibold mb-2">Improvement tips</p>
                  <ul className="list-disc pl-5 text-sm space-y-1">
                    {result.recommendations.map((tip) => (
                      <li key={tip}>{tip}</li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
