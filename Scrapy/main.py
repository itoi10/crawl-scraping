import subprocess
import scrapy
from scrapy.exceptions import DropItem


class MySpider(scrapy.Spider):
    name = "my_spider"
    start_urls = ["https://www.nikkei.com/"]

    def parse(self, response):
        """一覧ページ処理"""
        # 詳細ページリクエスト
        for detail_href in response.css('article h2 a[href*="/article/"]'):
            yield response.follow(detail_href, self.parse_article)

    def parse_article(self, response):
        """記事ページ処理"""
        item = dict()
        item["title"] = response.css("h1[class*=title]::text").get(default="").strip()
        item["time"] = response.css("main header time::text").get(default="").strip()
        item["content"] = response.css("main section[class*=container]").xpath("string()").get(default="").strip()
        item["url"] = response.url
        yield item

    custom_settings = {
        # robots.txtポリシーを尊重する
        "ROBOTSTXT_OBEY": True,
        # ダウンロード間隔 デフォルト0
        "DOWNLOAD_DELAY": 1,
        # リクエストヘッダーの言語をjaに設定
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ja",
        },
        # アイテム・パイプライン
        "ITEM_PIPELINES": {"main.MyItemPipeline": 500},
        # 出力ファイルを日本語にする
        "FEED_EXPORT_ENCODING": "utf-8"
        # ログレベル デフォルト"DEBUG"
        # "LOG_LEVEL": "INFO",
    }


class MyItemPipeline:
    def process_item(self, item, spider):
        # コンテンツの無いitemを除外
        if item["content"]:
            return item
        else:
            raise DropItem(f"drop item {item = }")


if __name__ == "__main__":
    # Scrapy実行
    subprocess.run("scrapy runspider main.py -O out.jl", shell=True)
