# 組合語言第八章｜圖解與追蹤

[互動網站](../../../index.html#/assembly-language/chapter-8/diagrams/) · [來源](../../../wiki/sources/src-20261105-assembly-ch8.md) · [逐頁 notes](../../../notes/assembly-language/chapter-8.md)

以下為依講義重繪的代理教學模型；位址為自編，不是實際執行截圖。假設 32 位元近呼叫、兩個 DWORD 引數、保存 EBP、兩個 DWORD 區域槽。

## 呼叫與返回

| 階段 | ESP | EBP | 重要內容 |
| --- | --- | --- | --- |
| 呼叫前 | 00100000h | 呼叫者值 | 尚無本次框架 |
| PUSH 6 | 000FFFFCh | 呼叫者值 | 第二引數 |
| PUSH 5 | 000FFFF8h | 呼叫者值 | 第一引數 |
| CALL | 000FFFF4h | 呼叫者值 | 返回位址在頂端 |
| PUSH EBP；MOV EBP,ESP | 000FFFF0h | 000FFFF0h | 舊 EBP；第一引數在 +8、第二在 +12 |
| SUB ESP,8 | 000FFFE8h | 000FFFF0h | 區域槽在 −4、−8 |
| LEAVE | 000FFFF4h | 呼叫者值 | 區域空間回收，恢復 EBP |
| RET 8 | 00100000h | 呼叫者值 | 取返回位址，再回收引數 |

依據：PDF pp. 9、12、15–18、23、27、39。正偏移走向較高位址，負偏移走向較低位址。保留空間不等於初始化，回收不等於清零。

## 值與位址兩層

```text
參數槽 p 存 A ── MOV ESI,p ──→ ESI=A
                                 │
                           MOV EAX,[ESI]
                                 ↓
                         EAX=位址 A 的內容
```

LEA 計算有效位址；本章 OFFSET 用於靜態可決定的偏移；ADDR 用於 INVOKE 的取位址語法。依據 PDF pp. 13–14、24–25、32–35、43–44。

## 多模組

```text
                sum.inc（共同原型）
                   ↓ INCLUDE
main.asm → main.obj ─┐
sum.asm  → sum.obj  ─┼─ link + libraries → program.exe
io.asm   → io.obj   ─┘
```

INCLUDE 提供宣告，不等於自動提供實作。跨模組可見性須檢查 PUBLIC／PRIVATE 等設定。依據 PDF pp. 46–49；可見性限制另見 [官方查證](../../../wiki/sources/web-20261105-microsoft-masm-procedures.md)。

## CountMatches 比較

| i | X | Y | 同位置相等 | X 在 Y 任意位置出現 |
| --- | --- | --- | --- | --- |
| 0 | 10 | 10 | 是 | 是 |
| 1 | 5 | 5 | 是 | 是 |
| 2 | 4 | 3 | 否 | 是 |
| 3 | −6 | 1 | 否 | 是 |
| 4 | 2 | 4 | 否 | 是 |
| 5 | 11 | 2 | 否 | 否 |
| 6 | 12 | −6 | 否 | 否 |

基本題得 2，加分題得 5；原題假設無重複元素。依據 PDF pp. 50–51。網站可修改等長、無重複的有號 32 位元整數陣列；空陣列回傳 0。互動使用 JavaScript 模型，不是 MASM 模擬器。
