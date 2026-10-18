import { render, screen } from '@testing-library/react'
import VideoProcessingPage from '@/app/dashboard/video-processing/page'
import { mockFetch, reply } from '@/test-utils'

const videos = [
  {
    video_id: 1,
    content_id: 10,
    title: 'Tutorial',
    status: 'completed',
    progress: 100,
    qualities: [{ quality: '720p', status: 'completed' }],
  },
  {
    video_id: 2,
    content_id: 11,
    title: 'Guide',
    status: 'in_progress',
    progress: 50,
    qualities: [
      { quality: '480p', status: 'completed' },
      { quality: '1080p', status: 'pending' },
    ],
  },
  {
    video_id: 3,
    content_id: 12,
    title: 'Demo',
    status: 'pending',
    progress: 0,
    qualities: [],
  },
  {
    video_id: 4,
    content_id: 13,
    title: 'Broken',
    status: 'failed',
    progress: 0,
    qualities: [],
  },
]

describe('/dashboard/video-processing page', () => {
  it('lists each video with its status, progress and per-quality transcoding', async () => {
    mockFetch({ 'GET /content/videos/processing': videos })
    render(<VideoProcessingPage />)

    expect(await screen.findByText('Tutorial')).toBeInTheDocument()
    expect(screen.getByText('completed', { selector: 'span' })).toBeInTheDocument()
    expect(screen.getByText('processing')).toBeInTheDocument()
    expect(screen.getByText('50% complete')).toBeInTheDocument()
    expect(screen.getByText('480p: completed · 1080p: pending')).toBeInTheDocument()
    expect(screen.getAllByText('0% complete')).toHaveLength(2)
    expect(screen.getByText('failed')).toBeInTheDocument()
  })

  it('shows the progress bar width for each video', async () => {
    mockFetch({ 'GET /content/videos/processing': videos })
    const { container } = render(<VideoProcessingPage />)
    await screen.findByText('Guide')

    const bars = Array.from(container.querySelectorAll('div.bg-blue-600')) as HTMLElement[]
    expect(bars.map((bar) => bar.style.width)).toEqual(['100%', '50%', '0%', '0%'])
  })

  it('says when the creator has no videos', async () => {
    mockFetch({ 'GET /content/videos/processing': [] })
    render(<VideoProcessingPage />)

    expect(await screen.findByText('You have no videos yet.')).toBeInTheDocument()
  })

  it('shows the server reason when videos cannot be loaded', async () => {
    mockFetch({ 'GET /content/videos/processing': reply({ detail: 'Videos offline' }, 503) })
    render(<VideoProcessingPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Videos offline')
  })

  it('uses a generic message when the request fails without an API error', async () => {
    global.fetch = jest.fn(() => Promise.reject(new TypeError('network down'))) as unknown as typeof fetch
    render(<VideoProcessingPage />)

    expect(await screen.findByText('Videos could not be loaded.')).toBeInTheDocument()
  })

  it('shows a loading placeholder while the videos are in flight', () => {
    global.fetch = jest.fn(() => new Promise<Response>(() => undefined)) as unknown as typeof fetch
    render(<VideoProcessingPage />)

    expect(screen.getByText('Loading videos…')).toBeInTheDocument()
  })
})
