---
title: "知識總覽"
type: overview
created: 2026-11-03
updated: 2026-11-05
status: reviewed
tags: [線性代數, 組合語言]
source_ids: [src-20261103-ce2005-lecture-5, web-20261103-mit-lecture9, src-20261103-ce2005-lecture-6, web-20261104-mit-coordinates-spaces, src-20261105-assembly-ch8, web-20261105-microsoft-masm-procedures]
---

# 知識總覽

[返回索引](index.md)

## 專案工作標準

後續新增課程 PDF 統一依 [PDF 課程教材與網站製作標準 v1.1](standards/PDF課程教材製作標準.md) 執行，預設包含原檔保存、Wiki 整合、完整逐頁中文教材、精簡簡報與講稿、網站章節及操作驗收；除非使用者明確縮小範圍，不只新增來源摘要。

教材品質依 v1.1：逐頁完整意譯、補清關鍵計算與推理，只有必要且緊扣當頁的補充才保留；長文字須通過桌面／手機可讀性檢查。

網站已加入線性代數 Lecture 5、6 與組合語言第八章，課程／章節由單元資料建立，閱讀進度分開保存；新增單元仍須由代理製作、註冊及驗收，沒有背景自動匯入功能。

## 範圍

目前已匯入 3 份 PDF，共 290 頁：

- [Lecture 5：線性獨立與基底](sources/src-20261103-ce2005-lecture-5.md)：87 頁逐頁教材、15 張簡報。
- [Lecture 6：座標、秩與線性轉換](sources/src-20261103-ce2005-lecture-6.md)：152 頁逐頁教材、20 張簡報與幾何互動。

- [組合語言第八章：進階程序](sources/src-20261105-assembly-ch8.md)：51 頁逐頁教材、16 張簡報、堆疊與匹配互動。

研究入口為[組合語言](topics/組合語言.md)及[線性代數](topics/線性代數.md)，網站入口為[知識課堂](../index.html)。兩筆 MIT 官方資料均只使用已讀範圍，見來源摘要。

## 目前主要結論

- 獨立性排除冗餘並保證 span 中表示的唯一性。（[來源](sources/src-20261103-ce2005-lecture-5.md)，PDF pp. 10–16、40–44）
- 基底同時獨立且生成整個空間，維度是任一基底的元素數。（同來源，PDF pp. 63、74–75）
- Wronskian 在某點非零足以證明獨立；恆為零不能一般性地反推相依。（同來源，PDF pp. 54–60）

- 座標由基底決定；同一線性算子在不同基底的表示矩陣相似，轉換方向須先定義。（[Lecture 6](sources/src-20261103-ce2005-lecture-6.md)，PDF pp. 18、127–145）
- rank(A)+nullity(A)=欄數；column space 的基底從原矩陣的 pivot 欄選取。（同來源，PDF pp. 57–65）

- 32 位元典型 EBP 框架的參數偏移由 PUSH 與 CALL 的寬度推得；傳值與傳址須分清。（[第八章來源](sources/src-20261105-assembly-ch8.md)，PDF pp. 9–18）
- CountMatches 同位置與跨位置匹配是不同問題，原題無重複時分別得 2 與 5。（同來源，PDF pp. 50–51）

## 證據缺口與下一步

- 已建立[跨講義比較](comparisons/從基底到矩陣表示.md)；目前仍以同一課程講義為主，MIT 查證不代表完整課程匯入。
- 先備章節 Section 3.2 尚未獨立匯入。
- 可從[方法選擇問答](questions/如何選擇獨立性判定方法.md)開始練習。

- 組合語言尚未匯入先備章節；特定 MASM／Irvine32 工具版本與原生執行尚未驗證。官方查證只採指定段落，未完整匯入手冊。
