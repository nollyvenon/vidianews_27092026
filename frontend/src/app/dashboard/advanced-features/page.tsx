'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';

interface Summary {
  recommendations: {
    total: number;
    click_through_rate: number;
    conversion_rate: number;
    by_type: { type: string; count: number; click_through_rate: number; conversion_rate: number }[];
  };
  retention: { subscribers: number; at_risk: number; average_churn_risk: number };
  personalization: { profiles: number; average_score: number };
  predictions: { deployed_models: number; average_accuracy: number; predictions_this_month: number };
  performance: { measured_endpoints: number; total_calls: number; average_response_time_ms: number };
}

interface AbTest {
  id: number;
  name: string;
  status: string;
  confidence: number;
  winner: string | null;
}

interface Insight {
  id: number;
  type: string;
  title: string;
  confidence_level: number;
}

interface Cohort {
  id: number;
  name: string;
  user_count: number;
}

const percent = (value: number) => `${value.toFixed(1)}%`;

/** Recommendations, retention, A/B tests, insights, cohorts, personalization, predictions and performance, from the live platform. */
export default function AdvancedFeaturesPage() {
  const [activeTab, setActiveTab] = useState('recommendations');
  const [summary, setSummary] = useState<Summary | null>(null);
  const [summaryError, setSummaryError] = useState<string | null>(null);
  const [tests, setTests] = useState<AbTest[] | null>(null);
  const [testsError, setTestsError] = useState<string | null>(null);
  const [insights, setInsights] = useState<Insight[] | null>(null);
  const [insightsError, setInsightsError] = useState<string | null>(null);
  const [cohorts, setCohorts] = useState<Cohort[] | null>(null);
  const [cohortsError, setCohortsError] = useState<string | null>(null);

  useEffect(() => {
    ApiClient.get('/advanced/summary')
      .then((data: Summary) => setSummary(data))
      .catch((err) => setSummaryError(errorMessage(err, 'Platform figures could not be loaded.')));
    ApiClient.get('/ab-tests')
      .then((data: AbTest[]) => setTests(Array.isArray(data) ? data : []))
      .catch((err) => setTestsError(errorMessage(err, 'A/B tests could not be loaded.')));
    ApiClient.get('/insights?limit=20')
      .then((data: Insight[]) => setInsights(Array.isArray(data) ? data : []))
      .catch((err) => setInsightsError(errorMessage(err, 'Insights could not be loaded.')));
    ApiClient.get('/cohorts')
      .then((data: Cohort[]) => setCohorts(Array.isArray(data) ? data : []))
      .catch((err) => setCohortsError(errorMessage(err, 'Cohorts could not be loaded.')));
  }, []);

  const completedTests = tests ? tests.filter((test) => test.status === 'completed') : [];
  const winningTests = completedTests.filter((test) => test.winner !== null);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Advanced Features</h1>
        <p className="text-gray-500 mt-2">Personalization, recommendations, retention, and predictions</p>
      </div>
      {summaryError && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{summaryError}</p>}

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4 lg:grid-cols-8">
          <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
          <TabsTrigger value="retention">Retention</TabsTrigger>
          <TabsTrigger value="abtest">A/B Tests</TabsTrigger>
          <TabsTrigger value="insights">Insights</TabsTrigger>
          <TabsTrigger value="cohorts">Cohorts</TabsTrigger>
          <TabsTrigger value="personalization">Personalization</TabsTrigger>
          <TabsTrigger value="predictions">Predictions</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
        </TabsList>

        <TabsContent value="recommendations" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Total Recommendations</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? summary.recommendations.total.toLocaleString() : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">Across all users</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Click-Through Rate</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? percent(summary.recommendations.click_through_rate) : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">Clicked recommendations</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? percent(summary.recommendations.conversion_rate) : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">Converted recommendations</p>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Recommendation Performance by Type</CardTitle>
              <CardDescription>CTR and conversion rates by recommendation type</CardDescription>
            </CardHeader>
            <CardContent>
              {summary && summary.recommendations.by_type.length === 0 ? (
                <p className="text-gray-500">No recommendations have been made yet.</p>
              ) : summary ? (
                <div className="space-y-4">
                  {summary.recommendations.by_type.map((row) => (
                    <div key={row.type} className="flex items-center justify-between">
                      <div>
                        <p className="font-medium">{row.type.replace(/_/g, ' ')}</p>
                        <p className="text-sm text-gray-500">{row.count.toLocaleString()} recommendations</p>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold">{percent(row.click_through_rate)} CTR</p>
                        <p className="text-sm text-gray-500">{percent(row.conversion_rate)} conversion</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">Loading recommendations…</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="retention" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">At-Risk Users</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? summary.retention.at_risk.toLocaleString() : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">
                  {summary && summary.retention.subscribers > 0
                    ? `${percent((summary.retention.at_risk / summary.retention.subscribers) * 100)} of subscribers`
                    : 'Churn risk above 80%'}
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Avg Churn Probability</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? summary.retention.average_churn_risk.toFixed(2) : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">{summary ? `${Math.round(summary.retention.average_churn_risk * 100)}% estimated churn risk` : 'Loading…'}</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="abtest" className="space-y-4">
          {testsError && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{testsError}</p>}
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Active Tests</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{tests ? tests.filter((test) => test.status === 'running').length : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">Running now</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Completed Tests</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{tests ? completedTests.length : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">{winningTests.length} with a winner</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Test Success Rate</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {tests ? (completedTests.length > 0 ? percent((winningTests.length / completedTests.length) * 100) : '0.0%') : '—'}
                </div>
                <p className="text-xs text-gray-500 mt-2">Completed tests with a winner</p>
              </CardContent>
            </Card>
          </div>
          {tests && tests.length > 0 && (
            <Card>
              <CardContent className="pt-6 space-y-2">
                {tests.map((test) => (
                  <div key={test.id} className="flex justify-between p-3 border rounded-lg">
                    <span className="font-medium">{test.name}</span>
                    <span className="text-sm text-gray-600">
                      {test.status} · {test.winner ? `winner: ${test.winner}` : 'no winner yet'}
                    </span>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="insights" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Key Insights</CardTitle>
              <CardDescription>Actionable insights from advanced analytics</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {insightsError && <p role="alert" className="text-red-700">{insightsError}</p>}
              {insights === null && !insightsError ? (
                <p className="text-gray-500">Loading insights…</p>
              ) : insights && insights.length === 0 ? (
                <p className="text-gray-500">No insights have been generated yet.</p>
              ) : insights ? (
                insights.map((insight) => (
                  <div key={insight.id} className="border-l-4 border-blue-500 bg-blue-50 p-4 rounded">
                    <p className="font-semibold text-blue-900">{insight.title}</p>
                    <p className="text-sm text-blue-800 mt-1">{insight.type.replace(/_/g, ' ')}</p>
                    <p className="text-xs text-blue-700 mt-2">Confidence: {Math.round(insight.confidence_level * 100)}%</p>
                  </div>
                ))
              ) : null}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="cohorts" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>User Cohorts</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {cohortsError && <p role="alert" className="text-red-700">{cohortsError}</p>}
              {cohorts === null && !cohortsError ? (
                <p className="text-gray-500">Loading cohorts…</p>
              ) : cohorts && cohorts.length === 0 ? (
                <p className="text-gray-500">No cohorts have been defined yet.</p>
              ) : cohorts ? (
                cohorts.map((cohort) => (
                  <div key={cohort.id} className="flex justify-between items-center p-3 border rounded-lg">
                    <p className="font-medium">{cohort.name}</p>
                    <p className="font-semibold">{cohort.user_count.toLocaleString()} users</p>
                  </div>
                ))
              ) : null}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="personalization" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Avg Personalization Score</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? summary.personalization.average_score.toFixed(2) : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">Scale 0 to 1</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Personalization Profiles</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? summary.personalization.profiles.toLocaleString() : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">Users with a profile</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="predictions" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Deployed Models</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? summary.predictions.deployed_models.toLocaleString() : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">In production</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Avg Model Accuracy</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? summary.predictions.average_accuracy.toFixed(3) : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">Deployed models</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Predictions This Month</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? summary.predictions.predictions_this_month.toLocaleString() : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">Since the first of the month</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="performance" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Measured Endpoints</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? summary.performance.measured_endpoints.toLocaleString() : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">Endpoints with recorded calls</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Total API Calls</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? summary.performance.total_calls.toLocaleString() : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">Recorded calls</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Avg Response Time</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{summary ? `${summary.performance.average_response_time_ms}ms` : '—'}</div>
                <p className="text-xs text-gray-500 mt-2">Weighted by calls</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
