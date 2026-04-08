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
