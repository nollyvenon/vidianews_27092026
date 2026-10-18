import React, { FormEvent, useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { CheckCircle2 } from 'lucide-react';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';
import { ContentPicker, ContentOption } from '@/components/content/content-picker';

interface Variant {
  id: number;
  variant_name: string;
  variant_type: string;
  impressions: number;
  clicks: number;
  conversions: number;
  ctr: number;
  conversion_rate: number;
}

interface Campaign {
  id: number;
  name: string;
  content_id: number;
  test_metric: string;
  status: string;
  winner: string | null;
  is_statistically_significant: boolean;
  variants: Variant[];
}

interface Analysis {
  p_value: number;
  is_significant: boolean;
  improvement_percent: number;
  recommended_action: string;
}

const TEST_METRICS = ['engagement', 'clicks', 'conversion', 'dwell_time'];
const VARIANT_TYPES = ['control', 'treatment'];

/** A/B tests for a content item: create them, add variants, record results and analyze. */
export default function ABTestingTab() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analyses, setAnalyses] = useState<Record<number, Analysis>>({});
  const [content, setContent] = useState<ContentOption | null>(null);
  const [name, setName] = useState('');
  const [metric, setMetric] = useState(TEST_METRICS[0]);
  const [hypothesis, setHypothesis] = useState('');

  const load = () =>
    ApiClient.get('/ab-testing/campaigns')
      .then((data: Campaign[]) => setCampaigns(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'A/B tests could not be loaded.')))
      .finally(() => setLoading(false));

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const run = async (action: () => Promise<unknown>) => {
    setError(null);
    try {
      await action();
      await load();
    } catch (err) {
      setError(errorMessage(err, 'That action could not be completed.'));
    }
  };

  const createCampaign = (event: FormEvent) => {
    event.preventDefault();
    if (!content) return;
    return run(async () => {
      await ApiClient.post('/ab-testing/campaigns', {
        content_id: content.id,
        name: name.trim(),
        test_metric: metric,
        hypothesis: hypothesis.trim(),
      });
      setName('');
      setHypothesis('');
    });
  };

  const analyze = async (campaign: Campaign) => {
    setError(null);
    try {
      const result: Analysis = await ApiClient.post(`/ab-testing/campaigns/${campaign.id}/analyze`, {});
      setAnalyses((current) => ({ ...current, [campaign.id]: result }));
      await load();
    } catch (err) {
      setError(errorMessage(err, 'The test could not be analyzed.'));
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>New A/B Test</CardTitle>
          <CardDescription>Compare two or more variants of a content item</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={createCampaign} className="space-y-3">
            <ContentPicker value={content?.id ?? null} onChange={setContent} label="Content to test" />
            <input
              className="w-full border rounded px-3 py-2"
              placeholder="Test name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
            <label className="block text-sm">
              <span className="block mb-1">Measured metric</span>
              <select className="w-full border rounded px-3 py-2" value={metric} onChange={(e) => setMetric(e.target.value)}>
                {TEST_METRICS.map((item) => (
                  <option key={item} value={item}>{item}</option>
                ))}
              </select>
            </label>
            <textarea
              className="w-full border rounded px-3 py-2"
              placeholder="Hypothesis"
              rows={2}
              value={hypothesis}
              onChange={(e) => setHypothesis(e.target.value)}
              required
            />
            <Button type="submit" disabled={!content || !name.trim() || !hypothesis.trim()}>Create test</Button>
          </form>
        </CardContent>
      </Card>

      {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
      {loading ? (
        <p className="text-sm text-gray-500">Loading A/B tests…</p>
      ) : campaigns.length === 0 ? (
        <p className="text-sm text-gray-500">No A/B tests yet.</p>
      ) : (
        campaigns.map((campaign) => (
          <Card key={campaign.id}>
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle>{campaign.name}</CardTitle>
                  <CardDescription>Measured by {campaign.test_metric}</CardDescription>
                </div>
                <Badge variant={campaign.status === 'running' ? 'default' : 'outline'}>{campaign.status}</Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {campaign.variants.length === 0 ? (
                <p className="text-sm text-gray-500">No variants yet. Add at least two to analyze the test.</p>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {campaign.variants.map((variant) => (
                    <VariantCard key={variant.id} variant={variant} onSaved={() => run(async () => undefined)} onError={setError} />
                  ))}
                </div>
              )}

              <AddVariantForm campaignId={campaign.id} onAdded={() => run(async () => undefined)} onError={setError} />

              <div className="flex items-center gap-3">
                <Button
                  variant="outline"
                  disabled={campaign.variants.length < 2}
                  onClick={() => analyze(campaign)}
                >
                  Analyze results
                </Button>
                {campaign.winner && (
                  <span className="flex items-center gap-2 text-sm">
                    <CheckCircle2 className="h-4 w-4 text-green-600" />
                    Variant {campaign.winner} is the winner
                  </span>
                )}
              </div>
              {analyses[campaign.id] && (
                <p className="text-sm text-gray-700">
                  p-value {analyses[campaign.id].p_value.toFixed(3)} ·{' '}
                  {analyses[campaign.id].is_significant ? 'statistically significant' : 'not significant'} ·{' '}
                  {analyses[campaign.id].improvement_percent.toFixed(1)}% change · {analyses[campaign.id].recommended_action}
                </p>
              )}
            </CardContent>
          </Card>
        ))
      )}
    </div>
  );
}

function VariantCard({
  variant,
  onSaved,
  onError,
}: {
  variant: Variant;
  onSaved: () => void;
  onError: (message: string) => void;
}) {
  const [impressions, setImpressions] = useState(String(variant.impressions));
  const [clicks, setClicks] = useState(String(variant.clicks));
  const [conversions, setConversions] = useState(String(variant.conversions));
  const [saving, setSaving] = useState(false);

  const save = async () => {
    setSaving(true);
    try {
      const query = new URLSearchParams({ impressions, clicks, conversions }).toString();
      await ApiClient.patch(`/ab-testing/variants/${variant.id}/performance?${query}`, {});
      onSaved();
    } catch (err) {
      onError(errorMessage(err, 'The results could not be saved.'));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="border rounded-lg p-4 space-y-2">
      <h4 className="font-medium text-sm">{variant.variant_name} <span className="text-gray-500">({variant.variant_type})</span></h4>
      <p className="text-sm">CTR {variant.ctr.toFixed(2)}% · Conversion {variant.conversion_rate.toFixed(2)}%</p>
      <div className="grid grid-cols-3 gap-2 text-sm">
        <label>
          <span className="block text-xs text-gray-600">Impressions</span>
          <input type="number" min={0} className="w-full border rounded px-2 py-1" value={impressions} onChange={(e) => setImpressions(e.target.value)} />
        </label>
        <label>
          <span className="block text-xs text-gray-600">Clicks</span>
          <input type="number" min={0} className="w-full border rounded px-2 py-1" value={clicks} onChange={(e) => setClicks(e.target.value)} />
        </label>
        <label>
          <span className="block text-xs text-gray-600">Conversions</span>
          <input type="number" min={0} className="w-full border rounded px-2 py-1" value={conversions} onChange={(e) => setConversions(e.target.value)} />
        </label>
      </div>
      <Button size="sm" variant="outline" onClick={save} disabled={saving}>Save results</Button>
    </div>
  );
}

function AddVariantForm({
  campaignId,
  onAdded,
  onError,
}: {
  campaignId: number;
  onAdded: () => void;
  onError: (message: string) => void;
}) {
  const [variantName, setVariantName] = useState('');
  const [variantType, setVariantType] = useState(VARIANT_TYPES[0]);

  const add = async (event: FormEvent) => {
    event.preventDefault();
    try {
      await ApiClient.post(`/ab-testing/campaigns/${campaignId}/variants`, {
        variant_name: variantName.trim(),
        variant_type: variantType,
      });
      setVariantName('');
      onAdded();
    } catch (err) {
      onError(errorMessage(err, 'The variant could not be added.'));
    }
  };

  return (
    <form onSubmit={add} className="flex flex-wrap gap-2 items-end">
      <label className="text-sm">
        <span className="block text-xs text-gray-600">Variant name</span>
        <input className="border rounded px-2 py-1" value={variantName} onChange={(e) => setVariantName(e.target.value)} required />
      </label>
      <label className="text-sm">
        <span className="block text-xs text-gray-600">Role</span>
        <select className="border rounded px-2 py-1" value={variantType} onChange={(e) => setVariantType(e.target.value)}>
          {VARIANT_TYPES.map((item) => (
            <option key={item} value={item}>{item}</option>
          ))}
        </select>
      </label>
      <Button type="submit" size="sm" variant="outline" disabled={!variantName.trim()}>Add variant</Button>
    </form>
  );
}
