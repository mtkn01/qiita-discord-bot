import os
import time
from datetime import datetime, timedelta, timezone
# from dotenv import load_dotenv

import requests
import urllib.parse

# load .env
# load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
QIITA_TOKEN = os.getenv("QIITA_TOKEN")

def is_yesterday(date_str: str) -> bool:
    if not date_str:
        return False

    # ISO8601 → dt
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    # JST
    jst = timezone(timedelta(hours=9))
    dt = dt.astimezone(jst)

    today_jst = datetime.now(jst).date()
    yesterday = today_jst - timedelta(days=1)

    return dt.date() == yesterday


def qiita_items():
    # ニュースを取得する
    query = urllib.parse.quote_plus('LLM')
    url = f"https://qiita.com/api/v2/items?query={query}&per_page=100"

    headers = {"Authorization": f"Bearer {QIITA_TOKEN}"} if QIITA_TOKEN else {}

    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()


def main():
    items = []

    for item in qiita_items():
        if is_yesterday(item.get("created_at")):
            score = item.get("likes_count", 0) + item.get("stocks_count", 0)
            items.append((score, item["title"], item["url"]))

    items = sorted(items, key=lambda x: x[0], reverse=True)[:10]

    if not items:
        text = "昨日の AI News (Qiita) が見つかりませんでした"
    else:
        lines = ["【昨日の AI News (Qiita) Top10】"]
        for i, (score, title, link) in enumerate(items, start=1):
            lines.append(f"{i}) {title}\n  Score: {score}\n  {link}")
        text = "\n-----\n".join(lines)

    # Discord Webhookで送信
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={"content": text})
    else:
        print("DISCORD_WEBHOOK_URL が設定されていません。")


if __name__ == "__main__":
    main()

# Discord Webhook 動作確認コード
# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()
# WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# data = {
#     "content": "Discord Webhook 動作確認"
# }

# requests.post(WEBHOOK_URL, json=data)
