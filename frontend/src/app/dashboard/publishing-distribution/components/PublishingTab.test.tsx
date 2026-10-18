import { fireEvent, screen, waitFor } from '@testing-library/react'
import PublishingTab from '@/app/dashboard/publishing-distribution/components/PublishingTab'
import { mockFetch, renderWithQuery, reply } from '@/test-utils'

function routes(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /content': { items: [{ id: 7, title: 'Storm report', status: 'published', content_type: 'article' }], total: 1 },
    'GET /content/7': { id: 7, title: 'Storm report', body: 'Body' },
    'GET /publishing/jobs/pending': [],
    ...extra,
  })
}

async function chooseContent() {
  fireEvent.change(await screen.findByRole('combobox'), { target: { value: '7' } })
  await screen.findByDisplayValue('Storm report')
}

function fillPublishTime(container: HTMLElement, value: string) {
  fireEvent.change(container.querySelector('input[type="datetime-local"]') as HTMLInputElement, { target: { value } })
}

describe('PublishingTab', () => {
  it('takes the title from the chosen content and needs a time before scheduling', async () => {
    routes()
    const { container } = renderWithQuery(<PublishingTab />)
    await chooseContent()
    const button = screen.getByRole('button', { name: 'Schedule Publication' })

    expect(button).toBeDisabled()
    fillPublishTime(container, '2026-11-01T09:00')
    expect(button).toBeEnabled()
  })

  it('toggles distribution channels on and off', async () => {
    const fetchMock = routes({
      'POST /publishing/jobs': { id: 1, title: 'Storm report', status: 'scheduled', scheduled_publish_time: new Date(2026, 10, 1, 9).toISOString(), distribution_channels: ['email'] },
    })
    const { container } = renderWithQuery(<PublishingTab />)
    await chooseContent()

    fireEvent.click(screen.getByText('Email'))
    fireEvent.click(screen.getByText('Website'))
    fillPublishTime(container, '2026-11-01T09:00')
    fireEvent.click(screen.getByRole('button', { name: 'Schedule Publication' }))

    await waitFor(() => expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/publishing/jobs') && init?.method === 'POST')).toBe(true))
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/publishing/jobs') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string).distribution_channels).toEqual(['email'])
  })

  it('schedules the chosen content at the local time as an absolute instant', async () => {
    const publishAt = new Date(2026, 10, 1, 9, 0).toISOString()
    const fetchMock = routes({
      'POST /publishing/jobs': { id: 7, title: 'Storm report', status: 'scheduled', scheduled_publish_time: publishAt, distribution_channels: ['website'] },
    })
    const { container } = renderWithQuery(<PublishingTab />)
    await chooseContent()
    fillPublishTime(container, '2026-11-01T09:00')

    fireEvent.click(screen.getByRole('button', { name: 'Schedule Publication' }))

    await waitFor(() => expect(fetchMock.mock.calls.some(([, init]) => init?.method === 'POST')).toBe(true))
    const post = fetchMock.mock.calls.find(([, init]) => init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({
      content_id: 7,
      title: 'Storm report',
      scheduled_publish_time: publishAt,
      distribution_channels: ['website'],
      auto_promote: true,
    })
    expect(String(post![0])).toMatch(/\/api\/v1\/publishing\/jobs$/)
  })

  it('lists the pending publications with their title, time and channels', async () => {
    routes({
      'GET /publishing/jobs/pending': [
        { id: 3, title: 'Morning brief', status: 'scheduled', scheduled_publish_time: new Date(2026, 10, 2, 8, 30).toISOString(), distribution_channels: ['rss'] },
      ],
    })
    renderWithQuery(<PublishingTab />)

    expect(await screen.findByRole('heading', { name: 'Morning brief' })).toBeInTheDocument()
    expect(screen.getByText('Nov 2, 08:30')).toBeInTheDocument()
    expect(screen.getByText('rss')).toBeInTheDocument()
    expect(screen.getByText('1 publications scheduled')).toBeInTheDocument()
  })

  it('shows progress while the publication is being scheduled', async () => {
    routes()
    global.fetch = jest.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === 'POST') return new Promise(() => undefined) as Promise<Response>
      const url = String(input)
      if (url.includes('/content/7')) return { ok: true, status: 200, json: async () => ({ id: 7, title: 'Storm report', body: '' }) } as Response
      return { ok: true, status: 200, json: async () => (url.includes('pending') ? [] : { items: [{ id: 7, title: 'Storm report', status: 'published', content_type: 'article' }], total: 1 }) } as Response
    }) as unknown as typeof fetch
    const { container } = renderWithQuery(<PublishingTab />)
    await chooseContent()
    fillPublishTime(container, '2026-11-01T09:00')

    fireEvent.click(screen.getByRole('button', { name: 'Schedule Publication' }))

    expect(await screen.findByRole('button', { name: /Scheduling/ })).toBeDisabled()
  })

  it('shows the server message and keeps the form when scheduling is refused', async () => {
    routes({ 'POST /publishing/jobs': reply({ detail: 'Your account has no organization yet.' }, 422) })
    const { container } = renderWithQuery(<PublishingTab />)
    await chooseContent()
    fillPublishTime(container, '2026-11-01T09:00')

    fireEvent.click(screen.getByRole('button', { name: 'Schedule Publication' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no organization yet.')
    expect(screen.getByDisplayValue('Storm report')).toBeInTheDocument()
  })

  it('shows the empty state when nothing is scheduled', async () => {
    routes()
    renderWithQuery(<PublishingTab />)

    expect(await screen.findByText('No scheduled publications')).toBeInTheDocument()
  })
})
