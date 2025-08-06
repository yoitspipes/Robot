require('dotenv').config();
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './Tests',
  timeout: 30000,
  use: {
    baseURL: process.env.RECORDER_URL,
    headless: false
  },
  reporter: [['html', { outputFolder: './playwright-report', open: 'always' }]],
  //globalSetup: './Tests/global-setup.js', // optional
});