from pathlib import Path
R=Path(__file__).resolve().parent.parent
entry='''
## [2026-11-05] ingest | 組合語言第八章：進階程序

- 依統一標準 v1.1 及既有線性代數教材結構製作。提供的 1151 ch8.pdf 已保留原名複製至 raw/pdfs/，SHA-256 d0ba6fff2d0cb5dd3e155f267023b8d1cf4a516418b1a38b130b9842d6735be4，與 Downloads 原檔一致。未改寫既有原始來源，未發布或上傳。
- 全部閱讀 PDF pp. 1–51；分頁文字與 51 頁渲染／聯絡表放 work/src-20261105-assembly-ch8/，pp. 34、41、44、45 另放大。保留封面、重複頁、遮答案頁及作業；以實體頁序引用，另列不同的內文頁碼。字型替代警告、版本與講義發布日期未知等限制記於來源。
- 新增來源摘要、組合語言主題、堆疊框架／呼叫慣例、值與位址／MASM 定址概念及 CountMatches 問答；補足雙向連結，更新 wiki/index.md、overview.md 與專案／網站說明。線性代數僅作教材與網站參考，不作本章學科證據。
- 有限外部查證實際讀取 8 個 Microsoft 官方頁面指定段落；raw/web 與 Wiki 分別記錄，維持 partial。釐清 INVOKE 32-bit 限制、PROC x64 FRAME、PROTO／LOCAL、stdcall 與可見性條件；其餘未讀內容不使用。
- 完成 notes/assembly-language/chapter-8.md 的 51 頁完整翻譯與講解、presentations/assembly-language/chapter-8/ 的 16 張精簡簡報及逐張講稿、圖解 Markdown。原文與教學修正分列；含 Arrary、FillArray 逗號與 0 長度、PUSH 寬度、指標與位址及自動框架條件等勘誤／提醒。
- teaching/assembly-language/chapter-8/ 保存 JSON 原稿、設定、可重建生成器、manifest、模型檢查與交付紀錄。生成 notes、網站資料及下載採同一份頁面與簡報內容；原稿及既有課程不互相覆蓋。
- 根 index.html 新增組合語言／第八章獨立註冊，新增 50 張原頁 WebP 與自製 SVG 封面；加入程式碼縮排呈現、混編頁碼、課程自己的名稱／說明。圖解含 8 階段堆疊追蹤、值／指標關係、多模組流程與可輸入陣列的 CountMatches 比較；共用閱讀器補末頁較短時的頁尾判定。
- 驗收：51 頁影像、頁碼／目錄搜尋／跳頁／鍵盤／放大、專注閱讀偏好與位置、獨立捲動、16 張簡報連點穩定／全螢幕、筆記／Markdown／下載／列印媒體、互動有效與無效輸入。1882×960、1255×640、390×844、768×900 全模式無頁面橫向溢出；桌面、矮視窗與手機截圖已視覺檢查；瀏覽器錯誤及載入失敗 0。
- 模擬 /sample-repo/ 網站子路徑，64 個本地腳本、樣式、下載、影像、PDF 與來源目標皆 HTTP 200。36 份 Markdown 的本地連結檢查無斷鏈，來源與 manifest 雜湊一致；線性代數 87／152 頁及原圖解仍可開啟。細節見 delivery.md、work 下 browser-results／path-results／file-results。
- 演算法／位移模型核對 5 組陣列（原題 2／5、空陣列、負數等）、FillArray 邊界、框架收支及 TestStack 位移通過。未以 MASM／Irvine32 原生組譯或執行，不宣稱原始機器碼測試通過；確切函式庫與 prologue 選項尚未驗證。無未完成教材頁段。
'''
log=R/'wiki/log.md'
if '## [2026-11-05] ingest | 組合語言第八章：進階程序' not in log.read_text(encoding='utf-8'):
    with log.open('a',encoding='utf-8') as f:f.write(entry)
print('Appended assembly import log')
