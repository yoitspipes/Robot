const { test, expect } = require('@playwright/test');

test('Check Playwright setup', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example Domain/);
});