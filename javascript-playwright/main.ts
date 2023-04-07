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

  function toUrl (links: HTMLLinkElement[]): string[] { return links.map(a => a.href) }

  const detailUrls = await page.$$eval('article h2 a[href*="/article/"]', toUrl)

  console.log(detailUrls.length)

  for (const url of detailUrls) {
    await page.goto(url)
    try {
      const title = await page.$eval('h1[class*=title]', (el) => el.textContent)
      const time = await page.$eval('main header time', (el) => el.textContent)
      const content = await page.$eval('main section[class*=container]', (el) => el.textContent)
      const data = { title, time, content, url }
      console.log(data)
    } catch (e) {
      console.log('取得失敗')
    }
  }

  await browser.close()
})()
