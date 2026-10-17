import { test, expect } from '@playwright/test'

test.describe('sign-in page', () => {
  test('renders the sign-in form with email and password fields', async ({ page }) => {
    await page.goto('/auth/login')

    await expect(page.getByRole('heading', { name: 'VidiNews' })).toBeVisible()
    await expect(page.getByPlaceholder('your@email.com')).toBeVisible()
    await expect(page.getByPlaceholder('••••••••')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Sign in' })).toBeVisible()
  })

  test('the email field only accepts email addresses', async ({ page }) => {
    await page.goto('/auth/login')

    const email = page.getByPlaceholder('your@email.com')
    await expect(email).toHaveAttribute('type', 'email')
  })
})
