# AI News Bot

このプロジェクトは、Qiitaから「大規模言語モデル」や「LLM」に関連する記事を取得し、前日のトップ10の記事をDiscord Webhookを通じて通知するPythonスクリプトです。

## ファイル構成

- **src/main.py**: メインスクリプト。Qiita APIを使用して記事を取得し、Discordに通知します。
- **.env**: 環境変数を設定するファイル。以下の変数を設定する必要があります。
  - `DISCORD_WEBHOOK_URL`: Discord WebhookのURL
  - `QIITA_TOKEN`: Qiita APIのアクセストークン（オプション）

## 主な機能

1. **Qiita APIから記事を取得**:
   - クエリ「大規模言語モデル OR LLM」で記事を検索。
   - 前日に作成された記事をフィルタリング。
   - 「いいね」数と「ストック」数をスコアとして計算し、トップ10の記事を選出。

2. **Discord Webhookで通知**:
   - トップ10の記事をフォーマットしてDiscordに送信。
   - Webhook URLが設定されていない場合は、コンソールにエラーメッセージを表示。

## 必要なPythonライブラリ

- `requests`
- `python-dotenv`（オプション）

## 使用方法

1. `.env`ファイルを作成し、必要な環境変数を設定します。
2. 必要なライブラリをインストールします:
   ```bash
   pip install -r requirements.txt
   ```
3. スクリプトを実行します:
   ```bash
   python src/main.py
   ```

## 注意事項

- Qiita APIのアクセストークンが設定されていない場合、認証なしでリクエストが行われます。
- Discord Webhook URLが設定されていない場合、通知は行われず、コンソールにメッセージが表示されます。

## ライセンス

このプロジェクトはMITライセンスの下で提供されます。
