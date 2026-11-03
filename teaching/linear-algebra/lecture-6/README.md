# Lecture 6 教材維護

依[統一標準 v1.0](../../../wiki/standards/PDF課程教材製作標準.md)製作，完成日期 2026-11-04。

- `pages.txt`：152 列，每列「標題｜中文翻譯｜觀念講解｜教學補充」，一列對應一個 PDF 實體頁。封面、分隔頁及結尾均保留。
- `slides.txt`：20 張，每列「標題｜分號分隔重點｜講解稿｜PDF 頁段」。
- `config.json`：課程、單元、來源、下載、影像、章節分組及文獻設定。
- `lesson.json`：以上內容生成的教材資料；不要直接修改輸出。
- `manifest.json`：來源與 Wiki 輸入雜湊、標準版本、頁數及張數。
- `delivery.md`：實際驗收結果與限制。

修改原稿後，在專案根目錄執行：

```text
python teaching/build_lesson.py teaching/linear-algebra/lecture-6
```

會重建 notes、簡報、講稿、網站下載與 `website/lessons/lecture-6.js`。原圖由保存的 PDF 以 130 dpi 產生 WebP，自製封面為 SVG。網站註冊資料後由共用介面載入；根目錄 `index.html` 已加入本單元腳本。

新增其他單元時建立獨立原稿、設定、來源、影像及資料腳本，加入根目錄 HTML，依各單元資料生成課程／章節，保留既有教材。未做成背景監看或自動辨識匯入工具。外部查證設定與生成工具中的參考文獻段落也必須依新單元實際來源調整。

數學內容參照[來源與勘誤](../../../wiki/sources/src-20261103-ce2005-lecture-6.md)。中文採忠實意譯，公式為 Unicode／逐列矩陣，未使用外部字型或排版服務。
