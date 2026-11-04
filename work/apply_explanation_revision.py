from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1]
protected=[root/'AGENTS.md',root/'index.html',root/'website/styles.css']+list((root/'wiki').rglob('*.md'))+list((root/'raw').rglob('*'))+list((root/'presentations').rglob('*.md'))+list((root/'website/assets').rglob('*'))
protected=[p for p in protected if p.is_file()]
(root/'work/content-revision-protected.json').write_text(json.dumps({p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in protected},ensure_ascii=False,indent=2),encoding='utf-8')
supplements={5:{
15:'勿把獨立理解成垂直：本講 p. 17 的 (1,1)ᵀ、(1,2)ᵀ 已證獨立，並未要求它們互相垂直。判斷仍以零組合的係數為準。',
19:'勘誤：原頁係數 (1,2,3,−1) 適用順序 (e₁,e₂,e₃,x)，不適用頁面列式的 (x,e₁,e₂,e₃)。依後者應為 (1,−1,−2,−3)，須連同向量順序一起更正。',
22:'原頁向量分量有重複下標的排字問題；此處按三維向量寫作 (x₁,x₂,x₃)ᵀ、(y₁,y₂,y₃)ᵀ，圖與結論不受影響。',
36:'主元計數檢查：k 個係數未知數需 k 個主元才會獨立。即使有零列，若所有係數欄仍各有主元，依然可能獨立；p. 28 就是具體例子。',
53:'關鍵差異：相依要求「存在同一個非零 c，使所有 x 都有 M(x)c=0」。只知道「每個 x 各自有某個非零解」較弱，不能把各點的解當作共用常數。',
60:'本例若改在 [0,1]，便有 x|x|=x²，取係數 (1,−1) 就證相依。這是原分段式直接推出的結果，說明不能省略函數題的指定區間。',
63:'原頁把「最小生成集」附在獨立條件旁，需與第二條生成性合讀。獨立本身不表示已生成 V，例如 ℝ³ 中一支非零向量只能生成一條直線。',
76:'原頁第三圖未單獨重列獨立前提；依 p. 24，必須 x、y 獨立且 z∉Span(x,y)，才能得到 Span(x,y,z)=ℝ³。',
77:'Wronskian 推廣為 0!·1!·…·n!，因導數矩陣上三角且對角元素依序為各階乘。C[a,b] 的此論證採 a<b；原頁最後寫「m 任意」應與前文的 n 統一。',
86:'本講 Pₙ 定義為次數小於 n，故 dim Pₙ=n；若別的教材用「次數至多 n」，其維度會是 n+1。比較題目時先核對定義，不能只看同一個下標。'},
6:{
9:'模型假設總人口固定、每年遷移比例相同；Aⁿ 才能一直使用同一個 A。此例沒有納入出生、死亡或遷移率隨時間改變。',
10:'−0.05 是非標準基底的係數，不是負的人口比例。兩項重建後為 (0.30,0.70)ᵀ，才是實際城市／郊區比例。',
11:'依同一公式代入，10、30、50 年城市比例約為 27.1719%、25.4098%、25.0773%。原頁取整數百分比後顯示 27%、25%、25%，捨入會隱藏仍在縮小的差距。',
18:'勘誤：原頁底部將 c、d 的箭頭標示反轉，並出現 c=Sd，與正文 x=Vc=Ud 不合。依正文正確為 d=Sc、S=U⁻¹V；反向則 c=S⁻¹d。',
30:'沿用本課定義，P₃ 指次數小於 3，因此基底有三項，對應 1、x、x²。不要把下標 3 誤讀為允許 x³。',
56:'不要把保留欄的「關係」當成保留 column space：同一係數清單仍可判相依，但消去後欄向量的數字已可能改變，所以取原空間基底要回 A。',
73:'原頁中間展開的第二分量有排字重複；應為 αx₂+βy₂，不能再寫成 αx₂+αx₂。上述翻譯已依分量加法更正，線性結論不變。',
110:'勘誤：原頁一式將 D(1) 寫成 0x+1，應為 0x+0。其矩陣第三欄 (0,0)ᵀ 已是正確值；可用常數導數為零直接核對。',
117:'快速核對第一欄：B(−1,4,−1)ᵀ=(−1+4−1,4−1,−1)ᵀ=(2,3,−1)ᵀ。乘回目標基底矩陣，是檢查座標欄方向最直接的方法。',
125:'編成第三座標為 1 的點後，不能直接在這個點集合套用向量子空間的線性檢查：兩個這樣的三維向量相加，第三座標會成 2。這是此頁矩陣線性與平面平移非線性可同時成立的原因。',
134:'本定理假設是同一 V 上的算子，兩端一起換成同一組新基底。若是一般 V→W 且兩端各有不同換法，就不能直接套同一個 S 的相似公式。',
137:'原頁孤立的 S⁻¹ASx=B 少了右端 x，或左端多了 x。矩陣乘 n×1 欄得到 n×1 欄，不能直接等於 n×n 的 B；尺寸可協助辨認這個筆誤。',
145:'若誤用原頁 p. 144 的 SBS⁻¹，會得到超對角元素 1/2、1；正確 S⁻¹BS 得 2、4，才與直接微分所得 A 一致。這可實際驗證順序錯誤的影響。',
151:'公式 Dⁿx=(0,x₂,4ⁿx₃)ᵀ 限 n≥1。n=0 時 D⁰=I，尚未做任何作用，第一座標也必須保留。'}}
for n,count in [(5,87),(6,152)]:
 path=root/f'teaching/linear-algebra/lecture-{n}/pages.txt'
 old=path.read_text(encoding='utf-8').splitlines()
 (root/f'work/lecture-{n}-pages-before-detail-revision.txt').write_text('\n'.join(old)+'\n',encoding='utf-8')
 def patches(kind):
  rows=(root/f'work/revised-{kind}-{n}.txt').read_text(encoding='utf-8').splitlines()
  return {int(k):v for k,v in (line.split('｜',1) for line in rows)}
 explanations=patches('explanations');translations=patches('translations')
 assert sorted(explanations)==list(range(1,count+1))
 result=[]
 for i,line in enumerate(old,1):
  title,translation,explanation,supplement=line.split('｜')
  result.append('｜'.join([title,translations.get(i,translation),explanations[i],supplements[n].get(i,'')]))
 assert len(result)==count
 path.write_text('\n'.join(result)+'\n',encoding='utf-8')
 print(f'Lecture {n}: rewrote {count} explanations, expanded {len(translations)} translations, retained {len(supplements[n])} relevant supplements.')
