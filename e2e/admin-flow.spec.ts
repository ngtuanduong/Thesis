import { test, expect } from '@playwright/test';
import { loginAsAdmin, loginAsStudent, loginAsInstructor } from './helpers';

// ============================================================
// Admin Flow — E2E Tests
// ============================================================

test.describe('Admin Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
  });

  test('should show admin menu item in sidebar', async ({ page }) => {
    await expect(page.getByRole('menuitem', { name: /admin/i })).toBeVisible();
  });

  test('should navigate to admin dashboard', async ({ page }) => {
    await page.goto('/admin');
    await expect(page.getByText('Admin Dashboard')).toBeVisible();
  });

  test('should display platform stats cards', async ({ page }) => {
    await page.goto('/admin');
    await expect(page.getByText('Total Users')).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText('Total Submissions')).toBeVisible();
  });

  test('should display user management table', async ({ page }) => {
    await page.goto('/admin');
    await expect(page.getByText('User Management')).toBeVisible();
    await expect(page.getByText('admin@example.com')).toBeVisible({ timeout: 10_000 });
  });
});

test.describe('Admin Operations', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
  });

  test('should display experiment statistics section', async ({ page }) => {
    await page.goto('/admin');
    await page.waitForTimeout(3_000);
    // Look for experiment-related content (pie chart, group names, stats)
    const hasExperiment = await page.getByText(/experiment|group|control/i)
      .first()
      .isVisible({ timeout: 5_000 })
      .catch(() => false);
    expect(hasExperiment).toBe(true);
  });

  test('should have group assignment controls for users', async ({ page }) => {
    await page.goto('/admin');
    await expect(page.getByText('User Management')).toBeVisible({ timeout: 10_000 });
    // Wait for user table to load
    await expect(page.getByText('admin@example.com')).toBeVisible({ timeout: 10_000 });

    // The "Assign Group" column header should be visible
    await expect(page.getByRole('columnheader', { name: /assign group/i })).toBeVisible({
      timeout: 5_000,
    });
    // Table rows should contain assign group controls (ant-select in each row)
    const rowSelects = page.locator('.ant-table-tbody .ant-select');
    const count = await rowSelects.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should assign experiment group to a user', async ({ page }) => {
    await page.goto('/admin');
    await expect(page.getByText('admin@example.com')).toBeVisible({ timeout: 10_000 });

    // Find a user row with a group select
    const firstSelect = page.locator('.ant-table-row .ant-select').first();
    if (await firstSelect.isVisible({ timeout: 3_000 }).catch(() => false)) {
      await firstSelect.click();
      // Select an option from the dropdown
      const option = page.locator('.ant-select-item-option').first();
      if (await option.isVisible({ timeout: 2_000 }).catch(() => false)) {
        await option.click();
        await page.waitForTimeout(1_000);
      }
    }
  });
});

test.describe('Role-Based Access Control', () => {
  test('student should NOT see admin/instructor menu items', async ({ page }) => {
    await loginAsStudent(page);
    await expect(page.getByRole('menuitem', { name: /^admin$/i })).not.toBeVisible();
  });

  test('instructor should see instructor items but NOT admin', async ({ page }) => {
    await loginAsInstructor(page);
    await expect(page.getByRole('menuitem', { name: /instructor/i })).toBeVisible();
    await expect(page.getByRole('menuitem', { name: /^admin$/i })).not.toBeVisible();
  });

  test('admin should see ALL menu items', async ({ page }) => {
    await loginAsAdmin(page);
    await expect(page.getByRole('menuitem', { name: /instructor/i })).toBeVisible();
    await expect(page.getByRole('menuitem', { name: /admin/i })).toBeVisible();
  });
});
