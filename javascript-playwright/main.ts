import { chromium } from '@playwright/test';

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();


  await page.goto('https://playwright.dev/');

  const h1_text = await page.textContent('h1.hero__title');
  console.log(h1_text);


  await browser.close();
})();
