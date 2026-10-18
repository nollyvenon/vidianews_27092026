import { test, expect } from '@playwright/test'
import { mockApi, tokens, user } from './fixtures'

/** What POST /auth/register answers while the account still needs its email confirmed. */
const pendingRegistration = {
  requires_verification: true,
  message: 'Check your email to confirm your account before signing in.',
  access_token: null,
  refresh_token: null,
  token_type: 'bearer',
}

test.describe('authentication flow', () => {
  test('signing in on /auth/login opens the dashboard for the user', async ({ page }) => {
    await mockApi(page, { 'POST /auth/login': tokens, 'GET /auth/me': user })
    await page.goto('/auth/login')

    await page.getByPlaceholder('your@email.com').fill(user.email)
    await page.getByPlaceholder('••••••••').fill('secret123')
    await page.getByRole('button', { name: 'Sign in' }).click()

    await expect(page).toHaveURL(/\/dashboard$/)
    await expect(page.getByRole('navigation')).toContainText(user.name)
  })

  test('signing in on /login uses the same session and opens the dashboard', async ({ page }) => {
    await mockApi(page, { 'POST /auth/login': tokens, 'GET /auth/me': user })
    await page.goto('/login')
    await expect(page).toHaveURL(/\/auth\/login$/)

    await page.getByPlaceholder('your@email.com').fill(user.email)
    await page.getByPlaceholder('••••••••').fill('secret123')
    await page.getByRole('button', { name: 'Sign in' }).click()

    await expect(page).toHaveURL(/\/dashboard$/)
    await expect(page.getByRole('navigation')).toContainText(user.name)
  })

  test('a rejected password shows the server message and keeps the visitor on the form', async ({ page }) => {
    await mockApi(page, { 'POST /auth/login': { status: 401, body: { detail: 'Invalid credentials' } } })
    await page.goto('/auth/login')

    await page.getByPlaceholder('your@email.com').fill(user.email)
    await page.getByPlaceholder('••••••••').fill('wrong-password')
    await page.getByRole('button', { name: 'Sign in' }).click()

    await expect(page.getByText('Invalid credentials')).toBeVisible()
    await expect(page).toHaveURL(/\/auth\/login$/)
  })

  test('the session is restored from the stored token after a reload', async ({ page }) => {
    await mockApi(page, { 'POST /auth/login': tokens, 'GET /auth/me': user })
    await page.goto('/auth/login')
    await page.getByPlaceholder('your@email.com').fill(user.email)
    await page.getByPlaceholder('••••••••').fill('secret123')
    await page.getByRole('button', { name: 'Sign in' }).click()
    await expect(page).toHaveURL(/\/dashboard$/)

    await page.reload()

    await expect(page).toHaveURL(/\/dashboard$/)
    await expect(page.getByRole('navigation')).toContainText(user.name)
  })

  test('a visitor without a session is sent to sign in', async ({ page }) => {
    await mockApi(page, {})
    await page.goto('/dashboard')

    await expect(page).toHaveURL(/\/auth\/login$/)
  })

  test('signing out ends the session and protected pages redirect to sign in', async ({ page }) => {
    await mockApi(page, { 'POST /auth/login': tokens, 'GET /auth/me': user })
    await page.goto('/auth/login')
    await page.getByPlaceholder('your@email.com').fill(user.email)
    await page.getByPlaceholder('••••••••').fill('secret123')
    await page.getByRole('button', { name: 'Sign in' }).click()
    await expect(page.getByRole('navigation')).toContainText(user.name)

    await page.getByRole('button', { name: 'Logout' }).click()
    await expect(page).toHaveURL(/\/auth\/login$/)

    await page.goto('/dashboard')
    await expect(page).toHaveURL(/\/auth\/login$/)
  })

  test('creating an account asks the visitor to confirm the email before signing in', async ({ page }) => {
    await mockApi(page, { 'POST /auth/register': pendingRegistration })
    await page.goto('/auth/signup')

    await page.getByLabel('First name').fill('Ada')
    await page.getByLabel('Last name').fill('Lovelace')
    await page.getByLabel('Email address').fill('ada@example.com')
    await page.getByLabel('Password (min 8 characters)').fill('secret123')
    await page.getByLabel('Confirm password').fill('secret123')
    await page.getByRole('button', { name: 'Create account' }).click()

    await expect(page.getByRole('heading', { name: 'Check your email' })).toBeVisible()
    await expect(page.getByText(/ada@example\.com/).first()).toBeVisible()
    await expect(page).not.toHaveURL(/\/dashboard$/)
  })

  test('the sign-up page sends first and last name separately with the confirmed password', async ({ page }) => {
    await mockApi(page, { 'POST /auth/register': tokens, 'GET /auth/me': user })
    await page.goto('/auth/signup')

    await page.getByLabel('First name').fill('Jane')
    await page.getByLabel('Last name').fill('Q Public')
    await page.getByLabel('Email address').fill('jane@example.com')
    await page.getByLabel('Password (min 8 characters)').fill('secret123')
    await page.getByLabel('Confirm password').fill('secret123')
    const registerRequest = page.waitForRequest(
      (request) => request.url().endsWith('/api/v1/auth/register') && request.method() === 'POST'
    )
    await page.getByRole('button', { name: 'Create account' }).click()

    expect((await registerRequest).postDataJSON()).toEqual({
      email: 'jane@example.com',
      password: 'secret123',
      password_confirm: 'secret123',
      first_name: 'Jane',
      last_name: 'Q Public',
    })
    await expect(page).toHaveURL(/\/dashboard$/)
  })

  test('the sign-up page refuses a confirmation that does not match before any request is made', async ({ page }) => {
    await mockApi(page, { 'POST /auth/register': tokens })
    await page.goto('/auth/signup')

    await page.getByLabel('First name').fill('Ada')
    await page.getByLabel('Last name').fill('Lovelace')
    await page.getByLabel('Email address').fill('ada@example.com')
    await page.getByLabel('Password (min 8 characters)').fill('secret123')
    await page.getByLabel('Confirm password').fill('secret999')
    await page.getByRole('button', { name: 'Create account' }).click()

    // Next.js adds its own role="alert" route announcer, so match the form's message by its text.
    await expect(page.locator('div[role="alert"]', { hasText: 'Passwords do not match' })).toBeVisible()
    await expect(page).toHaveURL(/\/auth\/signup$/)
  })

  test('the old register address redirects to the sign-up page', async ({ page }) => {
    await page.goto('/register')

    await expect(page).toHaveURL(/\/auth\/signup$/)
  })

  test('the site root opens the public introduction', async ({ page }) => {
    await page.goto('/')

    await expect(page).toHaveURL(/\/home$/)
    await expect(page.getByRole('heading', { level: 1, name: 'AetherCMS AI' })).toBeVisible()
  })
})

