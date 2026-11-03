---
title: "知識總覽"
type: overview
created: 2026-11-03
updated: 2026-11-03
status: reviewed
tags: [線性代數]
source_ids: [src-20261103-ce2005-lecture-5, web-20261103-mit-lecture9]
---

# 知識總覽

[返回索引](index.md)

## 專案工作標準

後續新增課程 PDF 統一依 [PDF 課程教材與網站製作標準 v1.0](standards/PDF課程教材製作標準.md) 執行，預設包含原檔保存、Wiki 整合、完整逐頁中文教材、精簡簡報與講稿、網站章節及操作驗收；除非使用者明確縮小範圍，不只新增來源摘要。

目前網站僅有 Lecture 5；規範及範本已通用化，後續新增單元時仍須實際擴充網站資料載入與課程／章節入口，不能假設已具備背景自動匯入功能。

## 範圍

目前已匯入 1 份 PDF：[CE2005 Lecture 5](sources/src-20261103-ce2005-lecture-5.md)，共 87 頁。研究入口為[線性代數](topics/線性代數.md)，目前涵蓋線性獨立、函數判準、基底與維度。

已建立 [87 頁中文教學筆記](../notes/linear-algebra/lecture-5.md)、15 張精簡簡報與 [HTML 課程入口](../website/index.html)。另有 1 筆 [MIT 官方逐字稿的部分查證](sources/web-20261103-mit-lecture9.md)，僅核對 pp. 1–3 的自由變數與獨立性定義，尚未完整匯入。

## 目前主要結論

- 獨立性排除冗餘並保證 span 中表示的唯一性。（[來源](sources/src-20261103-ce2005-lecture-5.md)，PDF pp. 10–16、40–44）
- 基底同時獨立且生成整個空間，維度是任一基底的元素數。（同來源，PDF pp. 63、74–75）
- Wronskian 在某點非零足以證明獨立；恆為零不能一般性地反推相依。（同來源，PDF pp. 54–60）

## 證據缺口與下一步

- 目前僅單一講義，沒有跨文件結論；可補入前一講或其他教材，建立比較與符號定義對照。
- 先備章節 Section 3.2 尚未獨立匯入。
- 可從[方法選擇問答](questions/如何選擇獨立性判定方法.md)開始練習。
