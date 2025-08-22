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
    await recExpressRunner.navSettingsTab(page);
    await page.waitForTimeout(1000);
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

test('Click on Mediasite Connections', async () => {
  //iterate through all elements with same class_name and find specific text?
  //await page.locator('.left-sub-link', { hasText: 'Mediasite Connections' }).click();

  //Or does this work
  await page.locator('text=Mediasite Connections').click();
});

test('Click Add New Connection', async () => {
  //Not sure why it fails to find/interact by elementId
  //await page.locator('#btnAddConnection').click();
  await page.locator('text=Add A New Connection').click();
});

test('Input Connection Name', async () => {
  await page.locator('#txtConnectionName').fill('Preview');
});

test('Input Service Root URL', async () => {
  const servRootUrl = process.env.PREV_URL;
  await page.locator('#txtServiceRootURL').fill(servRootUrl);
});

test('Input Username and Password', async () => {
  const username = process.env.PREV_USER;
  const password = process.env.PREV_PASS;

  await page.locator('#modalForm #txtUsername').fill(username);
  await page.locator('#modalForm #txtPassword').fill(password);
});

test('Click Test Connection and Verify Success', async () => {
  await page.locator('#btnTestConnection').click();
  await expect(page.locator('#modalForm #lblTestMessage')).toHaveText("Test Successful");
});

test('Click Add Button To Save The MVP Connection', async () => {
  await page.locator('#modalForm #btnAdd').click();
});

test('Click on Scheduler Connections', async () => {
  await page.locator('text=Scheduler Connections').click();
  await page.waitForTimeout(1000);
});

test('Enable Scheduler', async () => {
  //await page.locator('.icheckbox_square').click();
  //await page.locator('.iCheck-helper').click();
  await page.locator('.icheckbox_square').first().click();
  //await page.locator('text=Enable Scheduler').click();
});

test('Click Add New (Scheduler) Connection', async () => {
  await page.locator('text=Add A New Connection').click();
});

test('Input Scheduler Connection Name', async () => {
  await page.locator('#txtConnectionName').fill('Preview');
});

test('Input Scheduler Service Root URL', async () => {
  const servRootUrl = process.env.PREV_URL;
  await page.locator('#txtServiceRootURL').fill(servRootUrl);
});

test('Input Scheduler Username and Password', async () => {
  const username = process.env.PREV_USER;
  const password = process.env.PREV_PASS;

  await page.locator('#modalForm #txtUsername').fill(username);
  await page.locator('#modalForm #txtPassword').fill(password);
});

test('Click Test Connection and Verify Success For Scheduler Connection', async () => {
  await page.locator('#btnTestConnection').click();
  await expect(page.locator('#modalForm #lblTestMessage')).toHaveText("Test Successful");
});

test('Click Add Button To Save The MVP Scheduler Connection', async () => {
  await page.locator('#modalForm #btnAdd').click();
  await page.waitForTimeout(1000);
});

test('Navigate To Scheduler Tab And Perform Sync', async  () => {
  await recExpressRunner.navSchedTab(page);
  await page.locator('#btnSync').click();
});

test('Verify Schedule Sync Is Successful And Not Disconnected', async () => {
  await expect(page.locator('#lblLastSync')).not.toHaveText('DISCONNECTED');
});

test('Navigate To Capture Tab', async () => {
  await recExpressRunner.navCaptureTab(page);
});

test('Open Inputs', async () => {
  await page.locator('#btnInputSelect').click();
});

test('Collapse All Input Chevrons', async () => {
  await recExpressRunner.collapseInputChevrons(page);
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

test('Collapse The Input Chevrons', async () => {
  await recExpressRunner.collapseInputChevrons(page);
});

test('Expand Desktop Capture Sources Again', async () => {
  await page.locator('text=Desktop Capture Sources').click();
});

test('Route Display 1 to Video 1', async () => {
  await page.locator('text=Desktop Capture 1').click();
  await expect(page.locator('#sourceRoutingTitle')).toHaveText('Outputs');
  await page.locator('#btnRouteVideo1').click();
});

test('Collapse Input Chevrons', async () => {
  await recExpressRunner.collapseInputChevrons(page);
});

test('Expand Test Sources Again', async () => {
  await page.locator('text=Test Sources').click();
});

test('Route Gray Bars Counter To Slide Input', async () => {
  await page.locator('#input-source-type-list').getByText('Gray Bars and Counter').click();
  await expect(page.locator('#sourceRoutingTitle')).toHaveText('Outputs');
  await page.locator('#btnRouteSlide').click();
});

test('Log Out of Recorder', async () => {
  await recExpressRunner.logoutRecorder(page);
});