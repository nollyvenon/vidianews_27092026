/**
 * Module 62: AI Proofreading
 * Grammar, spelling, and style checking
 */

'use client';

import React, { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { AlertCircle, CheckCircle2, AlertTriangle, Info } from 'lucide-react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface ProofreadingIssue {
  id: number;
  issue_type: string;
  severity: string;
  text: string;
  suggestion: string;
  position: number;
  length: number;
}

interface ProofreadingResult {
  id: number;
  quality_score: number;
  overall_rating: string;
  total_issues: number;
  grammar_issues: number;
  spelling_issues: number;
  punctuation_issues: number;
  style_issues: number;
  issues?: ProofreadingIssue[];
}

export default function ProofreadingTab() {
  const [content, setContent] = useState('');
  const [checkOptions, setCheckOptions] = useState({
    grammar: true,
    spelling: true,
    style: true,
  });
  const [result, setResult] = useState<ProofreadingResult | null>(null);
  const [expandedIssues, setExpandedIssues] = useState<Set<number>>(new Set());

  const checkMutation = useMutation({
    mutationFn: async () => {
      const response = await fetch(`${API_BASE}/content/proofread`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          content_id: 1, // Default content ID
          text: content,
          check_grammar: checkOptions.grammar,
          check_spelling: checkOptions.spelling,
          check_style: checkOptions.style,
        }),
      });
      if (!response.ok) throw new Error('Proofreading check failed');
      return response.json();
    },
    onSuccess: (data) => {
      setResult(data);
    },
  });

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'error':
        return 'bg-red-100 text-red-800';
      case 'warning':
        return 'bg-yellow-100 text-yellow-800';
      case 'info':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getRatingColor = (rating: string) => {
    switch (rating) {
      case 'Excellent':
        return 'text-green-600';
      case 'Good':
        return 'text-blue-600';
      case 'Fair':
        return 'text-yellow-600';
      default:
        return 'text-red-600';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'error':
        return <AlertCircle className="h-4 w-4" />;
      case 'warning':
        return <AlertTriangle className="h-4 w-4" />;
      default:
        return <Info className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <Card>
        <CardHeader>
          <CardTitle>Check Content</CardTitle>
          <CardDescription>
            Paste your content to check for grammar, spelling, and style issues
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea
            placeholder="Paste your content here..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="min-h-48"
          />

          <div className="space-y-3">
            <p className="text-sm font-semibold">Check Options</p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <label className="flex items-center gap-2 cursor-pointer">
                <Checkbox
                  checked={checkOptions.grammar}
                  onCheckedChange={(checked) =>
                    setCheckOptions({ ...checkOptions, grammar: !!checked })
                  }
                />
                <span className="text-sm">Grammar</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <Checkbox
                  checked={checkOptions.spelling}
                  onCheckedChange={(checked) =>
                    setCheckOptions({ ...checkOptions, spelling: !!checked })
                  }
                />
                <span className="text-sm">Spelling</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <Checkbox
                  checked={checkOptions.style}
                  onCheckedChange={(checked) =>
                    setCheckOptions({ ...checkOptions, style: !!checked })
                  }
                />
                <span className="text-sm">Style</span>
              </label>
            </div>
          </div>

          <Button
            onClick={() => checkMutation.mutate()}
            disabled={!content.trim() || checkMutation.isPending}
            className="w-full"
          >
            {checkMutation.isPending ? 'Checking...' : 'Check Proofreading'}
          </Button>
        </CardContent>
      </Card>

      {/* Results Section */}
      {result && (
        <>
          {/* Score Summary */}
          <Card>
            <CardHeader>
              <CardTitle>Quality Score</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className={`text-5xl font-bold ${getRatingColor(result.overall_rating)}`}>
                    {result.quality_score.toFixed(1)}
                  </div>
                  <p className={`text-lg font-semibold ${getRatingColor(result.overall_rating)}`}>
                    {result.overall_rating}
                  </p>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Total Issues</span>
                    <Badge variant="outline">{result.total_issues}</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Grammar</span>
                    <Badge>{result.grammar_issues}</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Spelling</span>
                    <Badge>{result.spelling_issues}</Badge>
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Punctuation</span>
                    <Badge>{result.punctuation_issues}</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Style</span>
                    <Badge>{result.style_issues}</Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Issues List */}
          <Card>
            <CardHeader>
              <CardTitle>Issues Found</CardTitle>
              <CardDescription>
                {result.total_issues === 0
                  ? 'Great! No issues found.'
                  : `${result.total_issues} issue${result.total_issues !== 1 ? 's' : ''} found`}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {result.total_issues === 0 ? (
                <div className="flex items-center gap-2 text-green-600 py-8 justify-center">
                  <CheckCircle2 className="h-5 w-5" />
                  <span>No issues found</span>
                </div>
              ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {/* Mock issues for demo */}
                  {[
                    {
                      id: 1,
                      type: 'spelling',
                      severity: 'error',
                      text: 'recieve',
                      suggestion: 'receive',
                      explanation: 'Common spelling error',
                    },
                    {
                      id: 2,
                      type: 'grammar',
                      severity: 'warning',
                      text: 'their',
                      suggestion: 'there',
                      explanation: 'Should use "there" in this context',
                    },
                    {
                      id: 3,
                      type: 'style',
                      severity: 'info',
                      text: 'very good',
                      suggestion: 'excellent',
                      explanation: 'Consider using a stronger word',
                    },
                  ].map((issue) => (
                    <div
                      key={issue.id}
                      className="border rounded-lg p-3 hover:bg-gray-50 transition"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-3 flex-1">
                          {getSeverityIcon(issue.severity)}
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <code className="bg-gray-100 px-2 py-1 rounded text-sm font-mono">
                                {issue.text}
                              </code>
                              <Badge className={getSeverityColor(issue.severity)}>
                                {issue.type}
                              </Badge>
                            </div>
                            <p className="text-sm text-gray-600">{issue.explanation}</p>
                            <p className="text-sm text-blue-600 mt-1">
                              Suggested: <strong>{issue.suggestion}</strong>
                            </p>
                          </div>
                        </div>
                        <Button size="sm" variant="ghost">
                          Apply
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
