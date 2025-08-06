require('dotenv').config({ path: '../.env' });
const { test, expect, chromium } = require('@playwright/test');
const path = require('path');
const recRunner = require('../Resources/recRunner');

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
    await page.goto(process.env.RECORDER_URL);
    await recRunner.loginRecorder(page);
    //Should see "Inputs" button upon successful Login
    await expect(page.locator('#btnInputSelect')).toBeVisible({ timeout: 5000 });
  } catch (err) {
    console.errors('Login failed. Aborting all tests.');
    throw new Error('Login failed. Aborting tests.');
  }
});

test.afterAll(async () => {
  await browser.close();
});

test('Verify Admin Is Logged In', async () => {
  //Should see "Inputs" button upon successful Login
  await expect(page.locator('#lblUsername')).toHaveText("Admin");
});

test('Verify Recorder in Idle State', async () => {
  await expect(page.locator('.recorder-status')).toHaveText('Idle');
});

test('Change Presentation Title', async () => {
  await recRunner.renamePreso(page, 'Playwright Recorder Smoke Test');
});

test('Verify Update Presentation Title', async () => {
  await expect(page.locator('.recorder-title')).toHaveText('Playwright Recorder Smoke Test');
});

test('Start Recording For ~3 Seconds', async () => {
  await page.locator('#btnRecord').click();
  await page.waitForTimeout(3000);
});

test('Verify Recorder Is In Recording State', async () => {
  await expect(page.locator('.recorder-status')).toContainText('Recording');
});

test('Pause Recording for ~3 Seconds', async () => {
  await page.locator('#btnPause').click();
  await page.waitForTimeout(3000);
});

test('Verify Recorder in Paused State', async () => {
  await expect(page.locator('.recorder-status')).toContainText('Paused');
});

test('Resume Recording', async () => {
  await page.locator('#btnResume').click();
});

test('Verify Recorder is Back to Recording State', async () => {
  await expect(page.locator('.recorder-status', { timeout: 5000 })).toContainText('Recording');
  //Let it record for another 10 seconds
  await page.waitForTimeout(10000);
});

test('Stop Recording', async () => {
  await page.locator('#btnStop').click();
  //await page.waitForTimeout(10000);
});

test('Verify Recorder is Back to Idle State', async () => {
  // Note this state transition might take awhile, but fail if >15sec
  await expect(page.locator('.recorder-status', { timeout: 15000 })).toHaveText('Idle');
});

test('Navigate to Presentations Tab', async () => {
  await recRunner.navPresoTab(page);
});

//TODO: False pass, doesn't actually find/delete presentation
test('Delete the Recorded Presentation', async () => {
  await recRunner.deletePresentation(page, 'Playwright Recorder Smoke Test');
  await page.waitForTimeout(5000);
});

test('Log Out of Recorder', async () => {
  await recRunner.logoutRecorder(page);
});