/**
 * Module 62: AI Proofreading
 * Grammar, spelling, and style checking
 */

'use client';

import React, { useEffect, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { AlertCircle, AlertTriangle, Info } from 'lucide-react';
import { ContentPicker, ContentOption } from '@/components/content/content-picker';

interface ProofreadingIssue {
  id: number;
  type: string;
  severity: string;
  text: string;
  suggestion: string;
  position: number;
  length: number;
}

interface ProofreadingResult {
  id: number;
  content_id: number;
  quality_score: number;
  overall_rating: string;
  total_issues: number;
  grammar_issues: number;
  spelling_issues: number;
  punctuation_issues: number;
  style_issues: number;
  issues: ProofreadingIssue[];
}

const SEVERITY_CLASSES: Record<string, string> = {
  error: 'bg-red-100 text-red-800',
  warning: 'bg-yellow-100 text-yellow-800',
  info: 'bg-blue-100 text-blue-800',
};

const RATING_CLASSES: Record<string, string> = {
  Excellent: 'text-green-600',
  Good: 'text-blue-600',
  Fair: 'text-yellow-600',
  Poor: 'text-red-600',
};

function SeverityIcon({ severity }: { severity: string }) {
  if (severity === 'error') return <AlertCircle className="h-4 w-4" />;
  if (severity === 'warning') return <AlertTriangle className="h-4 w-4" />;
  return <Info className="h-4 w-4" />;
}

export default function ProofreadingTab() {
  const [content, setContent] = useState('');
  const [selected, setSelected] = useState<ContentOption | null>(null);
  const [checkOptions, setCheckOptions] = useState({ grammar: true, spelling: true, style: true });
  const [result, setResult] = useState<ProofreadingResult | null>(null);
  const [applied, setApplied] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [saveStatus, setSaveStatus] = useState<string | null>(null);

  useEffect(() => {
    if (selected?.body !== undefined) setContent(selected.body ?? '');
  }, [selected]);

  const checkMutation = useMutation({
    mutationFn: async () => {
      const check = await ApiClient.post('/proofread', {
        content_id: selected?.id,
        text: content,
        check_grammar: checkOptions.grammar,
        check_spelling: checkOptions.spelling,
        check_style: checkOptions.style,
      });
      return ApiClient.get(`/proofread/${check.id}`) as Promise<ProofreadingResult>;
    },
    onSuccess: (data) => {
      setApplied(null);
      setResult(data);
    },
  });

  /** Persists the edited text to the chosen content item. Applying a suggestion only changes the editor until this runs. */
  const saveToContent = async () => {
    if (!selected) return;
    setSaving(true);
    setSaveError(null);
    setSaveStatus(null);
    try {
      await ApiClient.put(`/content/${selected.id}`, { body: content });
      setSelected({ ...selected, body: content });
      setSaveStatus('Saved to the content item.');
    } catch (err) {
      setSaveError(errorMessage(err, 'The text could not be saved to the content.'));
    } finally {
      setSaving(false);
    }
  };

  /** Replaces the first occurrence of the flagged text in the editor with its suggestion. */
  const applySuggestion = (issue: ProofreadingIssue) => {
    if (!content.includes(issue.text)) {
      setApplied(`"${issue.text}" is no longer in the text.`);
      return;
    }
    setContent(content.replace(issue.text, issue.suggestion));
    setApplied(`Applied "${issue.suggestion}".`);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Check Content</CardTitle>
          <CardDescription>Choose the content to proofread; its text loads here and can be edited.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <ContentPicker value={selected?.id ?? null} onChange={setSelected} />
          <Textarea
            placeholder="Choose content above to load its text…"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="min-h-48"
          />
          <div className="flex flex-wrap items-center gap-3">
            <Button
              variant="outline"
              onClick={saveToContent}
              disabled={!selected || saving || content === (selected?.body ?? '')}
            >
              {saving ? 'Saving…' : 'Save text to content'}
            </Button>
            {saveStatus && <p role="status" className="text-sm text-gray-700">{saveStatus}</p>}
            {saveError && <p role="alert" className="text-sm text-red-700">{saveError}</p>}
          </div>

          <div className="space-y-3">
            <p className="text-sm font-semibold">Check Options</p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {(['grammar', 'spelling', 'style'] as const).map((option) => (
                <label key={option} className="flex items-center gap-2 cursor-pointer">
                  <Checkbox
                    checked={checkOptions[option]}
                    onCheckedChange={(checked) => setCheckOptions({ ...checkOptions, [option]: !!checked })}
                  />
                  <span className="text-sm capitalize">{option}</span>
                </label>
              ))}
            </div>
          </div>

          {checkMutation.isError && (
            <p role="alert" className="text-sm text-red-700">
              {errorMessage(checkMutation.error, 'The proofreading check failed.')}
            </p>
          )}

          <Button
            onClick={() => checkMutation.mutate()}
            disabled={!selected || !content.trim() || checkMutation.isPending}
            className="w-full"
          >
            {checkMutation.isPending ? 'Checking...' : 'Check Proofreading'}
          </Button>
        </CardContent>
      </Card>

      {result && (
        <>
          <Card>
            <CardHeader>
              <CardTitle>Quality Score</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className={`text-5xl font-bold ${RATING_CLASSES[result.overall_rating] ?? 'text-gray-700'}`}>
                    {Number(result.quality_score).toFixed(1)}
                  </div>
                  <p className={`text-lg font-semibold ${RATING_CLASSES[result.overall_rating] ?? ''}`}>
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
              {applied && <p role="status" className="text-sm text-gray-700 mb-3">{applied}</p>}
              {result.issues.length === 0 ? (
                <p className="text-center text-green-700 py-6">No issues found</p>
              ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {result.issues.map((issue) => (
                    <div key={issue.id} className="border rounded-lg p-3 hover:bg-gray-50 transition">
                      <div className="flex items-start justify-between gap-3">
                        <div className="flex items-start gap-3 flex-1">
                          <SeverityIcon severity={issue.severity} />
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <code className="bg-gray-100 px-2 py-1 rounded text-sm font-mono">{issue.text}</code>
                              <Badge className={SEVERITY_CLASSES[issue.severity] ?? 'bg-gray-100 text-gray-800'}>
                                {issue.type}
                              </Badge>
                            </div>
                            <p className="text-sm text-blue-600">
                              Suggested: <strong>{issue.suggestion}</strong>
                            </p>
                          </div>
                        </div>
                        <Button size="sm" variant="ghost" onClick={() => applySuggestion(issue)}>
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
