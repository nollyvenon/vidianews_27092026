import { renderHook } from '@testing-library/react'
import { useAuth } from '@/hooks/useAuth'
import { buildAuth, renderWithAuth } from '@/test-utils'
import { AuthContext } from '@/lib/auth-context'
import { createElement, ReactNode } from 'react'

describe('useAuth', () => {
  it('returns the session from the nearest auth provider', () => {
    const auth = buildAuth()
    const wrapper = ({ children }: { children: ReactNode }) =>
      createElement(AuthContext.Provider, { value: auth }, children)

    const { result } = renderHook(() => useAuth(), { wrapper })

    expect(result.current).toBe(auth)
  })

  it('throws when used outside an auth provider', () => {
    const consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)

    expect(() => renderHook(() => useAuth())).toThrow('useAuth must be used within AuthProvider')

    consoleError.mockRestore()
  })

  it('is reachable from components rendered inside the test wrapper', () => {
    const Probe = () => {
      const { user } = useAuth()
      return createElement('span', null, user?.email)
    }
    const { getByText } = renderWithAuth(createElement(Probe))

    expect(getByText('editor@example.com')).toBeInTheDocument()
  })
})
