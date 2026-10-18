'use client'

import { FormEvent, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

interface ResearchAnswer {
  id: number
  query: string
  summary: string | null
  created_at: string
}

interface LibraryDocument {
  id: number
  title: string
  document_type: string
  is_indexed: boolean
  created_at: string
}

export default function ResearchPage() {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [documentType, setDocumentType] = useState('text')
  const [documents, setDocuments] = useState<LibraryDocument[]>([])
  const [matches, setMatches] = useState<LibraryDocument[] | null>(null)
  const [search, setSearch] = useState('')
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState<ResearchAnswer | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  const run = async (action: () => Promise<void>) => {
    setError(null)
    setBusy(true)
    try {
      await action()
    } catch (err) {
      setError(errorMessage(err, 'That request could not be completed.'))
    } finally {
      setBusy(false)
    }
  }

  const addDocument = (event: FormEvent) => {
    event.preventDefault()
    return run(async () => {
      const created: LibraryDocument = await ApiClient.post('/ai/documents', {
        title: title.trim(),
        content,
        document_type: documentType,
      })
      setDocuments((prev) => [created, ...prev])
      setTitle('')
      setContent('')
    })
  }

  const searchDocuments = (event: FormEvent) => {
    event.preventDefault()
    return run(async () => {
      setMatches((await ApiClient.get(`/ai/documents/search?query=${encodeURIComponent(search)}`)) as LibraryDocument[])
    })
  }

  const ask = (event: FormEvent) => {
    event.preventDefault()
    return run(async () => {
      setAnswer(await ApiClient.post('/ai/research', { query: question }))
    })
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Document Research</h1>
      <p className="text-gray-600">Add documents to your library, then ask questions. Answers come only from your documents.</p>

      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

      <Card>
        <CardHeader>
          <CardTitle>Ask a question</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={ask} className="space-y-3">
            <Input placeholder="What do your documents say about…" value={question} onChange={(e) => setQuestion(e.target.value)} required />
            <Button type="submit" disabled={busy || !question.trim()}>Ask</Button>
          </form>
          {answer && (
            <div className="mt-4 border-l-4 border-blue-500 pl-4">
              <p className="text-sm text-gray-500">Question: {answer.query}</p>
              <p className="whitespace-pre-wrap">{answer.summary}</p>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Add a document</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={addDocument} className="space-y-3">
            <Input placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
            <select className="border rounded-md px-3 py-2" value={documentType} onChange={(e) => setDocumentType(e.target.value)}>
              <option value="text">Text</option>
              <option value="pdf">PDF</option>
              <option value="webpage">Web page</option>
              <option value="code">Code</option>
              <option value="markdown">Markdown</option>
            </select>
            <Textarea placeholder="Document text" rows={6} value={content} onChange={(e) => setContent(e.target.value)} required />
            <Button type="submit" disabled={busy || !title.trim() || !content.trim()}>Add document</Button>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Search your library</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <form onSubmit={searchDocuments} className="flex gap-2">
            <Input placeholder="Search documents" value={search} onChange={(e) => setSearch(e.target.value)} />
            <Button type="submit" disabled={busy || !search.trim()}>Search</Button>
          </form>
          {matches !== null && matches.length === 0 && <p className="text-gray-500">No documents match.</p>}
          <ul className="space-y-2">
            {(matches ?? documents).map((doc) => (
              <li key={doc.id} className="border rounded-md p-3">
                <span className="font-medium">{doc.title}</span>
                <span className="ml-2 text-xs text-gray-500">{doc.document_type}</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}
