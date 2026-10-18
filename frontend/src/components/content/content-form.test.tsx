import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { ApiError } from '@/lib/api-error'
import { ContentForm, ContentValues, EMPTY_CONTENT, slugify } from '@/components/content/content-form'

const existing: ContentValues = {
  title: 'Storm report',
  slug: 'storm-report',
  description: 'Summary',
  body: 'Body',
  content_type: 'video',
  status: 'published',
  access_level: 'private',
  thumbnail_url: 'https://cdn.example.com/a.png',
}

describe('slugify', () => {
  it('lowercases the value and joins words with hyphens', () => {
    expect(slugify('  Storm Report, Part 2!  ')).toBe('storm-report-part-2')
  })

  it('returns an empty string when nothing URL-safe remains', () => {
    expect(slugify('---!!!')).toBe('')
  })

  it('limits the slug to 500 characters', () => {
    expect(slugify('a'.repeat(600))).toHaveLength(500)
  })
})

describe('ContentForm', () => {
  it('starts from empty values with the submit label provided', () => {
    render(<ContentForm submitLabel="Create content" onSubmit={jest.fn()} />)

    expect(screen.getByLabelText('Title')).toHaveValue('')
    expect(screen.getByLabelText('Type')).toHaveValue(EMPTY_CONTENT.content_type)
    expect(screen.getByRole('button', { name: 'Create content' })).toBeEnabled()
  })

  it('derives the slug from the title until the author edits the slug', () => {
    render(<ContentForm submitLabel="Create content" onSubmit={jest.fn()} />)

    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Storm Report' } })
    expect(screen.getByLabelText('Slug')).toHaveValue('storm-report')

    fireEvent.change(screen.getByLabelText('Slug'), { target: { value: 'custom-slug' } })
    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Another Title' } })
    expect(screen.getByLabelText('Slug')).toHaveValue('custom-slug')
  })

  it('keeps the stored slug of an existing item when its title changes', () => {
    render(<ContentForm initial={existing} submitLabel="Save changes" onSubmit={jest.fn()} />)

    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Storm report revised' } })

    expect(screen.getByLabelText('Slug')).toHaveValue('storm-report')
  })

  it('submits every field the author has set', async () => {
    const onSubmit = jest.fn().mockResolvedValue(undefined)
    render(<ContentForm submitLabel="Create content" onSubmit={onSubmit} />)

    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Launch day' } })
    fireEvent.change(screen.getByLabelText('Summary'), { target: { value: 'Our launch' } })
    fireEvent.change(screen.getByLabelText('Body'), { target: { value: 'We launched.' } })
    fireEvent.change(screen.getByLabelText('Type'), { target: { value: 'newsletter' } })
    fireEvent.change(screen.getByLabelText('Status'), { target: { value: 'scheduled' } })
    fireEvent.change(screen.getByLabelText('Access'), { target: { value: 'members_only' } })
    fireEvent.change(screen.getByLabelText('Thumbnail URL'), { target: { value: 'https://cdn.example.com/x.png' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create content' }))

    await waitFor(() => expect(onSubmit).toHaveBeenCalledTimes(1))
    expect(onSubmit).toHaveBeenCalledWith({
      title: 'Launch day',
      slug: 'launch-day',
      description: 'Our launch',
      body: 'We launched.',
      content_type: 'newsletter',
      status: 'scheduled',
      access_level: 'members_only',
      thumbnail_url: 'https://cdn.example.com/x.png',
    })
  })

  it('disables the button while saving', async () => {
    let finish: () => void = () => undefined
    const onSubmit = jest.fn(() => new Promise<void>((resolve) => (finish = resolve)))
    render(<ContentForm initial={existing} submitLabel="Save changes" onSubmit={onSubmit} />)

    fireEvent.click(screen.getByRole('button', { name: 'Save changes' }))

    expect(await screen.findByRole('button', { name: 'Saving…' })).toBeDisabled()
    finish()
    expect(await screen.findByRole('button', { name: 'Save changes' })).toBeEnabled()
  })

  it('shows the server message when saving is refused', async () => {
    const onSubmit = jest.fn().mockRejectedValue(new ApiError('Slug already used'))
    render(<ContentForm initial={existing} submitLabel="Save changes" onSubmit={onSubmit} />)

    fireEvent.click(screen.getByRole('button', { name: 'Save changes' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Slug already used')
  })

  it('shows a generic message when saving fails without a server reason', async () => {
    const onSubmit = jest.fn().mockRejectedValue(new Error('Failed to fetch'))
    render(<ContentForm initial={existing} submitLabel="Save changes" onSubmit={onSubmit} />)

    fireEvent.click(screen.getByRole('button', { name: 'Save changes' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('The content could not be saved.')
  })

  it('clears a previous error when the author submits again', async () => {
    const onSubmit = jest
      .fn()
      .mockRejectedValueOnce(new ApiError('Slug already used'))
      .mockResolvedValueOnce(undefined)
    render(<ContentForm initial={existing} submitLabel="Save changes" onSubmit={onSubmit} />)

    fireEvent.click(screen.getByRole('button', { name: 'Save changes' }))
    expect(await screen.findByRole('alert')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Save changes' }))
    await waitFor(() => expect(screen.queryByRole('alert')).not.toBeInTheDocument())
  })
})
