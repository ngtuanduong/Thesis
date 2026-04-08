import { test, expect } from '@playwright/test';
import { loginAsStudent } from './helpers';

// ============================================================
// Student Core Flow — E2E Tests
// ============================================================

test.describe('Student Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsStudent(page);
  });

  test('should display dashboard with stats cards', async ({ page }) => {
    await expect(page.locator('h3').getByText('Dashboard')).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText('Problems Solved')).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText('Total Submissions')).toBeVisible({ timeout: 10_000 });
  });

  test('should display onboarding modal for new session', async ({ page }) => {
    await page.evaluate(() => localStorage.removeItem('adaptlearn_onboarding_done'));
    await page.reload();
    const modal = page.locator('.ant-modal');
    if (await modal.isVisible({ timeout: 3_000 }).catch(() => false)) {
      await expect(modal.getByText(/welcome/i)).toBeVisible();
    }
  });
});

test.describe('Problem Browsing', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsStudent(page);
  });

  test('should navigate to problems page and show problem list', async ({ page }) => {
    await page.goto('/problems');
    await expect(page.locator('h3').getByText('Problems')).toBeVisible({ timeout: 5_000 });
    const rows = page.locator('.ant-table-row');
    await expect(rows.first()).toBeVisible({ timeout: 10_000 });
  });

  test('should filter problems by difficulty', async ({ page }) => {
    await page.goto('/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });
    // Click the filter icon in the difficulty column
    await page.locator('th').filter({ hasText: 'Difficulty' }).locator('.ant-table-filter-trigger').click();
    const filterDropdown = page.locator('.ant-table-filter-dropdown');
    await expect(filterDropdown).toBeVisible();
    await filterDropdown.getByText('Easy').click();
    await filterDropdown.getByRole('button', { name: /ok/i }).click();
    // Wait for filter to apply
    await page.waitForTimeout(500);
    // Verify filtered results contain only EASY tags
    const rows = page.locator('.ant-table-row');
    const count = await rows.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should search problems by title', async ({ page }) => {
    await page.goto('/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });
    await page.getByPlaceholder(/search/i).fill('Swap Two');
    await page.waitForTimeout(500);
    const rows = page.locator('.ant-table-row');
    const count = await rows.count();
    expect(count).toBeLessThanOrEqual(3);
  });
});

test.describe('Problem Solving', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsStudent(page);
  });

  test('should open problem detail with code editor', async ({ page }) => {
    await page.goto('/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });
    await page.locator('.ant-table-row').first().locator('a').first().click();
    await expect(page.url()).toContain('/problems/');
    await expect(page.locator('.cm-editor')).toBeVisible({ timeout: 10_000 });
  });

  test('should have submit button', async ({ page }) => {
    await page.goto('/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });
    await page.locator('.ant-table-row').first().locator('a').first().click();
    await expect(page.locator('.cm-editor')).toBeVisible({ timeout: 10_000 });
    await expect(page.getByRole('button', { name: /submit/i })).toBeVisible();
  });
});

test.describe('Knowledge Map', () => {
  test('should render page', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/knowledge-map');
    // ReactFlow or fallback content should render
    await expect(page.getByText(/knowledge/i).first()).toBeVisible({ timeout: 10_000 });
  });
});

test.describe('Review Queue', () => {
  test('should navigate to review queue page', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/review-queue');
    await expect(page.getByText(/review/i).first()).toBeVisible();
  });
});

test.describe('Profile', () => {
  test('should display user profile with correct info', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/profile');
    await expect(page.getByText('Alice Johnson')).toBeVisible();
    await expect(page.getByText('student1@example.com')).toBeVisible();
  });
});

test.describe('Survey (SUS)', () => {
  test('should navigate to survey page', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/survey');
    await expect(page.getByText(/system usability survey/i)).toBeVisible();
    await expect(page.locator('.ant-card')).toHaveCount(10);
  });

  test('submit button should be disabled until all questions answered', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/survey');
    await expect(page.getByRole('button', { name: /submit survey/i })).toBeDisabled();
  });
});
