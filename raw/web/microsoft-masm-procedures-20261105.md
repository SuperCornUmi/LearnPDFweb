# Microsoft MASM 程序：有限外部查證

查閱日：2026-11-05。來源作者：Microsoft。以下只記實際讀過的網頁段落，沒有完整匯入 MASM、Irvine32 或處理器手冊。全文未下載；保留網址及轉述查閱紀錄。Microsoft 網頁的登入提示以外，正文由瀏覽工具實際取得。

- [Microsoft Learn｜INVOKE](https://learn.microsoft.com/en-us/cpp/assembler/masm/invoke?view=msvc-170)：2026-11-05 有限查證：正文與語法；32-bit MASM 的適用範圍。
- [Microsoft Learn｜PROC](https://learn.microsoft.com/en-us/cpp/assembler/masm/proc?view=msvc-170)：2026-11-05 有限查證：語法與 Remarks；含 x64 FRAME，未使用其完整例程。
- [Microsoft Learn｜PROTO](https://learn.microsoft.com/en-us/cpp/assembler/masm/proto?view=msvc-170)：2026-11-05 有限查證：定義、語法與參數；原型與語言慣例。
- [Microsoft Learn｜LOCAL](https://learn.microsoft.com/en-us/cpp/assembler/masm/local-masm?view=msvc-170)：2026-11-05 有限查證：程序內 LOCAL 的語法與生命期。
- [Microsoft Learn｜OPTION](https://learn.microsoft.com/en-us/cpp/assembler/masm/option-masm?view=msvc-170)：2026-11-05 有限查證：選項列表中的 PROC／PROLOGUE／EPILOGUE。
- [Microsoft Learn｜PUBLIC](https://learn.microsoft.com/en-us/cpp/assembler/masm/public-masm?view=msvc-170)：2026-11-05 有限查證：定義與語法；跨模組可見性。
- [Microsoft Learn｜__stdcall](https://learn.microsoft.com/en-us/cpp/cpp/stdcall?view=msvc-170)：僅正文及 Remarks 表：右至左、callee 清引數；未匯入範例。
- [Microsoft Learn｜x64 calling convention](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170)：僅 defaults、alignment、parameter passing：釐清本章與 Windows x64 範圍；其餘未使用。

## 採用的結論與交叉核對

- INVOKE 文件明列 32-bit MASM；PROC 文件同時列出 ml64 的 FRAME，故本地 PDF pp. 2、36 的警語不能擴大成「64 位元沒有 PROC」。
- PROTO 提供程序原型；LOCAL 在程序中建立生命期限於該程序的堆疊變數。與 PDF pp. 6–8、21、28–30 對照。
- __stdcall 表明右至左傳參數、callee 清理堆疊；與 PDF pp. 12、18、39 的範例一致。本地講義沒有完整建置選項，因此稱「類 stdcall 教學配置」，不猜每段實際設定。
- Windows x64 前四個整數位置通常使用 RCX、RDX、R8、R9，並有 shadow space 與對齊要求。此項只用來限制本章 32 位元模型的外推，不製作 x64 教材。
- PROC 語法允許 PUBLIC／PRIVATE／EXPORT，OPTION 列出 PROC 與框架選項，PUBLIC 將名稱供其他模組使用。足以提醒 PDF p. 47 的「自動隱藏」不能取代實際可見性設定；本文未斷言每版 MASM 的預設值。

## 未採用／未完成

未閱讀 x64 unwind 的完整規則、未執行官方範例，也未核對特定 Irvine32 函式庫版本；不把搜尋結果摘要當成正文證據。沒有其他待匯入候選。
