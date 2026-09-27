/**
 * Module 65: Brand Voice Consistency Checking
 * Ensure content aligns with brand guidelines
 */

'use client';

import React, { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { AlertCircle, CheckCircle2, AlertTriangle, TrendingUp } from 'lucide-react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface VoiceViolation {
  id: number;
  violation_type: string;
  severity: string;
  description: string;
  suggested_fix: string;
}

interface BrandVoiceResult {
  id: number;
  consistency_score: number;
  compliance_percentage: number;
  brand_alignment: string;
  total_violations: number;
  tone_violations: number;
  style_violations: number;
  terminology_violations: number;
  violations: VoiceViolation[];
}

export default function BrandVoiceTab() {
  const [content, setContent] = useState('');
  const [result, setResult] = useState<BrandVoiceResult | null>(null);

  const checkMutation = useMutation({
    mutationFn: async () => {
      const response = await fetch(`${API_BASE}/content/brand-voice/check`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          content_id: 1,
          text: content,
          brand_voice_guide_id: 1,
        }),
      });
      if (!response.ok) throw new Error('Brand voice check failed');
      return response.json();
    },
    onSuccess: (data) => {
      setResult(data);
    },
  });

  const getAlignmentColor = (alignment: string) => {
    switch (alignment) {
      case 'Excellent':
        return 'text-green-600 bg-green-50';
      case 'Good':
        return 'text-blue-600 bg-blue-50';
      case 'Fair':
        return 'text-yellow-600 bg-yellow-50';
      case 'Poor':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 text-red-800';
      case 'high':
        return 'bg-orange-100 text-orange-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
      case 'high':
        return <AlertCircle className="h-4 w-4" />;
      case 'medium':
        return <AlertTriangle className="h-4 w-4" />;
      default:
        return <CheckCircle2 className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <Card>
        <CardHeader>
          <CardTitle>Check Brand Voice</CardTitle>
          <CardDescription>
            Verify your content aligns with brand guidelines and tone
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
            {checkMutation.isPending ? 'Analyzing...' : 'Check Brand Voice'}
          </Button>
        </CardContent>
      </Card>

      {/* Results Section */}
      {result && (
        <>
          {/* Alignment Overview */}
          <Card className={getAlignmentColor(result.brand_alignment)}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Brand Voice Alignment
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <p className="text-sm font-semibold mb-2">Consistency Score</p>
                  <div className="text-3xl font-bold">{result.consistency_score.toFixed(1)}</div>
                  <p className="text-sm text-gray-600 mt-1">out of 100</p>
                </div>

                <div>
                  <p className="text-sm font-semibold mb-2">Alignment Status</p>
                  <p className="text-3xl font-bold">{result.brand_alignment}</p>
                  <p className="text-sm text-gray-600 mt-1">
                    {result.compliance_percentage.toFixed(1)}% compliant
                  </p>
                </div>
              </div>

              <div>
                <p className="text-sm font-semibold mb-2">Compliance Level</p>
                <Progress value={result.compliance_percentage} className="h-2" />
              </div>
            </CardContent>
          </Card>

          {/* Violation Categories */}
          <Card>
            <CardHeader>
              <CardTitle>Violation Summary</CardTitle>
              <CardDescription>
                Total violations found: {result.total_violations}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="border rounded-lg p-4">
                  <p className="text-sm font-semibold mb-2">Tone Violations</p>
                  <div className="text-2xl font-bold text-orange-600">
                    {result.tone_violations}
                  </div>
                  <p className="text-xs text-gray-600 mt-1">
                    Voice inconsistencies detected
                  </p>
                </div>

                <div className="border rounded-lg p-4">
                  <p className="text-sm font-semibold mb-2">Style Violations</p>
                  <div className="text-2xl font-bold text-blue-600">
                    {result.style_violations}
                  </div>
                  <p className="text-xs text-gray-600 mt-1">
                    Writing style mismatches
                  </p>
                </div>

                <div className="border rounded-lg p-4">
                  <p className="text-sm font-semibold mb-2">Terminology Violations</p>
                  <div className="text-2xl font-bold text-red-600">
                    {result.terminology_violations}
                  </div>
                  <p className="text-xs text-gray-600 mt-1">
                    Brand terminology issues
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Detailed Violations */}
          {result.violations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Issues Found</CardTitle>
                <CardDescription>
                  {result.violations.length} issue{result.violations.length !== 1 ? 's' : ''} to address
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {result.violations.map((violation) => (
                    <div
                      key={violation.id}
                      className="border rounded-lg p-3 hover:bg-gray-50 transition"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div className="flex items-start gap-3 flex-1">
                          {getSeverityIcon(violation.severity)}
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <span className="font-semibold text-sm">
                                {violation.violation_type}
                              </span>
                              <Badge className={getSeverityColor(violation.severity)}>
                                {violation.severity}
                              </Badge>
                            </div>
                            <p className="text-sm text-gray-600 mb-2">
                              {violation.description}
                            </p>
                            <p className="text-sm text-blue-600">
                              Suggestion: <strong>{violation.suggested_fix}</strong>
                            </p>
                          </div>
                        </div>
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
              <CardTitle>Improvement Recommendations</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {result.consistency_score < 70 && (
                  <li className="flex items-start gap-2 text-sm">
                    <span className="text-orange-600 font-bold">•</span>
                    <span>Review and align content tone with established brand voice guidelines</span>
                  </li>
                )}
                {result.tone_violations > 3 && (
                  <li className="flex items-start gap-2 text-sm">
                    <span className="text-orange-600 font-bold">•</span>
                    <span>Multiple tone inconsistencies detected. Consider rewriting key sections</span>
                  </li>
                )}
                {result.terminology_violations > 2 && (
                  <li className="flex items-start gap-2 text-sm">
                    <span className="text-orange-600 font-bold">•</span>
                    <span>Use standard terminology from brand guidelines for technical terms</span>
                  </li>
                )}
                {result.style_violations > 3 && (
                  <li className="flex items-start gap-2 text-sm">
                    <span className="text-orange-600 font-bold">•</span>
                    <span>Adjust writing style to match brand formatting and structure standards</span>
                  </li>
                )}
                {result.compliance_percentage >= 90 && (
                  <li className="flex items-start gap-2 text-sm">
                    <span className="text-green-600 font-bold">✓</span>
                    <span>Excellent brand voice alignment! Content is well-aligned with guidelines</span>
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
