import { chromium } from '@playwright/test';

(async () => {
  const browserOptions = {
    headless: true,
    // slowMo: 100,
    // proxy: {
    //   server: 'http://proxy.example.com:8080',
    //   username: 'username',
    //   password: 'password',
    // }
  };
  const browser = await chromium.launch(browserOptions);
  const context = await browser.newContext();
  const page = await context.newPage();


  await page.goto('https://www.nikkei.com/');



  const detail_urls = await page.$$eval(
    'article h2 a[href*="/article/"]',
    (links: HTMLLinkElement[])  => links.map(a => a.href)
  );

  console.log(detail_urls);

  await browser.close();
})();
