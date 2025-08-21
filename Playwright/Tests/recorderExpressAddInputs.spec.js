require('dotenv').config({ path: '../.env' });
const { test, expect, chromium } = require('@playwright/test');
const path = require('path');
const recExpressRunner = require('../Resources/recExpressRunner');

let browser;
let context;
let page;

test.beforeAll(async () => {
  browser = await chromium.launch({
    channel: 'msedge',
    headless: false,
    args: [
      '--ignore-certificate-errors',
      '--allow-running-insecure-content',
      //'--start-maximized',
      '--disable-web-security'
    ]
  });
  context = await browser.newContext();
  page = await context.newPage();
  // If launch/login fails, use tis try/catch to abort all tests
  try {
    await page.goto(process.env.RECEXPRESS_URL);
    await page.waitForTimeout(1000);
    await recExpressRunner.navSettingsTab(page);
    await page.waitForTimeout(2000);
    await recExpressRunner.loginRecorder(page);
    //Should see "Inputs" button upon successful Login
    //await expect(page.locator('#btnInputSelect')).toBeVisible({ timeout: 5000 });
  } catch (err) {
    console.errors('Launch failed. Aborting all tests.');
    throw new Error('Launch failed. Aborting tests.');
  }
});

test.afterAll(async () => {
  await browser.close();
});

test('Verify Admin Is Logged In', async () => {
  //Should see "admin" in top-right of window upon successful Login
  await expect(page.locator('#lblUsername')).toHaveText("Admin");
});

test('Navigate To Capture Tab', async () => {
  await recExpressRunner.navCaptureTab(page);
});

test('Open Inputs', async () => {
  await page.locator('#btnInputSelect').click();
});

test('Collapse File Sources', async () => {
  await page.locator('text=File Sources').click();
});

test('Expand Desktop Capture Sources', async () => {
  await page.locator('text=Desktop Capture Sources').click();
});

test('Click "+" Icon To Add A New Display Source ', async () => {
  //TODO - this could be refined better
  await page.getByRole('button', { name: '+' }).click();
});

test('Choose Display 1 And Click Add Source', async () => {
  await page.locator('text=Desktop Capture 1').click();
  await page.locator('#addLocalSource').click();
});

test('Collapse Desktop Capture Sources', async () => {
  await page.locator('text=Desktop Capture Sources').click();
});

test('Expand Test Sources', async () => {
  await page.locator('text=Test Sources').click();
});

test('Click "+" Icon And Add All Test Sources', async () => {
  await page.getByRole('button', { name: '+' }).click();
  await page.locator('text=Black Video').click();
  await page.locator('text=Gray Bars and Counter').click();
  await page.locator('text=Silence').click();
  await page.locator('text=1 kHz Tone').click();
  await page.locator('#addLocalSource').click();
});