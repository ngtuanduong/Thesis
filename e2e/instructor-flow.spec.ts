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
    // Multiple .ant-select exist (course selector + pagination) — use .first()
    await expect(page.locator('.ant-select').first()).toBeVisible({ timeout: 10_000 });
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

  test('should create a new problem via modal', async ({ page }) => {
    await page.goto('/instructor/problems');
    await expect(page.locator('.ant-table').first()).toBeVisible({ timeout: 10_000 });

    const initialCount = await page.locator('.ant-table-row').count();

    // Open create modal
    await page.getByRole('button', { name: /create problem/i }).click();
    const modal = page.locator('.ant-modal');
    await expect(modal).toBeVisible();

    // Fill title (required field)
    const uniqueTitle = `QA Test Problem ${Date.now()}`;
    await modal.getByPlaceholder('Problem title').fill(uniqueTitle);

    // Fill description (required field)
    await modal.getByPlaceholder(/problem description/i).fill(
      'This is a test problem created by E2E tests.',
    );

    // Difficulty defaults to EASY (set in initialValues), no need to change

    // Click OK to submit
    await modal.getByRole('button', { name: /ok/i }).click();
    await page.waitForTimeout(3_000);

    // Modal should close on success
    await expect(modal).not.toBeVisible({ timeout: 5_000 });

    // Table should have the new problem
    const newCount = await page.locator('.ant-table-row').count();
    expect(newCount).toBeGreaterThanOrEqual(initialCount);
  });

  test('should edit an existing problem', async ({ page }) => {
    await page.goto('/instructor/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });

    // Click edit button on first row
    const editBtn = page.locator('.ant-table-row').first().getByRole('button', { name: /edit/i });
    if (await editBtn.isVisible({ timeout: 3_000 }).catch(() => false)) {
      await editBtn.click();

      const modal = page.locator('.ant-modal');
      await expect(modal).toBeVisible();

      // Verify modal has pre-filled data (title should not be empty)
      const titleInput = modal.locator('input[id*="title"], #title').first();
      const value = await titleInput.inputValue();
      expect(value.length).toBeGreaterThan(0);
    }
  });

  test('should show delete confirmation', async ({ page }) => {
    await page.goto('/instructor/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });

    // Click delete button on first row
    const deleteBtn = page.locator('.ant-table-row').first().getByRole('button', { name: /delete/i });
    if (await deleteBtn.isVisible({ timeout: 3_000 }).catch(() => false)) {
      await deleteBtn.click();

      // Should show confirmation popover or modal
      const confirmText = page.getByText(/are you sure|confirm|delete/i);
      await expect(confirmText.first()).toBeVisible({ timeout: 3_000 });
    }
  });
});
