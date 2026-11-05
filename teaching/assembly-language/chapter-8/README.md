# 組合語言第八章教材維護

依 [統一標準 v1.1](../../../wiki/standards/PDF課程教材製作標準.md) 製作，日期 2026-11-05。

- `content.json`：51 頁原稿，含完整中文意譯、觀念講解與選用補充；空補充不顯示。程式碼保留 Markdown fence 與縮排。
- `slides.json`：16 張精簡投影片及同編號講稿、PDF 實體頁碼。
- `config.json`：課程、單元、分組、來源、外部文獻及網站路徑。
- `build.py`：生成 notes、簡報、講稿、下載、lesson.json 與獨立資料腳本；只重建本單元，不改既有課程。
- `manifest.json`：標準版本、輸入 SHA-256、完成範圍與原生執行狀態。
- `check_models.py`／`model-results.json`：演算法與數值模型檢查，不能取代 MASM 原生執行。
- `delivery.md`：實際驗收與限制。

在專案根目錄執行（python 請替換為環境內可用的 Python 執行檔）：

```text
python teaching/assembly-language/chapter-8/build.py
python teaching/assembly-language/chapter-8/check_models.py
node work/check-assembly.cjs
node work/check-assembly-paths.cjs
```

PDF 原圖由 Poppler 渲染 51 頁，網站只使用第 2–51 頁的 WebP，第 1 頁為自製 SVG；來源 PDF 不改。`work/prepare_assembly.py` 記錄擷取後的轉圖步驟；分頁文字與聯絡表在 `work/src-20261105-assembly-ch8/`。該準備腳本用於本次匯入，不應用來覆蓋既有 raw metadata。

共用程式碼呈現支援 fence 與多段文字；根 HTML 載入獨立單元資料與 `website/assembly-diagrams.js`。網站圖解與 Markdown 圖解須一起維護。不要重新執行 `work/write_assembly_content.py`／`write_assembly_support.py` 去覆蓋使用者後續改寫；正式內容修改以本資料夾 JSON 與 Wiki 為準。

原檔 SHA-256：`d0ba6fff2d0cb5dd3e155f267023b8d1cf4a516418b1a38b130b9842d6735be4`。原檔為混編講義，實際發布日期未知，2015 是封面版本，不將 metadata 建立日期當成發布日。
