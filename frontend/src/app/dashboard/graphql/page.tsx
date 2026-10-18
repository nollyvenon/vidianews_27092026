'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface SavedQuery {
  id: number
  name: string
  query_string: string
  execution_count: number
  avg_execution_time_ms: number
}

interface RunResult {
  elapsed_ms: number
  response: { data?: unknown; errors?: { message: string }[] }
}

interface SchemaType {
  name: string
  fields: { name: string; type: string }[]
}

const SAMPLE_QUERY = '{ contents(limit: 5) { id title viewsCount } }'

/** A query explorer over the platform's public content, with saved queries and the live schema. */
export default function GraphQLPage() {
  const [queryInput, setQueryInput] = useState('')
  const [saveName, setSaveName] = useState('')
  const [result, setResult] = useState<RunResult | null>(null)
  const [saved, setSaved] = useState<SavedQuery[] | null>(null)
  const [schema, setSchema] = useState<SchemaType[] | null>(null)
  const [showSchema, setShowSchema] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)

  const loadSaved = () =>
    ApiClient.get('/graphql/queries')
      .then((data: SavedQuery[]) => setSaved(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Saved queries could not be loaded.')));

  useEffect(() => {
    loadSaved();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const execute = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setNotice(null);
    try {
      const run: RunResult = await ApiClient.post('/graphql/run', { query: queryInput });
      setResult(run);
    } catch (err) {
      setError(errorMessage(err, 'The query could not be run.'));
    }
  };

  const saveQuery = async () => {
    setError(null);
    setNotice(null);
    try {
      const created: { name: string } = await ApiClient.post('/graphql/query', {
        name: saveName.trim(),
        query_string: queryInput,
      });
      setNotice(`Saved "${created.name}".`);
      setSaveName('');
      await loadSaved();
    } catch (err) {
      setError(errorMessage(err, 'The query could not be saved.'));
    }
  };

  const runSaved = async (item: SavedQuery) => {
    setError(null);
    setNotice(null);
    try {
      const run: RunResult = await ApiClient.post('/graphql/execute', { query_id: item.id });
      setResult(run);
      await loadSaved();
    } catch (err) {
      setError(errorMessage(err, 'The saved query could not be run.'));
    }
  };

  const toggleSchema = async () => {
    if (showSchema) {
      setShowSchema(false);
      return;
    }
    setError(null);
    try {
      const data: { types: SchemaType[] } = await ApiClient.get('/graphql/schema');
      setSchema(data.types);
      setShowSchema(true);
    } catch (err) {
      setError(errorMessage(err, 'The schema could not be loaded.'));
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">GraphQL Explorer</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3 mb-6">{error}</p>}
      {notice && <p role="status" className="text-green-700 mb-6">{notice}</p>}

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Query Editor</h2>
          <form onSubmit={execute}>
            <textarea
              value={queryInput}
              onChange={(e) => setQueryInput(e.target.value)}
              placeholder={SAMPLE_QUERY}
              aria-label="Query"
              className="w-full h-40 p-3 border border-gray-300 rounded font-mono text-sm focus:outline-none"
            />
            <div className="flex flex-wrap gap-2 mt-3 items-center">
              <button type="submit" disabled={!queryInput.trim()} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
                Execute
              </button>
              <input
                className="border rounded px-2 py-2"
                placeholder="Name to save as"
                aria-label="Query name"
                value={saveName}
                onChange={(e) => setSaveName(e.target.value)}
              />
              <button
                type="button"
                onClick={saveQuery}
                disabled={!saveName.trim() || !queryInput.trim()}
                className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 disabled:opacity-50"
              >
                Save Query
              </button>
            </div>
          </form>
          {result && (
            <div className="mt-4">
              <p className="text-sm text-gray-600 mb-2">Ran in {result.elapsed_ms.toFixed(2)} ms</p>
              {result.response.errors && (
                <ul className="text-sm text-red-700 mb-2 list-disc pl-5">
                  {result.response.errors.map((item, index) => (
                    <li key={index}>{item.message}</li>
                  ))}
                </ul>
              )}
              <pre className="bg-gray-50 border rounded p-3 text-xs overflow-x-auto">{JSON.stringify(result.response.data ?? null, null, 2)}</pre>
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Saved Queries</h2>
          {saved === null && !error ? (
            <p className="text-gray-500">Loading saved queries…</p>
          ) : saved && saved.length === 0 ? (
            <p className="text-gray-500">No saved queries yet.</p>
          ) : saved ? (
            <div className="space-y-3">
              {saved.map((item) => (
                <div key={item.id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <p className="font-semibold">{item.name}</p>
                    <span className="text-sm text-gray-600">{item.execution_count.toLocaleString()} executions</span>
                  </div>
                  <p className="text-sm text-gray-600">Avg Response: {item.avg_execution_time_ms.toFixed(1)}ms</p>
                  <button type="button" onClick={() => runSaved(item)} className="mt-2 text-sm text-blue-600 hover:underline">
                    Run {item.name}
                  </button>
                </div>
              ))}
            </div>
          ) : null}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Schema Documentation</h2>
          <button type="button" onClick={toggleSchema} className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50">
            {showSchema ? 'Hide Schema' : 'View Full Schema'}
          </button>
          {showSchema && schema && (
            <div className="mt-4 space-y-4">
              {schema.map((type) => (
                <div key={type.name}>
                  <p className="font-semibold">type {type.name}</p>
                  <ul className="font-mono text-sm pl-4">
                    {type.fields.map((field) => (
                      <li key={field.name}>{field.name}: {field.type}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
