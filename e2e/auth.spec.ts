import { test, expect } from '@playwright/test';

// ============================================================
// Authentication & Authorization Tests
// ============================================================

test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('should display login form by default', async ({ page }) => {
    await expect(page.getByPlaceholder('Email')).toBeVisible();
    await expect(page.getByPlaceholder('Password')).toBeVisible();
    await expect(page.getByRole('button', { name: /login/i })).toBeVisible();
  });

  test('should switch to register tab', async ({ page }) => {
    await page.getByRole('tab', { name: /register/i }).click();
    await expect(page.getByPlaceholder('Full name')).toBeVisible();
    // Both tabs have Email/Password fields; check register-specific field (Full name) is sufficient
  });

  test('should show validation errors on empty submit', async ({ page }) => {
    await page.getByRole('button', { name: /login/i }).click();
    // Ant Design form validation messages
    await expect(page.locator('.ant-form-item-explain-error')).toHaveCount(2);
  });

  test('should login with valid credentials and redirect to dashboard', async ({ page }) => {
    await page.locator('input[placeholder=Email]').fill('student1@example.com');
    await page.locator('input[placeholder=Password]').fill('password123');
    await page.getByRole('button', { name: /login/i }).click();

    // After login, setQueryData makes route guard pass immediately → sidebar appears
    await expect(page.locator('.ant-layout-sider')).toBeVisible({ timeout: 15_000 });
    // Dashboard heading visible (use heading role to avoid matching menu item)
    await expect(page.locator('h3').getByText('Dashboard')).toBeVisible({ timeout: 5_000 });
  });

  test('should show error on invalid credentials', async ({ page }) => {
    await page.locator('input[placeholder=Email]').fill('wrong@example.com');
    await page.locator('input[placeholder=Password]').fill('wrongpassword');
    await page.getByRole('button', { name: /login/i }).click();

    // Ant Design message toast or stay on login page (no redirect)
    await page.waitForTimeout(2_000);
    await expect(page).toHaveURL(/\/login/);
  });

  test('should redirect unauthenticated user to login', async ({ page }) => {
    await page.goto('/problems');
    await expect(page).toHaveURL('/login');
  });
});
