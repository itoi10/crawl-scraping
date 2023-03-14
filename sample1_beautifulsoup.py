from __future__ import annotations

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class BSTool:
    def __init__(self, url: str):
        self.rsp = requests.get(url)
        self.url = self.rsp.url
        self.soup = BeautifulSoup(self.rsp.content, "html.parser")

    def text(self, css_selector: str):
        """テキスト取得"""
        if elms := self.soup.select(css_selector):
            return elms[0].text
        return ""

    def get_urls(self, css_selector: str):
        """指定したCSSセレクタからURL一覧取得"""
        return [urljoin(self.url, a.get("href")) for a in self.soup.select(css_selector) if a.get("href")]


def fetch_article(article_url: str) -> dict[str, str]:
    print(f"{article_url = }")
    bs = BSTool(article_url)
    item = dict()
    item["title"] = bs.text("h1[class*=title]")
    item["time"] = bs.text("main header time")
    item["content"] = bs.text("main section[class*=container]")
    item["url"] = bs.url
    return item


if __name__ == "__main__":
    bs = BSTool("https://www.nikkei.com/")
    article_urls = bs.get_urls('article h2 a[href*="/article/"]')
    article_items = map(fetch_article, article_urls)

    with open("./out_bs.jsonl", "w", encoding="utf8") as f:
        for item in article_items:
            if item["content"]:
                print(item)
                f.write(str(item) + "\n")
