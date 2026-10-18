import React, { FormEvent, useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';

interface Engine {
  id: number;
  name: string;
  recommendation_type: string;
  is_active: boolean;
}

interface Recommendation {
  id: number;
  recommended_content_ids: number[];
  recommendation_scores: number[];
}

interface PoolItem {
  id: number;
  title: string;
}

const RECOMMENDATION_TYPES = ['collaborative', 'content_based', 'hybrid', 'trending', 'personalized'];
const PREFERENCE_CATEGORIES = ['topic', 'author', 'content_type', 'publication_frequency', 'engagement_level'];

/** Recommendation engines, personalised preferences and recommendations for the signed-in user. */
export default function RecommendationsTab() {
  const [engines, setEngines] = useState<Engine[]>([]);
  const [pool, setPool] = useState<PoolItem[]>([]);
  const [selectedPool, setSelectedPool] = useState<number[]>([]);
  const [engineId, setEngineId] = useState<number | null>(null);
  const [result, setResult] = useState<Recommendation | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [engineName, setEngineName] = useState('');
  const [engineType, setEngineType] = useState(RECOMMENDATION_TYPES[0]);
  const [category, setCategory] = useState(PREFERENCE_CATEGORIES[0]);
  const [value, setValue] = useState('');
  const [weight, setWeight] = useState('1');
  const [loading, setLoading] = useState(true);

  const loadEngines = () =>
    ApiClient.get('/content-recommendations/engines')
      .then((data: Engine[]) => {
        const list = Array.isArray(data) ? data : [];
        setEngines(list);
        setEngineId((current) => current ?? list.find((engine) => engine.is_active)?.id ?? null);
      })
      .catch((err) => setError(errorMessage(err, 'Recommendation engines could not be loaded.')))
      .finally(() => setLoading(false));

  useEffect(() => {
    loadEngines();
    ApiClient.get('/content?page=1&page_size=100')
      .then((data: { items?: PoolItem[] }) => setPool(Array.isArray(data?.items) ? data.items : []))
      .catch((err) => setError(errorMessage(err, 'Your content could not be loaded.')));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const run = async (action: () => Promise<void>, success: string) => {
    setError(null);
    setNotice(null);
    try {
      await action();
      setNotice(success);
    } catch (err) {
      setError(errorMessage(err, 'That action could not be completed.'));
    }
  };

  const createEngine = (event: FormEvent) => {
    event.preventDefault();
    return run(async () => {
      await ApiClient.post('/content-recommendations/engines', { name: engineName.trim(), recommendation_type: engineType });
      setEngineName('');
      await loadEngines();
    }, 'Engine created');
  };

  const recordPreference = (event: FormEvent) => {
    event.preventDefault();
    return run(async () => {
      await ApiClient.post('/content-recommendations/preferences', {
        category,
        value: value.trim(),
        weight: Number(weight) || 1,
      });
      setValue('');
    }, 'Preference saved');
  };

  const generate = (event: FormEvent) => {
    event.preventDefault();
    if (engineId === null) return;
    return run(async () => {
      const recommendation: Recommendation = await ApiClient.post(
        `/content-recommendations/generate?engine_id=${engineId}`,
        { content_pool: selectedPool, num_recommendations: Math.min(5, selectedPool.length) },
      );
      setResult(recommendation);
    }, 'Recommendations generated');
  };

  const toggleItem = (id: number) =>
    setSelectedPool((current) => (current.includes(id) ? current.filter((item) => item !== id) : [...current, id]));

  const titleOf = (id: number) => pool.find((item) => item.id === id)?.title ?? `Content #${id}`;

  return (
    <div className="space-y-6">
      {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
      {notice && <p role="status" className="text-sm text-green-700">{notice}</p>}

      <Card>
        <CardHeader>
          <CardTitle>Recommendation Engines</CardTitle>
          <CardDescription>Engines decide how content is recommended to your audience</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {loading ? (
            <p className="text-sm text-gray-500">Loading engines…</p>
          ) : engines.length === 0 ? (
            <p className="text-sm text-gray-500">No engines yet. Create one below.</p>
          ) : (
            <ul className="space-y-2 text-sm">
              {engines.map((engine) => (
                <li key={engine.id} className="border rounded p-3">
                  <span className="font-medium">{engine.name}</span> · {engine.recommendation_type}
                  {!engine.is_active && <span className="ml-2 text-gray-500">(inactive)</span>}
                </li>
              ))}
            </ul>
          )}
          <form onSubmit={createEngine} className="flex flex-wrap gap-2 items-end">
            <input
              className="border rounded px-3 py-2"
              placeholder="Engine name"
              value={engineName}
              onChange={(e) => setEngineName(e.target.value)}
              required
            />
            <select aria-label="Engine type" className="border rounded px-3 py-2" value={engineType} onChange={(e) => setEngineType(e.target.value)}>
              {RECOMMENDATION_TYPES.map((item) => (
                <option key={item} value={item}>{item}</option>
              ))}
            </select>
            <Button type="submit" variant="outline" disabled={!engineName.trim()}>Create engine</Button>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Your Preferences</CardTitle>
          <CardDescription>Tell the engine what you care about</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={recordPreference} className="flex flex-wrap gap-2 items-end">
            <select aria-label="Preference category" className="border rounded px-3 py-2" value={category} onChange={(e) => setCategory(e.target.value)}>
              {PREFERENCE_CATEGORIES.map((item) => (
                <option key={item} value={item}>{item}</option>
              ))}
            </select>
            <input className="border rounded px-3 py-2" placeholder="Value" value={value} onChange={(e) => setValue(e.target.value)} required />
            <input
              type="number"
              min={0}
              max={2}
              step={0.1}
              className="border rounded px-3 py-2 w-24"
              aria-label="Weight"
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
            />
            <Button type="submit" variant="outline" disabled={!value.trim()}>Save preference</Button>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Generate Recommendations</CardTitle>
          <CardDescription>Pick the content the engine may recommend, then generate</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <form onSubmit={generate} className="space-y-3">
            <label className="block text-sm">
              <span className="block mb-1">Engine</span>
              <select
                className="w-full border rounded px-3 py-2"
                value={engineId ?? ''}
                onChange={(e) => setEngineId(e.target.value ? Number(e.target.value) : null)}
              >
                <option value="">Select an engine…</option>
                {engines.map((engine) => (
                  <option key={engine.id} value={engine.id}>{engine.name}</option>
                ))}
              </select>
            </label>
            <fieldset className="space-y-1">
              <legend className="text-sm mb-1">Content pool</legend>
              {pool.length === 0 ? (
                <p className="text-sm text-gray-500">You have no content to recommend yet.</p>
              ) : (
                pool.map((item) => (
                  <label key={item.id} className="flex items-center gap-2 text-sm">
                    <input type="checkbox" checked={selectedPool.includes(item.id)} onChange={() => toggleItem(item.id)} />
                    {item.title}
                  </label>
                ))
              )}
            </fieldset>
            <Button type="submit" disabled={engineId === null || selectedPool.length === 0}>Generate</Button>
          </form>

          {result && (
            <ol className="space-y-2 text-sm">
              {result.recommended_content_ids.map((id, index) => (
                <li key={id} className="border rounded p-3 flex justify-between">
                  <span>{titleOf(id)}</span>
                  <span className="text-gray-600">score {(result.recommendation_scores[index] ?? 0).toFixed(2)}</span>
                </li>
              ))}
            </ol>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
