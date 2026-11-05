---
title: "CountMatches 如何區分位置與跨位置匹配？"
type: question
created: 2026-11-05
updated: 2026-11-05
status: reviewed
tags: [組合語言, MASM, 程序]
source_ids: [src-20261105-assembly-ch8]
---

# CountMatches 如何區分位置與跨位置匹配？

[返回索引](../index.md) · [組合語言](../topics/組合語言.md) · [原題來源](../sources/src-20261105-assembly-ch8.md) · [notes](../../notes/assembly-language/chapter-8.md#pdf-p-50)

## 證據與回答

基本題只計 xᵢ=yᵢ 的位置，兩陣列 10,5,4,−6,2,11,12 與 10,5,3,1,4,2,−6 只有前兩格相等，因此回傳 2。加分題不限制同位置，在原題「沒有重複元素」的假設下，共同值 10、5、4、−6、2 共 5 個。（[來源](../sources/src-20261105-assembly-ch8.md)，PDF pp. 50–51）

## 代理演算法展開

基本題每輪讀兩個 DWORD，CMP 相等才增加 EAX，再把兩指標各加 4，做共同長度次。長度 0 在入口返回；除了 EAX，實際改寫的暫存器都要保存。這也串起 [指標](../concepts/值與位址及MASM定址.md) 與 [框架／介面](../concepts/堆疊框架與呼叫慣例.md)。（依原題 PDF p. 50 推導）

加分題可外層走 x、內層搜尋 y，時間 O(n²)；無重複時找到就退出內層，每個共同值只計一次。這是代理解題方法，不是原頁提供的程式。若允許重複，須先釐清計不同值、每個 x 的成功次數或全部配對，不能由原題例子唯一決定。

可重建的模型測試見 [驗證腳本](../../teaching/assembly-language/chapter-8/check_models.py)；結果與原生執行限制見 [交付紀錄](../../teaching/assembly-language/chapter-8/delivery.md)。
