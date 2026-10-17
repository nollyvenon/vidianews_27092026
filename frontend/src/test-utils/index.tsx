import { ReactElement } from 'react'
import { render, RenderResult } from '@testing-library/react'
import { AuthContext, AuthContextType, User } from '@/lib/auth-context'

/** Signed-in user used by default in page tests. */
export const testUser: User = {
  id: 1,
  email: 'editor@example.com',
  name: 'Test Editor',
  role: 'admin',
  organization_id: 10,
  tenant_id: 20,
  created_at: '2026-01-01T00:00:00Z',
}

/** Auth context value for a signed-in session. Override any field per test. */
export function buildAuth(overrides: Partial<AuthContextType> = {}): AuthContextType {
  return {
    token: 'test-token',
    user: testUser,
    loading: false,
    login: jest.fn(),
    logout: jest.fn(),
    signup: jest.fn(),
    ...overrides,
  }
}

/** Renders a component inside the auth context the dashboard reads from. */
export function renderWithAuth(
  ui: ReactElement,
  auth: AuthContextType = buildAuth()
): RenderResult & { auth: AuthContextType } {
  return {
    auth,
    ...render(<AuthContext.Provider value={auth}>{ui}</AuthContext.Provider>),
  }
}

/** Response returned by a mocked route. Wrap a body in `reply` to choose the status code. */
export class Reply {
  constructor(
    readonly body: unknown,
    readonly status: number = 200
  ) {}
}

export function reply(body: unknown, status = 200): Reply {
  return new Reply(body, status)
}

type RouteValue = unknown | Reply | ((url: string, init?: RequestInit) => unknown | Reply)

function resolveRoute(value: RouteValue, url: string, init?: RequestInit): Reply {
  const resolved = typeof value === 'function' ? (value as (u: string, i?: RequestInit) => unknown)(url, init) : value
  return resolved instanceof Reply ? resolved : new Reply(resolved, 200)
}

function toFetchResponse(result: Reply): Response {
  const ok = result.status >= 200 && result.status < 300
  return {
    ok,
    status: result.status,
    statusText: ok ? 'OK' : 'Error',
    json: async () => result.body,
    text: async () => JSON.stringify(result.body),
  } as unknown as Response
}

/**
 * Installs a `fetch` mock that answers requests from a route table.
 *
 * Keys have the form `'METHOD /path'`. A request matches when its method is equal and its
 * pathname equals the key path or ends with it, so `'GET /settings/me'` matches both
 * `/settings/me` and `/api/v1/settings/me`. Unmatched requests get a 404 with `{ detail }`,
 * the same shape the backend returns.
 */
export function mockFetch(routes: Record<string, RouteValue> = {}): jest.Mock {
  const fetchMock = jest.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input)
    const { pathname } = new URL(url, 'http://localhost')
    const method = (init?.method ?? 'GET').toUpperCase()

    const key = Object.keys(routes).find((route) => {
      const [routeMethod, routePath] = route.split(' ')
      return routeMethod === method && (pathname === routePath || pathname.endsWith(routePath))
    })

    if (!key) {
      return toFetchResponse(new Reply({ detail: `Not found: ${method} ${pathname}` }, 404))
    }
    return toFetchResponse(resolveRoute(routes[key], url, init))
  })

  global.fetch = fetchMock as unknown as typeof fetch
  return fetchMock
}

/** Resolves on the next macrotask so pending promise chains and state updates flush. */
export const flushPromises = () => new Promise((resolve) => setTimeout(resolve, 0))
