import { test, expect } from '@playwright/test';
import { loginAsStudent } from './helpers';

// ============================================================
// Error Handling & Graceful Degradation — E2E Tests
// ============================================================

test.describe('Error Handling', () => {
  test('should handle API 500 error gracefully (no white screen)', async ({ page }) => {
    await loginAsStudent(page);

    // Intercept problems API and return 500
    await page.route('**/api/problems', (route) =>
      route.fulfill({
        status: 500,
        body: JSON.stringify({ message: 'Internal Server Error' }),
      }),
    );

    await page.goto('/problems');
    await page.waitForTimeout(2_000);

    // Page should not be blank — should show some content (error message or layout)
    const bodyText = await page.textContent('body');
    expect(bodyText).toBeTruthy();
    expect(bodyText!.length).toBeGreaterThan(10);
  });

  test('should handle network timeout gracefully', async ({ page }) => {
    await loginAsStudent(page);

    // Abort API requests to simulate network failure
    await page.route('**/api/adaptive/**', (route) => route.abort('timedout'));

    await page.goto('/');
    await page.waitForTimeout(3_000);

    // Dashboard layout should still be visible even if some API calls fail
    await expect(page.locator('.ant-layout-sider')).toBeVisible();
  });

  test('should not show white screen on page reload', async ({ page }) => {
    await loginAsStudent(page);

    // Navigate to a page and reload
    await page.goto('/problems');
    await expect(page.locator('.ant-layout-sider')).toBeVisible({ timeout: 10_000 });

    await page.reload();
    await page.waitForTimeout(2_000);

    // Should either show content or redirect to login (not blank)
    const bodyText = await page.textContent('body');
    expect(bodyText!.length).toBeGreaterThan(10);
  });
});
