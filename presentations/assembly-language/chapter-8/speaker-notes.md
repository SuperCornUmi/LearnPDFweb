# 組合語言第八章｜16 張逐張講稿

對應 slides.md；每張交代目的、講解順序與易錯處。

## 投影片 1｜從 CALL／RET 到完整程序介面

教學目的：建立本章地圖。先詢問 CALL 如何知道回哪裡，再追問兩個數如何交給程序。說明介面、實作與呼叫慣例各負責一部分；先理解手動堆疊，再讀 MASM 的便利寫法。易錯處：把所有 PROC 都誤認為 64 位元不支援。

依據：PDF pp. 1–9；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-1)。

## 投影片 2｜PROTO、PROC、INVOKE 各做什麼

教學目的：分清組譯期與執行期。以 MySub 為例，先寫 PROTO，再寫呼叫，最後寫主體；原型沒有可執行實作。將 ArraySum 的指標及長度拆開讀。易錯處：漏掉 PROC 後或換行參數間的逗號。

依據：PDF pp. 2–8；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-2)。

## 投影片 3｜傳值與傳址：堆疊裡放了什麼

教學目的：以 AddTwo 與 Swap 比較。畫出變數與參數槽兩層：第一層是呼叫端資料，第二層是堆疊複本；用箭頭表示傳址。指出圖中 0 與 4 是簡化 offset，不能直接當作實際可用的絕對位址。

依據：PDF pp. 10–15；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-10)。

## 投影片 4｜5、6 如何走進 AddTwo

教學目的：自己推得偏移，不死背。令原 ESP=S，逐步寫出 S−4、S−8、S−12、S−16；最後 EBP=S−16，第一參數相差 8 bytes。用互動框架追蹤確認各個階段。

依據：PDF pp. 9、12、15、18；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-9)。

## 投影片 5｜RET 8 的 8 是 bytes

教學目的：區分返回位址和引數回收。帶學生從 POP EBP 後的 ESP 位置算起，RET 8 總共讓 ESP 增加 12。再比較只用 RET 並由 caller ADD ESP,8 的情況。易錯處：把 8 當成參數數量或含返回位址的大小。

依據：PDF pp. 11、16–18、39；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-11)。

## 投影片 6｜減法測出參數順序

教學目的：讓加法掩蓋不了順序錯誤。先讓讀者預測照抄上一張先取 +12 會怎樣，再求正確 30−14。說明手動框架版本與具名 PROC 版本二選一，避免重複 prologue。

依據：PDF pp. 18–20；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-18)。

## 投影片 7｜小型別與 PUSH 寬度

教學目的：拆開資料型別、參數槽與指令運算元寬度。先計算 x 的 78h 零擴充；再用 TestStack 的 FF58→FF54→FF52 追蹤。易錯處：宣稱 16-bit PUSH 每次都會 fault，或以為 MOV AX 會清掉 EAX 高半部。

依據：PDF pp. 19、45；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-19)。

## 投影片 8｜區域變數放在 EBP 的另一側

教學目的：畫 x 在 −4、y 在 −8，和參數 +8 比較。區分名稱作用域與儲存生命期，再說遞迴各層有各自 temp。易錯處：把局部變數當作其他程序絕對無法透過指標存取的資料。

依據：PDF pp. 21–23、28–30；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-21)。

## 投影片 9｜MOV、OFFSET、LEA、ADDR

教學目的：先用 EBP=00100020h 算 LEA [EBP−8] 得 00100018h，再假設該處存 20 比較 MOV 的結果。回到 Ex1Array+12，說明 MASM 具型別標號直接也是記憶體運算元。

依據：PDF pp. 24–25、32–35、43–44；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-24)。

## 投影片 10｜ENTER／LEAVE 與自動框架

教學目的：手動三行對照 ENTER，再把退出反向追蹤。區分釋放與清零。易錯處：丟棄應還原的保存暫存器，或同時保留 MASM 自動框架與重複手寫 prologue。

依據：PDF pp. 26–30、39；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-26)。

## 投影片 11｜從具名參數到實際偏移

教學目的：將 AddTwo 的兩個版本上下對照；0Ch=12 先換算，再從兩個 4-byte 框架項目推偏移。以 Swap 的 PTR DWORD 和 ReadFile 的 PTR BYTE 區分指向型別與指標寬度。

依據：PDF pp. 36–40；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-36)。

## 投影片 12｜FillArray：可追蹤的迴圈

教學目的：用三個 byte 都填 7 的例子追蹤三輪。先在遮答案頁推理缺少運算元，再看揭露頁。易錯處：arraySize=0 仍先寫一個 byte，LOOP 再下溢；指標非空也不等於有足夠可寫空間。

依據：PDF pp. 41–42；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-41)。

## 投影片 13｜暫存器實驗：值與位址分家

教學目的：把 12 bytes 除 4 得索引 3，讀出 50，再換十六進位。追問若陣列重新載入，哪一組通常不變？數值不因載入位址改變，但取址結果可能改變。不要把 DumpRegs 的旗標當成這幾條 MOV 做出的比較。

依據：PDF pp. 43–45；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-43)。

## 投影片 14｜多模組：宣告、組譯、連結

教學目的：以 main、輸入、加總、顯示模組畫資料流。修改介面時可能需重組所有依賴模組。易錯處：以為 INCLUDE 會自動連入函式實作，或把所有 PROC 都當作預設 private。

依據：PDF pp. 46–49；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-46)。

## 投影片 15｜CountMatches：先把基本規格寫清楚

教學目的：把規格變成迴圈不變量：已比較前 i 個位置，EAX 等於其中相等數。CMP 前將一側載入暫存器，兩個指標每輪加 4。原題另要求兩組陣列測試、PROTO 與 INVOKE，不能只交函式。

依據：PDF pp. 50–51；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-50)。

## 投影片 16｜基本 2、加分 5：同一資料不同問題

教學目的：逐對讀七個位置，再在第二陣列搜尋第一陣列各值，讓兩種算法差異可見。用互動比對改成無匹配或全匹配的資料。模型測試可驗證預期值，但不等於 MASM 原生機器碼已執行。

依據：PDF pp. 50–51；[notes 對應頁段](../../../notes/assembly-language/chapter-8.md#pdf-p-50)。

