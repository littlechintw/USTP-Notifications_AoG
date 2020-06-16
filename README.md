北聯大通知 Docs
===

## 創作理念

科技日新月異，智慧家庭的概念越來越流行，也有越來越多家庭加入智慧家庭的行列，在 2019 年 11 月，Google 開始在臺灣販售智慧家庭裝置，使用者可以藉由「說出指令」完成特定的動作，而 Google 也提供開發者上架服務，所以希望能藉由這個服務，讓使用者可以更快的獲取新資訊！

## 功能說明（執行成果畫面圖文說明）

==由於未上架，故無法在開發者除外帳戶測試、使用。==

- 有螢幕裝置
    - 可查詢北聯大四校之最新通知
    - 每次查詢提供最新 3 則通知
    - 可直接點選公告並導向公告網頁位置

- 音訊輸出裝置
    - 可查詢北聯大四校之最新通知
    - 每次查詢提供最新 3 則通知
    - 裝置將直接說出公告內容

[以有螢幕裝置展示成果畫面]

1. 打開 Google Assistant 並說出「我要跟北聯大通知說話」切換至服務

![](https://i.imgur.com/olpgYZz.png)

2. 說出「幫助」可以查看服務的詳細內容

![](https://i.imgur.com/bSyXWH6.png)

3. 說出「北大公告」可以查看臺北大學最新3則公告

![](https://i.imgur.com/VF8zsJf.png)

4. 說出「海大公告」可以查看海洋大學最新3則公告

![](https://i.imgur.com/kxSP9E2.png)

5. 說出「北醫公告」可以查看臺北醫學大學最新3則公告

![](https://i.imgur.com/lqhNFV9.png)

6. 說出「北科公告」可以查看臺北科技大學最新3則公告

![](https://i.imgur.com/l4cRSw7.png)

7. 說出「掰掰」可離開服務

![](https://i.imgur.com/92RXPc1.png)

## 程式流程、資料分析流程或系統架構圖

![](https://i.imgur.com/LR2zovR.png)

## 程式開發與執行環境說明

- Python3
    - Flask
    - bs4
    - feedparser
- Ubuntu 18.04.2 LTS
- ngrok (Not necessarily needed)

## Dialogflow (無程式碼)
    - Intents (功能)
    ![](https://i.imgur.com/zKTB1Mp.png)
        1. **幫助選單功能**
        2. **四校查詢最新訊息功能**
        3. **離開功能**
        - *訓練字彙範例*
        ![](https://i.imgur.com/eZWv2MW.png)
        - *開啟 webhook call 功能*
        ![](https://i.imgur.com/lhBfs1l.png)

    - Entities (字彙定義)
    ![](https://i.imgur.com/rXMqRZM.png)
        1. **定義幫助選單字彙**
        2. **定義四校的相關字彙**
        3. **定義最新訊息字彙**
        4. **定義離開功能字彙**
        - *幫助選單字彙範例*
        ![](https://i.imgur.com/iqu3xvN.png)
        
    - Fulfillment
        - Webhook 設定
        ![](https://i.imgur.com/SKq7VLv.png)
