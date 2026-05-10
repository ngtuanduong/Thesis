import { test, expect } from '@playwright/test';
import { loginAsStudent } from './helpers';

// ============================================================
// Performance — E2E Tests
// ============================================================

test.describe('Page Load Performance', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsStudent(page);
  });

  test('dashboard should load within 5 seconds', async ({ page }) => {
    const start = Date.now();
    await page.goto('/');
    await expect(page.locator('.ant-layout-sider')).toBeVisible({ timeout: 5_000 });
    const duration = Date.now() - start;

    expect(duration).toBeLessThan(5_000);
  });

  test('problems list should load within 5 seconds', async ({ page }) => {
    const start = Date.now();
    await page.goto('/problems');
    await expect(page.locator('.ant-table').first()).toBeVisible({ timeout: 5_000 });
    const duration = Date.now() - start;

    expect(duration).toBeLessThan(5_000);
  });

  test('problem detail with code editor should load within 8 seconds', async ({ page }) => {
    await page.goto('/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });
    await page.locator('.ant-table-row').first().locator('a').first().click();

    const start = Date.now();
    await expect(page.locator('.cm-editor')).toBeVisible({ timeout: 8_000 });
    const duration = Date.now() - start;

    expect(duration).toBeLessThan(8_000);
  });

  test('knowledge map should render within 8 seconds', async ({ page }) => {
    const start = Date.now();
    await page.goto('/knowledge-map');
    // Wait for either ReactFlow graph or empty state message
    await expect(
      page.getByText(/knowledge map|no knowledge data/i).first(),
    ).toBeVisible({ timeout: 8_000 });
    const duration = Date.now() - start;

    expect(duration).toBeLessThan(8_000);
  });
});
