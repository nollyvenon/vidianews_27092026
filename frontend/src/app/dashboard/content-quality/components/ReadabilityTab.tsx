/**
 * Module 64: Content Readability Analysis
 * Flesch, Gunning Fog, SMOG, and more
 */

'use client';

import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { BookOpen, BarChart3, Target } from 'lucide-react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface ReadabilityResult {
  id: number;
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
}

export default function ReadabilityTab() {
  const [content, setContent] = useState('');
  const [result, setResult] = useState<ReadabilityResult | null>(null);

  const checkMutation = useMutation({
    mutationFn: async () => {
      const response = await fetch(`${API_BASE}/content/readability/check`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          content_id: 1,
          text: content,
        }),
      });
      if (!response.ok) throw new Error('Readability check failed');
      return response.json();
    },
    onSuccess: (data) => {
      setResult(data);
    },
  });

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'Easy':
        return 'text-green-600 bg-green-50';
      case 'Moderate':
        return 'text-blue-600 bg-blue-50';
      case 'Difficult':
        return 'text-orange-600 bg-orange-50';
      case 'Very Difficult':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getMetricDescription = (score: number) => {
    if (score >= 90) return 'Very Easy - 5th grade level';
    if (score >= 80) return 'Easy - 6th grade level';
    if (score >= 70) return 'Fairly Easy - 7th grade level';
    if (score >= 60) return 'Standard - 8th-9th grade level';
    if (score >= 50) return 'Fairly Difficult - 10th-12th grade level';
    if (score >= 30) return 'Difficult - College level';
    return 'Very Difficult - College graduate level';
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <Card>
        <CardHeader>
          <CardTitle>Analyze Readability</CardTitle>
          <CardDescription>
            Check readability metrics and complexity of your content
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea
            placeholder="Paste your content here..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="min-h-48"
          />

          <Button
            onClick={() => checkMutation.mutate()}
            disabled={!content.trim() || checkMutation.isPending}
            className="w-full"
          >
            {checkMutation.isPending ? 'Analyzing...' : 'Check Readability'}
          </Button>
        </CardContent>
      </Card>

      {/* Results Section */}
      {result && (
        <>
          {/* Main Readability Score */}
          <Card className={getLevelColor(result.readability_level)}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5" />
                Readability Level
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <p className="text-sm font-semibold mb-2">Reading Level</p>
                  <p className="text-3xl font-bold">{result.readability_level}</p>
                  <p className="text-sm text-gray-600 mt-1">{result.target_audience_grade_level}</p>
                </div>

                <div>
                  <p className="text-sm font-semibold mb-2">Complexity Score</p>
                  <div className="text-3xl font-bold">{result.complexity_score.toFixed(0)}</div>
                  <p className="text-xs text-gray-600 mt-1">
                    {result.complexity_score > 70
                      ? 'High complexity'
                      : result.complexity_score > 40
                      ? 'Moderate complexity'
                      : 'Low complexity'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Readability Metrics */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Readability Metrics
              </CardTitle>
              <CardDescription>
                Multiple readability indexes for comprehensive analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Flesch Reading Ease */}
                <div className="border rounded-lg p-4">
                  <p className="font-semibold text-sm mb-3">Flesch Reading Ease</p>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-2xl font-bold">{result.flesch_reading_ease.toFixed(1)}</span>
                      <span className="text-xs bg-gray-100 px-2 py-1 rounded">0-100</span>
                    </div>
                    <p className="text-xs text-gray-600">
                      {getMetricDescription(result.flesch_reading_ease)}
                    </p>
                  </div>
                </div>

                {/* Flesch-Kincaid Grade */}
                <div className="border rounded-lg p-4">
                  <p className="font-semibold text-sm mb-3">Flesch-Kincaid Grade</p>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-2xl font-bold">{result.flesch_kincaid_grade.toFixed(1)}</span>
                      <span className="text-xs bg-gray-100 px-2 py-1 rounded">Grade Level</span>
                    </div>
                    <p className="text-xs text-gray-600">
                      Requires grade {Math.round(result.flesch_kincaid_grade)} level education
                    </p>
                  </div>
                </div>

                {/* Gunning Fog */}
                <div className="border rounded-lg p-4">
                  <p className="font-semibold text-sm mb-3">Gunning Fog Index</p>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-2xl font-bold">{result.gunning_fog_index.toFixed(1)}</span>
                      <span className="text-xs bg-gray-100 px-2 py-1 rounded">Grade Level</span>
                    </div>
                    <p className="text-xs text-gray-600">
                      Years of education needed to understand
                    </p>
                  </div>
                </div>

                {/* SMOG */}
                <div className="border rounded-lg p-4">
                  <p className="font-semibold text-sm mb-3">SMOG Index</p>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-2xl font-bold">{result.smog_index.toFixed(1)}</span>
                      <span className="text-xs bg-gray-100 px-2 py-1 rounded">Grade Level</span>
                    </div>
                    <p className="text-xs text-gray-600">
                      Based on polysyllabic word count
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Content Statistics */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5" />
                Content Statistics
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <p className="text-sm font-semibold text-gray-600">Words</p>
                  <p className="text-2xl font-bold">{result.word_count}</p>
                </div>

                <div className="text-center">
                  <p className="text-sm font-semibold text-gray-600">Sentences</p>
                  <p className="text-2xl font-bold">{result.sentence_count}</p>
                </div>

                <div className="text-center">
                  <p className="text-sm font-semibold text-gray-600">Paragraphs</p>
                  <p className="text-2xl font-bold">{result.paragraph_count}</p>
                </div>

                <div className="text-center">
                  <p className="text-sm font-semibold text-gray-600">Avg Sentence</p>
                  <p className="text-2xl font-bold">{result.avg_sentence_length.toFixed(1)} words</p>
                </div>
              </div>

              <div className="mt-6 space-y-3">
                <div>
                  <p className="text-sm font-semibold mb-1">Average Word Length</p>
                  <p className="text-sm text-gray-600">
                    {result.avg_word_length.toFixed(1)} characters per word
                    {result.avg_word_length > 5.5
                      ? ' - Consider using shorter words'
                      : result.avg_word_length < 4.5
                      ? ' - Good word length'
                      : ' - Optimal word length'}
                  </p>
                </div>

                <div>
                  <p className="text-sm font-semibold mb-1">Average Sentence Length</p>
                  <p className="text-sm text-gray-600">
                    {result.avg_sentence_length.toFixed(1)} words per sentence
                    {result.avg_sentence_length > 20
                      ? ' - Consider breaking into shorter sentences'
                      : result.avg_sentence_length < 10
                      ? ' - Sentences might be too short'
                      : ' - Good sentence length'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle>Improvement Tips</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {result.complexity_score > 70 && (
                  <li className="flex items-start gap-2 text-sm">
                    <span className="text-orange-600 font-bold">•</span>
                    <span>Consider simplifying complex sentences and using shorter words</span>
                  </li>
                )}
                {result.avg_sentence_length > 20 && (
                  <li className="flex items-start gap-2 text-sm">
                    <span className="text-orange-600 font-bold">•</span>
                    <span>Break long sentences into shorter, more digestible ones</span>
                  </li>
                )}
                {result.avg_word_length > 5.5 && (
                  <li className="flex items-start gap-2 text-sm">
                    <span className="text-orange-600 font-bold">•</span>
                    <span>Replace complex words with simpler alternatives</span>
                  </li>
                )}
                {result.flesch_reading_ease >= 60 && result.flesch_reading_ease < 70 && (
                  <li className="flex items-start gap-2 text-sm">
                    <span className="text-green-600 font-bold">✓</span>
                    <span>Good readability level for general audience</span>
                  </li>
                )}
              </ul>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
