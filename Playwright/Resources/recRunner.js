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
}

async function navSettingsTab(page) {
  const presTab = page.locator('.btn-settings');
  await presTab.click();
}

async function navSchedTab(page) {
  const presTab = page.locator('.btn-schedules');
  await presTab.click();
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
  // Narrow down to presentation items
  const allPresos = page.locator('.presentation-item');
  const count = await allPresos.count();

  for (let i = 0; i < count; i++) {
    const item = allPresos.nth(i);
    const text = await item.textContent();

    if (text && text.includes(presoTitle)) {
      // Click the Delete button within the matched item only
      const checkbox = item.locator('.grid-row-checkbox');
      const deleteBtn = page.locator('#btnDelete');
      await checkbox.click();
      await deleteBtn.click();
      await page.waitForTimeout(12000);

      await expect(page.locator('.confirm-content')).toContainText(
        'Are you sure you want to permanently delete this presentation?'
      );

      await page.locator('#btnOk').click();
      await page.waitForTimeout(2000);
      break;
    }
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