from pathlib import Path
root=Path(__file__).resolve().parents[1]
def read(p):return (root/p).read_text(encoding='utf-8-sig')
def write(p,s):(root/p).write_text(s,encoding='utf-8')
def replace(p,a,b):
 s=read(p);assert a in s,(p,a);write(p,s.replace(a,b))
replace('website/app.js',"自製學習封面：線性獨立與基底", "自製學習封面：'+esc(M.title)+'")
# The alt attribute is inside a template expression; use its own template literal.
replace('website/app.js',"'自製學習封面：'+esc(M.title)+''", "`自製學習封面：${esc(M.title)}`")
replace('website/app.js','scheduled=false;const top=stream.scrollTop','scheduled=false;if(!stream.isConnected)return;const top=stream.scrollTop')
replace('website/app.js','requestAnimationFrame(()=>{fitReader();jump(n)});','requestAnimationFrame(()=>{if(stream.isConnected){fitReader();jump(n)}});')
replace('teaching/linear-algebra/lecture-6/pages.txt','公式可記為「目標基底矩陣的逆 × 來源基底矩陣」，但必須確保兩組都是真正基底。','公式可記為「目標基底矩陣的逆 × 來源基底矩陣」。原頁底部箭頭的 c、d 標示與正文相反；依 x=Vc=Ud，正確方向為 c → d，d=U⁻¹Vc。兩組必須都是真正基底。')
replace('AGENTS.md','網站目前只有該單元，後續須實際擴充課程／章節載入與導覽，保留舊章節可用。','網站已以 `window.LESSONS` 按單元註冊資料，支援 Lecture 5、6；新增單元須建立獨立 `config.json`、教材與資料腳本，加入根目錄 HTML 的腳本載入，保留舊章節可用。頁數、路徑及閱讀進度依單元取得。')
replace('wiki/standards/PDF課程教材製作標準.md','目前網站是單一 Lecture 5 的實作參考，尚不是自動支援任意課程的匯入器。**新增第二份教材時必須實際擴充課程／章節資料載入與導覽，必要時抽離現有單元專用程式；不可只改畫面名稱或交付一份未連入網站的新檔。** 不代表背景會自動監看 PDF；仍由代理收到檔案後執行。','網站已支援 Lecture 5、6，以 `window.LESSONS` 註冊各單元，課程／章節由單元資料建立。新增單元建立 `teaching/<course>/<unit>/config.json` 與教材，生成獨立資料腳本並加入根目錄 HTML；各單元分別保存閱讀進度。**不可只改畫面名稱或交付一份未連入網站的新檔。** 不代表背景會自動監看 PDF；仍由代理收到檔案後執行。')
replace('wiki/index.md','## 主題綜整','- [CE2005 Lecture 6：座標、秩與線性轉換](sources/src-20261103-ce2005-lecture-6.md)：152 頁完整閱讀，從換基底到相似矩陣，附原文勘誤。\n- [MIT：座標與子空間補充查證](sources/web-20261104-mit-coordinates-spaces.md)：官方課程指定段落核對座標、值域與核；部分閱讀。\n\n## 主題綜整')
replace('wiki/index.md','## 實體','- [座標與換基底](concepts/座標與換基底.md)：唯一座標與轉換矩陣的方向。\n- [矩陣子空間與秩零度](concepts/矩陣子空間與秩零度.md)：row、column、null space 的基底與維度。\n- [線性轉換的核與值域](concepts/線性轉換的核與值域.md)：線性條件、單射、滿射與秩零度。\n- [矩陣表示與相似](concepts/矩陣表示與相似.md)：由基底像建立矩陣，並追蹤換基底方向。\n\n## 實體')
replace('wiki/index.md','## 跨文件比較\n\n尚無頁面。','## 跨文件比較\n\n- [從基底到矩陣表示](comparisons/從基底到矩陣表示.md)：串連 Lecture 5 的唯一表示與 Lecture 6 的座標、核、矩陣表示。')
write('wiki/index.md',read('wiki/index.md')+'\n- [Lecture 6 逐頁中文筆記](../notes/linear-algebra/lecture-6.md)：PDF pp. 1–152 全部對應。\n- [Lecture 6 精簡簡報](../presentations/linear-algebra/lecture-6/slides.md) · [20 張講解稿](../presentations/linear-algebra/lecture-6/speaker-notes.md)。\n- [Lecture 6 圖解整理](../presentations/linear-algebra/lecture-6/diagrams.md)：座標流向、相似交換圖及幾何互動對照。\n')
for p in ['wiki/overview.md','wiki/topics/線性代數.md','wiki/concepts/線性代數教學補充.md']:
 replace(p,'updated: 2026-11-03','updated: 2026-11-04')
 replace(p,'web-20261103-mit-lecture9]','web-20261103-mit-lecture9, src-20261103-ce2005-lecture-6, web-20261104-mit-coordinates-spaces]')