test.describe('dashboard smoke test', () => {
  test('dashboard sections render without uncaught page errors once signed in', async ({ page }) => {
    // This test visits every section in turn, so it needs more than the default per-test limit.
    test.setTimeout(120_000)
    const pageErrors: string[] = []
    page.on('pageerror', (error) => pageErrors.push(error.message))

    await mockApi(page, {
      'POST /auth/login': tokens,
      'GET /auth/me': user,
      'GET /content': { items: [], total: 0 },
      'GET /content/calendar/events': { events: [] },
      'GET /ai/chats': [],
      'GET /courses': [],
      'GET /membership-types': [],
      'GET /subscriptions/me/active': { status: 404, body: { detail: 'No active subscription' } },
      'GET /notifications/me': [{ id: 1, title: 'New follower', message: 'Sarah followed you', is_read: false, created_at: '2026-10-17T10:00:00Z' }],
      'GET /analytics/revenue': [],
      'GET /analytics/engagement': [],
      'GET /admin/logs': [],
      'GET /system/health': { status: 404, body: { detail: 'No health data available' } },
      'GET /system/alerts': [],
      'GET /health': { status: 'ok', database: 'ok' },
      'GET /feature-flags': [],
      'GET /security/audit-logs': [],
      'GET /moderation/queue/pending': [],
      'GET /platform/followers/1': [],
      'GET /cache/stats/summary': { total_entries: 0, hot_entries: 0, warm_entries: 0, cold_entries: 0, total_hits: 0, avg_hits_per_entry: 0, hit_rate: 0 },
    })
    await page.goto('/auth/login')
    await page.getByPlaceholder('your@email.com').fill(user.email)
    await page.getByPlaceholder('••••••••').fill('secret123')
    await page.getByRole('button', { name: 'Sign in' }).click()
    await expect(page).toHaveURL(/\/dashboard$/)

    await page.goto('/dashboard/content-quality')
    await expect(page.getByRole('heading', { name: 'Content Quality' })).toBeVisible()
    await page.goto('/dashboard/memberships')
    await expect(page.getByRole('heading', { name: 'Membership Plans' })).toBeVisible()
    await page.goto('/dashboard/courses')
    await expect(page.getByRole('heading', { name: 'Courses' })).toBeVisible()
    await page.goto('/dashboard/ai/chat')
    await expect(page.getByText('Create a new chat to get started')).toBeVisible()

    const wiredPages: Array<[string, string]> = [
      ['/dashboard/alerts', 'Alerts'],
      ['/dashboard/analytics-dashboard', 'Analytics Dashboard'],
      ['/dashboard/logs', 'System Logs'],
      ['/dashboard/monitoring', 'System Monitoring'],
      ['/dashboard/features', 'Feature Flags'],
      ['/dashboard/security', 'Security Settings'],
      ['/dashboard/moderation', 'Content Moderation'],
      ['/dashboard/followers', 'My Network'],
      ['/dashboard/subscriptions', 'Subscription Tiers'],
      ['/dashboard/cache', 'Cache Configuration'],
      ['/dashboard/user-management', 'User Management'],
      ['/dashboard/discover', 'Discover'],
      ['/dashboard/enterprise', 'Enterprise Dashboard'],
      ['/dashboard/docs', 'Documentation'],
      ['/dashboard/graphql', 'GraphQL Explorer'],
      ['/dashboard/api-versions', 'API Versions'],
      ['/dashboard/realtime', 'Live Feed'],
      ['/dashboard/video-processing', 'Video Processing'],
      ['/dashboard/testing', 'Test Suites'],
      ['/dashboard/advanced-platform', 'Advanced Platform'],
      ['/dashboard/advanced-features', 'Advanced Features'],
    ]
    for (const [path, heading] of wiredPages) {
      await page.goto(path)
      await expect(page.getByRole('heading', { level: 1, name: heading, exact: true })).toBeVisible()
    }

    expect(pageErrors).toEqual([])
  })
})
