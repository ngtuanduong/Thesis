import { test, expect } from '@playwright/test';
import { loginAsStudent, loginAsInstructor } from './helpers';

// ============================================================
// Security & Access Control — E2E Tests
//
// Note: The app protects routes at the API level (backend returns
// 401/403), not at the client routing level. Students CAN navigate
// to /admin but the page shows empty data because the API rejects
// unauthorized requests. The sidebar menu items are hidden by role.
// ============================================================

test.describe('Route Protection — Menu Visibility', () => {
  test('student should NOT see admin or instructor menu items', async ({ page }) => {
    await loginAsStudent(page);
    // Admin menu should be hidden for students
    await expect(page.getByRole('menuitem', { name: /^admin$/i })).not.toBeVisible();
    // Instructor menu should be hidden for students
    await expect(page.getByRole('menuitem', { name: /instructor/i })).not.toBeVisible();
  });

  test('instructor should see instructor menu but NOT admin', async ({ page }) => {
    await loginAsInstructor(page);
    await expect(page.getByRole('menuitem', { name: /instructor/i })).toBeVisible();
    await expect(page.getByRole('menuitem', { name: /^admin$/i })).not.toBeVisible();
  });
});

test.describe('API-Level Protection', () => {
  test('unauthenticated API call should return 401', async ({ page }) => {
    const response = await page.request.get('http://localhost:3000/api/problems', {
      headers: { Authorization: '' },
    });
    expect(response.status()).toBe(401);
  });

  test('student API call to admin endpoint should be rejected', async ({ page }) => {
    // Login as student and get token
    const loginRes = await page.request.post('http://localhost:3000/api/auth/login', {
      data: { email: 'student1@example.com', password: 'password123' },
    });
    const { token } = await loginRes.json();

    // Try to access admin-only endpoint with student token
    const adminRes = await page.request.get('http://localhost:3000/api/admin/stats', {
      headers: { Authorization: `Bearer ${token}` },
    });
    // Should be 403 Forbidden (role-based protection)
    expect(adminRes.status()).toBe(403);
  });

  test('malformed token should cause redirect to /login', async ({ page }) => {
    await page.addInitScript(() => {
      window.localStorage.setItem('token', 'invalid-garbage-token-12345');
    });

    await page.goto('/');
    await page.waitForTimeout(3_000);

    await expect(page).toHaveURL(/\/login/);
  });

  test('empty token should redirect to login', async ({ page }) => {
    await page.addInitScript(() => {
      window.localStorage.setItem('token', '');
    });

    await page.goto('/problems');
    await expect(page).toHaveURL(/\/login/);
  });
});