replace('wiki/overview.md','目前網站僅有 Lecture 5；規範及範本已通用化，後續新增單元時仍須實際擴充網站資料載入與課程／章節入口，不能假設已具備背景自動匯入功能。','網站已加入 Lecture 5、6，課程／章節由單元資料建立，閱讀進度分開保存；新增單元仍須由代理製作、註冊及驗收，沒有背景自動匯入功能。')
start=read('wiki/overview.md');a=start.index('目前已匯入 1 份 PDF');b=start.index('## 目前主要結論',a)
start=start[:a]+'''目前已匯入 2 份 PDF，共 239 頁：

- [Lecture 5：線性獨立與基底](sources/src-20261103-ce2005-lecture-5.md)：87 頁逐頁教材、15 張簡報。
- [Lecture 6：座標、秩與線性轉換](sources/src-20261103-ce2005-lecture-6.md)：152 頁逐頁教材、20 張簡報與幾何互動。

研究入口為[線性代數](topics/線性代數.md)，網站入口為[知識課堂](../index.html)。兩筆 MIT 官方資料均只使用已讀範圍，見來源摘要。

'''+start[b:];write('wiki/overview.md',start)
replace('wiki/overview.md','- 目前僅單一講義，沒有跨文件結論；可補入前一講或其他教材，建立比較與符號定義對照。','- 已建立[跨講義比較](comparisons/從基底到矩陣表示.md)；目前仍以同一課程講義為主，MIT 查證不代表完整課程匯入。')
replace('wiki/overview.md','## 證據缺口與下一步','- 座標由基底決定；同一線性算子在不同基底的表示矩陣相似，轉換方向須先定義。（[Lecture 6](sources/src-20261103-ce2005-lecture-6.md)，PDF pp. 18、127–145）\n- rank(A)+nullity(A)=欄數；column space 的基底從原矩陣的 pivot 欄選取。（同來源，PDF pp. 57–65）\n\n## 證據缺口與下一步')
replace('wiki/topics/線性代數.md','目前只涵蓋線性獨立、基底與維度，並非整門線性代數課程。以下為單一講義的整合，尚無跨來源比較。','目前涵蓋 Lecture 5、6：線性獨立、基底、座標、矩陣子空間、秩、線性轉換及相似矩陣，並非整門課程。兩講的銜接見[從基底到矩陣表示](../comparisons/從基底到矩陣表示.md)。')
write('wiki/topics/線性代數.md',read('wiki/topics/線性代數.md')+'''
## Lecture 6：由抽象空間到計算

- [座標與換基底](../concepts/座標與換基底.md)：把唯一表示轉為座標向量。
- [矩陣子空間與秩零度](../concepts/矩陣子空間與秩零度.md)：比較 row、column、null space。
- [線性轉換的核與值域](../concepts/線性轉換的核與值域.md)：把矩陣的零空間與欄空間推廣到映射。
- [矩陣表示與相似](../concepts/矩陣表示與相似.md)：基底像決定矩陣，同一算子隨座標改變表示。
- [152 頁筆記](../../notes/linear-algebra/lecture-6.md) · [20 張簡報](../../presentations/linear-algebra/lecture-6/slides.md) · [來源與勘誤](../sources/src-20261103-ce2005-lecture-6.md) · [MIT 部分查證](../sources/web-20261104-mit-coordinates-spaces.md)。
''')
write('wiki/concepts/線性代數教學補充.md',read('wiki/concepts/線性代數教學補充.md')+'''
## Lecture 6 的推導、條件與勘誤

依[原始來源](../sources/src-20261103-ce2005-lecture-6.md)，完整例題與逐頁細節見[Lecture 6 notes](../../notes/linear-algebra/lecture-6.md)。

- p. 18：底部 c、d 箭頭標示與正文相反；由 x=Vc=Ud 應得 d=U⁻¹Vc。
- p. 73：線性驗證的第二分量應為 αx₂+βy₂，不能重複 αx₂。
- p. 110：D(1)=0，原頁一處寫成 0x+1；矩陣第三欄為零，與正確導數相符。
- p. 137：S⁻¹ASx 等於 Bx；若等號右側只寫 B，須同時去掉左側 x。
- pp. 144–145：依原頁 S 的方向，正確 A=S⁻¹BS；p. 144 的 A=SBS⁻¹ 順序錯誤，p. 145 計算則正確。以實際矩陣相乘核對。
- row reduction 保留 row space、null space，但通常改變 column space；選欄基底要回到原矩陣（pp. 41–65）。
- [MIT 指定段落](../sources/web-20261104-mit-coordinates-spaces.md) 核對座標與核／值域觀念；未用未讀影片。
- 幾何互動為代理重繪示意：原點旋轉、1.5 倍縮放、y 軸反射及位移 (2,1)。位移不符合 T(0)=0，採齊次座標展示，不能稱為 ℝ² 上的線性轉換。原講義 pp. 97–107 的位移例為 (6,2)，兩者明確區分。
''')
replace('README.md','首個單元為線性代數 Lecture 5，含 87 頁逐頁中文翻譯與講解、15 張精簡簡報及講解稿、完整筆記、概念圖與互動示意。','目前有線性代數 Lecture 5（87 頁／15 張簡報）與 Lecture 6（152 頁／20 張簡報），共 239 頁逐頁中文教材，均含講解稿、完整筆記與互動圖解。')
replace('README.md','目前已匯入 CE2005 Lecture 5，','目前已匯入 CE2005 Lecture 5、6，')
replace('README.md','- [教材維護說明]','- [Lecture 6 逐頁筆記](notes/linear-algebra/lecture-6.md) · [精簡簡報](presentations/linear-algebra/lecture-6/slides.md) · [講解稿](presentations/linear-algebra/lecture-6/speaker-notes.md) · [維護說明](teaching/linear-algebra/lecture-6/README.md)\n- [教材維護說明]')
replace('website/README.md','網站目前只有 Lecture 5 的資料與專用路由；新增單元時須擴充資料載入、路由、課程／章節卡片、資產及下載連結，保留舊單元。','網站目前包含 Lecture 5、6，以 `window.LESSONS` 註冊獨立單元；新增單元建立教材及 `config.json`，生成資料腳本並加入根目錄 HTML，課程／章節卡片由資料建立，保留舊單元。')
replace('website/README.md','所有課程 → 線性代數 → Lecture 5','所有課程 → 線性代數 → Lecture 5 或 Lecture 6')
replace('website/README.md','87 頁成對排列','依單元的 87／152 頁成對排列')
replace('website/README.md','15 張、每張講解稿','Lecture 5 為 15 張、Lecture 6 為 20 張，均有每張講解稿')
replace('website/README.md','87 頁連續閱讀','依單元全部頁面連續閱讀')
replace('website/README.md','及二維向量夾角互動。','及二維向量夾角互動；Lecture 6 另有換基底流程、相似交換圖與幾何轉換互動。')
for p in ['wiki/concepts/基底與維度.md','wiki/concepts/線性獨立與相依.md','wiki/sources/src-20261103-ce2005-lecture-5.md']:
 write(p,read(p)+'\n## 後續單元串連\n\n[Lecture 6](../sources/src-20261103-ce2005-lecture-6.md) 將獨立與基底用於座標、矩陣子空間與線性轉換；兩講的概念對應見[從基底到矩陣表示](../comparisons/從基底到矩陣表示.md)。\n')
 replace(p,'updated: 2026-11-03','updated: 2026-11-04')
print('Updated standards, Wiki navigation and cross-links, website docs and page-18 errata.')
