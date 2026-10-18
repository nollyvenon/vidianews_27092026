import { fireEvent, screen, waitFor } from '@testing-library/react'
import ProofreadingTab from '@/app/dashboard/content-quality/components/ProofreadingTab'
import { mockFetch, renderWithQuery, reply } from '@/test-utils'

const check = {
  id: 5,
  content_id: 7,
  quality_score: 87.5,
  overall_rating: 'Good',
  total_issues: 2,
  grammar_issues: 0,
  spelling_issues: 1,
  punctuation_issues: 0,
  style_issues: 1,
}
const issues = [
  { id: 1, type: 'spelling', severity: 'error', text: 'recieve', suggestion: 'receive', position: 13, length: 7 },
  { id: 2, type: 'style', severity: 'info', text: 'very good', suggestion: 'excellent', position: 30, length: 9 },
]
const body = 'The storm arrived early. Their team recieve the very good news.'

function routes(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /content': { items: [{ id: 7, title: 'Storm report', status: 'published', content_type: 'article' }], total: 1 },
    'GET /content/7': { id: 7, title: 'Storm report', body },
    'POST /proofread': check,
    'GET /proofread/5': { ...check, issues },
    ...extra,
  })
}

async function runCheck() {
  fireEvent.change(await screen.findByRole('combobox'), { target: { value: '7' } })
  await screen.findByDisplayValue(body)
  fireEvent.click(screen.getByRole('button', { name: 'Check Proofreading' }))
}

