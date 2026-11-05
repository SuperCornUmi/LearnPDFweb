from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
U=R/'teaching/assembly-language/chapter-8'
S=[]
def slide(title,bullets,speaker,refs):S.append(dict(number=len(S)+1,title=title,bullets=bullets,speaker=speaker,refs=refs))
slide('從 CALL／RET 到完整程序介面',['主線：介面 → 引數 → 框架 → 區域資料 → 跨模組','32 位元 MASM；本章堆疊模型不直接套到 x64','保留 51 個 PDF 頁碼，重複頁與練習頁不略過'],'教學目的：建立本章地圖。先詢問 CALL 如何知道回哪裡，再追問兩個數如何交給程序。說明介面、實作與呼叫慣例各負責一部分；先理解手動堆疊，再讀 MASM 的便利寫法。易錯處：把所有 PROC 都誤認為 64 位元不支援。','1–9')
slide('PROTO、PROC、INVOKE 各做什麼',['PROTO：先提供參數介面','PROC...ENDP：定義程序主體','INVOKE：依原型及呼叫慣例準備引數並呼叫'],'教學目的：分清組譯期與執行期。以 MySub 為例，先寫 PROTO，再寫呼叫，最後寫主體；原型沒有可執行實作。將 ArraySum 的指標及長度拆開讀。易錯處：漏掉 PROC 後或換行參數間的逗號。','2–8')
slide('傳值與傳址：堆疊裡放了什麼',['傳值：複製 5、6；改副本不直接改原變數','傳址：複製 A、A+4；解參考才能改原資料','參數槽大小與被指向資料大小是兩回事'],'教學目的：以 AddTwo 與 Swap 比較。畫出變數與參數槽兩層：第一層是呼叫端資料，第二層是堆疊複本；用箭頭表示傳址。指出圖中 0 與 4 是簡化 offset，不能直接當作實際可用的絕對位址。','10–15')
slide('5、6 如何走進 AddTwo',['PUSH 6 → PUSH 5 → CALL AddTwo','CALL 再壓入返回位址','PUSH EBP；MOV EBP,ESP 後：+8 是 5，+12 是 6'],'教學目的：自己推得偏移，不死背。令原 ESP=S，逐步寫出 S−4、S−8、S−12、S−16；最後 EBP=S−16，第一參數相差 8 bytes。用互動框架追蹤確認各個階段。','9、12、15、18')
slide('RET 8 的 8 是 bytes',['先取回 4-byte 返回位址，再略過 8-byte 引數','框架與保存暫存器須先恢復','清理由誰做取決於慣例；不能重複清除'],'教學目的：區分返回位址和引數回收。帶學生從 POP EBP 後的 ESP 位置算起，RET 8 總共讓 ESP 增加 12。再比較只用 RET 並由 caller ADD ESP,8 的情況。易錯處：把 8 當成參數數量或含返回位址的大小。','11、16–18、39')
slide('減法測出參數順序',['Difference(30,14) 應得到 16','MOV EAX,[EBP+8]；SUB EAX,[EBP+12]','右至左壓入不代表算式也反過來'],'教學目的：讓加法掩蓋不了順序錯誤。先讓讀者預測照抄上一張先取 +12 會怎樣，再求正確 30−14。說明手動框架版本與具名 PROC 版本二選一，避免重複 prologue。','18–20')
slide('小型別與 PUSH 寬度',['BYTE 不可直接用 PUSH r/m8','無號小值用 MOVZX；有號值須留意 MOVSX','PUSH AX 減 2，PUSH EAX 減 4；與介面配置須一致'],'教學目的：拆開資料型別、參數槽與指令運算元寬度。先計算 x 的 78h 零擴充；再用 TestStack 的 FF58→FF54→FF52 追蹤。易錯處：宣稱 16-bit PUSH 每次都會 fault，或以為 MOV AX 會清掉 EAX 高半部。','19、45')
slide('區域變數放在 EBP 的另一側',['參數常在正偏移；區域資料常在負偏移','兩個 DWORD 共保留 8 bytes','每次呼叫各有框架；LOCAL 不會自動初始化'],'教學目的：畫 x 在 −4、y 在 −8，和參數 +8 比較。區分名稱作用域與儲存生命期，再說遞迴各層有各自 temp。易錯處：把局部變數當作其他程序絕對無法透過指標存取的資料。','21–23、28–30')
slide('MOV、OFFSET、LEA、ADDR',['MOV：依運算元讀值','OFFSET：靜態可決定的偏移；LEA：執行時計算有效位址','ADDR：INVOKE 的取位址語法；指標不等於內容'],'教學目的：先用 EBP=00100020h 算 LEA [EBP−8] 得 00100018h，再假設該處存 20 比較 MOV 的結果。回到 Ex1Array+12，說明 MASM 具型別標號直接也是記憶體運算元。','24–25、32–35、43–44')
slide('ENTER／LEAVE 與自動框架',['ENTER 8,0：保存 EBP、建立基準、保留 8 bytes','LEAVE：MOV ESP,EBP；POP EBP','PROC／LOCAL 是組譯器語法；ENTER／LEAVE 是指令'],'教學目的：手動三行對照 ENTER，再把退出反向追蹤。區分釋放與清零。易錯處：丟棄應還原的保存暫存器，或同時保留 MASM 自動框架與重複手寫 prologue。','26–30、39')
slide('從具名參數到實際偏移',['val1 → DWORD PTR [EBP+8]','val2 → DWORD PTR [EBP+0Ch]','指標參數先取位址，再用間接定址讀寫'],'教學目的：將 AddTwo 的兩個版本上下對照；0Ch=12 先換算，再從兩個 4-byte 框架項目推偏移。以 Swap 的 PTR DWORD 和 ReadFile 的 PTR BYTE 區分指向型別與指標寬度。','36–40')
slide('FillArray：可追蹤的迴圈',['ECX=長度；ESI=目前位址；AL=填入值','MOV [ESI],AL → INC ESI → LOOP','修正逗號、0 長度入口及 ESI 保存條件'],'教學目的：用三個 byte 都填 7 的例子追蹤三輪。先在遮答案頁推理缺少運算元，再看揭露頁。易錯處：arraySize=0 仍先寫一個 byte，LOOP 再下溢；指標非空也不等於有足夠可寫空間。','41–42')
slide('暫存器實驗：值與位址分家',['Ex1Array+12 對應第四個 SDWORD：50=32h','EAX=EBX=00000032h','ECX=EDX=00404010h 是原圖該次執行的位址'],'教學目的：把 12 bytes 除 4 得索引 3，讀出 50，再換十六進位。追問若陣列重新載入，哪一組通常不變？數值不因載入位址改變，但取址結果可能改變。不要把 DumpRegs 的旗標當成這幾條 MOV 做出的比較。','43–45')
slide('多模組：宣告、組譯、連結',['各 ASM → 各 OBJ → link → 單一 EXE','共同 .inc 放跨模組原型，INCLUDE 分享宣告','可見性與連結輸入須配合；原型不等於實作'],'教學目的：以 main、輸入、加總、顯示模組畫資料流。修改介面時可能需重組所有依賴模組。易錯處：以為 INCLUDE 會自動連入函式實作，或把所有 PROC 都當作預設 private。','46–49')
slide('CountMatches：先把基本規格寫清楚',['輸入：兩個 PTR SDWORD 與共同長度','逐位置相等才累計；EAX 傳回','改動的其他暫存器須恢復；空陣列先返回'],'教學目的：把規格變成迴圈不變量：已比較前 i 個位置，EAX 等於其中相等數。CMP 前將一側載入暫存器，兩個指標每輪加 4。原題另要求兩組陣列測試、PROTO 與 INVOKE，不能只交函式。','50–51')
slide('基本 2、加分 5：同一資料不同問題',['逐位置：只有 10 與 5 在同位置相等 → 2','跨位置：共同元素 10、5、4、−6、2 → 5','原題假設無重複；有重複時須重訂計數語意'],'教學目的：逐對讀七個位置，再在第二陣列搜尋第一陣列各值，讓兩種算法差異可見。用互動比對改成無匹配或全匹配的資料。模型測試可驗證預期值，但不等於 MASM 原生機器碼已執行。','50–51')
(U/'slides.json').write_text(json.dumps(S,ensure_ascii=False,indent=2),encoding='utf-8')
refs=[dict(title='組合語言第八章｜原始 PDF',url='raw/pdfs/1151 ch8.pdf',detail='主要來源 · PDF pp. 1–51 · Kip R. Irvine · 2015 版投影片與課堂增補混編')]
for slug,title,detail in [('invoke','INVOKE','正文與語法；32-bit MASM 的適用範圍'),('proc','PROC','語法與 Remarks；含 x64 FRAME，未使用其完整例程'),('proto','PROTO','定義、語法與參數；原型與語言慣例'),('local-masm','LOCAL','程序內 LOCAL 的語法與生命期'),('option-masm','OPTION','選項列表中的 PROC／PROLOGUE／EPILOGUE'),('public-masm','PUBLIC','定義與語法；跨模組可見性')]:
    refs.append(dict(title='Microsoft Learn｜'+title,url=f'https://learn.microsoft.com/en-us/cpp/assembler/masm/{slug}?view=msvc-170',detail='2026-11-05 有限查證：'+detail))
