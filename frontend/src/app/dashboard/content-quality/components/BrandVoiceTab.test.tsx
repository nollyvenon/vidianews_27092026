import { fireEvent, screen, waitFor } from '@testing-library/react'
import BrandVoiceTab from '@/app/dashboard/content-quality/components/BrandVoiceTab'
import { mockFetch, renderWithQuery, reply } from '@/test-utils'

const guide = { id: 1, name: 'House style', tone: { formal: true }, personality_traits: ['direct'], is_active: true }
const contentItem = { id: 7, title: 'Storm report', status: 'published', content_type: 'article' }
const checkResult = {
  id: 3,
  content_id: 7,
  check_result: 'partial',
  overall_score: 72,
  compliance_score: 80,
  tone_match_score: 70,
  consistency_score: 66,
  recommendations: ['Use the house tone in the opening line'],
}

function baseRoutes(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /brand-voice/guide': [guide],
    'GET /content': { items: [contentItem], total: 1 },
    'GET /content/7': { id: 7, title: 'Storm report', body: 'The storm arrived early.' },
    ...extra,
  })
}

async function chooseContent() {
  fireEvent.change(await screen.findByRole('combobox'), { target: { value: '7' } })
  await screen.findByDisplayValue('The storm arrived early.')
}

describe('BrandVoiceTab', () => {
  it('asks for a brand guide when the organization has none and creates one', async () => {
    const fetchMock = mockFetch({
      'GET /brand-voice/guide': [],
      'POST /brand-voice/guide': { ...guide, id: 2 },
      'GET /content': { items: [], total: 0 },
    })
    renderWithQuery(<BrandVoiceTab />)

    fireEvent.change(await screen.findByRole('textbox', { name: 'Guide name' }), { target: { value: 'Newsroom' } })
    fireEvent.change(screen.getByRole('textbox', { name: 'Tone keywords (comma separated)' }), {
      target: { value: 'formal, warm' },
    })
    fireEvent.change(screen.getByRole('textbox', { name: 'Personality traits (comma separated)' }), {
      target: { value: 'direct' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Create brand guide' }))

    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/brand-voice/guide') && init?.method === 'POST')).toBe(true)
    )
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/brand-voice/guide') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({
      name: 'Newsroom',
      tone: { formal: true, warm: true },
      personality_traits: ['direct'],
      vocabulary_level: 'Moderate',
    })
  })

  it('shows the active guide and loads the chosen content into the editor', async () => {
    baseRoutes()
    renderWithQuery(<BrandVoiceTab />)

    expect(await screen.findByText('House style')).toBeInTheDocument()
    await chooseContent()
    expect(screen.getByRole('button', { name: 'Check Brand Voice' })).toBeEnabled()
  })

  it('keeps the check disabled until content is chosen', async () => {
    baseRoutes()
    renderWithQuery(<BrandVoiceTab />)

    await screen.findByText('House style')
    expect(screen.getByRole('button', { name: 'Check Brand Voice' })).toBeDisabled()
  })

  it('checks the content against the active guide and shows the scores and recommendations', async () => {
    const fetchMock = baseRoutes({ 'POST /brand-voice/check': checkResult })
    renderWithQuery(<BrandVoiceTab />)
    await chooseContent()

    fireEvent.click(screen.getByRole('button', { name: 'Check Brand Voice' }))

    expect(await screen.findByText('Result: Partially compliant')).toBeInTheDocument()
    expect(screen.getByText('80.0%')).toBeInTheDocument()
    expect(screen.getByText('Use the house tone in the opening line')).toBeInTheDocument()
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/brand-voice/check') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({
      content_id: 7,
      text: 'The storm arrived early.',
      guide_id: 1,
    })
  })

  it('shows the server explanation when the check cannot run', async () => {
    baseRoutes({ 'POST /brand-voice/check': reply({ detail: 'AI features are not configured: set ANTHROPIC_API_KEY on the server' }, 503) })
    renderWithQuery(<BrandVoiceTab />)
    await chooseContent()

    fireEvent.click(screen.getByRole('button', { name: 'Check Brand Voice' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('ANTHROPIC_API_KEY')
  })

  it('omits the recommendations list when the result has none', async () => {
    baseRoutes({ 'POST /brand-voice/check': { ...checkResult, check_result: 'compliant', recommendations: [] } })
    renderWithQuery(<BrandVoiceTab />)
    await chooseContent()

    fireEvent.click(screen.getByRole('button', { name: 'Check Brand Voice' }))

    expect(await screen.findByText('Result: Compliant')).toBeInTheDocument()
    expect(screen.queryByText('Recommendations')).not.toBeInTheDocument()
  })

  it('shows progress while the check runs', async () => {
    global.fetch = jest.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input)
      if (init?.method === 'POST') return new Promise(() => undefined) as Promise<Response>
      if (url.includes('/brand-voice/guide')) return { ok: true, status: 200, json: async () => [guide] } as Response
      if (url.includes('/content/7')) return { ok: true, status: 200, json: async () => ({ id: 7, body: 'The storm arrived early.' }) } as Response
      return { ok: true, status: 200, json: async () => ({ items: [contentItem], total: 1 }) } as Response
    }) as unknown as typeof fetch
    renderWithQuery(<BrandVoiceTab />)
    await chooseContent()

    fireEvent.click(screen.getByRole('button', { name: 'Check Brand Voice' }))

    expect(await screen.findByRole('button', { name: 'Analyzing…' })).toBeDisabled()
  })

  it('reports that the content list could not be loaded', async () => {
    mockFetch({
      'GET /brand-voice/guide': [guide],
      'GET /content': reply({ detail: 'Your account has no workspace yet.' }, 500),
    })
    renderWithQuery(<BrandVoiceTab />)

    expect(await screen.findByText('Your account has no workspace yet.')).toBeInTheDocument()
  })
})
