from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class MyDriver(webdriver.Chrome):
    """WebDriverの拡張クラス"""

    def __init__(self):
        options = Options()
        options.add_argument("--headless")  # headlessモード (ブラウザを表示しない)
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--lang=ja")
        service = ChromeService(executable_path=ChromeDriverManager().install())
        super().__init__(service=service, options=options)
        self.implicitly_wait(3)  # 暗黙の待機時間 (要素が見つかるまで指定秒数待機する)

    def __del__(self):
        self.quit()

    def get_text(self, xpath: str) -> str:
        """XPATHで指定の要素のテキストを取得する"""
        if elms := self.find_elements(By.XPATH, xpath):
            return elms[0].text
        return ""

    def open_tab(self, url: str):
        """新しいタブで指定のURLを開く"""
        self.execute_script(f'window.open("{url}")')
        self.switch_to.window(self.window_handles[-1])

    def close_tab(self):
        """タブを閉じる"""
        self.close()
        self.switch_to.window(self.window_handles[-1])


if __name__ == "__main__":

    with MyDriver() as driver, open("./out_selenium.jsonl", "w", encoding="utf8") as f:
        driver.get("https://www.nikkei.com/")

        for article_url in [
            a.get_attribute("href")
            for a in driver.find_elements(By.XPATH, '//article//h2//a[contains(@href,"/article/")]')
        ]:
            print(f"{article_url = }")
            driver.open_tab(article_url)

            item = dict()
            item["title"] = driver.get_text('//h1[contains(@class,"title")]')
            item["time"] = driver.get_text("//main//header//time")
            item["content"] = driver.get_text('//main//section[contains(@class,"container")]')
            item["url"] = driver.current_url

            if item["content"]:
                print(item)
                f.write(str(item) + "\n")

            driver.close_tab()
