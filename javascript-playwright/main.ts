import { chromium } from '@playwright/test'

void (async () => {
  const browserOptions = {
    headless: true
    // proxy: {
    //   server: 'http://proxy.example.com:8080',
    //   username: 'username',
    //   password: 'password',
    // }
  }

  const browser = await chromium.launch(browserOptions)
  const context = await browser.newContext()
  const page = await context.newPage()

  await page.goto('https://www.nikkei.com/')

  const detailUrls = await page.$$eval(
    'article h2 a[href*="/article/"]',
    (links: HTMLLinkElement[]) => links.map(a => a.href)
  )

  console.log(detailUrls)

  await browser.close()
})()
