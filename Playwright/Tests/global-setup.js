// global-setup.js
require('dotenv').config();
const { chromium } = require('@playwright/test');

module.exports = async () => {
  const browser = await chromium.launch({
    headless: false,
    args: [
      '--ignore-certificate-errors',
      '--allow-running-insecure-content',
      '--start-maximized',
      '--disable-web-security'
    ]
  });
  const context = await browser.newContext();
  const page = await context.newPage();

  const username = process.env.RECORDER_USER;
  const password = process.env.RECORDER_PASS;

  await page.goto(process.env.RECORDER_URL);
  await page.fill('#txtLogin', username);
  await page.fill('#txtPassword', password);
  await page.click('#btnLogin');
  await page.waitForSelector('#btnInputSelect'); // ensures login succeeded

  // Save authenticated state
  await context.storageState({ path: 'auth/storageState.json' });

  await browser.close();
};