import { fireEvent, screen, waitFor } from '@testing-library/react'
import PlagiarismTab from '@/app/dashboard/content-quality/components/PlagiarismTab'
import { mockFetch, renderWithQuery, reply } from '@/test-utils'

function routes(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /content': { items: [{ id: 7, title: 'Storm report', status: 'published', content_type: 'article' }], total: 1 },
    'GET /content/7': { id: 7, title: 'Storm report', body: 'Some submitted article text' },
    ...extra,
  })
}

async function runCheck() {
  fireEvent.change(await screen.findByRole('combobox'), { target: { value: '7' } })
  await screen.findByDisplayValue('Some submitted article text')
  fireEvent.click(screen.getByRole('button', { name: 'Check Plagiarism' }))
}

describe('PlagiarismTab', () => {
  it('explains that matching needs a similarity provider and keeps the check disabled until content is chosen', async () => {
    routes()
    renderWithQuery(<PlagiarismTab />)

    expect(screen.getByText(/Plagiarism matching needs a similarity-search provider/)).toBeInTheDocument()
    expect(await screen.findByRole('combobox')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Check Plagiarism' })).toBeDisabled()
  })

  it('reports the server refusal instead of showing a result', async () => {
    const fetchMock = routes({
      'POST /plagiarism/check': reply(
        { detail: 'Plagiarism detection is not available: no similarity-search provider is configured on this server' },
        503
      ),
    })
    renderWithQuery(<PlagiarismTab />)
    await runCheck()

    expect(await screen.findByRole('alert')).toHaveTextContent('no similarity-search provider is configured')
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/plagiarism/check') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({ content_id: 7, text: 'Some submitted article text' })
    expect(screen.queryByText('Matched Sources')).not.toBeInTheDocument()
  })

  it('shows progress while the check runs', async () => {
    routes()
    global.fetch = jest.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === 'POST') return new Promise(() => undefined) as Promise<Response>
      const url = String(input)
      return { ok: true, status: 200, json: async () => (url.includes('/content/7') ? { id: 7, body: 'Some submitted article text' } : { items: [{ id: 7, title: 'Storm report', status: 'published', content_type: 'article' }], total: 1 }) } as Response
    }) as unknown as typeof fetch
    renderWithQuery(<PlagiarismTab />)
    await waitFor(() => expect(screen.getByRole('combobox')).toBeInTheDocument())
    await runCheck()

    expect(await screen.findByRole('button', { name: 'Checking…' })).toBeDisabled()
  })
})
