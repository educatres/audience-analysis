# 課堂聽眾專注度分析

`index.html` 是一個單檔網頁工具，可透過瀏覽器鏡頭定時擷取課堂畫面，呼叫支援 Responses API 格式的視覺模型，估算聽眾總人數、疑似不專心人數、使用手機人數與比例趨勢。

本工具只在頁面中保留數字與文字摘要，不會把照片保存到本機頁面紀錄中。分析結果適合作為課堂觀察輔助，不應用於個人評分、紀律處分或身分辨識。

## 功能特色

- 單檔 HTML，免建置、免安裝前端套件。
- 支援長庚 CGU LLM、OpenAI API 與自定義 Responses-compatible endpoint。
- 可選擇內建鏡頭、USB camera、前鏡頭或後鏡頭。
- 支援手動拍攝與定時自動分析。
- 顯示總人數、疑似不專心人數、不專心比例、手機使用比例與最近摘要。
- 內建比例趨勢圖與 Dashboard 模式，便於課堂現場快速掌握狀態。
- 可隱藏影像預覽，降低現場干擾。

## 使用者介面展示

![課堂聽眾專注度分析 Dashboard 與結果展示](UI2.jpg)

## 線上使用

GitHub Pages：https://educatres.github.io/audience-analysis/

## 系統需求

- 現代瀏覽器：建議使用 Chrome 或 Edge。
- 可用攝影機：內建鏡頭、USB camera 或手機後鏡頭。
- 可連線的視覺模型 API：
  - 長庚 CGU LLM API
  - OpenAI API
  - 其他相容 `/responses` 格式的 API endpoint
- API key 或 Bearer Authorization token。

> 注意：瀏覽器啟用鏡頭通常需要安全來源。建議透過 `localhost` 或 HTTPS 開啟，不建議直接用 `file://` 開啟，因為部分瀏覽器可能無法正常列出 USB camera。

## 安裝方式

### 方法一：下載專案

1. 點選 GitHub 頁面的 **Code**。
2. 選擇 **Download ZIP**。
3. 解壓縮後進入專案資料夾。

### 方法二：使用 Git Clone

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

## 啟動方式

建議使用本機 HTTP server 啟動，讓瀏覽器能穩定使用攝影機權限。

```bash
python3 -m http.server 8000
```

啟動後在瀏覽器開啟：

```text
http://localhost:8000/
```

## 使用流程

1. 開啟頁面後，確認瀏覽器允許使用攝影機。
2. 在 **API 來源** 選擇：
   - `長庚 CGU LLM`
   - `OpenAI`
   - `自定義`
3. 確認 **Endpoint**。若輸入的是 API base URL，系統會自動補成 `/responses` endpoint。
4. 輸入 **API key / Authorization**。
   - 可直接輸入 API key。
   - 也可輸入完整 `Bearer ...`。
5. 輸入或確認 **模型** 名稱。
6. 設定 **間隔秒數**，最小值為 10 秒。
7. 按下 **開啟鏡頭**，並選擇需要的鏡頭來源。
8. 按下 **開始分析** 啟動定時分析。
9. 需要單次分析時，可按 **手動拍攝**。
10. 需要停止定時分析時，按 **暫停**。
11. 需要清空頁面紀錄時，按 **清除紀錄**。

## API 設定說明

| 欄位 | 說明 |
| --- | --- |
| API 來源 | 選擇預設服務或自定義服務。 |
| Endpoint | API base URL 或完整 `/responses` endpoint。 |
| API key / Authorization | API key 或 `Bearer ...` 授權字串。 |
| 模型 | 支援影像輸入的模型名稱。 |
| 間隔秒數 | 自動分析的拍攝間隔，最低 10 秒。 |
| 鏡頭來源 | 自動選擇、前鏡頭、後鏡頭或瀏覽器列出的攝影機。 |

預設 API 來源：

| 來源 | 預設 Endpoint | 預設模型 |
| --- | --- | --- |
| 長庚 CGU LLM | `https://air.cgu.edu.tw/cgullmapi/v1` | `gpt-6-luna` |
| OpenAI | `https://api.openai.com/v1` | `gpt-6-luna` |
| 自定義 | 自行輸入 | 自行輸入 |

## 畫面與指標

- **總人數**：畫面中可見的聽課人物總數。
- **疑似不專心**：依可見行為估算的人數，例如低頭看非課堂物品、轉頭交談、睡覺、離席或長時間未面向講者。
- **不專心比例**：疑似不專心人數除以總人數。
- **使用手機比率**：正在使用或明顯看手機的人數比例。
- **比例趨勢**：依照每次分析結果繪製的不專心比例變化。
- **最近摘要**：模型回傳的一句繁體中文觀察摘要。

## Dashboard 模式

點選右上角 **Dashboard 模式** 可切換成現場儀表板視覺狀態。背景色會依最近一次不專心比例變化：

| 比例 | 狀態 |
| --- | --- |
| 小於 20% | 綠色 |
| 20% 到 50% | 黃色 |
| 高於 50% | 紅色 |

## 隱私與安全

- 頁面不會將拍攝照片保存到分析紀錄中。
- 每次分析會將當下擷取的影像送到你設定的 API endpoint。
- API key 只在目前瀏覽器頁面中使用，程式未將 API key 寫入 localStorage 或後端資料庫。
- 請在合法、透明且取得必要同意的情境下使用攝影機分析。
- 分析結果僅供群體觀察參考，不應用於辨識個人、推測敏感屬性、個人懲處或正式評分。

## 常見問題

### 無法開啟鏡頭

- 請確認瀏覽器已允許攝影機權限。
- 請使用 Chrome 或 Edge。
- 請透過 `http://localhost:8000/` 或 HTTPS 開啟。
- 若使用 USB camera，先按 **開啟鏡頭**，再按 **重新掃描鏡頭**。

### 看不到 USB camera 名稱

瀏覽器通常要在使用者允許攝影機權限後，才會顯示完整裝置名稱。請先開啟鏡頭並允許權限，再重新掃描鏡頭。

### API 回應失敗

- 確認 API key 是否正確。
- 確認模型是否支援影像輸入。
- 確認 endpoint 是否可連線，且服務支援 `/responses` 格式。
- 若使用自定義 API，請確認伺服器允許瀏覽器跨來源請求。

### 分析結果不準確

模型分析會受鏡頭角度、光線、遮擋、畫面模糊與座位密度影響。請將攝影機放在穩定位置，並讓畫面包含足夠清楚的課堂全景。

## 專案結構

```text
.
├── UI2.jpg
├── index.html
├── LICENSE
└── README.md
```

## 授權

本專案採用 MIT License，詳見 [LICENSE](LICENSE)。
