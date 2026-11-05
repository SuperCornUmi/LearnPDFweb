---
title: "值、位址與 MASM 定址"
type: concept
created: 2026-11-05
updated: 2026-11-05
status: reviewed
tags: [組合語言, MASM, 程序]
source_ids: [src-20261105-assembly-ch8]
---

# 值、位址與 MASM 定址

[返回索引](../index.md) · [組合語言](../topics/組合語言.md) · [來源](../sources/src-20261105-assembly-ch8.md)

傳值把資料複製到引數槽；本章傳址把位址複製到槽，程序透過間接定址存取原資料。指標也是值，與它指向的內容是兩層。（[來源](../sources/src-20261105-assembly-ch8.md)，PDF pp. 11–14）

| 寫法 | 本章意思 | 依據 |
| --- | --- | --- |
| MOV EAX,具型別標號 | 讀取內容，不因省方括號就變成位址 | PDF pp. 43–44 |
| MOV EAX,[ESI] | 讀 ESI 所指位置的 DWORD | PDF p. 42；寬度依目的暫存器教學展開 |
| OFFSET 標號 | 靜態可決定的偏移 | PDF pp. 24–25、43 |
| LEA ESI,[EBP-8] | 依當前 EBP 算有效位址，不讀該處內容 | PDF pp. 24–25 |
| INVOKE ...,ADDR x | 以組譯器語法傳 x 的位址 | PDF pp. 32–35 |

原例 SDWORD 每格 4 bytes，+12 指第四元素 50。原圖讀值 EAX=EBX=32h，取址 ECX=EDX=00404010h，後者僅是該次執行範例。別把 [EBX] 視為無條件傳 EBX 位址，也別把 16 位元分段模型的 far pointer 與 flat offset 混同。（同來源，PDF pp. 32–35、43–44）

代理例：若 EBP=00100020h，[EBP−8] 存 20，LEA ESI,[EBP−8] 得 00100018h；MOV ESI,[EBP−8] 得 20。兩者用途不同。（依 PDF p. 25 展開）

相關：[框架](堆疊框架與呼叫慣例.md) · [CountMatches](../questions/CountMatches如何區分位置與跨位置匹配.md)。
