import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { useParams } from 'next/navigation'
import CourseDetailPage from '@/app/dashboard/courses/[id]/page'
import { mockFetch, reply } from '@/test-utils'

const course = {
  id: 7,
  title: 'Storytelling Basics',
  description: 'Structure a story',
  instructor_id: 4,
  price: 49,
  average_rating: 4.2,
  total_reviews: 3,
  difficulty_level: 'beginner',
  duration_hours: 6,
  learning_objectives: ['Hook viewers'],
}
const sections = [
  {
    id: 1,
    title: 'Week 1: Hooks',
    lessons: [
      { id: 11, title: 'The cold open', video_url: '', video_duration: 12, is_completed: false },
      { id: 12, title: 'Pacing', video_url: '', video_duration: 9, is_completed: true },
    ],
  },
]
const reviews = [{ id: 1, user_id: 2, rating: 5, title: 'Great', content: 'Learned a lot' }]
const enrollment = {
  id: 90,
  course_id: 7,
  status: 'active',
  progress_percentage: 50,
  lessons_completed: 1,
  certificate_issued: false,
}

function baseRoutes(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /courses/7': course,
    'GET /courses/7/sections': sections,
    'GET /courses/7/reviews': reviews,
    ...extra,
  })
}

describe('/dashboard/courses/[id] page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
    ;(useParams as jest.Mock).mockReturnValue({ id: '7' })
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows the course details, its sections and reviews before enrolling', async () => {
    baseRoutes()
    render(<CourseDetailPage />)

    expect(await screen.findByRole('heading', { name: 'Storytelling Basics' })).toBeInTheDocument()
    expect(screen.getByText('★ 4.2 (3 reviews)')).toBeInTheDocument()
    expect(screen.getByText('6h total duration')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Enroll Now - $49.00' })).toBeInTheDocument()
    expect(screen.getByText('Week 1: Hooks')).toBeInTheDocument()
    expect(screen.getByText('Great')).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Leave a Review' })).not.toBeInTheDocument()
  })

  it('expands a section to show its lessons and collapses it again', async () => {
    baseRoutes()
    render(<CourseDetailPage />)

    fireEvent.click(await screen.findByRole('button', { name: /Week 1: Hooks/ }))
    expect(screen.getByText('The cold open')).toBeInTheDocument()
    expect(screen.getByText('12 minutes')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Mark Complete' })).not.toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: /Week 1: Hooks/ }))
    expect(screen.queryByText('The cold open')).not.toBeInTheDocument()
  })

  it('enrolls the user and unlocks lesson completion and reviews', async () => {
    baseRoutes({ 'POST /courses/7/enroll': enrollment })
    render(<CourseDetailPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Enroll Now - $49.00' }))

    expect(await screen.findByText('Enrollment Status: active')).toBeInTheDocument()
    expect(screen.getByText('1 lessons completed')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Leave a Review' })).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: /Week 1: Hooks/ }))
    expect(screen.getByRole('button', { name: 'Mark Complete' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: '✓ Completed' })).toBeInTheDocument()
  })

  it('marks a lesson complete and refreshes the enrollment progress', async () => {
    const fetchMock = baseRoutes({
      'POST /courses/7/enroll': enrollment,
      'POST /enrollments/90/lessons/11/complete': { ok: true },
      'GET /enrollments/90': { ...enrollment, lessons_completed: 2, progress_percentage: 100, certificate_issued: true },
    })
    render(<CourseDetailPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'Enroll Now - $49.00' }))
    fireEvent.click(await screen.findByRole('button', { name: /Week 1: Hooks/ }))

    fireEvent.click(screen.getAllByRole('button', { name: 'Mark Complete' })[0])

    expect(await screen.findByText('2 lessons completed')).toBeInTheDocument()
    expect(screen.getByText('✓ Certificate Earned')).toBeInTheDocument()
    expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/enrollments/90/lessons/11/complete') && init?.method === 'POST')).toBe(true)
  })

  it('submits a review and reloads the review list', async () => {
    const fetchMock = baseRoutes({
      'POST /courses/7/enroll': enrollment,
      'POST /courses/7/reviews': { id: 2 },
    })
    render(<CourseDetailPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'Enroll Now - $49.00' }))
    await screen.findByRole('heading', { name: 'Leave a Review' })

    fireEvent.change(screen.getByRole('combobox'), { target: { value: '4' } })
    fireEvent.change(screen.getByPlaceholderText('Share your experience...'), { target: { value: 'Solid course' } })
    fireEvent.click(screen.getByRole('button', { name: 'Submit Review' }))

    await waitFor(() => expect(screen.getByPlaceholderText('Share your experience...')).toHaveValue(''))
    const postCall = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/courses/7/reviews') && init?.method === 'POST')
    expect(JSON.parse(postCall![1].body as string)).toEqual({ rating: 4, content: 'Solid course' })
    expect(screen.getByRole('combobox')).toHaveValue('5')
  })

  it('shows the not-found message when the course does not exist', async () => {
    baseRoutes({ 'GET /courses/7': reply({ detail: 'Course not found' }, 404) })
    render(<CourseDetailPage />)

    expect(await screen.findByText('Course not found')).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Storytelling Basics' })).not.toBeInTheDocument()
  })

  it('shows the not-found message and logs when the course request cannot be made', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch
    render(<CourseDetailPage />)

    expect(await screen.findByText('Course not found')).toBeInTheDocument()
    expect(consoleError).toHaveBeenCalledWith('Failed to load course:', expect.any(Error))
  })

  it('keeps the enroll button and logs when enrolment is rejected', async () => {
    baseRoutes({ 'POST /courses/7/enroll': reply({ detail: 'Sold out' }, 409) })
    render(<CourseDetailPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'Enroll Now - $49.00' }))

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Enrollment failed:', 409))
    expect(screen.getByRole('button', { name: 'Enroll Now - $49.00' })).toBeInTheDocument()
  })

  it('logs a failed lesson completion', async () => {
    global.fetch = jest.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input)
      if (init?.method === 'POST' && url.endsWith('/enroll')) return { ok: true, json: async () => enrollment } as Response
      if (init?.method === 'POST' && url.includes('/lessons/')) throw new Error('network down')
      if (url.endsWith('/courses/7')) return { ok: true, json: async () => course } as Response
      if (url.endsWith('/sections')) return { ok: true, json: async () => sections } as Response
      return { ok: true, json: async () => reviews } as Response
    }) as unknown as typeof fetch
    render(<CourseDetailPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'Enroll Now - $49.00' }))
    fireEvent.click(await screen.findByRole('button', { name: /Week 1: Hooks/ }))

    fireEvent.click(screen.getAllByRole('button', { name: 'Mark Complete' })[0])

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Lesson completion failed:', expect.any(Error)))
  })

  it('logs a failed review submission', async () => {
    global.fetch = jest.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input)
      if (init?.method === 'POST' && url.endsWith('/enroll')) return { ok: true, json: async () => enrollment } as Response
      if (init?.method === 'POST' && url.endsWith('/reviews')) throw new Error('network down')
      if (url.endsWith('/courses/7')) return { ok: true, json: async () => course } as Response
      if (url.endsWith('/sections')) return { ok: true, json: async () => sections } as Response
      return { ok: true, json: async () => reviews } as Response
    }) as unknown as typeof fetch
    render(<CourseDetailPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'Enroll Now - $49.00' }))
    await screen.findByRole('heading', { name: 'Leave a Review' })

    fireEvent.click(screen.getByRole('button', { name: 'Submit Review' }))

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Review submission failed:', expect.any(Error)))
  })
})
