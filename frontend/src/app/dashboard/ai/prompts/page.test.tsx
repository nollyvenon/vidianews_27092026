import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import PromptsPage from '@/app/dashboard/ai/prompts/page'
import { mockFetch, reply } from '@/test-utils'

const prompts = [
  { id: 1, name: 'Summarise article', category: 'content', usage_count: 5, rating: 4.5, created_at: '2026-10-01' },
  { id: 2, name: 'Tone check', category: 'analysis', usage_count: 0, rating: 3, created_at: '2026-10-01' },
]

describe('/dashboard/ai/prompts page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows a loading state, then the prompts with usage and rating', async () => {
    mockFetch({ 'GET /ai/templates': prompts })
    render(<PromptsPage />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()
    expect(await screen.findByText('Summarise article')).toBeInTheDocument()
    expect(screen.getByText('Used 5 times')).toBeInTheDocument()
    expect(screen.getByText('⭐ 4.5')).toBeInTheDocument()
    expect(screen.getByText('⭐ 3.0')).toBeInTheDocument()
  })

  it('reloads the prompts for the selected category', async () => {
    const fetchMock = mockFetch({ 'GET /ai/templates': prompts })
    render(<PromptsPage />)
    await screen.findByText('Summarise article')

    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'creative' } })

    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('category=creative'))).toBe(true))
  })

  it('shows the empty state for a category with no prompts', async () => {
    mockFetch({ 'GET /ai/templates': [] })
    render(<PromptsPage />)

    expect(await screen.findByText('No prompts in this category yet.')).toBeInTheDocument()
  })

  it('logs the failure and shows the empty state when prompts cannot be loaded', async () => {
    mockFetch({ 'GET /ai/templates': reply({ detail: 'down' }, 500) })
    render(<PromptsPage />)

    expect(await screen.findByText('No prompts in this category yet.')).toBeInTheDocument()
    expect(consoleError).toHaveBeenCalledWith('Failed to fetch prompts', expect.any(Error))
  })
})
