---
title: "組合語言第八章：進階程序"
type: source
created: 2026-11-05
updated: 2026-11-05
status: reviewed
tags: [組合語言, MASM, 程序]
source_ids: [src-20261105-assembly-ch8]
source_file: "raw/pdfs/1151 ch8.pdf"
authors: ["Kip R. Irvine"]
published: null
coverage: "PDF pp. 1–51 全部文字閱讀、全部影像聯絡表核對；pp. 34、41、44、45 另放大"
extraction: "pypdf 分頁擷取；Poppler 51 頁渲染；圖中文字人工核對；無需 OCR"
---

# 組合語言第八章：進階程序

[返回索引](../index.md) · [原始 PDF](../../raw/pdfs/1151%20ch8.pdf) · [完整 notes](../../notes/assembly-language/chapter-8.md) · [網站](../../index.html#/assembly-language/chapter-8/pages/1)

## 一句話摘要與背景

以 32 位元 MASM 示範具名程序、堆疊參數、區域變數與跨模組介面，最後用陣列匹配作業整合。不是完整指令集／ABI 手冊。（PDF pp. 1–51）

封面為 Irvine《Assembly Language for x86 Processors》7th Edition, Global Edition，2015；部分頁尾來自 2007 年第五版，並混有課堂實驗與作業。檔案建立時間 2023-10-31 僅是 PDF metadata，不等於課程出版日期；實際教師、修改者與講義發布日期未知，published 保持 null。原作者來源明確，增補作者不推測。SHA-256 見 [metadata](../../raw/metadata/src-20261105-assembly-ch8.json)。

## 核心問題與重點（原文主張）

1. PROC 為參數命名，PROTO 先宣告介面，INVOKE 依介面傳引數；PTR 型別區分指標與資料。（PDF pp. 2–8、31–40）
2. 一次呼叫的框架包含參數、返回位址、保存暫存器與區域資料；典型 EBP 框架固定基準。（PDF pp. 9、15–18）
3. 傳值複製資料；傳址複製 offset，讓程序透過指標改寫原資料。圖中的 0／4 是簡化 offset。（PDF pp. 11–14；後一句是代理解讀）
4. RET n 返回後另外回收 n bytes；LOCAL、ENTER／LEAVE 展示局部配置與恢復。（PDF pp. 16、21–30）
5. MOV 讀內容，LEA 計算有效位址；OFFSET／ADDR 用於特定組譯語境。（PDF pp. 24–25、32–35、43–44）
6. ASM 各自成 OBJ，再連成 EXE；include 放跨模組原型。（PDF pp. 46–49）
7. CountMatches 基本題按相同位置計數得 2，加分題跨位置計數得 5；原題假設沒有重複。（PDF pp. 50–51）

## 閱讀地圖

| PDF 實體頁 | 內容 | 原頁尾 |
| --- | --- | --- |
| 1–8 | 程序介面與原型 | 封面、2–8 |
| 9–20 | 框架、傳值／址、RET、小型別、Difference | 10–21 |
| 21–30 | 區域資料、LEA、ENTER／LEAVE、LOCAL | 23–31、33 |
| 31–40 | INVOKE／ADDR 與 PROC 例子 | 34–43 |
| 41–45 | FillArray、值與位址、TestStack | 44–48 |
| 46–49 | 多模組 | 49–52 |
| 50–51 | Homework 3 | 53–54 |

## 圖表、方法與核對

- AddTwo(5,6) 框架：+8=5、+12=6；可從兩次參數 PUSH、CALL、PUSH EBP 各 4 bytes 推出。（PDF pp. 12、15、18）
- 區域 x、y 在 −4、−8，兩個 DWORD 共 8 bytes；TestStack 的 10-byte 陣列在原圖占 12-byte 框架配置。（PDF pp. 23、45）
- Ex1Array 第四元素 50=32h；原圖 EAX／EBX 為值，ECX／EDX 為 00404010h。固定地址只屬圖中的該次執行。（PDF pp. 43–44）
- pp. 34、41、43 是遮答案頁，文字擷取會取得部分被遮內容；以視覺呈現為準，答案在 pp. 35、42、44 對照。不誤稱遮住的內容在原頁可見。

## 勘誤與適用條件（代理核對／推論）

| 頁碼 | 原文或簡化 | 教材處理 |
| --- | --- | --- |
| 2、6、36 | 64-bit 不適用警語 | 限制於本章參數語法；PROC 本身有 ml64 FRAME 形式，見官方查證 |
| 10 | 同名 DumpMem 的兩種介面 | 不能只改 caller 就假設函式實作會改；未取得對應堆疊版本 |
| 17 | C/C++ 固定使用 EBP | 只針對使用 frame pointer 的例子，最佳化／ABI 不一定如此 |
| 19 | 16-bit PUSH 可能 fault；只示範 MOVZX | 非必然 fault，p.45 顯示 2-byte PUSH；有號擴充須保留符號 |
| 21 | 只有程序內能修改區域變數 | 名稱作用域與指標可存取性要分清；區域儲存釋放不等於清零 |
| 22 | MOV [EBP-4],立即值 | 以 DWORD PTR 明確指定寬度 |
| 32 | [EBX] 被稱位址運算式 | 普通間接運算元讀的是內容，不能等同 ADDR／EBX |
| 34–35 | Arrary | 修正為已宣告的 Array；原檔不改 |
| 41–42 | fillVal:BYTE 後漏逗號 | 補逗號；原迴圈假設長度>0，教學另加入口檢查與 ESI 保存條件 |
| 45 | MOV AX 後 PUSH EAX；RET 8 | 高半部未清零；依賴自動 epilogue 還原框架，不能套到裸 RET |
| 47 | 模組程序自動隱藏 | 實際須檢查 PROC 可見性／OPTION 設定，不猜預設 |
| 50–51 | bonus 匹配 | 無重複前提；有重複時如何計數仍須另訂規格 |

## 知識連結與後續問題

[組合語言主題](../topics/組合語言.md) · [堆疊框架與呼叫慣例](../concepts/堆疊框架與呼叫慣例.md) · [值、位址與 MASM 定址](../concepts/值與位址及MASM定址.md) · [CountMatches 問答](../questions/CountMatches如何區分位置與跨位置匹配.md) · [Microsoft 官方有限查證](web-20261105-microsoft-masm-procedures.md)。

線性代數教材僅作製作與閱讀介面參考，不作本章機器指令的證據。外部證據與本地 PDF 分列，原文與代理修正分列。

## 閱讀進度與限制

已讀 PDF pp. 1–51，無未讀頁段；全頁影像已核對聯絡表，程式與圖中疑點另放大。Poppler 曾警告 Symbol／ArialUnicode 替代字型，圖像實查中關鍵 ASCII 指令與數值可辨識，未以擷取亂碼補造文字。模型運算與網站檢查另見交付紀錄；未把文件內要求當作執行授權，也未執行原 PDF 程式。未上傳／發布原檔。
