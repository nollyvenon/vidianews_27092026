import { ApiError, errorMessage, messageFromDetail } from '@/lib/api-error'

describe('messageFromDetail', () => {
  it('returns a non-blank string detail unchanged', () => {
    expect(messageFromDetail('Email already registered')).toBe('Email already registered')
  })

  it('returns the message of the structured APIException shape', () => {
    expect(messageFromDetail({ success: false, error: { code: 'CONFLICT', message: 'Slug taken' } })).toBe('Slug taken')
  })

  it('falls back to a top-level message field', () => {
    expect(messageFromDetail({ message: 'Try again later' })).toBe('Try again later')
  })

  it.each([
    ['a blank string', '   '],
    ['an empty object', {}],
    ['an error without a message', { error: { code: 'X' } }],
    ['a non-string message', { message: 42 }],
    ['an empty message', { error: { message: '' } }],
    ['a number', 500],
    ['null', null],
    ['undefined', undefined],
  ])('returns null for %s', (_label, detail) => {
    expect(messageFromDetail(detail)).toBeNull()
  })
})

describe('ApiError', () => {
  it('carries the server message and its own name', () => {
    const error = new ApiError('Not allowed')

    expect(error).toBeInstanceOf(Error)
    expect(error.name).toBe('ApiError')
    expect(error.message).toBe('Not allowed')
  })
})

describe('errorMessage', () => {
  it('prefers the server detail of an axios-style response error', () => {
    const error = { response: { data: { detail: 'Order is locked' } } }

    expect(errorMessage(error, 'Fallback')).toBe('Order is locked')
  })

  it('reads a structured detail from an axios-style response error', () => {
    const error = { response: { data: { detail: { error: { message: 'Card declined' } } } } }

    expect(errorMessage(error, 'Fallback')).toBe('Card declined')
  })

  it('uses the fallback when the response carries no usable detail', () => {
    expect(errorMessage({ response: { data: {} } }, 'Fallback')).toBe('Fallback')
    expect(errorMessage({ response: undefined }, 'Fallback')).toBe('Fallback')
  })

  it('uses the message of an ApiError raised by the API client', () => {
    expect(errorMessage(new ApiError('Slug taken'), 'Fallback')).toBe('Slug taken')
  })

  it('uses the fallback for an ApiError with an empty message', () => {
    expect(errorMessage(new ApiError(''), 'Fallback')).toBe('Fallback')
  })

  it('does not expose the message of a plain network or programming error', () => {
    expect(errorMessage(new Error('Failed to fetch'), 'Fallback')).toBe('Fallback')
  })

  it.each([
    ['null', null],
    ['undefined', undefined],
    ['a string', 'boom'],
  ])('uses the fallback for %s', (_label, error) => {
    expect(errorMessage(error, 'Fallback')).toBe('Fallback')
  })
})