refs += [dict(title='Microsoft Learn｜__stdcall',url='https://learn.microsoft.com/en-us/cpp/cpp/stdcall?view=msvc-170',detail='僅正文及 Remarks 表：右至左、callee 清引數；未匯入範例'),dict(title='Microsoft Learn｜x64 calling convention',url='https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170',detail='僅 defaults、alignment、parameter passing：釐清本章與 Windows x64 範圍；其餘未使用')]
meta=dict(key='assembly-language/chapter-8',course='assembly-language',courseName='組合語言',courseTag='COMPUTER SYSTEMS · x86',courseDescription='從資料、位址與堆疊，理解程序如何運作。',unit='chapter-8',label='第八章',number=8,title='進階程序與堆疊框架',english='Advanced Procedures',pdf='raw/pdfs/1151 ch8.pdf',assetBase='website/assets/assembly-ch8/',sourceWiki='wiki/sources/src-20261105-assembly-ch8.md',sourceId='src-20261105-assembly-ch8',externalSourceId='web-20261105-microsoft-masm-procedures',downloads='website/downloads/assembly-chapter-8',script='website/lessons/assembly-chapter-8.js',groups=[['程序介面',1,8],['堆疊與參數',9,20],['區域變數與框架',21,30],['MASM 呼叫與定址',31,40],['程式追蹤',41,45],['多模組',46,49],['作業與比對',50,51]],diagrams='assembly',expectedPages=51,references=refs,referenceNote='51 頁完整對應；保留原教材與遮答案頁，勘誤及適用條件另列於來源與 notes。程式碼未經 MASM／Irvine32 原生組譯執行，模型驗證與網站驗收分別記錄。外部文獻需連網；使用範圍見 Wiki。')
(U/'config.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
def write(path,text):
    p=R/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def front(title,kind,ids,status='reviewed'):
    return f'---\ntitle: "{title}"\ntype: {kind}\ncreated: 2026-11-05\nupdated: 2026-11-05\nstatus: {status}\ntags: [組合語言, MASM, 程序]\nsource_ids: [{ids}]\n'
sid=meta['sourceId'];wid=meta['externalSourceId']
webbody='''# Microsoft MASM 程序：有限外部查證

查閱日：2026-11-05。來源作者：Microsoft。以下只記實際讀過的網頁段落，沒有完整匯入 MASM、Irvine32 或處理器手冊。全文未下載；保留網址及轉述查閱紀錄。Microsoft 網頁的登入提示以外，正文由瀏覽工具實際取得。

'''
for r in refs[1:]:webbody+=f'- [{r["title"]}]({r["url"]})：{r["detail"]}。\n'
webbody+='''
## 採用的結論與交叉核對

- INVOKE 文件明列 32-bit MASM；PROC 文件同時列出 ml64 的 FRAME，故本地 PDF pp. 2、36 的警語不能擴大成「64 位元沒有 PROC」。
- PROTO 提供程序原型；LOCAL 在程序中建立生命期限於該程序的堆疊變數。與 PDF pp. 6–8、21、28–30 對照。
- __stdcall 表明右至左傳參數、callee 清理堆疊；與 PDF pp. 12、18、39 的範例一致。本地講義沒有完整建置選項，因此稱「類 stdcall 教學配置」，不猜每段實際設定。
- Windows x64 前四個整數位置通常使用 RCX、RDX、R8、R9，並有 shadow space 與對齊要求。此項只用來限制本章 32 位元模型的外推，不製作 x64 教材。
- PROC 語法允許 PUBLIC／PRIVATE／EXPORT，OPTION 列出 PROC 與框架選項，PUBLIC 將名稱供其他模組使用。足以提醒 PDF p. 47 的「自動隱藏」不能取代實際可見性設定；本文未斷言每版 MASM 的預設值。

## 未採用／未完成

未閱讀 x64 unwind 的完整規則、未執行官方範例，也未核對特定 Irvine32 函式庫版本；不把搜尋結果摘要當成正文證據。沒有其他待匯入候選。
'''
write('raw/web/microsoft-masm-procedures-20261105.md',webbody)
write(f'wiki/sources/{wid}.md',front('Microsoft：MASM 程序與呼叫慣例有限查證','source',wid,'partial')+'source_file: "raw/web/microsoft-masm-procedures-20261105.md"\nauthors: [Microsoft]\npublished: null\ncoverage: "8 個官方頁面指定段落；未完整閱讀官方手冊"\nextraction: "瀏覽工具讀取實際正文；轉述紀錄"\n---\n\n'+webbody+'\n[返回索引](../index.md) · [查閱紀錄](../../raw/web/microsoft-masm-procedures-20261105.md) · [PDF 來源](src-20261105-assembly-ch8.md) · [堆疊概念](../concepts/堆疊框架與呼叫慣例.md)\n')
write(f'wiki/sources/{sid}.md',front('組合語言第八章：進階程序','source',sid)+'''source_file: "raw/pdfs/1151 ch8.pdf"
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
''')
write('wiki/topics/組合語言.md',front('組合語言','topic',sid+', '+wid)+'''---

# 組合語言

[返回索引](../index.md) · [來源](../sources/src-20261105-assembly-ch8.md) · [教材](../../notes/assembly-language/chapter-8.md) · [網站](../../index.html#/assembly-language)

目前只有第八章，先備的暫存器、基本定址與迴圈章節尚未匯入。這是一份 32 位元 MASM 教材，不等同完整組合語言課程。

主線依序為「[值與位址](../concepts/值與位址及MASM定址.md) → [堆疊框架](../concepts/堆疊框架與呼叫慣例.md) → 程序介面與區域變數 → 多模組 → [陣列匹配](../questions/CountMatches如何區分位置與跨位置匹配.md)」。（[第八章來源](../sources/src-20261105-assembly-ch8.md)，PDF pp. 2–51；順序為代理教學編排）

必要條件：同一個程序的 caller／callee 必須共用參數型別、順序與清理規則；不能把 32 位元 EBP 模型直接改名成 RBP 就當作 x64。（同來源，PDF pp. 9–18、31–40；[官方範圍查證](../sources/web-20261105-microsoft-masm-procedures.md)）

後續可匯入先備章節與確切 Irvine32／MASM 工具版本；目前未驗證其原生編譯。課程視覺沿用線性代數，學科概念分開維護。
''')
write('wiki/concepts/堆疊框架與呼叫慣例.md',front('堆疊框架與呼叫慣例','concept',sid+', '+wid)+'''---

# 堆疊框架與呼叫慣例

[返回索引](../index.md) · [組合語言](../topics/組合語言.md) · [來源](../sources/src-20261105-assembly-ch8.md)

堆疊框架是一次呼叫所需參數、返回位址、保存暫存器與區域資料的組織；呼叫慣例則約定傳遞、回傳、保存與清理責任。框架是一種配置，不是每個 ABI 都固定採同樣 EBP 形式。（[來源](../sources/src-20261105-assembly-ch8.md)，PDF pp. 9、11、16–18）

## 32 位元兩個 DWORD 的推導（代理教學展開）

呼叫前 ESP=S。依序 PUSH 第二引數、PUSH 第一引數、CALL、PUSH EBP，每步減 4，最後 EBP=S−16。於是第一引數位置 S−8=EBP+8、第二引數 S−4=EBP+12；[EBP+4] 為返回位址，[EBP] 為舊 EBP。（同來源，PDF pp. 12、15、18）

保留兩個 DWORD 區域變數再 SUB ESP,8；位置在 −4、−8。LEAVE 先令 ESP=EBP，再 POP EBP；RET 8 再取返回位址並回收引數 8 bytes。RET 不會自動知道哪些一般 PUSH 應保存或捨棄。（同來源，PDF pp. 16、23、26–30）

## 邊界與錯誤

小型別的資料寬度不一定等於引數槽寬度；圖中 PUSH AX 只減 2，TestStack 的 WORD／BYTE 參數仍以共 8 bytes 清理。MOV AX 不會清 EAX 高 16 位。不要把它與 MOVZX 混為一談。（同來源，PDF pp. 19、45）

官方 __stdcall 文件核對右至左與 callee 清理；官方 x64 文件顯示 Windows x64 使用另一套寄存器與堆疊約定。只採有限段落，不推廣為所有平台規則。（[Microsoft 查證](../sources/web-20261105-microsoft-masm-procedures.md)）

相關：[值與位址](值與位址及MASM定址.md) · [完整逐頁追蹤](../../notes/assembly-language/chapter-8.md#pdf-p-45)。
''')
write('wiki/concepts/值與位址及MASM定址.md',front('值、位址與 MASM 定址','concept',sid)+'''---

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
''')
write('wiki/questions/CountMatches如何區分位置與跨位置匹配.md',front('CountMatches 如何區分位置與跨位置匹配？','question',sid)+'''---

# CountMatches 如何區分位置與跨位置匹配？

[返回索引](../index.md) · [組合語言](../topics/組合語言.md) · [原題來源](../sources/src-20261105-assembly-ch8.md) · [notes](../../notes/assembly-language/chapter-8.md#pdf-p-50)

## 證據與回答

基本題只計 xᵢ=yᵢ 的位置，兩陣列 10,5,4,−6,2,11,12 與 10,5,3,1,4,2,−6 只有前兩格相等，因此回傳 2。加分題不限制同位置，在原題「沒有重複元素」的假設下，共同值 10、5、4、−6、2 共 5 個。（[來源](../sources/src-20261105-assembly-ch8.md)，PDF pp. 50–51）

## 代理演算法展開

基本題每輪讀兩個 DWORD，CMP 相等才增加 EAX，再把兩指標各加 4，做共同長度次。長度 0 在入口返回；除了 EAX，實際改寫的暫存器都要保存。這也串起 [指標](../concepts/值與位址及MASM定址.md) 與 [框架／介面](../concepts/堆疊框架與呼叫慣例.md)。（依原題 PDF p. 50 推導）

加分題可外層走 x、內層搜尋 y，時間 O(n²)；無重複時找到就退出內層，每個共同值只計一次。這是代理解題方法，不是原頁提供的程式。若允許重複，須先釐清計不同值、每個 x 的成功次數或全部配對，不能由原題例子唯一決定。

可重建的模型測試見 [驗證腳本](../../teaching/assembly-language/chapter-8/check_models.py)；結果與原生執行限制見 [交付紀錄](../../teaching/assembly-language/chapter-8/delivery.md)。
''')
print('Wrote 16 slides, config, sources and knowledge pages')
