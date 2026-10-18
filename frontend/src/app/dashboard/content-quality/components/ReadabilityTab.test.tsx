import { fireEvent, screen } from '@testing-library/react'
import ReadabilityTab, { describeReadingEase } from '@/app/dashboard/content-quality/components/ReadabilityTab'
import { mockFetch, renderWithQuery, reply } from '@/test-utils'

const baseResult = {
  id: 3,
  content_id: 7,
  word_count: 120,
  sentence_count: 8,
  paragraph_count: 2,
  flesch_reading_ease: 65,
  flesch_kincaid_grade: 8.4,
  gunning_fog_index: 10.2,
  smog_index: 9.1,
  readability_level: 'Moderate',
  target_audience_grade_level: 'Grade 8',
  complexity_score: 50,
  avg_word_length: 5,
  avg_sentence_length: 15,
  recommendations: ['Break long sentences into shorter ones.'],
}

function routes(result: Record<string, unknown> = baseResult) {
  return mockFetch({
    'GET /content': { items: [{ id: 7, title: 'Storm report', status: 'published', content_type: 'article' }], total: 1 },
    'GET /content/7': { id: 7, title: 'Storm report', body: 'Some readable text.' },
    'POST /readability/check': result,
  })
}

async function runCheck() {
  fireEvent.change(await screen.findByRole('combobox'), { target: { value: '7' } })
  await screen.findByDisplayValue('Some readable text.')
  fireEvent.click(screen.getByRole('button', { name: 'Check Readability' }))
}

describe('ReadabilityTab', () => {
  it('needs content to be chosen before the analysis can run', async () => {
    routes()
    renderWithQuery(<ReadabilityTab />)

    expect(await screen.findByRole('combobox')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Check Readability' })).toBeDisabled()
  })

  it('posts the content id and text, then shows the level, indexes and statistics', async () => {
    const fetchMock = routes()
    renderWithQuery(<ReadabilityTab />)
    await runCheck()

    expect(await screen.findByText('Moderate')).toBeInTheDocument()
    expect(screen.getByText('Grade 8')).toBeInTheDocument()
    expect(screen.getByText('65.0')).toBeInTheDocument()
    expect(screen.getByText('8.4')).toBeInTheDocument()
    expect(screen.getByText('10.2')).toBeInTheDocument()
    expect(screen.getByText('9.1')).toBeInTheDocument()
    expect(screen.getByText('Requires grade 8 level education')).toBeInTheDocument()
    expect(screen.getByText('120')).toBeInTheDocument()
    expect(screen.getByText('15.0 words')).toBeInTheDocument()
    expect(screen.getByText('Break long sentences into shorter ones.')).toBeInTheDocument()

    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/readability/check') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({ content_id: 7, text: 'Some readable text.' })
  })

  it('labels high and low complexity', async () => {
    routes({ ...baseResult, complexity_score: 75 })
    renderWithQuery(<ReadabilityTab />)
    await runCheck()

    expect(await screen.findByText('High complexity')).toBeInTheDocument()
  })

  it('labels moderate and low complexity', async () => {
    routes({ ...baseResult, complexity_score: 55, recommendations: [] })
    renderWithQuery(<ReadabilityTab />)
    await runCheck()

    expect(await screen.findByText('Moderate complexity')).toBeInTheDocument()
    expect(screen.queryByText('Improvement tips')).not.toBeInTheDocument()
  })

  it('shows the low complexity label for simple text', async () => {
    routes({ ...baseResult, complexity_score: 20 })
    renderWithQuery(<ReadabilityTab />)
    await runCheck()

    expect(await screen.findByText('Low complexity')).toBeInTheDocument()
  })

  it('shows the server message when the check fails', async () => {
    mockFetch({
      'GET /content': { items: [{ id: 7, title: 'Storm report', status: 'published', content_type: 'article' }], total: 1 },
      'GET /content/7': { id: 7, title: 'Storm report', body: 'Some readable text.' },
      'POST /readability/check': reply({ detail: 'Your account has no organization yet.' }, 422),
    })
    renderWithQuery(<ReadabilityTab />)
    await runCheck()

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no organization yet.')
  })

  it('describes each Flesch reading ease band', () => {
    expect(describeReadingEase(95)).toBe('Very Easy - 5th grade level')
    expect(describeReadingEase(85)).toBe('Easy - 6th grade level')
    expect(describeReadingEase(75)).toBe('Fairly Easy - 7th grade level')
    expect(describeReadingEase(65)).toBe('Standard - 8th-9th grade level')
    expect(describeReadingEase(55)).toBe('Fairly Difficult - 10th-12th grade level')
    expect(describeReadingEase(40)).toBe('Difficult - College level')
    expect(describeReadingEase(10)).toBe('Very Difficult - College graduate level')
  })
})
