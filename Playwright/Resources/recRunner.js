require('dotenv').config({ path: '../.env' });
/**
 * Logs into the Recorder UI using default credentials.
 * @param {import('@playwright/test').Page} page - Playwright page object.
 */
async function loginRecorder(page) {
  const loginUser = page.locator('#txtLogin',{ timeout: 5000 });
  const loginPwd = page.locator('#txtPassword');
  const loginButton = page.locator('#btnLogin');
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

async function navSettingsTab(page) {
  const settTab = page.locator('.btn-settings');
  await settTab.click();
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

async function logoutRecorder(page) {
  const userBox = page.locator('#lblUsername');
  await userBox.click();

  const signOut = page.locator('#btnLogout');
  await signOut.click();
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



module.exports = {
  loginRecorder,
  navPresoTab,
  navSettingsTab,
  navSchedTab,
  openInputs,
  closeInputs,
  renamePreso,
  logoutRecorder,
  deletePresentation
};