import { cn } from '@/lib/utils'

describe('cn', () => {
  it('joins truthy class names and drops falsy ones', () => {
    expect(cn('px-2', false, undefined, 'text-sm', null, 'font-bold')).toBe('px-2 text-sm font-bold')
  })

  it('supports conditional object syntax', () => {
    expect(cn({ 'bg-red-500': true, 'bg-blue-500': false })).toBe('bg-red-500')
  })

  it('returns an empty string when nothing is truthy', () => {
    expect(cn(false, null, undefined)).toBe('')
  })
})
