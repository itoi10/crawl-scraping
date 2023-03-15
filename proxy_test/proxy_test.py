import time

import requests


def main():
    """プロキシを経由するとIPアドレスが変更されるか確認する"""

    # グローバルIPアドレスを確認するAPI
    url = "http://httpbin.org/ip"

    # プロキシ設定 (プロキシのdockerコンテナを起動しておく)
    proxies = {
        "http": "socks5://localhost:9050",
        "https": "socks5://localhost:9050",
    }

    print("With proxy (socks5://localhost:9050)")
    for i in range(10):
        rsp = requests.get(url, proxies=proxies)
        print(i, rsp.text)
        time.sleep(3)

    print("Without proxy")
    for i in range(5):
        rsp = requests.get(url)
        print(i, rsp.text)
        time.sleep(3)


if __name__ == "__main__":
    main()
