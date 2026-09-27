/**
 * Module 63: Plagiarism Detection
 * Originality and source matching
 */

'use client';

import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { AlertCircle, CheckCircle2, AlertTriangle, ExternalLink } from 'lucide-react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface Source {
  url: string;
  similarity_percent: number;
  matched_text: string;
}

interface PlagiarismResult {
  id: number;
  similarity_percentage: number;
  originality_percentage: number;
  plagiarism_risk: string;
  status: string;
  total_sources_found: number;
  ai_content_percentage: number;
  human_content_percentage: number;
  detected_sources: Source[];
}

export default function PlagiarismTab() {
  const [content, setContent] = useState('');
  const [result, setResult] = useState<PlagiarismResult | null>(null);

  const checkMutation = useMutation({
    mutationFn: async () => {
      const response = await fetch(`${API_BASE}/content/plagiarism/check`, {
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
      if (!response.ok) throw new Error('Plagiarism check failed');
      return response.json();
    },
    onSuccess: (data) => {
      setResult(data);
    },
  });

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'Low':
        return 'text-green-600 bg-green-50';
      case 'Medium':
        return 'text-yellow-600 bg-yellow-50';
      case 'High':
        return 'text-orange-600 bg-orange-50';
      case 'Critical':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getRiskBadgeColor = (risk: string) => {
    switch (risk) {
      case 'Low':
        return 'bg-green-100 text-green-800';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'High':
        return 'bg-orange-100 text-orange-800';
      case 'Critical':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <Card>
        <CardHeader>
          <CardTitle>Check Plagiarism</CardTitle>
          <CardDescription>
            Analyze your content for plagiarism and originality
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
            {checkMutation.isPending ? 'Analyzing...' : 'Check Plagiarism'}
          </Button>
        </CardContent>
      </Card>

      {/* Results Section */}
      {result && (
        <>
          {/* Risk Overview */}
          <Card className={getRiskColor(result.plagiarism_risk)}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Plagiarism Assessment</CardTitle>
                {result.plagiarism_risk === 'Low' && <CheckCircle2 className="h-6 w-6" />}
                {result.plagiarism_risk === 'Medium' && <AlertTriangle className="h-6 w-6" />}
                {['High', 'Critical'].includes(result.plagiarism_risk) && (
                  <AlertCircle className="h-6 w-6" />
                )}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div>
                  <p className="text-sm font-semibold mb-2">Similarity</p>
                  <div className="text-3xl font-bold">{result.similarity_percentage.toFixed(1)}%</div>
                </div>

                <div>
                  <p className="text-sm font-semibold mb-2">Originality</p>
                  <div className="text-3xl font-bold">{result.originality_percentage.toFixed(1)}%</div>
                </div>

                <div>
                  <p className="text-sm font-semibold mb-2">Risk Level</p>
                  <Badge className={getRiskBadgeColor(result.plagiarism_risk)}>
                    {result.plagiarism_risk}
                  </Badge>
                </div>

                <div>
                  <p className="text-sm font-semibold mb-2">Status</p>
                  <Badge variant="outline">{result.status}</Badge>
                </div>
              </div>

              <div className="space-y-3">
                <div>
                  <p className="text-sm font-semibold mb-2">Similarity Distribution</p>
                  <Progress
                    value={result.similarity_percentage}
                    className="h-2"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-gray-600">Human Content</p>
                    <p className="text-lg font-semibold">{result.human_content_percentage.toFixed(1)}%</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">AI Content</p>
                    <p className="text-lg font-semibold">{result.ai_content_percentage.toFixed(1)}%</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Sources Found */}
          {result.total_sources_found > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Matched Sources</CardTitle>
                <CardDescription>
                  Found {result.total_sources_found} potential source{result.total_sources_found !== 1 ? 's' : ''}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {result.detected_sources.map((source, idx) => (
                    <div key={idx} className="border rounded-lg p-3 hover:bg-gray-50 transition">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="font-semibold text-sm mb-2 line-clamp-1">{source.url}</p>
                          <div className="space-y-2">
                            <div className="flex items-center justify-between">
                              <span className="text-xs text-gray-600">Similarity: {source.similarity_percent}%</span>
                              <Progress value={source.similarity_percent} className="h-1 w-24" />
                            </div>
                            <p className="text-xs text-gray-600 italic">
                              "{source.matched_text.substring(0, 80)}..."
                            </p>
                          </div>
                        </div>
                        <a
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800 ml-4 flex-shrink-0"
                        >
                          <ExternalLink className="h-4 w-4" />
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle>Recommendations</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {result.similarity_percentage < 10 && (
                  <li className="flex items-start gap-2 text-sm">
                    <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                    <span>Excellent! Your content is highly original.</span>
                  </li>
                )}
                {result.ai_content_percentage > 30 && (
                  <li className="flex items-start gap-2 text-sm">
                    <AlertTriangle className="h-4 w-4 text-yellow-600 mt-0.5 flex-shrink-0" />
                    <span>High AI-generated content detected. Consider adding more original insights.</span>
                  </li>
                )}
                {result.similarity_percentage > 20 && (
                  <li className="flex items-start gap-2 text-sm">
                    <AlertTriangle className="h-4 w-4 text-yellow-600 mt-0.5 flex-shrink-0" />
                    <span>Add proper citations for quoted or paraphrased content.</span>
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
