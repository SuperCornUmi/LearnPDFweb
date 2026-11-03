# PDF 重點整理 LLM Wiki

## 新增 PDF 的統一流程

直接提供課程 PDF 即可，代理先讀 [AGENTS.md](AGENTS.md) 與 [統一製作標準 v1.0](wiki/standards/PDF課程教材製作標準.md)，依序完成：保存原檔、更新 Wiki、完整逐頁中文 notes、精簡簡報與講稿、適合的圖解及網站課程／章節。若只需要其中一部分，當次明確說明即可。

逐頁講解每頁都保留；簡報依重點合併頁面。網站沿用自製封面、寬幅原頁、可收合目錄、獨立捲動的連續講解及換張不跳頂。細節、外部資料查證、程式碼講解及驗收依統一標準執行。新增教材範本位於 `templates/`，不需每次重新說明相同規則。

## 教學網站

開啟 [知識課堂](website/index.html)，依「課程 → 章節」進入。首個單元為線性代數 Lecture 5，含 87 頁逐頁中文翻譯與講解、15 張精簡簡報及講解稿、完整筆記、概念圖與互動示意。網站支援離線閱讀，沒有上傳原始文件。

- [Markdown 逐頁筆記](notes/linear-algebra/lecture-5.md)
- [簡報逐張內容](presentations/linear-algebra/lecture-5/slides.md) · [簡報講解稿](presentations/linear-algebra/lecture-5/speaker-notes.md)
- [教材維護說明](teaching/linear-algebra/lecture-5/README.md) · [網站使用說明](website/README.md)

這是一個由 LLM 持續維護的繁體中文 PDF 知識庫，依使用者提供的 Karpathy「LLM Wiki」模式建立。原始文件保持不變，摘要、概念、交叉比較與問答會隨閱讀逐步累積。

## 開始使用

1. 把 PDF 放進 `raw/pdfs/`。需要補充出版資訊或閱讀目標時，可在 `raw/metadata/` 新增文字檔。
2. 在此資料夾開啟你的 LLM 代理，請它先讀取 [AGENTS.md](AGENTS.md)。
3. 下達：「請依 AGENTS.md 匯入 raw/pdfs/檔名.pdf，整理重點並整合到 Wiki。」
4. 從 [知識索引](wiki/index.md) 閱讀結果，再追問、比較或補讀。

可直接使用的指令：

- 「匯入這份 PDF，特別注意研究方法、限制與可採取的行動。」
- 「根據現有 Wiki 比較各來源對某主題的看法，附 PDF 頁碼，將比較保存到 Wiki。」
- 「接續上次未讀完的頁面，更新摘要與相關概念。」
- 「依 AGENTS.md 執行健檢，修正斷鏈與索引，列出仍待確認的證據。」

## 目錄

```text
AGENTS.md          代理的中文工作規範
raw/pdfs/          原始 PDF（保留不變）
raw/metadata/      使用者提供的來源資訊
wiki/index.md      知識入口
wiki/overview.md   研究範圍、結論與缺口
wiki/log.md        追加式操作歷史
wiki/sources/      每份 PDF 的重點摘要
wiki/topics/       跨來源主題
wiki/concepts/     概念與定義
wiki/entities/     人物、機構與方法等實體
wiki/comparisons/  跨文件比較
wiki/questions/    保存的問答與待解問題
wiki/standards/    集中且有版本的專案製作標準
notes/             按課程與單元保存完整逐頁中文教材
presentations/     精簡簡報逐張內容及講解稿
teaching/          結構化教材、生成工具、來源雜湊及交付紀錄
website/           課程／章節／模式切換的本機 HTML
templates/         頁面範本
work/              可重建的擷取文字、OCR 與頁面影像
```

目前已匯入 CE2005 Lecture 5，請從知識索引閱讀。往後在此 Wiki 工作中提供課程 PDF，預設依統一流程完成教材與網站更新；保留所有既有來源及章節。此框架不會在聊天外自行監控資料夾，目前網站也不是通用的自動匯入器；新單元由代理依標準實際擴充。PDF 擷取與 OCR 能力取決於代理環境，處理不完整時保留待辦與實際讀取範圍。

引用使用 PDF 實體頁序（從 1 起算），並可附上不同的內文頁碼。一般編輯器即可閱讀；也可將此資料夾作為 Obsidian 知識庫開啟，不需要額外插件。