describe('ProofreadingTab', () => {
  it('starts with all three check options selected and needs content to run', async () => {
    routes()
    renderWithQuery(<ProofreadingTab />)

    expect(await screen.findByRole('combobox')).toBeInTheDocument()
    expect(screen.getByRole('checkbox', { name: 'grammar' })).toBeChecked()
    expect(screen.getByRole('checkbox', { name: 'spelling' })).toBeChecked()
    expect(screen.getByRole('checkbox', { name: 'style' })).toBeChecked()
    expect(screen.getByRole('button', { name: 'Check Proofreading' })).toBeDisabled()
  })

  it('creates the check with the selected options and then loads its issues', async () => {
    const fetchMock = routes()
    renderWithQuery(<ProofreadingTab />)
    await screen.findByRole('combobox')
    fireEvent.click(screen.getByRole('checkbox', { name: 'grammar' }))
    await runCheck()

    expect(await screen.findByText('87.5')).toBeInTheDocument()
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/proofread') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({
      content_id: 7,
      text: body,
      check_grammar: false,
      check_spelling: true,
      check_style: true,
    })
  })

  it('shows the rating, the issue breakdown and every issue the service found', async () => {
    routes()
    renderWithQuery(<ProofreadingTab />)
    await runCheck()

    expect(await screen.findByText('Good')).toHaveClass('text-blue-600')
    expect(screen.getByText('2 issues found')).toBeInTheDocument()
    expect(screen.getByText('recieve')).toBeInTheDocument()
    expect(screen.getByText('very good')).toBeInTheDocument()
    // Check-option labels share these words, so match the issue badges by their colour class.
    expect(screen.getAllByText('spelling').some((node) => node.classList.contains('bg-red-100'))).toBe(true)
    expect(screen.getAllByText('style').some((node) => node.classList.contains('bg-blue-100'))).toBe(true)
  })

  it('applies a suggestion to the editor text', async () => {
    routes()
    renderWithQuery(<ProofreadingTab />)
    await runCheck()

    fireEvent.click((await screen.findAllByRole('button', { name: 'Apply' }))[0])

    expect(screen.getByDisplayValue(/Their team receive the very good news/)).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent('Applied "receive".')
  })

  it('reports when a flagged passage is no longer in the text', async () => {
    routes()
    renderWithQuery(<ProofreadingTab />)
    await runCheck()
    fireEvent.click((await screen.findAllByRole('button', { name: 'Apply' }))[0])
    fireEvent.click(screen.getAllByRole('button', { name: 'Apply' })[0])

    expect(screen.getByRole('status')).toHaveTextContent('"recieve" is no longer in the text.')
  })

  it('shows a clean result when there are no issues', async () => {
    routes({
      'POST /proofread': { ...check, quality_score: 99, overall_rating: 'Excellent', total_issues: 0, spelling_issues: 0, style_issues: 0 },
      'GET /proofread/5': { ...check, quality_score: 99, overall_rating: 'Excellent', total_issues: 0, spelling_issues: 0, style_issues: 0, issues: [] },
    })
    renderWithQuery(<ProofreadingTab />)
    await runCheck()

    expect(await screen.findByText('Great! No issues found.')).toBeInTheDocument()
    expect(screen.getByText('No issues found')).toBeInTheDocument()
    expect(screen.getByText('Excellent')).toHaveClass('text-green-600')
  })

  it.each([
    ['Fair', 'text-yellow-600'],
    ['Poor', 'text-red-600'],
  ])('colours a %s rating', async (rating, colour) => {
    routes({ 'GET /proofread/5': { ...check, overall_rating: rating, issues: [] } })
    renderWithQuery(<ProofreadingTab />)
    await runCheck()

    expect(await screen.findByText(rating)).toHaveClass(colour)
  })

  it('styles warning issues and falls back to a neutral style for unknown types', async () => {
    routes({
      'GET /proofread/5': {
        ...check,
        issues: [
          { id: 3, type: 'grammar', severity: 'warning', text: 'their', suggestion: 'there', position: 0, length: 5 },
          { id: 4, type: 'punctuation', severity: 'hint', text: 'news', suggestion: 'news.', position: 0, length: 4 },
        ],
      },
    })
    renderWithQuery(<ProofreadingTab />)
    await runCheck()

    expect(await screen.findByText('2 issues found')).toBeInTheDocument()
    expect(screen.getAllByText('grammar').some((node) => node.classList.contains('bg-yellow-100'))).toBe(true)
    expect(screen.getAllByText('punctuation').some((node) => node.classList.contains('bg-gray-100'))).toBe(true)
  })

  it('shows the server message when the check cannot run', async () => {
    routes({ 'POST /proofread': reply({ detail: 'AI features are not configured: set ANTHROPIC_API_KEY on the server' }, 503) })
    renderWithQuery(<ProofreadingTab />)
    await runCheck()

    expect(await screen.findByRole('alert')).toHaveTextContent('ANTHROPIC_API_KEY')
  })

  it('shows progress while the check runs', async () => {
    routes()
    global.fetch = jest.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input)
      if (init?.method === 'POST') return new Promise(() => undefined) as Promise<Response>
      return { ok: true, status: 200, json: async () => (url.includes('/content/7') ? { id: 7, body } : { items: [{ id: 7, title: 'Storm report', status: 'published', content_type: 'article' }], total: 1 }) } as Response
    }) as unknown as typeof fetch
    renderWithQuery(<ProofreadingTab />)
    await waitFor(() => expect(screen.getByRole('combobox')).toBeInTheDocument())
    await runCheck()

    expect(await screen.findByRole('button', { name: 'Checking...' })).toBeDisabled()
  })

  it('saves the edited text to the chosen content item', async () => {
    const fetchMock = routes({ 'PUT /content/7': { id: 7, body: 'Corrected text' } })
    renderWithQuery(<ProofreadingTab />)
    fireEvent.change(await screen.findByRole('combobox'), { target: { value: '7' } })
    await screen.findByDisplayValue(body)

    const save = screen.getByRole('button', { name: 'Save text to content' })
    expect(save).toBeDisabled()
    fireEvent.change(screen.getByDisplayValue(body), { target: { value: 'Corrected text' } })
    fireEvent.click(save)

    expect(await screen.findByRole('status')).toHaveTextContent('Saved to the content item.')
    const put = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/content/7') && init?.method === 'PUT')
    expect(JSON.parse(put![1].body as string)).toEqual({ body: 'Corrected text' })
    expect(screen.getByRole('button', { name: 'Save text to content' })).toBeDisabled()
  })

  it('shows the server reason when the text cannot be saved to the content item', async () => {
    routes({ 'PUT /content/7': reply({ detail: 'Content is archived' }, 409) })
    renderWithQuery(<ProofreadingTab />)
    fireEvent.change(await screen.findByRole('combobox'), { target: { value: '7' } })
    await screen.findByDisplayValue(body)
    fireEvent.change(screen.getByDisplayValue(body), { target: { value: 'Edited' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save text to content' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Content is archived')
  })
})
