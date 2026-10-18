'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface Doc {
  id: number
  title: string
  slug: string
  doc_type: string
  views: number
  version: string
}

interface ApiDoc {
  id: number
  endpoint: string
  method: string
}

const DOC_TYPES = ['guide', 'reference', 'tutorial', 'api'] as const

/** Published documentation with view counts, a form to publish new documents, and the API reference. */
export default function DocsPage() {
  const [docs, setDocs] = useState<Doc[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  const [apiDocs, setApiDocs] = useState<ApiDoc[] | null>(null)
  const [apiError, setApiError] = useState<string | null>(null)
  const [showApiDocs, setShowApiDocs] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [title, setTitle] = useState('')
  const [slug, setSlug] = useState('')
  const [docType, setDocType] = useState<(typeof DOC_TYPES)[number]>('guide')
  const [content, setContent] = useState('')

  const loadDocs = () =>
    ApiClient.get('/docs')
      .then((data: Doc[]) => setDocs(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Documentation could not be loaded.')));

  useEffect(() => {
    loadDocs();
    ApiClient.get('/docs/api/all')
      .then((data: ApiDoc[]) => setApiDocs(Array.isArray(data) ? data : []))
      .catch((err) => setApiError(errorMessage(err, 'API documentation could not be loaded.')));
  }, []);

  const publish = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setNotice(null);
    try {
      const created: { id: number; title: string } = await ApiClient.post('/docs', {
        title: title.trim(),
        slug: slug.trim(),
        content: content.trim(),
        doc_type: docType,
      });
      await ApiClient.put(`/docs/${created.id}/publish`, {});
      setNotice(`Published "${created.title}".`);
      setTitle('');
      setSlug('');
      setContent('');
      setShowForm(false);
      await loadDocs();
    } catch (err) {
      setError(errorMessage(err, 'The document could not be published.'));
    }
  };

  const totalViews = (docs ?? []).reduce((sum, doc) => sum + doc.views, 0);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Documentation</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3 mb-6">{error}</p>}
      {notice && <p role="status" className="text-green-700 mb-6">{notice}</p>}

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Published Docs</h2>
            <button
              type="button"
              onClick={() => setShowForm((open) => !open)}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
            >
              {showForm ? 'Cancel' : '+ New Doc'}
            </button>
          </div>

          {showForm && (
            <form onSubmit={publish} className="border rounded-lg p-4 mb-4 space-y-3">
              <input className="border rounded px-3 py-2 w-full" placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
              <input
                className="border rounded px-3 py-2 w-full"
                placeholder="URL slug, e.g. getting-started"
                pattern="[a-z0-9]+(-[a-z0-9]+)*"
                value={slug}
                onChange={(e) => setSlug(e.target.value)}
                required
              />
              <label className="block text-sm">
                <span className="block text-xs text-gray-600">Type</span>
                <select className="border rounded px-2 py-2" value={docType} onChange={(e) => setDocType(e.target.value as (typeof DOC_TYPES)[number])}>
                  {DOC_TYPES.map((item) => (
                    <option key={item} value={item}>{item}</option>
                  ))}
                </select>
              </label>
              <textarea className="border rounded px-3 py-2 w-full h-32" placeholder="Content" value={content} onChange={(e) => setContent(e.target.value)} required />
              <button type="submit" disabled={!title.trim() || !slug.trim() || !content.trim()} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 text-sm">
                Publish document
              </button>
            </form>
          )}

          {docs === null && !error ? (
            <p className="text-gray-500">Loading documents…</p>
          ) : docs && docs.length === 0 ? (
            <p className="text-gray-500">No published documents yet.</p>
          ) : docs ? (
            <div className="space-y-3">
              {docs.map((doc) => (
                <div key={doc.id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-semibold">{doc.title}</p>
                      <p className="text-sm text-gray-600 mt-1">Type: {doc.doc_type}</p>
                    </div>
                    <div className="text-right">
                      <span className="inline-block px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium mb-2">
                        Published
                      </span>
                      <p className="text-sm text-gray-600">{doc.views.toLocaleString()} views</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : null}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">API Documentation</h2>
          <button
            type="button"
            onClick={() => setShowApiDocs((open) => !open)}
            className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 text-sm"
          >
            {showApiDocs ? 'Hide API docs' : 'View All API Docs'}
          </button>
          {apiError && <p role="alert" className="text-red-700 mt-3">{apiError}</p>}
          {showApiDocs && (
            <div className="mt-4 space-y-2">
              {apiDocs === null && !apiError ? (
                <p className="text-gray-500">Loading endpoints…</p>
              ) : apiDocs && apiDocs.length === 0 ? (
                <p className="text-gray-500">No API endpoints are documented yet.</p>
              ) : apiDocs ? (
                apiDocs.map((item) => (
                  <p key={item.id} className="font-mono text-sm">
                    <span className="font-semibold">{item.method}</span> {item.endpoint}
                  </p>
                ))
              ) : null}
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Documentation Stats</h2>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold">{docs ? docs.length.toLocaleString() : '—'}</p>
              <p className="text-xs text-gray-600">Total Docs</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-blue-600">{docs ? totalViews.toLocaleString() : '—'}</p>
              <p className="text-xs text-gray-600">Total Views</p>
            </div>
            <div>
              <p className="text-2xl font-bold">{apiDocs ? apiDocs.length.toLocaleString() : '—'}</p>
              <p className="text-xs text-gray-600">API Endpoints</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
