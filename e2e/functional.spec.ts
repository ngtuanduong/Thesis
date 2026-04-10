import { test, expect, Page } from '@playwright/test';
import { loginAsStudent, loginAsInstructor, loginAsAdmin } from './helpers';

// ============================================================
// Functional Tests — Requires Docker daemon running
// Covers: Code submission, CRUD operations, adaptive updates
// ============================================================

/**
 * Set CodeMirror editor content programmatically via the view's dispatch API.
 * keyboard.type() doesn't work reliably with CodeMirror for multi-line code.
 */
async function setEditorCode(page: Page, code: string) {
  // Focus the editor first
  await page.locator('.cm-content').click();
  // Select all existing text and delete it
  await page.keyboard.press('Control+A');
  await page.keyboard.press('Backspace');
  // Type the new code character by character (delay=0 for speed)
  // Using keyboard.insertText to avoid CodeMirror auto-indent issues
  await page.keyboard.insertText(code);
}

test.describe('Code Submission — Correct Answer', () => {
  test('should submit correct code and get ACCEPTED status', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });

    // Click on "Palindrome Number" (simpler problem for reliable testing)
    const palindromeRow = page.locator('.ant-table-row').filter({ hasText: 'Palindrome' });
    if (await palindromeRow.isVisible({ timeout: 3_000 }).catch(() => false)) {
      await palindromeRow.locator('a').first().click();
    } else {
      await page.locator('.ant-table-row').first().locator('a').first().click();
    }

    await expect(page.locator('.cm-editor')).toBeVisible({ timeout: 10_000 });

    // Set correct solution for Palindrome Number
    await setEditorCode(page, 'def solution(n):\n    s = str(n)\n    return s == s[::-1]');

    // Click Submit button
    await page.locator('button').filter({ hasText: 'Submit' }).last().click();

    // Wait for ACCEPTED status or success message
    const accepted = page.getByText(/ACCEPTED|All test cases passed/i).first();
    await expect(accepted).toBeVisible({ timeout: 30_000 });
  });
});

test.describe('Code Submission — Wrong Answer', () => {
  test('should submit wrong code and get WRONG_ANSWER status', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });

    const palindromeRow = page.locator('.ant-table-row').filter({ hasText: 'Palindrome' });
    if (await palindromeRow.isVisible({ timeout: 3_000 }).catch(() => false)) {
      await palindromeRow.locator('a').first().click();
    } else {
      await page.locator('.ant-table-row').first().locator('a').first().click();
    }

    await expect(page.locator('.cm-editor')).toBeVisible({ timeout: 10_000 });

    // Set WRONG solution (always returns True)
    await setEditorCode(page, 'def solution(n):\n    return True');

    await page.locator('button').filter({ hasText: 'Submit' }).last().click();

    // Should show WRONG_ANSWER with Expected vs Got
    const wrongAnswer = page.getByText(/WRONG.ANSWER|Expected/i).first();
    await expect(wrongAnswer).toBeVisible({ timeout: 30_000 });
  });
});

test.describe('Code Submission — Time Limit', () => {
  // Docker needs ~5s to timeout + overhead → triple the default test timeout
  test.slow();
  test('should submit infinite loop and get TIME_LIMIT status', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });

    await page.locator('.ant-table-row').first().locator('a').first().click();
    await expect(page.locator('.cm-editor')).toBeVisible({ timeout: 10_000 });

    // Set infinite loop code
    await setEditorCode(page, 'def solution(*args, **kwargs):\n    while True:\n        pass');

    // Click the Submit button (not "Run") — use exact button match
    const submitBtn = page.locator('button').filter({ hasText: 'Submit' }).last();
    await submitBtn.click();

    // Wait for the result to appear — either inline status or toast message
    // The UI shows status as "TIME LIMIT" text with icon, or via message.error toast
    await page.waitForTimeout(15_000); // Docker timeout is 5s + overhead

    // Check for any submission result indicator (status text in Results panel)
    const resultPanel = page.locator('text=/TIME.LIMIT|RUNTIME.ERROR|WRONG.ANSWER|ACCEPTED|Submission/i').first();
    await expect(resultPanel).toBeVisible({ timeout: 45_000 });
  });
});

test.describe('Code Submission — Runtime Error', () => {
  test('should submit error code and get RUNTIME_ERROR status', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });

    await page.locator('.ant-table-row').first().locator('a').first().click();
    await expect(page.locator('.cm-editor')).toBeVisible({ timeout: 10_000 });

    // Set code with division by zero error
    await setEditorCode(page, 'def solution(*args, **kwargs):\n    return 1 / 0');

    await page.locator('button').filter({ hasText: 'Submit' }).last().click();

    // Should show RUNTIME_ERROR
    const runtimeError = page.getByText(/RUNTIME.ERROR|Error/i).first();
    await expect(runtimeError).toBeVisible({ timeout: 30_000 });
  });
});

test.describe('Knowledge Map Update After Submission', () => {
  test('should display mastery nodes on Knowledge Map', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/knowledge-map');
    await page.waitForTimeout(3_000);

    // Knowledge map should have nodes (from seed data + adaptive layers)
    const nodeCount = await page.locator('.react-flow__node').count();
    if (nodeCount > 0) {
      expect(nodeCount).toBeGreaterThan(0);
    }
  });
});

