require('dotenv').config({ path: '../.env' });
/**
 * Logs into the Recorder UI using default credentials.
 * @param {import('@playwright/test').Page} page - Playwright page object.
 */

const { expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

async function navSettingsTab(page) {
  const settTab = page.locator('.btn-settings');
  await settTab.click();
}
async function loginRecorder(page) {

  //Will need to trigger login modal to perform most tests
  //await navSettingsTab(page);

  //Apparently Recorder Express has two elementId's = txtLogin, tried below but failed:
  //const loginUser = page.locator('input#txtLogin[name="loginUsername"]',{ timeout: 5000 });

  //Attempt to target the second one for now..
  //const loginUser = page.locator('#txtLogin').nth(1);

  //Yikes, not like this (seemed to be the "active" element but wasn't)
  //const loginUser = page.locator('*:focus');

  //That was wild.
  const loginUser = page.getByLabel('Login');
  const loginPwd = page.getByRole('textbox', { name: 'Password', exact: true });
  const loginButton = page.getByRole('button', { name: 'Login' });
  const username = process.env.RECORDER_USER;
  const password = process.env.RECORDER_PASS;

  await loginUser.fill(username);
  await loginPwd.fill(password);
  await loginButton.click();
}

async function navPresoTab(page) {
  const presTab = page.locator('.btn-presentations');
  await presTab.click();
  await page.waitForTimeout(1000);
}

async function navCaptureTab(page) {
  const capTab = page.locator('.btn-recorder');
  await capTab.click();
}

async function navSchedTab(page) {
  const schedTab = page.locator('.btn-schedules');
  await schedTab.click();
}

async function openInputs(page) {
  const inputSel = page.locator('#btnInputSelect');
  await inputSel.click();
}

async function closeInputs(page) {
  const inputSel = page.locator('#btnInputSelect');
  await inputSel.click();
}

async function renamePreso(page, newTitle) {
  const penIcon = page.locator('.icon-pencil');
  await penIcon.click();

  const titleField = page.locator('#txtTitle');
  await titleField.fill('');
  await titleField.fill(newTitle);

  await page.waitForTimeout(1000);

  await page.locator('#btnOk').click();
}

async function importPreso(page, triggerSelector, inputSelector, folderPath) {
  try {
    if (triggerSelector) {
      await page.click(triggerSelector);
    }

    const fileInput = page.locator(inputSelector);
    await expect(fileInput).toHaveCount(1); // Ensure input exists

    if (!fs.existsSync(folderPath)) {
      throw new Error(`Folder not found: ${folderPath}`);
    }

    const files = fs.readdirSync(folderPath)
      .filter(file => fs.statSync(path.join(folderPath, file)).isFile())
      .map(file => path.join(folderPath, file));

    if (files.length === 0) {
      throw new Error(`No files found in folder: ${folderPath}`);
    }

    await fileInput.setInputFiles(files);
    await page.waitForTimeout(1000);
  } catch (err) {
    console.error(`❌ importPreso failed for folder: ${folderPath}`);
    console.error(`Error: ${err.message}`);
    throw err; // Re-throw to let the test framework handle it
  }
}

async function importPresoXml(page, triggerSelector, inputSelector, filePath) {
  try {
    if (triggerSelector) {
      await page.click(triggerSelector);
    }

    const fileInput = page.locator(inputSelector);
    await expect(fileInput).toHaveCount(1); // Ensure input exists

    if (!fs.existsSync(filePath)) {
      throw new Error(`File not found: ${filePath}`);
    }

    const stat = fs.statSync(filePath);
    if (!stat.isFile()) {
      throw new Error(`Path is not a file: ${filePath}`);
    }

    await fileInput.setInputFiles(filePath);
    await page.waitForTimeout(1000);
  } catch (err) {
    console.error(`❌ importPreso failed for file: ${filePath}`);
    console.error(`Error: ${err.message}`);
    throw err;
  }
}



async function importPresentation(page, triggerSelector, filePath, options = {}) {
  const { successSelector, expectedText } = options;

  // Wait for the filechooser event and trigger the upload
  const [fileChooser] = await Promise.all([
    page.waitForEvent('filechooser'),
    page.locator(triggerSelector).click()
  ]);

  await fileChooser.setFiles(filePath);

  // Optional post-upload validation
  if (successSelector) {
    const successLocator = page.locator(successSelector);
    await expect(successLocator).toBeVisible();

    if (expectedText) {
      await expect(successLocator).toHaveText(expectedText);
    }
  }
}

async function logoutRecorder(page) {
  const userBox = page.locator('#lblUsername');
  await userBox.click();

  const signOut = page.locator('#btnLogout');
  await signOut.click();
}

//Needed to deal with pesky input type chevrons
async function collapseInputChevrons(page) {
  while (true) {
    const chevrons = await page.$$('.icon-chevron-down-white');
    if (chevrons.length === 0) break;

    for (const chevron of chevrons) {
      try {
        await chevron.click();
        await page.waitForTimeout(200); // Allow DOM to settle
      } catch (err) {
        console.warn('Failed to click chevron:', err);
      }
    }
  }
}

//This will find the Presentation by title, click "Delete" but will NOT confirm delete
async function deletePresentation(page, presoTitle) {
  const allPresos = page.locator('.presentation-item');
  const count = await allPresos.count();
  let found = false;

  for (let i = 0; i < count; i++) {
    const item = allPresos.nth(i);
    const titleLocator = item.locator('.presentation-item-name');
    const titleText = await titleLocator.textContent();

    if (titleText && titleText.trim().includes(presoTitle)) {
      found = true;

      const deleteBtn = item.locator('#btnDelete'); // scoped to item
      await deleteBtn.click();
      break;
    }
  }

  if (!found) {
    throw new Error(`Presentation titled "${presoTitle}" was not found.`);
  }
}
//Below will attempt playback of Presentation, requires full Presentation title
async function clickPresentationByTitle(page, title) {
  await page.locator(`.grid-row-title:has-text("${title}"):visible`).click();
}


async function exportPresentation(page, presoTitle) {
  const allPresos = page.locator('.presentation-item');
  const count = await allPresos.count();
  let found = false;

  for (let i = 0; i < count; i++) {
    const item = allPresos.nth(i);
    const titleLocator = item.locator('.presentation-item-name');
    const titleText = await titleLocator.textContent();

    if (titleText && titleText.trim().includes(presoTitle)) {
      found = true;

      const moreBtn = item.locator('#btnMore'); // scoped to item
      await moreBtn.click();
      const exportBtn = item.locator('#btnExport');
      await exportBtn.click();
      break;
    }
  }

  if (!found) {
    throw new Error(`Presentation titled "${presoTitle}" was not found.`);
  }
}

module.exports = {
  loginRecorder,
  navPresoTab,
  navSettingsTab,
  navCaptureTab,
  navSchedTab,
  openInputs,
  closeInputs,
  collapseInputChevrons,
  renamePreso,
  logoutRecorder,
  clickPresentationByTitle,
  deletePresentation,
  importPreso,
  importPresentation,
  importPresoXml,
  exportPresentation
};