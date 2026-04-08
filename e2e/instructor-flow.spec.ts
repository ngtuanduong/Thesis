import { test, expect } from '@playwright/test';
import { loginAsInstructor } from './helpers';

// ============================================================
// Instructor Flow — E2E Tests
// ============================================================

test.describe('Instructor Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsInstructor(page);
  });

  test('should show instructor menu items in sidebar', async ({ page }) => {
    await expect(page.getByRole('menuitem', { name: /instructor/i })).toBeVisible();
  });

  test('should navigate to instructor dashboard', async ({ page }) => {
    await page.goto('/instructor');
    await expect(page.getByText('Instructor Dashboard')).toBeVisible();
  });

  test('should display course selector and stats', async ({ page }) => {
    await page.goto('/instructor');
    await expect(page.locator('.ant-select')).toBeVisible({ timeout: 10_000 });
  });
});

test.describe('Problem Management', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsInstructor(page);
  });

  test('should navigate to problem management page', async ({ page }) => {
    await page.goto('/instructor/problems');
    await expect(page.getByText('Problem Management')).toBeVisible();
  });

  test('should display problems table with actions', async ({ page }) => {
    await page.goto('/instructor/problems');
    await expect(page.locator('.ant-table').first()).toBeVisible({ timeout: 10_000 });
  });

  test('should open create problem modal', async ({ page }) => {
    await page.goto('/instructor/problems');
    await page.getByRole('button', { name: /create problem/i }).click();
    const modal = page.locator('.ant-modal');
    await expect(modal).toBeVisible();
  });
});
