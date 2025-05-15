# LineBot 串接 OpenAI 與 TDX 運輸資料流通服務平臺

## 簡介

本專案是一個 Line Bot 應用，它整合了 OpenAI 的自然語言處理能力以及 TDX 運輸資料流通服務平臺的即時交通資訊。使用者可以透過 Line 與機器人互動，查詢高雄捷運的即時到站資訊，並與 OpenAI 模型進行對話。


## 主要功能

* **高雄捷運即時到站查詢：**
    * 使用者輸入指定格式（例如：`R 左營`），即可查詢該站點的捷運即時到站資訊，包括列車目的地和預計到站時間。
    * 支援查詢不同路線（例如：紅線 R、橘線 O）的站點資訊。
* **AI 對話模式：**
    * 使用者輸入特定指令（例如：`AI`），即可進入與 OpenAI 模型進行對話的模式。
    * OpenAI 模型將根據使用者的輸入生成回應，提供問答、閒聊等功能。
* **基本指令：**
    * `高捷`：切換至高雄捷運即時到站查詢模式。
    * `AI`：切換至 AI 對話模式。
    * `結束`：返回首頁模式。

## 技術棧

* **後端框架：** Flask (Python)
* **Line Bot SDK：** line-bot-sdk (Python)
* **NGROK：** 用於本地開發時將 Flask 應用程式暴露到公網
* **OpenAI API：** 用於自然語言處理
* **TDX API (運輸資料流通服務平臺)：** 用於獲取高雄捷運即時到站資訊
* **其他函式庫：**
    * `requests`: 用於發送 HTTP 請求
    * `json`: 用於處理 JSON 資料
    * `speech_recognition` (可能未使用但已引入): 用於語音辨識 (目前程式碼中似乎未實際使用)
    * `pydub` (可能未使用但已引入): 用於音訊處理 (目前程式碼中似乎未實際使用)

## 環境需求

* Python 3.x
* pip (Python 的套件管理工具)
* Line Developers 帳號與相關設定 (Channel access token, Channel secret)
* OpenAI API 金鑰
* TDX 運輸資料流通服務平臺應用程式 ID (app\_id) 與應用程式金鑰 (app\_key)
* NGROK (用於本地測試)

## 安裝與設定

1.  **複製儲存庫 (如果您有將程式碼上傳到 GitHub)：**
    ```bash
    git clone 
    cd 
    ```

2.  **安裝相依套件：**
    ```bash
    pip install Flask flask-ngrok line-bot-sdk requests openai
    ```

3.  **設定 Line Bot API 憑證：**
    * 在您的 Line Developers Console 中取得 **Channel access token** 和 **Channel secret**。
    * 將程式碼中的 `'YOUR_CHANNEL_ACCESS_TOKEN'` 和 `'YOUR_CHANNEL_SECRET'` 替換為您的憑證。

4.  **設定 OpenAI API 金鑰：**
    * 在您的 OpenAI 帳戶中取得 API 金鑰。
    * 將程式碼中的 `openai.api_key = ''` 替換為您的 OpenAI API 金鑰。

5.  **設定 TDX API 憑證：**
    * 前往 TDX 運輸資料流通服務平臺申請應用程式 ID (app\_id) 和應用程式金鑰 (app\_key)。
    * 將程式碼中的 `app_id = ''` 和 `app_key = ''` 替換為您的憑證。

## 運行 Line Bot (本地開發)

1.  **啟動 NGROK：**
    * 下載並安裝 NGROK。
    * 在終端機中運行以下命令，將您的 Flask 應用程式的預設端口 (通常是 5000) 暴露到公網：
        ```bash
        ngrok http 5000
        ```
    * NGROK 會提供一個公開的 HTTPS URL，例如 `https://your-ngrok-url.ngrok.io`。

2.  **更新 Line Bot 的 Webhook URL：**
    * 前往您的 Line Developers Console。
    * 在您的 Bot 設定中，找到 **Webhook URL** 的選項。
    * 將 NGROK 提供的 HTTPS URL 貼上，並在末尾加上 `/callback`，例如：`https://your-ngrok-url.ngrok.io/callback`。
    * 啟用 **Use webhook** 選項。

3.  **運行 Flask 應用程式：**

    ```bash
    python main.py
    ```

現在，您的 Line Bot 應該可以透過 NGROK 的公開 URL 接收來自 Line 的訊息。您可以在 Line App 中搜尋您的 Bot 並開始互動。

## 使用說明

1.  **與 Line Bot 聊天：** 在 Line App 中找到您的機器人並打開聊天視窗。
2.  **查詢高雄捷運到站資訊：** 輸入 `高捷` 後，按照提示輸入路線代號和站名，例如 `R 左營` 或 `O 文化中心`。機器人將回覆該站點的即時到站資訊。
3.  **進入 AI 對話模式：** 輸入 `AI`，即可開始與 OpenAI 模型進行對話。您可以輸入任何問題或想聊的話題。
4.  **返回首頁模式：** 輸入 `結束`，機器人將回到預設的回應模式。

