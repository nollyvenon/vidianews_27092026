import { act, renderHook } from '@testing-library/react'
import { toast, useToast } from '@/hooks/use-toast'

const LIFETIME_MS = 4000

describe('use-toast', () => {
  beforeEach(() => {
    jest.useFakeTimers()
  })

  afterEach(() => {
    jest.useRealTimers()
  })

  it('adds a toast to every subscriber', () => {
    const { result } = renderHook(() => useToast())
    act(() => {
      toast({ title: 'Saved', description: 'Content saved' })
    })
    expect(result.current.toasts).toHaveLength(1)
    expect(result.current.toasts[0]).toMatchObject({ title: 'Saved', variant: 'default' })
  })

  it('removes a toast when it is dismissed', () => {
    const { result } = renderHook(() => useToast())
    let id = 0
    act(() => {
      id = toast({ title: 'Oops', variant: 'destructive' }).id
    })
    act(() => {
      result.current.dismiss(id)
    })
    expect(result.current.toasts.find((item) => item.id === id)).toBeUndefined()
  })

  it('removes a toast automatically after its lifetime', () => {
    const { result } = renderHook(() => useToast())
    act(() => {
      toast({ title: 'Brief' })
    })
    expect(result.current.toasts.some((item) => item.title === 'Brief')).toBe(true)
    act(() => {
      jest.advanceTimersByTime(LIFETIME_MS)
    })
    expect(result.current.toasts.some((item) => item.title === 'Brief')).toBe(false)
  })

  it('returns a dismiss handle from toast()', () => {
    const { result } = renderHook(() => useToast())
    let handle: { id: number; dismiss: () => void } | undefined
    act(() => {
      handle = toast({ title: 'Handle' })
    })
    act(() => {
      handle?.dismiss()
    })
    expect(result.current.toasts.some((item) => item.title === 'Handle')).toBe(false)
  })
})
