from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
U=R/'teaching/assembly-language/chapter-8';U.mkdir(parents=True,exist_ok=True)
P=[]
def add(title,t,e,s=''):
    P.append(dict(page=len(P)+1,title=title,translation=t.strip(),explanation=e.strip(),supplement=s.strip()))
add('第八章：進階程序', '''《x86 處理器組合語言》第七版、全球版。作者 Kip R. Irvine；第八章：進階程序（Advanced Procedures）。投影片由作者製作，Pearson Education © 2015。

原頁授權聲明：可為個人或課堂用途修改、複製本投影片，但須保留版權聲明、作者姓名與標題。原檔完整保留此聲明；網站另用自製學習封面。''', '''本章要把「CALL 到某處，RET 回來」擴充成可重用的程序介面：呼叫者如何交付資料、被呼叫者如何找參數及區域變數、最後如何恢復堆疊。

閱讀先備是暫存器、MOV、PUSH／POP、CALL／RET 與基本定址。本教材主要採 32 位元 MASM、EBP 堆疊框架與類 stdcall 的例子；它不是所有 x86／C++／x64 程式的通用配置。''')
add('PROC：具名參數與型別', '''PROC 偽指令宣告程序，並可附上具名參數串列。基本表示為：
```asm
label PROC paramList
; 每個參數：paramName:type
```
paramList 內參數以逗號分隔。type 可為 BYTE、SBYTE、WORD 等標準組合語言型別，也可為指向這些型別的指標。原頁旁註「不適用於 64-bit 模式」。''', '''參數名稱是組譯器提供的符號，不是新增 CPU 暫存器。例如 val1:DWORD 告訴 MASM 此參數按 32 位元資料使用；p:PTR DWORD 表示傳入指標，指向 DWORD 資料，而不是直接傳入那個 DWORD。

帶參數的實際常用寫法是下一頁的「程序名 PROC, 參數串列」；本頁是概略語法。PROC 在組譯時建立程序結構及符號，CPU 執行的是它生成的指令。''', '''範圍釐清：本頁的 64-bit 警語應限於這套 32 位元具名堆疊參數用法，不能推成「ml64 完全沒有 PROC」。官方 PROC 文件另有 x64 的 FRAME 語法；見本單元 Microsoft 查證來源。''')
add('PROC：參數換行格式', '''參數串列可另起一行或多行，PROC 後須有逗號：
```asm
label PROC,
    paramList
```
可在同一行寫多個參數：
```asm
param1:type1, param2:type2, ..., paramN:typeN
```
也可每行一個；除最後一個參數外，各項之間仍須有逗號。原圖箭頭特別指出 PROC 後的逗號。''', '''換行只是排版，逗號才負責分隔。先看程序名稱，再列「名稱:型別」；如果第二行仍有下一個參數，上一行末尾要保留逗號。

這個規則在 PDF pp. 41–42 的 FillArray 將再次用到：原碼少一個分隔逗號，不應因換行而以為可以省略。''')
add('AddTwo：兩整數相加', '''AddTwo 接收兩個整數，以 EAX 傳回和：
```asm
AddTwo PROC,
    val1:DWORD, val2:DWORD
    mov eax,val1
    add eax,val2
    ret
AddTwo ENDP
```''', '''輸入是 val1 與 val2 兩個 DWORD；輸出是 EAX。MOV 先把 val1 的值複製到 EAX，ADD 再將 val2 加入。例如輸入 5 與 6，EAX 依序為 5、11。

這裡沒手寫 PUSH EBP，不代表沒有框架；在本章設定下，MASM 可依 PROC 參數產生進入／退出程式碼。PDF p. 39 會展示展開形式。DWORD 加法保留低 32 位元；若要判斷有號／無號溢位，還須檢查旗標，原例未做。''')
add('INVOKE：帶引數呼叫', '''32 位元模式的 INVOKE 偽指令可取代手動準備多個引數再 CALL 的寫法。
```asm
INVOKE procedureName [, argumentList]
```
引數串列可省略，項目以逗號分隔。引數可以是立即值與整數運算式、變數名稱、位址及 ADDR 運算式、暫存器名稱。''', '''argument 是呼叫端實際提供的資料，parameter 是程序端接收它的名稱。例如 INVOKE AddTwo,5,6 中，5、6 是引數，val1、val2 是參數。

INVOKE 是組譯時的便利語法；MASM 依原型及呼叫慣例安排引數並生成 CALL。它不是 CPU 另有一條能理解任意型別的 INVOKE 指令，亦不會自行替你判斷指標指向的記憶體是否有效。''')
add('PROTO：先宣告介面', '''PROTO 建立程序原型：
```asm
label PROTO paramList
```
原頁說明：64 位元模式不允許這裡的參數串列；每個以 INVOKE 呼叫的程序都要有原型，完整的程序定義也可充當自己的原型。''', '''原型告訴 MASM 名稱、參數型別與順序，讓呼叫點不必等到程序實作才知道如何傳參數。只有 PROTO 並不產生函式主體，也不能代替連結時的實作。

如果完整 PROC 定義在呼叫點之前，組譯器已有介面資訊；如果定義在後面或另一個模組，先寫 PROTO。原型與實作必須一致，否則呼叫端與被呼叫端可能對堆疊內容有不同解讀。''')
add('PROTO、INVOKE 與實作的位置', '''典型配置：程序原型放在程式前方，INVOKE 放在程式碼區段，程序實作稍後出現。
```asm
MySub PROTO             ; 程序原型
.code
INVOKE MySub            ; 呼叫
MySub PROC              ; 實作
    ; ...
MySub ENDP
```''', '''由上到下分清三件事：PROTO 宣告「有這個介面」，INVOKE 是執行時要發生的呼叫，PROC...ENDP 是被執行的主體。此例沒有參數，所以原型與呼叫都不附引數。

這張只是位置示意，省略主程序入口、正常結束及完整主體。若把片段逐字串成可執行流程，不能讓呼叫返回後又直接落入程序本體；完整程式要安排主程序的結束或跳轉。''')
add('ArraySum 的指標與長度原型', '''ArraySum 原型列出兩個參數：
```asm
ArraySum PROTO,
    ptrArray:PTR DWORD,  ; 指向陣列
    szArray:DWORD        ; 陣列大小
```''', '''ptrArray 是陣列第一個元素的位址；szArray 提供元素數，因為只有指標無法知道陣列長度。PTR DWORD 指出每個元素按 4 bytes 解讀，但指標本身在本章 flat 32 位元模型也是 4 bytes。

若三個 DWORD 位於 A、A+4、A+8，呼叫者傳 A 與 3；實作才知道要讀三次，每次位址加 4。這張只宣告介面，沒有相加流程或實際回傳值的程式。''')
add('堆疊框架的建立', '''堆疊框架（stack frame）也稱活動紀錄（activation record），是為一次程序呼叫保留的堆疊區域，包含返回位址、傳入參數、保存的暫存器與區域變數。

建立步驟：呼叫者先將引數壓入堆疊並呼叫程序；被呼叫者將 EBP 壓入堆疊，再令 EBP=ESP；需要區域變數時，從 ESP 減去固定大小以保留空間。''', '''堆疊向較低位址成長，所以 PUSH 會讓 ESP 變小。EBP 固定作為這次呼叫的定位基準，ESP 則可因 PUSH 或區域配置繼續移動。

本章典型框架內，[EBP] 是舊 EBP，[EBP+4] 是返回位址，[EBP+8] 起是參數，負偏移處放區域變數。這個配置由「32 位元近呼叫＋先存 EBP」推得；若省略 frame pointer 或換呼叫慣例，不能直接套用。''')
add('堆疊參數與暫存器參數', '''原頁認為堆疊參數較方便，並比較兩種呼叫方式，問哪種較容易：
```asm
; 暫存器介面
pushad
mov esi,OFFSET array
mov ecx,LENGTHOF array
mov ebx,TYPE array
call DumpMem
popad

; 假設採堆疊介面的版本
push TYPE array
push LENGTHOF array
push OFFSET array
call DumpMem
```''', '''兩段要交付的資訊相同：陣列起始位址、元素數及每個元素的 bytes 數。左段先保存通用暫存器，再設定 ESI／ECX／EBX；右段把三筆資料壓入堆疊，由程序依位置讀取。

右段比較簡潔的前提，是被呼叫程序真的採這種堆疊介面，並且雙方約定誰清除 12 bytes 的引數。PUSHAD／POPAD 也會保存及還原 EAX，所以不能把這個模板直接套在以 EAX 回傳結果的呼叫上。''', '''介面警告：這是「兩種可能介面」的比較，不代表只改呼叫端就能改用原本的同名函式。本教材未取得／執行所用 Irvine32 函式庫的對應實作，不把右段聲稱為可直接替換的已測試程式。''')
add('傳值呼叫的步驟', '''傳值（passing by value）：把引數的值壓入堆疊；原頁建議在保護模式只使用 32 位元值以維持堆疊對齊。接著呼叫程序，有傳回值時從 EAX 接收；若被呼叫者未移除引數，由呼叫者移除。''', '''傳值複製的是資料本身。被呼叫者改寫參數副本，並不因此改寫呼叫者原變數；如果值本身是位址，仍可透過該位址修改被指向物。

以兩個 DWORD 為例，參數共占 8 bytes。若 callee 用 RET 8 清除，caller 就不能再 ADD ESP,8；若 callee 只用 RET，caller 便須依約補回。少清或重複清都會破壞 ESP。這裡的 4-byte 建議不等於所有 ABI 的對齊規則。''')
add('傳值範例：CALL 前的 5 與 6', '''資料及呼叫：
```asm
.data
val1 DWORD 5
val2 DWORD 6
.code
push val2
push val1
call AddTwo
```
CALL 前的圖由高至低位址為 val2 的值 6、val1 的值 5；ESP 指向 5 所在的頂端。''', '''用 S 表示壓引數前的 ESP。PUSH val2 後 ESP=S−4，[S−4]=6；PUSH val1 後 ESP=S−8，[S−8]=5。因為先壓第二個引數，再壓第一個，引數一離返回位址最近。

圖上還沒有返回位址，因為它畫的是 CALL 之前。執行 CALL 才會再占 4 bytes；在 AddTwo 內建立框架後，5 對應 [EBP+8]，6 對應 [EBP+12]。''')
add('傳址呼叫的步驟', '''傳址（passing by reference）：將引數的偏移位址壓入堆疊，再呼叫程序；若有傳回值則從 EAX 接收。若被呼叫者未移除引數，呼叫者須移除。''', '''此處「傳址」的機制，是把位址當成引數值傳入。要交換兩個原變數，程序須先取得各位址，再讀寫該位址的內容；只交換堆疊上的指標副本不會交換原資料。

例如 p 指向 val1，MOV ESI,p 取得位址，MOV EAX,[ESI] 才讀到 val1。傳值與傳址在 PUSH 時都會複製某個 32 位元值，差別在這個值被雙方約定解讀成「資料」還是「指標」。''')
add('傳址範例：Swap 的兩個位址', '''原資料仍是 val1=5、val2=6，但改傳位址：
```asm
push OFFSET val2
push OFFSET val1
call Swap
```
CALL 前的示意圖顯示：val2 的 offset 為 00000004，val1 的 offset 為 00000000；ESP 指向 val1 的 offset。''', '''這次堆疊不是 6 和 5，而是兩個儲存位置。圖把資料起點簡化成 0，所以相鄰 DWORD 的偏移相差 4；不表示 Windows 實際把變數放在可直接使用的絕對位址 0。

若 val1 在 A，val2 就在 A+4。Swap 須把 [A] 與 [A+4] 的內容互換，結果 val1=6、val2=5。這些寫入是程序實作的責任；CALL 本身不會交換資料。''')
add('CALL 之後多出的返回位址', '''CALL 後的堆疊圖，由高至低位址為：val2 的值或位址、val1 的值或位址、返回位址；ESP 指向返回位址。''', '''近 CALL 一方面改變 EIP，使執行轉到程序入口；另一方面先把「CALL 後下一條指令的位置」壓入堆疊，以便 RET 回來。

承接前例，CALL 前 ESP=S−8，CALL 後 ESP=S−12。此時 [ESP] 是返回位址，[ESP+4] 是第一個參數，[ESP+8] 是第二個參數；這還不是 EBP 框架。再 PUSH EBP 之後，參數相對 EBP 的偏移才變成 +8、+12。''')
add('RET 與 RET n', '''RET 從子程序返回：將堆疊頂端彈入指令指標 EIP 或 IP，控制流程轉到該位址。
```asm
ret
ret n
```
選用的 n 表示在載入返回位址後，再把堆疊指標增加 n bytes。''', '''在本章 32 位元近返回中，RET 先消耗 4-byte 返回位址。RET 8 另外略過 8 bytes 的引數；總計 ESP 比執行前增加 12。

若目前 ESP 還指著區域變數或未 POP 的暫存器，RET 會把錯誤資料當成返回位址。故順序必須先恢復框架，再 RET；RET n 的 n 是 bytes 數，不是參數個數，也不是包含返回位址的總大小。''')
add('以 EBP 固定偏移存取參數', '''原頁說 C／C++ 函式以相對 EBP 的常數偏移存取堆疊參數，例如 [EBP+8]。EBP 稱為基底指標或框架指標，保存堆疊框架的基底；函式執行期間不改變 EBP，返回前須恢復它原本的值。''', '''固定 EBP 的好處是定位穩定：即使 ESP 因配置區域空間或 PUSH 暫存器改變，參數仍在原本的 EBP+8、EBP+12。程序用自己的 EBP 工作，結束時 POP 回呼叫者的 EBP，才能延續上一層框架。

這是使用 frame pointer 的教學模型。最佳化的 C／C++ 編譯結果可以省略 EBP 框架，其他 ABI 也可能用暫存器傳參數，因此「所有 C/C++ 函式都這樣存取」會超出原例適用範圍。''')
add('AddTwo：手動基底偏移定址', '''原頁 AddTwo(5,6) 的程式：
```asm
AddTwo PROC
    push ebp
    mov ebp,esp
    mov eax,[ebp+12]
    add eax,[ebp+8]
    pop ebp
    ret 8
```
圖中 [EBP] 是舊 EBP，[EBP+4] 是返回位址，[EBP+8]=5，[EBP+12]=6；此時 EBP 與 ESP 相同。''', '''先 PUSH EBP 保存舊框架，再 MOV EBP,ESP。讀 [EBP+12] 使 EAX=6，加入 [EBP+8] 的 5，得到 11。這裡把第二參數先讀入仍正確，是因為加法交換律；下一個減法練習不能照抄相同順序。

本例沒有區域變數或額外未還原的 PUSH，所以 POP EBP 前 ESP 仍等於框架基底，可直接取回舊 EBP。RET 8 接著返回並清除兩個 DWORD 引數。''')
add('8／16 位元引數的擴充', '''原頁提醒：不能直接 PUSH 8 位元值；PUSH 16 位元運算元可能造成 page fault 或 ESP 對齊問題。建議先以 MOVZX 將較小引數擴充為 32 位元：
```asm
.data
charVal BYTE 'x'
.code
movzx eax,charVal
push eax
call Uppercase
```''', ''''x' 的字元碼為 78h。MOVZX 把來源 8 位元值放入 EAX 低位並把高位清零，得到 00000078h；PUSH EAX 按 4 bytes 傳入，維持本章參數槽配置。

原頁的 fault 說法不是必然：PDF p. 45 就示範 PUSH AX 合法地讓 ESP 減 2。問題是混入 2-byte PUSH 後，ESP 不再維持原有 4-byte 邊界，與假設 4-byte 參數槽的介面可能不相容；不能說每次 PUSH AX 都會 fault。''', '''MOVZX 適合無號資料／字元。若要把有號 BYTE 的 −1 保持成 32 位元 −1，應使用符號擴充 MOVSX，否則零擴充會把 FFh 解讀成 255。這是依二補數表示補充的適用條件。''')
add('練習：Difference(30,14)', '''建立 Difference 程序，計算第一引數 Val1 減第二引數 Val2：Val1−Val2。
```asm
push 14              ; Val2
push 30              ; Val1
call Difference      ; 預期 EAX=16
```
CALL 前圖示 ESP 指向 30，其上一格為 14。''', '''這題檢查「壓入順序」和「算術順序」是否分得清楚。右至左壓入後，建立標準框架的第一引數在 +8，第二引數在 +12。

代理教學解法（手動框架版本）：
```asm
Difference PROC
    push ebp
    mov ebp,esp
    mov eax,[ebp+8]   ; 30
    sub eax,[ebp+12]  ; 30-14=16
    pop ebp
    ret 8
Difference ENDP
```
EAX 先載入被減數，再減去第二參數。若反過來，結果是 −16。此片段為教學推導，未經 MASM 組譯執行。''')
add('區域變數：範圍與生命期', '''原頁說明：只有子程序內的敘述能看見或修改區域變數；子程序結束時，它使用的儲存空間釋放。不同函式可有同名區域變數而不衝突。區域變數對遞迴程序及多個執行緒執行的程序十分重要。''', '''同名不衝突，首先是名稱的作用域不同；每次呼叫的儲存位置也可不同。遞迴每深入一次就建立一份新框架，因此每層的 temp 不會直接覆蓋上一層 temp。

「只有程序內可修改」是名稱可見性的簡化說法：如果把區域變數位址傳出去，其他程序仍能在它有效期間透過指標存取它。返回後不可繼續把該指標當成仍有效的區域儲存。區域變數也不保證整個程序就執行緒安全，仍要看共享資料。''')
add('手動配置兩個 DWORD 區域變數', '''明確配置區域變數時，從 ESP 減去所需總大小。原頁配置 locA 與 locB 兩個 32 位元區域變數並初始化：
```asm
MySub PROC
    push ebp
    mov ebp,esp
    add esp,-8
    mov [ebp-4],123456h ; locA
    mov [ebp-8],0       ; locB
    ; ...
```''', '''兩個 DWORD 共需 2×4=8 bytes。ADD ESP,−8 與 SUB ESP,8 效果相同，只保留空間，還不會自動清零；後面的 MOV 才分別寫入初值。

EBP−4 和 EBP−8 是各 4-byte 槽的起點。原碼沒有用具名型別或暫存器指明 MOV 的資料寬度，MASM 可能無法判定；可明確寫成 MOV DWORD PTR [EBP-4],123456h 及 MOV DWORD PTR [EBP-8],0。下一頁提供明確寬度的版本。結束時還須 MOV ESP,EBP、POP EBP 再返回。''')
add('x=10、y=20 的框架配置', '''用兩個 DWORD 區域變數表示 int x=10,y=20：
```asm
MySub PROC
    push ebp
    mov ebp,esp
    sub esp,8
    mov DWORD PTR [ebp-4],10
    mov DWORD PTR [ebp-8],20
```
圖由高至低位址：返回位址、保存的 EBP、x=10（EBP−4）、y=20（EBP−8）。''', '''如果建立框架後 EBP=B，SUB ESP,8 使 ESP=B−8。x 使用 B−4 至 B−1，y 使用 B−8 至 B−5；兩塊相鄰且不重疊。

DWORD PTR 是對記憶體存取寬度的指定，不是要把立即值變成指標。程式片段只展示進入與初始化，未展示退出；須先把 ESP 還原到 B，才能 POP 到保存的舊 EBP。''')
add('LEA：區域變數位址不能用 OFFSET', '''LEA 取得有效位址；OFFSET 運算子只能提供組譯／連結可決定的固定偏移。要取得堆疊參數或區域變數的位址，需要 LEA。原例：
```asm
CopyString PROC, count:DWORD
LOCAL temp[20]:BYTE
mov edi,OFFSET count  ; 無效運算元
mov esi,OFFSET temp   ; 無效運算元
; 應該用哪條指令？
```''', '''count 與 temp 的實際位置由當次呼叫的 EBP 決定，每次呼叫可不同；OFFSET 無法把目前執行時的 EBP 算進固定常數。

教學替代是 LEA EDI,count 與 LEA ESI,temp，由 MASM 將具名項目解析成框架相對定址。count 的位址與 count 的值不同：若要取數值用 MOV EDI,count；若要讓另一程序透過指標存取這個參數槽才取位址。''')
add('LEA 範例：EBP−8 的位址', '''假設區域變數在 [EBP−8]，要把該變數的位址放入 ESI。不能使用：
```asm
mov esi,OFFSET [ebp-8] ; 錯誤
```
應使用：
```asm
lea esi,[ebp-8]
```''', '''假設 EBP=00100020h，LEA 計算 00100020h−8=00100018h，將此位址放入 ESI；它不會讀取 00100018h 裡面儲存的數值。

若該位置存 20，MOV ESI,[EBP-8] 會得到 20，而 LEA ESI,[EBP-8] 得到 00100018h。這正是「值」與「位置」的差別；方括號在 LEA 中提供有效位址運算式，不表示本指令會解參考讀值。''')
add('ENTER：建立框架的指令', '''ENTER 為被呼叫程序建立堆疊框架：保存 EBP、設定框架基底、保留區域變數空間。
```asm
MySub PROC
    enter 8,0
```
在本例等價於：
```asm
push ebp
mov ebp,esp
sub esp,8
```''', '''第一個引數 8 指保留 8 bytes，第二個 0 表示此例不建立巢狀語言框架鏈。若執行前 ESP=S，保存 EBP 後為 S−4；令 EBP=S−4；再保留 8 bytes，ESP=S−12。

ENTER 是 CPU 指令，LOCAL／PROC 則是組譯器偽指令。這裡的等價展開只針對第二運算元為 0 的簡單情況；不要把所有 ENTER 的語意都縮成固定三行。''')
add('LEAVE：回收框架後再 RET', '''LEAVE 結束程序的堆疊框架。原頁程序先 ENTER 8,0，中間執行主體，然後 LEAVE、RET。
```asm
enter 8,0
; ...
leave
ret
```
本例 LEAVE 的等價操作：
```asm
mov esp,ebp           ; 釋放區域空間
pop ebp
```''', '''MOV ESP,EBP 把堆疊頂端直接移回保存舊 EBP 的位置，所以不必逐一 POP 區域變數。POP EBP 再把上一層框架基底恢復，這時 ESP 才指向返回位址，RET 因而能正確返回。

回收空間不是擦除內容；只是這段堆疊不再由本次呼叫占有。如果程序另外保存了 ESI／EBX 等必須還原的暫存器，應按它們實際存放的配置先還原；不能用 LEAVE 丟棄應恢復的值。''')
add('LOCAL：宣告有型別的區域變數', '''LOCAL 宣告區域變數串列，緊接在 PROC 後方，每個變數指定型別。
```asm
LOCAL varlist

MySub PROC
LOCAL var1:BYTE, var2:WORD, var3:SDWORD
```''', '''LOCAL 讓組譯器替你安排堆疊位置，主體中可直接用 var1、var2、var3，不必手算所有 EBP 偏移。BYTE 是 1 byte、WORD 是 2 bytes、SDWORD 是有號 4 bytes；實際配置還可能包含對齊空間，不能只把 1+2+4 當成所有版本必然生成的框架大小。

宣告只保留儲存空間，未給初值。若後續要累計 sum，必須先初始化，不能假設新區域變數從 0 開始。''')
add('LOCAL temp 的 MASM 展開', '''原始宣告：
```asm
Example1 PROC
LOCAL temp:DWORD
    ; ...
    ret
Example1 ENDP
```
原頁展示 MASM 生成的形式：
```asm
Example1 PROC
    push ebp
    mov ebp,esp
    add esp,0FFFFFFFCh ; ESP 加 -4
    ; ...
    mov esp,ebp
    pop ebp
    ret
Example1 ENDP
```''', '''32 位元二補數中 FFFFFFFCh 代表 −4，所以 ADD ESP,FFFFFFFCh 為 temp 保留 4 bytes。temp 在本例對應 [EBP−4]，而不是全域資料區的固定位置。

返回前先釋放區域空間、恢復舊 EBP，再取回返回位址。這張是「宣告與生成指令」的對照；不要把自動框架與同一份手寫框架一起重複放進同個帶參數程序，否則會多保存一次 EBP、偏移也會不同。''')
add('Example1 的框架圖', '''Example1 的堆疊框架圖：返回位址位於 EBP+4；舊 EBP 位於 EBP；區域 DWORD temp 位於 EBP−4。配置完成後 ESP 指向 temp，也就是 EBP−4。''', '''每格 4 bytes。EBP 保持基準不動，ESP 因 temp 的存在向下移一格；因此 EBP 和 ESP 不是永遠相同。

先辨認正方向：EBP+4 往較高位址找到返回位址，EBP−4 往較低位址找到區域變數。如果此時再 PUSH EAX，ESP 會變 EBP−8，但 temp 仍在 EBP−4。這就是用 EBP 而非不斷變動的 ESP 定位區域資料的原因。''')
add('再看 INVOKE 與 32 位元限制', '''本頁重述 INVOKE：32 位元模式下，可用它準備多個引數並呼叫程序。
```asm
INVOKE procedureName [, argumentList]
```
引數可為立即值／整數運算式、變數名稱、位址／ADDR 運算式或暫存器名稱；原頁再次標示不適用於 64-bit 模式。''', '''現在已看過框架，可把高階寫法與堆疊連起來：INVOKE 在呼叫端安排引數，PROC 在程序端為參數命名，兩者依同一原型與呼叫慣例配合。

在本章常見的右至左堆疊傳參數模型中，INVOKE AddTwo,5,6 可概念展開為 PUSH 6、PUSH 5、CALL AddTwo；其他呼叫慣例或引數型別不一定照此固定三行。Microsoft 官方 INVOKE 文件明列它是 32-bit MASM 用法。''')
add('INVOKE 的四種引數', '''原頁資料與範例：
```asm
.data
byteVal BYTE 10
wordVal WORD 1000h
.code
INVOKE Sub1,byteVal,wordVal ; 直接運算元
INVOKE Sub2,ADDR byteVal   ; 變數位址
INVOKE Sub3,eax,(10 * 20)  ; 暫存器、整數運算式
INVOKE Sub4,[ebx]         ; 原頁稱位址運算式／間接運算元
```''', '''Sub1 收到兩個變數的值；Sub2 收到 byteVal 的位址，兩者不能混淆。Sub3 的第二個引數是組譯時可計算的 200，第一個則取呼叫當時 EAX 的內容。

最後一行要釐清：普通 [EBX] 是讀 EBX 所指記憶體的內容，不等於傳 EBX 這個位址，也不等於 ADDR。只有該內容本身是一個有效指標且原型期望指標時，才構成傳入該指標；原型還須足以判定資料大小。這些範例省略各 Sub 的 PROTO，不能據此假設任意型別組合都可直接組譯。''')
add('ADDR：依記憶體模型取得指標', '''ADDR 在 32 位元 INVOKE 呼叫中可用來傳遞指標引數，依程式的記憶體模型回傳 near 或 far 指標。原頁對照：Small 模型為 16-bit offset；Large 模型為 32-bit segment/offset；Flat 模型為 32-bit offset。旁註不適用於 64-bit 模式。
```asm
.data
myWord WORD ?
.code
INVOKE mySub,ADDR myWord
```''', '''在本章 flat 32 位元環境，ADDR myWord 提供 myWord 的 32 位元位址；myWord 自己只有 2 bytes，這不影響指標的 4-byte 大小。

Small／Large 是原頁帶入的舊式分段記憶體模型對照；Large 的「32 位元」指 segment 與 offset 的組合寬度，不能當成 flat 32-bit 線性位址的同義詞。ADDR 是 INVOKE 的組譯器運算子；不是執行時的一條 CPU ADDR 指令。''')
add('INVOKE Swap：先自行展開', '''原頁宣告 20 個未初始化 DWORD，並要求對照 INVOKE 與相對應程式碼：
```asm
.data
Array DWORD 20 DUP(?)
.code
; ...
INVOKE Swap, ADDR Arrary, ADDR [Array+4]
```
原頁「Corresponding Code」下方以青色方塊遮住答案；下一頁揭露。''', '''先判斷要交換哪兩個物件：第一個是 Array[0]，第二個是 Array[1]。DWORD 每格 4 bytes，因此第二元素的位址是 Array+4，不是 Array+1。

教學推導：若第一參數為第一元素位址、第二參數為第二元素位址，採右至左傳入時要先壓 Array+4，再壓 Array。原頁 Arrary 是拼字錯誤，應為已宣告的 Array；保留原文並在下一頁給出修正形式。20 DUP(?) 只配置空間，未給可交換的確定初值。''')
add('INVOKE Swap：展開答案與拼字勘誤', '''本頁與前頁同題，原呼叫仍寫成：
```asm
INVOKE Swap, ADDR Arrary, ADDR [Array+4]
```
這次揭露對應程式碼：
```asm
push OFFSET Array+4
push OFFSET Array
call Swap
```
資料宣告仍為 Array DWORD 20 DUP(?)。''', '''勘誤：宣告的是 Array，呼叫中的 Arrary 應改為 Array。修正後概念寫法為 INVOKE Swap,ADDR Array,ADDR [Array+4]。

兩次 PUSH 都傳位址，不讀取陣列元素；原型可寫 Swap PROTO,pValX:PTR DWORD,pValY:PTR DWORD。交換過程才經由這兩個指標讀寫元素。如果陣列未先初始化，雖可談位址配置，卻不能宣稱交換後有哪兩個固定數值。''')
add('再看 PROC 參數宣告', '''本頁重述 PROC：宣告程序並可附具名參數串列；各參數以逗號分隔，形式為 paramName:type。型別可為 BYTE、SBYTE、WORD 等標準型別，或指向這些型別的指標。原頁列 label PROC paramList，並附 64-bit 不適用警語。''', '''前面已把參數看成框架中的位置，這裡可重新理解型別：名稱供人閱讀，型別讓 MASM 知道讀取幾 bytes，以及 INVOKE 應如何檢查引數。

例如 pValX:PTR DWORD 的參數槽保存位址；若寫 MOV EAX,pValX，是載入指標，不是直接讀取它指向的 DWORD。仍須再以 [EAX] 等間接定址解參考。PROC 這個指令本身也有 x64 形式，限制應讀成本章參數配置的限制。''')
add('再看參數串列與逗號', '''參數串列可放一行或多行；另起行時格式為：
```asm
label PROC,
    param1:type1,
    param2:type2,
    ; ...
    paramN:typeN
```
原頁另列同一行以逗號分隔的方式，並以箭頭指出 PROC 後的逗號不可省略。''', '''這是 PDF p. 3 的重複內容，仍保留實體頁碼。現在可以用它檢查後面 FillArray：fillVal:BYTE 後還有 arraySize:DWORD，所以兩者之間需要逗號。

程序宣告最後一個參數後不必為了換行再加逗號。不要把逗號放入名稱或型別，因為它是參數間的分隔符，而不是型別的一部分。''')
add('再看具名 AddTwo', '''AddTwo 接收兩整數，以 EAX 回傳和。本頁重列：
```asm
AddTwo PROC,
    val1:DWORD, val2:DWORD
    mov eax,val1
    add eax,val2
    ret
AddTwo ENDP
```''', '''把本頁與下一頁成對讀：這裡用 val1／val2，下一頁會改寫成 [EBP+8]／[EBP+0Ch]。因此具名參數讓原始碼更易讀，底層仍是框架相對存取。

程序承諾 EAX 帶回結果；輸入 5、6 時，MOV 取 5，ADD 得 11，退出框架不應把 EAX 用 POPAD 或其他還原操作覆蓋回舊值。''')
add('具名參數如何變成 EBP 偏移', '''MASM 將 AddTwo 的參數名稱轉成相對 EBP 的偏移；原頁展開：
```asm
AddTwo PROC
    push ebp
    mov ebp,esp
    mov eax,DWORD PTR [ebp+8]
    add eax,DWORD PTR [ebp+0Ch]
    leave
    ret 8
AddTwo ENDP
```''', '''0Ch 就是十進位 12。第一個參數的位移 +8，來自舊 EBP 的 4 bytes 與返回位址的 4 bytes；第二個再往上 4 bytes，所以是 +12。

LEAVE 恢復舊框架，RET 8 返回並清除兩個 DWORD 引數。這是講義在其 MASM 設定下展示的展開結果，不表示不同語言慣例、prologue 選項或版本必定逐字生成同樣指令。''')
add('Swap 與 ReadFile 的介面', '''原頁提供兩個程序範本：
```asm
Swap PROC,
    pValX:PTR DWORD,
    pValY:PTR DWORD
    ; ...
Swap ENDP

ReadFile PROC,
    pBuffer:PTR BYTE
LOCAL fileHandle:DWORD
    ; ...
ReadFile ENDP
```''', '''Swap 的兩個指標讓程序能改寫兩個 DWORD；ReadFile 的 pBuffer 是外部傳入的位址，而 fileHandle 是這次呼叫自己使用的區域 DWORD。

兩者在框架的位置性質不同：參數位於正偏移，區域變數通常在負偏移。PTR BYTE 表示緩衝區元素按 byte 解讀，不提供緩衝區長度或讀入上限。原頁只展示介面，省略實作及退出流程；此 ReadFile 名稱也不能據此認定為完整 Windows API 宣告。''')
add('FillArray：補上寫入與位址遞增', '''FillArray 接收 byte 陣列指標、要複製到每個元素的單一 byte 值，以及陣列大小。原頁程式骨架：
```asm
FillArray PROC,
    pArray:PTR BYTE, fillVal:BYTE
    arraySize:DWORD
    mov ecx,arraySize
    mov esi,pArray
    mov al,fillVal
L1: mov ; 運算元以青色遮住
    inc ; 運算元以青色遮住
    loop L1
    ret
FillArray ENDP
```
完整揭露在下一頁；原頁 fillVal:BYTE 後漏逗號。''', '''先依三個準備步驟推理：ECX 是剩餘次數，ESI 是目前元素位址，AL 是填入值。迴圈每次應把 AL 寫到 [ESI]，再將 ESI 加 1，才能移到下一個 BYTE。

教學填空為 MOV [ESI],AL 與 INC ESI。LOOP 會先讓 ECX 減 1，再於非零時跳回；因此本骨架需要 arraySize>0。若長度為 0，卻先進入主體，就會寫入不應寫的元素，之後還可能發生極長迴圈。''')
add('FillArray：完整流程與邊界修正', '''本頁揭露 FillArray 的迴圈：
```asm
FillArray PROC,
    pArray:PTR BYTE, fillVal:BYTE
    arraySize:DWORD
    mov ecx,arraySize
    mov esi,pArray
    mov al,fillVal
L1: mov [esi],al
    inc esi
    loop L1
    ret
FillArray ENDP
```
輸入及用途與前頁相同：將指定 byte 填入整個 byte 陣列。原碼仍漏了 fillVal 後的逗號。''', '''以 pArray=A、fillVal=7、arraySize=3 為例：初始 ECX=3、ESI=A、AL=7；三輪分別寫 [A]、[A+1]、[A+2]，每輪 ESI 加 1，ECX 依序變 2、1、0，最後不跳回。

教學修正分三件事：①在 fillVal:BYTE 後補逗號；②在第一次寫入前加 JECXZ Done，讓 0 長度直接退出；③若介面要求保存 ESI，使用 USES ESI 或正確的保存／還原。Done 應放在 RET 前。傳入非零長度時，也須確保緩衝區有至少該長度可寫；原例未做界限檢查。''')
add('讀值還是取位址：先預測結果', '''原頁陣列與指令：
```asm
.data
Ex1Array SDWORD 10,-20,30,50,40,-2
.code
main PROC
    mov eax,Ex1Array+12
    mov ebx,[Ex1Array+12]
    mov ecx,OFFSET Ex1Array+12
    lea edx,Ex1Array+12
    call DumpRegs
    ; ...
```
下方輸出在本頁以青色方塊遮住；下一頁揭露結果。''', '''每個 SDWORD 占 4 bytes，所以 +12 位移到索引 3 的第四元素 50。MASM 的具型別資料標號可直接表示記憶體運算元，因此前兩條 MOV 都讀取該元素的值；是否有方括號不是唯一判斷依據。

OFFSET 與 LEA 則都在此例取得第四元素的位址。先預測 EAX=EBX=50、ECX=EDX=該位址，再看下一頁。這個 MASM 語法不能直接類比其他組譯器的所有同形寫法。''')
add('讀值與取位址：暫存器結果', '''原碼與前頁相同。註解換算 50=16×3+2=00000032h。DumpRegs 圖顯示：
```text
EAX=00000032  EBX=00000032
ECX=00404010  EDX=00404010
ESI=00000000  EDI=00000000
EBP=0018FF90  ESP=0018FF88
EIP=0040101B  EFL=00000246
CF=0 SF=0 ZF=1 OF=0 AF=0 PF=1
```
前兩個是第四元素的值，後兩個是該次範例執行的位址。''', '''50 除 16 得商 3、餘 2，故十六進位為 32h。EAX／EBX 都是 00000032h；ECX／EDX 的 00404010h 則指向該資料。反推本次陣列起點為 00404010h−0Ch=00404004h。

位址只是這張圖的執行結果，重新連結或載入後可能不同。這段 MOV 與 LEA 不負責計算 50−某值，故不可把畫面上的 ZF=1 等旗標硬解成「剛做了比較」；旗標可能來自先前狀態。''')
add('TestStack：追蹤不同寬度的 PUSH', '''原頁程序及觀察值（十六進位）：
```asm
TestStack PROC,
    arg1:WORD,
    arg2:BYTE
LOCAL temp[10]:BYTE
    call DumpRegs         ; ESP=0019FF58, EBP=0019FF64
    mov ax,arg1
    push eax
    call DumpRegs         ; ESP=0019FF54
    push ax
    call DumpRegs         ; ESP=0019FF52
    push WORD PTR 10
    call DumpRegs         ; ESP=0019FF50
    push 10
    call DumpRegs         ; ESP=0019FF4C
    ret 8
TestStack ENDP
```
圖另記「呼叫 TestStack 前 ESP=0019FF74」。''', '''由 FF74 到框架 EBP=FF64 共減 10h=16 bytes，可與兩個各占 4 bytes 的引數槽、返回位址、舊 EBP 對應。LOCAL temp[10]:BYTE 後 ESP=FF58，比 EBP 再低 0Ch=12 bytes：圖展示了局部配置含對齊的情況，不只配置 10 bytes。

接著從 FF58 起，PUSH EAX 減 4，PUSH AX 減 2，PUSH WORD PTR 10 減 2，PUSH 10 在本模式減 4，得到 FF54、FF52、FF50、FF4C。MOV AX,arg1 只更新 EAX 的低 16 位，所以隨後 PUSH EAX 的高 16 位不可假定為零。

RET 8 清的是兩個引數槽，不是前面測試 PUSH 的 12 bytes。原頁依賴 MASM 自動 epilogue 恢復 ESP／EBP；如果改成完全手寫框架而直接 RET 8，會從錯誤位置取返回位址。圖中的 DumpRegs 數值視為觀察呼叫者狀態，並非要額外永久累計每個 CALL 的返回位址。''')
add('多模組程式的建置流程', '''多模組程式將原始程式分成不同 ASM 檔案。每個 ASM 檔案（模組）各自組譯為 OBJ；同一程式的全部 OBJ 再由 link 工具連結為單一 EXE。''', '''分清兩個階段：組譯器處理單個模組內的指令與符號，產生機器碼及待解析的外部符號；連結器把各模組放在一起，解析跨模組的名稱與位址。

所以 PROTO 能讓呼叫端知道介面，卻不能憑空補出程序的機器碼。若組譯成功但找不到外部函式實作，仍會在連結階段失敗。流程圖為「main.asm→main.obj」及「helper.asm→helper.obj」，兩者再一起連到程式 EXE。''')
add('多模組的優點與封裝條件', '''大型程式分成來源模組後較容易撰寫、維護、除錯。修改一行程式時，通常只需重新組譯它所屬的模組；已組譯模組的連結所需時間較少。模組可集中邏輯相關的程式與資料。

原頁把封裝說明為：程序與變數在模組內自動隱藏，除非將它們宣告為 public。''', '''拆分讓每個模組有可理解的責任，例如一個處理輸入、一個加總、一個顯示。修改加總實作時，若介面不變，其餘模組的原始碼可能不必重組。

但原頁的 public 說法需要條件：MASM 的程序可見性也受預設與選項影響，不能保證每個 PROC 自動 private。應檢查實際 PUBLIC／PRIVATE 及匯出符號設定。若共同 include 的介面變更，所有依賴它的模組也可能都要重組；「只重組一個」不是所有變更都成立。''')
add('建立多模組程式的步驟', '''基本步驟：建立主模組；為每個程序或一組相關程序建立獨立來源模組；建立 include 檔，放入外部程序（跨模組呼叫者）的原型；使用 INCLUDE 讓各模組都取得這些原型。''', '''先定介面，再分工實作。例如 main 呼叫 ArraySum，把 ArraySum 的 PROTO 放進共同 sum.inc；main.asm 與實作模組都 INCLUDE 它，讓型別與順序有共同依據。

INCLUDE 是組譯前／組譯時引入宣告內容，不會把另一個 OBJ 自動連入 EXE。仍要組譯實作模組並在連結時提供它；宣告、實作、可見性與連結輸入四件事都要配合。''')
add('sum.inc：三個外部程序的原型', '''sum.inc 包含不在 Irvine32 函式庫內的外部函式原型：
```asm
INCLUDE Irvine32.inc
PromptForIntegers PROTO,
    ptrPrompt:PTR BYTE,  ; 提示字串
    ptrArray:PTR DWORD,  ; 陣列
    arraySize:DWORD     ; 陣列大小
ArraySum PROTO,
    ptrArray:PTR DWORD,  ; 陣列
    count:DWORD         ; 元素數
DisplaySum PROTO,
    ptrPrompt:PTR BYTE,  ; 提示字串
    theSum:DWORD        ; 陣列總和
```''', '''三個介面串成資料流：PromptForIntegers 用提示字串引導輸入，把數值寫入陣列；ArraySum 根據陣列位址和長度求和；DisplaySum 接收提示及已算出的和。

前兩者都需要指標加長度，第三者接收的是總和值，不是指向總和的指標。此頁只有原型，未展示完整實作或所有回傳約定；不可僅憑原型就說已執行並得到結果。也不要以為 INCLUDE Irvine32.inc 已包含這三個自訂程序。''')
add('作業三：CountMatches 規格', '''撰寫 CountMatches：接收兩個有號雙字陣列的指標，以及第三個參數表示兩陣列共同長度。對每個第一陣列的元素 xᵢ，若同位置 yᵢ 相等，計數加一，最後用 EAX 回傳相等元素的數量。

另寫測試程式，呼叫 CountMatches 並傳入兩組不同的陣列配對。用 INVOKE 傳遞堆疊參數，為 CountMatches 建立 PROTO；程序改動的暫存器，除了 EAX 之外都須保存並還原。

加分題（額外 2 分）：計算所有相符元素，不限相同位置。''', '''基本題是逐位置比較，不是搜尋另一陣列任意位置。教學介面可寫 CountMatches PROTO,pX:PTR SDWORD,pY:PTR SDWORD,count:DWORD。

流程：EAX=0；若 count=0 直接返回；用兩個指標各讀一個 DWORD，以 CMP 判斷相等，相等才增加 EAX；兩指標各加 4，重複 count 次。CMP 不能直接同時使用兩個一般記憶體運算元，因此先把其中一個元素載入暫存器。

保存 ESI／EDI／ECX／EDX 等實際改動的暫存器；不要把 EAX 的結果還原掉。加分題可用外層取 xᵢ、內層搜尋 yⱼ；下一頁的「無重複元素」假設讓匹配數有明確集合交集解讀。''')
add('作業三：基本 2 筆、加分 5 筆', '''基本題對下列陣列回報 2 筆匹配：
```asm
array1 SDWORD 10,5,4,-6,2,11,12
array2 SDWORD 10,5,3,1,4,2,-6
```
加分題對相同兩陣列回報 5 筆匹配。原頁特別假設陣列中沒有重複元素。''', '''基本題依序比較：(10,10) 相等、(5,5) 相等，接著 (4,3)、(−6,1)、(2,4)、(11,2)、(12,−6) 都不相等，所以 EAX=2。

加分題允許跨位置，兩陣列共同元素為 10、5、4、−6、2，共 5 個。11 與 12 不在第二陣列，因此不計。若不允許位置不同的匹配，就不能把結果算成 5。

代理測試設計另包含空陣列、全相等、完全不相等與負數；演算法模型測試及 MASM 原生執行的狀態分別記錄在交付報告。若允許重複，須先決定是交集不同值數、成功找到的元素數，還是所有相等配對數，原題沒有替重複情況下定義。''')
assert len(P)==51
(U/'content.json').write_text(json.dumps(P,ensure_ascii=False,indent=2),encoding='utf-8')
print('Authored',len(P),'pages')
