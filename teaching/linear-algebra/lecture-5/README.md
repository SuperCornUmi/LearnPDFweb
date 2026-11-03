# Lecture 5 教材來源

此單元是第一份實作參考；後續教材以 [統一製作標準 v1.0](../../../wiki/standards/PDF課程教材製作標準.md) 為準，使用 `templates/` 的通用範本。此處的 87 頁、15 張與來源路徑僅適用 Lecture 5，不應直接複製成其他單元的固定值。

- `pages.txt`：87 列，每列為「標題｜中文翻譯｜觀念講解｜教學補充」；按 PDF 頁序排列，勿刪除空白用途的頁面。
- `slides.txt`：15 張精簡簡報，每列為「標題｜以分號分隔的重點｜講解稿｜PDF 頁碼」。
- `build.py`：由同一份內容生成 Markdown 筆記、簡報、講稿、JSON 與網站資料。
- `manifest.json`：記錄這次製作採用的 Wiki、PDF、教材原稿雜湊，供後續比對更新。

修改教材時先改 pages.txt／slides.txt，再使用環境中的 Python 執行 build.py。原始頁面影像位於 website/assets/lecture5/，源自保存的 PDF；原始 PDF 不修改。

日期：2026-11-03。中文為忠實意譯；重複頁尾資訊未逐頁複製。公式以 Unicode 與逐列矩陣表示，無需網路字型或數學排版 CDN。
