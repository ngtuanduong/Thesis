import { type Page, expect } from '@playwright/test';

const API_BASE = 'http://localhost:3000/api';

/**
 * Login via API and inject token into localStorage.
 * Bypasses UI login form for reliability in E2E tests.
 */
export async function loginViaApi(page: Page, email: string, password: string) {
  // Call login API directly
  const response = await page.request.post(`${API_BASE}/auth/login`, {
    data: { email, password },
  });
  const data = await response.json();

  if (!data.token) {
    throw new Error(`Login failed for ${email}: ${JSON.stringify(data)}`);
  }

  // Set token in localStorage before navigating
  await page.addInitScript((token: string) => {
    window.localStorage.setItem('token', token);
  }, data.token);

  // Navigate to dashboard and wait for layout to render
  await page.goto('/');
  await expect(page.locator('.ant-layout-sider')).toBeVisible({ timeout: 15_000 });
}

export async function loginAsStudent(page: Page) {
  await loginViaApi(page, 'student1@example.com', 'password123');
}

export async function loginAsInstructor(page: Page) {
  await loginViaApi(page, 'instructor@example.com', 'password123');
}

export async function loginAsAdmin(page: Page) {
  await loginViaApi(page, 'admin@example.com', 'password123');
}
