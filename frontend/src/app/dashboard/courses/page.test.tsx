import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import CoursesPage from '@/app/dashboard/courses/page'
import { mockFetch, reply } from '@/test-utils'

const courses = [
  {
    id: 1,
    title: 'Intro to Editing',
    description: 'Cut your first video',
    instructor_id: 4,
    price: 49,
    status: 'published',
    average_rating: 4.5,
    total_enrollments: 120,
    thumbnail_url: 'https://cdn.example.com/editing.jpg',
    difficulty_level: 'beginner',
  },
  {
    id: 2,
    title: 'Advanced Color Grading',
    description: 'Grade like a pro',
    instructor_id: 4,
    price: 99.9,
    status: 'published',
    average_rating: 4.9,
    total_enrollments: 40,
    thumbnail_url: '',
    difficulty_level: 'advanced',
  },
]

describe('/dashboard/courses page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows a loading state, then the course catalogue', async () => {
    mockFetch({ 'GET /courses': courses })
    render(<CoursesPage />)

    expect(screen.getByText('Loading courses...')).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'Intro to Editing' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Advanced Color Grading' })).toBeInTheDocument()
    expect(screen.getByText('★ 4.5')).toBeInTheDocument()
    expect(screen.getByText('120 students')).toBeInTheDocument()
    expect(screen.getByText('$99.90')).toBeInTheDocument()
  })

  it('shows the thumbnail only for courses that have one', async () => {
    mockFetch({ 'GET /courses': courses })
    render(<CoursesPage />)
    await screen.findByRole('heading', { name: 'Intro to Editing' })

    const thumbnail = screen.getByRole('img', { name: 'Intro to Editing' })
    expect(thumbnail).toHaveAttribute('src', expect.stringContaining('editing.jpg'))
    expect(screen.queryByRole('img', { name: 'Advanced Color Grading' })).not.toBeInTheDocument()
  })

  it('filters the catalogue by title as the user types', async () => {
    mockFetch({ 'GET /courses': courses })
    render(<CoursesPage />)
    await screen.findByRole('heading', { name: 'Intro to Editing' })

    fireEvent.change(screen.getByPlaceholderText('Search courses...'), { target: { value: 'color' } })

    expect(screen.queryByRole('heading', { name: 'Intro to Editing' })).not.toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Advanced Color Grading' })).toBeInTheDocument()
  })

  it('filters the catalogue by difficulty level', async () => {
    mockFetch({ 'GET /courses': courses })
    render(<CoursesPage />)
    await screen.findByRole('heading', { name: 'Intro to Editing' })

    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'beginner' } })

    expect(screen.getByRole('heading', { name: 'Intro to Editing' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Advanced Color Grading' })).not.toBeInTheDocument()
  })

  it('links to course creation and to each course', async () => {
    mockFetch({ 'GET /courses': courses })
    render(<CoursesPage />)
    await screen.findByRole('heading', { name: 'Intro to Editing' })

    expect(screen.getByRole('link', { name: 'Create Course' })).toHaveAttribute('href', '/dashboard/courses/create')
    expect(screen.getAllByRole('link', { name: 'View Course' })[0]).toHaveAttribute('href', '/dashboard/courses/1')
  })

  it('shows an empty catalogue and logs when the courses cannot be loaded', async () => {
    mockFetch({ 'GET /courses': reply({ detail: 'down' }, 500) })
    render(<CoursesPage />)

    expect(await screen.findByRole('heading', { name: 'Courses' })).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: 'View Course' })).not.toBeInTheDocument()
    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Failed to load courses:', expect.any(Error)))
  })

  it('treats a catalogue response that is not a list as an empty catalogue', async () => {
    mockFetch({ 'GET /courses': { detail: 'unexpected' } })
    render(<CoursesPage />)

    expect(await screen.findByRole('heading', { name: 'Courses' })).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: 'View Course' })).not.toBeInTheDocument()
  })
})