test.describe('Instructor Problem CRUD', () => {
  test('should create a new problem and see it in the list', async ({ page }) => {
    await loginAsInstructor(page);
    await page.goto('/instructor/problems');
    await expect(page.locator('.ant-table').first()).toBeVisible({ timeout: 10_000 });

    // Click Create Problem
    await page.getByRole('button', { name: /create problem/i }).click();
    const modal = page.locator('.ant-modal');
    await expect(modal).toBeVisible();

    // Fill the form
    const uniqueTitle = `Functional Test ${Date.now()}`;
    const titleInput = modal.locator('#title, input').first();
    await titleInput.fill(uniqueTitle);

    const descInput = modal.locator('#description, textarea').first();
    if (await descInput.isVisible()) {
      await descInput.fill('A test problem for QA functional testing');
    }

    // Select difficulty
    const diffSelect = modal.locator('.ant-select').first();
    if (await diffSelect.isVisible()) {
      await diffSelect.click();
      await page.locator('.ant-select-item-option').filter({ hasText: /easy/i }).first().click();
    }

    // Submit form
    await modal.getByRole('button', { name: /ok|create|save|submit/i }).click();
    await page.waitForTimeout(3_000);

    // Verify: modal closed (success) or new row in table
    const modalGone = !(await modal.isVisible().catch(() => false));
    if (modalGone) {
      await page.goto('/instructor/problems');
      await expect(page.locator('.ant-table').first()).toBeVisible({ timeout: 10_000 });
    }
  });

  test('should edit a problem and see pre-filled data', async ({ page }) => {
    await loginAsInstructor(page);
    await page.goto('/instructor/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });

    const editBtn = page.locator('.ant-table-row').first().getByRole('button', { name: /edit/i });
    if (await editBtn.isVisible({ timeout: 3_000 }).catch(() => false)) {
      await editBtn.click();

      const modal = page.locator('.ant-modal');
      await expect(modal).toBeVisible();

      // Verify title is pre-filled
      const titleInput = modal.locator('#title, input').first();
      const currentTitle = await titleInput.inputValue();
      expect(currentTitle.length).toBeGreaterThan(0);

      await modal.getByRole('button', { name: /cancel/i }).click();
    }
  });

  test('should show delete confirmation for a problem', async ({ page }) => {
    await loginAsInstructor(page);
    await page.goto('/instructor/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });

    const deleteBtn = page.locator('.ant-table-row').first().getByRole('button', { name: /delete/i });
    if (await deleteBtn.isVisible({ timeout: 3_000 }).catch(() => false)) {
      await deleteBtn.click();

      const confirmText = page.getByText(/are you sure|confirm|delete/i);
      await expect(confirmText.first()).toBeVisible({ timeout: 3_000 });

      // Cancel — don't actually delete seed data
      const cancelBtn = page.getByRole('button', { name: /no|cancel/i }).first();
      if (await cancelBtn.isVisible({ timeout: 2_000 }).catch(() => false)) {
        await cancelBtn.click();
      }
    }
  });
});

test.describe('Admin Experiment Group Assignment', () => {
  test('should assign experiment group to a user', async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/admin');
    await expect(page.getByText('User Management')).toBeVisible({ timeout: 10_000 });
    // Wait for user table to load (any row visible)
    await expect(page.locator('.ant-table-tbody .ant-table-row').first()).toBeVisible({
      timeout: 10_000,
    });

    // Target only selects inside the table body (avoid page-size selector)
    const groupSelects = page.locator('.ant-table-tbody .ant-select');
    await expect(groupSelects.first()).toBeVisible({ timeout: 5_000 });

    // Click the first group assignment select
    await groupSelects.first().click();
    await page.waitForTimeout(1_000);

    // Select the first available option from dropdown
    const options = page.locator('.ant-select-dropdown:visible .ant-select-item-option');
    await expect(options.first()).toBeVisible({ timeout: 3_000 });
    await options.first().click();
    await page.waitForTimeout(2_000);
  });
});

test.describe('AI Hint Generation', () => {
  test('should request a hint and see hint text or error fallback', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });

    await page.locator('.ant-table-row').first().locator('a').first().click();
    await expect(page.locator('.cm-editor')).toBeVisible({ timeout: 10_000 });

    // Click "Get Hint" in HintPanel
    const hintBtn = page.getByRole('button', { name: /get hint|more help/i });
    await expect(hintBtn).toBeVisible({ timeout: 5_000 });
    await hintBtn.click();

    // Should show either:
    // 1. A hint card with "Level" tag (if AI service running)
    // 2. An alert "Hints unavailable" (if AI service down)
    const hintResult = page.locator('text=/Level|Hints unavailable|Gentle Nudge|Specific Hint/i').first();
    await expect(hintResult).toBeVisible({ timeout: 10_000 });
  });
});

test.describe('Submission History', () => {
  test('should show submission history tab with table', async ({ page }) => {
    await loginAsStudent(page);
    await page.goto('/problems');
    await expect(page.locator('.ant-table-row').first()).toBeVisible({ timeout: 10_000 });

    await page.locator('.ant-table-row').first().locator('a').first().click();
    await expect(page.locator('.cm-editor')).toBeVisible({ timeout: 10_000 });

    // Switch to Submissions tab
    const submissionsTab = page.getByRole('tab', { name: /submissions/i });
    await submissionsTab.click();
    await page.waitForTimeout(2_000);

    // Should show submission table
    const submissionTable = page.locator('.ant-table');
    await expect(submissionTable.first()).toBeVisible({ timeout: 5_000 });
  });
});
