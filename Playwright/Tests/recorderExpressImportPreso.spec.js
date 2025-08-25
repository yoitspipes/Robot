require('dotenv').config({ path: '../.env' });
const { test, expect, chromium } = require('@playwright/test');
const { execFile } = require('child_process');
const path = require('path');
const recExpressRunner = require('../Resources/recExpressRunner');

function runPythonImport(presoName) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.resolve(__dirname, '../Resources/desktop_windows.py');

    execFile('python', [scriptPath, presoName], (error, stdout, stderr) => {
      console.log(stdout);
      if (error) {
        console.error(`❌ Python script failed: ${stderr}`);
        return reject(error);
      }
      resolve(stdout);
    });
  });
}

let browser;
let context;
let page;

test.beforeAll(async () => {
  browser = await chromium.launch({
    channel: 'chrome',
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

test('Navigate To Presentations Tab', async () => {
  recExpressRunner.navPresoTab(page);
  await page.waitForTimeout(1000);
});

test('Click Import Presentation Button', async () => {
  await page.locator('#btnReaddPresentation').click();
  //await recExpressRunner.importPresoXml(page, null, 'input[type="file"]', 'C:/Users/mediasite/Documents/Recorded Presentations/import_this/RecordedPresentation_70.xml');
});

test('Simulate User Input With Windows Dialog', async ({ page }) => {
  try {
    await runPythonImport('import_this');
  } catch (err) {
    console.error('❌ import_preso failed during test:', err.message);
    throw err;
  }
  await page.waitForTimeout(1000);
});

test('Verify Imported Presentation Appears In List With Correct Status', async () => {
  await page.locator('.presentation-item-status').getByText('Imported');
});

//test('')

test('Log Out of Recorder', async () => {
  await recExpressRunner.logoutRecorder(page);
});