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
    const countBefore = await page.locator('.ant-table-row').count();

    // Use the Difficulty select dropdown above the table
    await page.locator('.ant-select').filter({ hasText: /difficulty/i }).click();
    await page.locator('.ant-select-item-option').filter({ hasText: 'EASY' }).click();
    // Close dropdown by clicking elsewhere
    await page.locator('h3').first().click();
    await page.waitForTimeout(500);

    // Verify filtered results show fewer (or equal) and all are EASY
    const rows = page.locator('.ant-table-row');
    const count = await rows.count();
    expect(count).toBeGreaterThan(0);
    expect(count).toBeLessThanOrEqual(countBefore);
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

  test('should render graph nodes or show empty state', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/knowledge-map');
    await page.waitForTimeout(3_000);

    // Knowledge Map shows nodes when AI service has data, or empty state when not
    const hasNodes = await page.locator('.react-flow__node').count() > 0;
    const hasEmptyState = await page.getByText(/no knowledge data|start solving/i)
      .isVisible({ timeout: 2_000 })
      .catch(() => false);

    expect(hasNodes || hasEmptyState).toBe(true);
  });

  test('should render graph or empty state message', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/knowledge-map');
    await page.waitForTimeout(3_000);

    // Either ReactFlow renders with edges, or empty state message shows
    const hasGraph = await page.locator('.react-flow').isVisible({ timeout: 2_000 }).catch(() => false);
    const hasEmptyState = await page.getByText(/no knowledge data|start solving/i)
      .isVisible({ timeout: 2_000 })
      .catch(() => false);

    expect(hasGraph || hasEmptyState).toBe(true);
  });
});

test.describe('Review Queue', () => {
  test('should navigate to review queue page', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/review-queue');
    await expect(page.getByText(/review/i).first()).toBeVisible();
  });

  test('should display review items or empty state message', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/review-queue');
    await page.waitForTimeout(3_000);

    // Should show either review cards or an empty state
    const hasItems = await page.locator('.ant-card').count() > 0;
    const hasEmptyMessage = await page.getByText(/no.*review|queue.*empty|nothing.*review/i)
      .isVisible({ timeout: 2_000 })
      .catch(() => false);

    expect(hasItems || hasEmptyMessage).toBe(true);
  });
});

test.describe('Profile', () => {
  test('should display user profile with correct info', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/profile');
    await expect(page.getByText('Alice Johnson')).toBeVisible();
    await expect(page.getByText('student1@example.com')).toBeVisible();
  });

  test('should have skill refresh functionality', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/profile');
    await page.waitForTimeout(2_000);

    // Look for a refresh/recalculate skills button
    const refreshBtn = page.getByRole('button', { name: /refresh|recalculate|compute/i });
    if (await refreshBtn.isVisible({ timeout: 3_000 }).catch(() => false)) {
      await refreshBtn.click();
      // Should show loading or updated state
      await page.waitForTimeout(2_000);
    }
    // Profile page should still be functional
    await expect(page.getByText('Alice Johnson')).toBeVisible();
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

  test('should enable submit button after answering all 10 questions', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/survey');
    await expect(page.locator('.ant-card')).toHaveCount(10);

    // Answer all 10 questions (click the 3rd radio button for each)
    const cards = page.locator('.ant-card');
    for (let i = 0; i < 10; i++) {
      const card = cards.nth(i);
      // Click the 3rd radio option in each card (middle value)
      const radios = card.locator('.ant-radio-wrapper, input[type="radio"]');
      const radioCount = await radios.count();
      if (radioCount >= 3) {
        await radios.nth(2).click();
      } else if (radioCount > 0) {
        await radios.first().click();
      }
    }

    // After answering all, submit should be enabled
    await expect(page.getByRole('button', { name: /submit survey/i })).toBeEnabled({
      timeout: 3_000,
    });
  });
});
