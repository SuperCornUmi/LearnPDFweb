# 組合語言第八章｜16 張精簡簡報

以教學主線合併 PDF 多頁；完整內容見 [逐頁 notes](../../notes/assembly-language/chapter-8.md)。

## 投影片 1｜從 CALL／RET 到完整程序介面

- 主線：介面 → 引數 → 框架 → 區域資料 → 跨模組
- 32 位元 MASM；本章堆疊模型不直接套到 x64
- 保留 51 個 PDF 頁碼，重複頁與練習頁不略過

依據：PDF pp. 1–9；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-1)。

## 投影片 2｜PROTO、PROC、INVOKE 各做什麼

- PROTO：先提供參數介面
- PROC...ENDP：定義程序主體
- INVOKE：依原型及呼叫慣例準備引數並呼叫

依據：PDF pp. 2–8；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-2)。

## 投影片 3｜傳值與傳址：堆疊裡放了什麼

- 傳值：複製 5、6；改副本不直接改原變數
- 傳址：複製 A、A+4；解參考才能改原資料
- 參數槽大小與被指向資料大小是兩回事

依據：PDF pp. 10–15；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-10)。

## 投影片 4｜5、6 如何走進 AddTwo

- PUSH 6 → PUSH 5 → CALL AddTwo
- CALL 再壓入返回位址
- PUSH EBP；MOV EBP,ESP 後：+8 是 5，+12 是 6

依據：PDF pp. 9、12、15、18；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-9)。

## 投影片 5｜RET 8 的 8 是 bytes

- 先取回 4-byte 返回位址，再略過 8-byte 引數
- 框架與保存暫存器須先恢復
- 清理由誰做取決於慣例；不能重複清除

依據：PDF pp. 11、16–18、39；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-11)。

## 投影片 6｜減法測出參數順序

- Difference(30,14) 應得到 16
- MOV EAX,[EBP+8]；SUB EAX,[EBP+12]
- 右至左壓入不代表算式也反過來

依據：PDF pp. 18–20；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-18)。

## 投影片 7｜小型別與 PUSH 寬度

- BYTE 不可直接用 PUSH r/m8
- 無號小值用 MOVZX；有號值須留意 MOVSX
- PUSH AX 減 2，PUSH EAX 減 4；與介面配置須一致

依據：PDF pp. 19、45；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-19)。

## 投影片 8｜區域變數放在 EBP 的另一側

- 參數常在正偏移；區域資料常在負偏移
- 兩個 DWORD 共保留 8 bytes
- 每次呼叫各有框架；LOCAL 不會自動初始化

依據：PDF pp. 21–23、28–30；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-21)。

## 投影片 9｜MOV、OFFSET、LEA、ADDR

- MOV：依運算元讀值
- OFFSET：靜態可決定的偏移；LEA：執行時計算有效位址
- ADDR：INVOKE 的取位址語法；指標不等於內容

依據：PDF pp. 24–25、32–35、43–44；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-24)。

## 投影片 10｜ENTER／LEAVE 與自動框架

- ENTER 8,0：保存 EBP、建立基準、保留 8 bytes
- LEAVE：MOV ESP,EBP；POP EBP
- PROC／LOCAL 是組譯器語法；ENTER／LEAVE 是指令

依據：PDF pp. 26–30、39；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-26)。

## 投影片 11｜從具名參數到實際偏移

- val1 → DWORD PTR [EBP+8]
- val2 → DWORD PTR [EBP+0Ch]
- 指標參數先取位址，再用間接定址讀寫

依據：PDF pp. 36–40；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-36)。

## 投影片 12｜FillArray：可追蹤的迴圈

- ECX=長度；ESI=目前位址；AL=填入值
- MOV [ESI],AL → INC ESI → LOOP
- 修正逗號、0 長度入口及 ESI 保存條件

依據：PDF pp. 41–42；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-41)。

## 投影片 13｜暫存器實驗：值與位址分家

- Ex1Array+12 對應第四個 SDWORD：50=32h
- EAX=EBX=00000032h
- ECX=EDX=00404010h 是原圖該次執行的位址

依據：PDF pp. 43–45；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-43)。

## 投影片 14｜多模組：宣告、組譯、連結

- 各 ASM → 各 OBJ → link → 單一 EXE
- 共同 .inc 放跨模組原型，INCLUDE 分享宣告
- 可見性與連結輸入須配合；原型不等於實作

依據：PDF pp. 46–49；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-46)。

## 投影片 15｜CountMatches：先把基本規格寫清楚

- 輸入：兩個 PTR SDWORD 與共同長度
- 逐位置相等才累計；EAX 傳回
- 改動的其他暫存器須恢復；空陣列先返回

依據：PDF pp. 50–51；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-50)。

## 投影片 16｜基本 2、加分 5：同一資料不同問題

- 逐位置：只有 10 與 5 在同位置相等 → 2
- 跨位置：共同元素 10、5、4、−6、2 → 5
- 原題假設無重複；有重複時須重訂計數語意

依據：PDF pp. 50–51；[notes 對應頁段](../../notes/assembly-language/chapter-8.md#pdf-p-50)。

