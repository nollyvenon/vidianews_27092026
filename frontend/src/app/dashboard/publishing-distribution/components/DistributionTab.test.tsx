import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import DistributionTab from '@/app/dashboard/publishing-distribution/components/DistributionTab'
import { mockFetch, reply } from '@/test-utils'

const channels = [
  { id: 1, type: 'email', display_name: 'Newsletter', success_rate: 89.5, priority: 1 },
  { id: 2, type: 'rss', display_name: 'RSS feed', success_rate: 12.1, priority: 3 },
]
const partners = [
  { id: 1, partner_name: 'News Agency Pro', partner_type: 'news_agency', articles_syndicated: 3, reach: 1200 },
]

function base(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /distribution/channels': channels,
    'GET /distribution/syndication-profiles': partners,
    ...extra,
  })
}

describe('DistributionTab', () => {
  it('shows a loading message until the channels arrive', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    render(<DistributionTab />)

    expect(screen.getByText('Loading channels…')).toBeInTheDocument()
  })

  it('lists the active channels with their type, priority and success rate', async () => {
    base()
    render(<DistributionTab />)

    expect(await screen.findByText('Newsletter')).toBeInTheDocument()
    expect(screen.getByText('Type: email · Priority 1')).toBeInTheDocument()
    expect(screen.getByText('89.5% success')).toBeInTheDocument()
    expect(screen.getByText('RSS feed')).toBeInTheDocument()
  })

  it('says when no channels are configured', async () => {
    base({ 'GET /distribution/channels': [] })
    render(<DistributionTab />)

    expect(await screen.findByText('No active distribution channels yet.')).toBeInTheDocument()
  })

  it('shows the server reason when channels cannot be loaded', async () => {
    base({ 'GET /distribution/channels': reply({ detail: 'Your account has no organization yet.' }, 422) })
    render(<DistributionTab />)

    expect(await screen.findByText('Your account has no organization yet.')).toBeInTheDocument()
  })

  it('lists the syndication partners with their articles and reach', async () => {
    base()
    render(<DistributionTab />)

    expect(await screen.findByText('News Agency Pro')).toBeInTheDocument()
    expect(screen.getByText('3 articles syndicated · news_agency')).toBeInTheDocument()
    expect(screen.getByText('1,200 reach')).toBeInTheDocument()
  })

  it('says when there are no syndication partners yet', async () => {
    base({ 'GET /distribution/syndication-profiles': [] })
    render(<DistributionTab />)

    expect(await screen.findByText('No syndication partners yet.')).toBeInTheDocument()
  })

  it('adds a syndication partner with its type and optional endpoint', async () => {
    const fetchMock = base({ 'POST /distribution/syndication-profiles': { id: 2, partner_name: 'Blog Net', partner_type: 'blog_network' } })
    render(<DistributionTab />)
    await screen.findByText('News Agency Pro')

    fireEvent.change(screen.getByPlaceholderText('Partner name'), { target: { value: ' Blog Net ' } })
    fireEvent.change(screen.getByLabelText('Partner type'), { target: { value: 'blog_network' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add partner' }))

    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/distribution/syndication-profiles') && init?.method === 'POST')).toBe(true),
    )
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/distribution/syndication-profiles') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({ partner_name: 'Blog Net', partner_type: 'blog_network', api_endpoint: null })
  })

  it('shows the server reason when a partner cannot be added', async () => {
    base({ 'POST /distribution/syndication-profiles': reply({ detail: 'Partner already exists' }, 400) })
    render(<DistributionTab />)
    await screen.findByText('News Agency Pro')

    fireEvent.change(screen.getByPlaceholderText('Partner name'), { target: { value: 'News Agency Pro' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add partner' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Partner already exists')
  })
})
