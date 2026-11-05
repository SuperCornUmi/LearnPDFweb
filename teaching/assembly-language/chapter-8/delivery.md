# 組合語言第八章｜交付與驗收

- 標準版本：1.1；製作日期：2026-11-05。
- 課程：`assembly-language`／組合語言；單元：`chapter-8`／進階程序與堆疊框架。
- 來源：`src-20261105-assembly-ch8`；保存於 `raw/pdfs/1151 ch8.pdf`，原檔不改。
- SHA-256：`d0ba6fff2d0cb5dd3e155f267023b8d1cf4a516418b1a38b130b9842d6735be4`。
- 版本：封面 2015 第七版全球版、混有第五版及課堂增補；實際講義發布日期未知。
- PDF 51 頁；已讀及教材完成 pp. 1–51，沒有未完成頁段。
- 簡報 16 張、講稿 16 節；依教學主線合併多頁。
- [網站](../../../index.html#/assembly-language/chapter-8/pages/1) · [notes](../../../notes/assembly-language/chapter-8.md) · [簡報](../../../presentations/assembly-language/chapter-8/slides.md) · [講稿](../../../presentations/assembly-language/chapter-8/speaker-notes.md) · [圖解](../../../presentations/assembly-language/chapter-8/diagrams.md)。
- 可重建來源：content.json、slides.json、config.json、build.py；輸入雜湊見 manifest.json。

## 內容審閱

逐頁讀取 pypdf 文字並對照 51 頁影像聯絡表，pp. 34、41、44、45 另放大；完整涵蓋術語、條件、指令、框架圖、範例與作業，不因重複而跳頁。保留先遮答案、後揭露的頁次。每頁分翻譯與講解，只有必要補充；補充空白時 notes／網站都沒有占位卡片。

講解具體展開：AddTwo 從 S 推得 +8／+12；Difference 計算順序；x／y 的 −4／−8 槽；LEA 的執行時計算；FillArray 三輪追蹤與零長度風險；Ex1Array 的 12-byte 位移及 50=32h；TestStack 的 4、2、2、4-byte PUSH 與 10-byte 陣列對齊配置；CountMatches 的 2／5 差異。

勘誤及條件集中於 [來源頁](../../../wiki/sources/src-20261105-assembly-ch8.md)，包含 Arrary、參數逗號、讀值／取址、64-bit 警語範圍及模組可見性。原文與代理修正分開。

外部查證使用 8 個 Microsoft 官方網頁的指定段落，記錄於 [Wiki](../../../wiki/sources/web-20261105-microsoft-masm-procedures.md) 與 raw/web。未完整閱讀的手冊部分不使用；這是 partial 外部來源，不因本地教材完成而改成完整閱讀。

## 實際驗收

已通過 `work/check-assembly.cjs` 的瀏覽器操作檢查：

- 從所有課程找到組合語言及第八章；新課程不再顯示線性代數名稱或 CE2005。
- 51 頁原圖／自製封面可載入，51 個頁碼與講解對應；程式碼保留縮排。
- 專注閱讀、展開／收起及重新載入偏好、目前頁碼、搜尋／目錄、跳頁、鍵盤、原圖放大與內外捲動隔離。
- 16 張簡報連續換張，捲動與按鈕位置穩定；鍵盤與全螢幕換張。
- 51 頁筆記閱讀、Markdown 切換、下載目標與列印媒體版面。
- 堆疊 8 階段，匹配預設 2／5、空陣列、負數及無效輸入處理。
- 1882×960、1255×640、390×844、768×900，各模式沒有頁面橫向溢出；桌面原圖完整等比例縮放。長程式區塊可在區塊內橫向捲動，長講解沿閱讀區向下讀取。
- 線性代數 87／152 頁與兩種原有圖解仍可開啟，既有教材原稿未重建或改寫。
- 瀏覽器 `pageerror`／資產載入失敗為 0。截圖另以人工視覺檢查桌面、矮視窗與手機。

瀏覽器證據與截圖：`work/src-20261105-assembly-ch8/browser-results.json` 及同資料夾 `website-*.png`。另以 `check-assembly-paths.cjs` 驗證 `/sample-repo/` 子路徑，結果記於 path-results.json；本地檔案／連結檢查結果記於 file-results.json。

共用閱讀器另補上「捲到最後且短頁無法置頂」時的末頁判定。長距離平滑跳頁須等待捲動完成；測試以實際到達位置判定，未把過渡中的頁碼當成失敗。

## 計算驗證與限制

`check_models.py` 通過 5 組陣列、空陣列／負數／相等與不等、堆疊進出平衡、PUSH 位移、基本數值及 FillArray 邊界模型；結果見 model-results.json。網站 JavaScript 模型另經瀏覽器操作。

**未以 MASM／Irvine32 原生組譯及執行**，不宣稱原始程式或教學修正版通過機器碼測試；函式庫版本、DumpMem 的替代堆疊介面、實際 prologue 選項均未自行猜定。Poppler 的字型替代警告已記於來源；關鍵指令與圖中數值由影像核對。

沒有上傳、推送或部署；外部文獻須連網，課程閱讀與互動可離線。來源檔及所有既有使用者筆記保留。
