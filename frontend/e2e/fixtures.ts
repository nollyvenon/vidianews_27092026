import { Page } from '@playwright/test'

/** Token pair returned by POST /auth/login and POST /auth/register. */
export const tokens = {
  access_token: 'e2e-access-token',
  refresh_token: 'e2e-refresh-token',
  token_type: 'bearer',
}

/** Profile returned by GET /auth/me. */
export const user = {
  id: 1,
  email: 'editor@example.com',
  name: 'E2E Editor',
  role: 'admin',
  organization_id: 1,
  tenant_id: 1,
  created_at: '2026-01-01T00:00:00Z',
}

/** A route answer with an explicit status. Plain values are answered with 200. */
export interface MockedReply {
  status: number
  body: unknown
}

function isMockedReply(value: unknown): value is MockedReply {
  return typeof value === 'object' && value !== null && 'status' in value && 'body' in value
}

/**
 * Answers every /api/v1 request from a route table keyed by "METHOD /path" (path without the
 * /api/v1 prefix). Unknown routes get a 404 with the backend's { detail } shape. The browser
 * talks to the frontend origin, so the mock intercepts the same URLs the app requests.
 */
export async function mockApi(page: Page, routes: Record<string, unknown>): Promise<void> {
  await page.route('**/api/v1/**', async (route) => {
    const request = route.request()
    const path = new URL(request.url()).pathname.replace(/^\/api\/v1/, '')
    const entry = routes[`${request.method()} ${path}`]

    if (entry === undefined) {
      await route.fulfill({
        status: 404,
        contentType: 'application/json',
        body: JSON.stringify({ detail: `Not found: ${request.method()} ${path}` }),
      })
      return
    }

    const reply: MockedReply = isMockedReply(entry) ? entry : { status: 200, body: entry }
    await route.fulfill({
      status: reply.status,
      contentType: 'application/json',
      body: JSON.stringify(reply.body),
    })
  })
}
