from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent.parent
def metadata(n,title,english,groups,diagrams):
    unit=f'lecture-{n}'
    return dict(key=f'linear-algebra/{unit}',course='linear-algebra',courseName='線性代數',unit=unit,label=f'Lecture {n}',number=n,title=title,english=english,pdf=f'raw/pdfs/CE2005_Lecture_{n}.pdf',assetBase=f'website/assets/lecture{n}/',sourceWiki=f'wiki/sources/src-20261103-ce2005-lecture-{n}.md',sourceId=f'src-20261103-ce2005-lecture-{n}',downloads=f'website/downloads/{unit}',script='website/lesson-data.js' if n==5 else f'website/lessons/{unit}.js',groups=groups,diagrams=diagrams,expectedPages=87 if n==5 else 152)
m5=metadata(5,'線性獨立與基底','Linear Independence and Bases',[['開場與目標',1,3],['獨立與相依',4,24],['系統與唯一表示',25,44],['多項式與函數',45,61],['基底與維度',62,86],['結束與回顧',87,87]],'independence')
m6=metadata(6,'座標、秩與線性轉換','Coordinates, Rank, and Linear Transformations',[['開場與目標',1,3],['座標與換基底',4,33],['矩陣子空間與秩',34,65],['線性轉換與核／值域',66,94],['矩陣表示與圖形',95,126],['相似矩陣',127,151],['結尾',152,152]],'coordinates')
data=json.loads((root/'teaching/linear-algebra/lecture-5/lesson.json').read_text(encoding='utf-8'))
m5['references']=data['references']
m5['referenceNote']='Lecture 5：87 頁完整對應；原文勘誤及視覺核對見 Wiki 來源頁。MIT Lecture 9 僅閱讀逐字稿 pp. 1–3。'
m6['references']=[dict(title='CE2005 Lecture 6｜原始 PDF',url=m6['pdf'],detail='主要來源 · 152 頁 · 鍾佳儒 · 原頁日期 2026-11-04'),dict(title='MIT｜Column Space and Nullspace',url='https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/ax-b-and-the-four-subspaces/column-space-and-nullspace/',detail='已核對官方 Session Overview，未完整閱讀影片或習題'),dict(title='MIT Lecture 31｜官方逐字稿',url='https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/46108efb43dcf33e989eb5e101fcf9b5_MIT18_06S10_L31.pdf',detail='有限查證 · 僅 PDF pp. 9–11 相關段落 · 2026-11-04')]
m6['referenceNote']='Lecture 6：152 頁完整對應。p.110 的常數導數、p.137 的孤立式、p.144 的相似乘法順序均在教材明示勘誤；來源紀錄含其他排字提醒。外部資料只採已查證段落。'
for m in [m5,m6]:
    folder=root/'teaching/linear-algebra'/m['unit'];folder.mkdir(exist_ok=True)
    (folder/'config.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
# Keep the existing, complete Lecture 5 generator, adding unit metadata/registration.
p=root/'teaching/linear-algebra/lecture-5/build.py';s=p.read_text(encoding='utf-8')
needle="(SITE/'lesson-data.js').write_text('window.LESSON = '+json.dumps(data,ensure_ascii=False)+';\\n',encoding='utf-8')"
assert needle in s
replacement="data['meta']=json.loads((HERE/'config.json').read_text(encoding='utf-8'))\n(SITE/'lesson-data.js').write_text('window.LESSONS=window.LESSONS||{};window.LESSON=window.LESSONS[\\\"linear-algebra/lecture-5\\\"]='+json.dumps(data,ensure_ascii=False)+';\\n',encoding='utf-8')"
s=s.replace(needle,replacement)
p.write_text(s,encoding='utf-8')
p=root/'index.html';s=p.read_text(encoding='utf-8').replace('<script src="website/app.js" defer></script>','<script src="website/lessons/lecture-6.js" defer></script><script src="website/app.js" defer></script>');p.write_text(s,encoding='utf-8')
pdf=root/m6['pdf'];h=hashlib.sha256(pdf.read_bytes()).hexdigest()
meta=dict(source_id=m6['sourceId'],original_path='C:/Users/miu99/Downloads/CE2005_Lecture_6.pdf',stored_path=m6['pdf'],sha256=h,bytes=pdf.stat().st_size,pages=152,import_started='2026-11-03',import_completed='2026-11-04',title=m6['english'],authors=['Chia-Ru Chung（鍾佳儒）'],published='2026-11-04')
(root/'raw/metadata'/f'{m6["sourceId"]}.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
cover=(root/'website/assets/lecture5/cover.svg').read_text(encoding='utf-8').replace('LECTURE 05','LECTURE 06').replace('線性獨立與基底','座標、秩與線性轉換').replace('線性獨立','座標、秩').replace('與基底','與線性轉換').replace('Linear Independence and Bases','Coordinates, Rank, and Linear Transformations').replace('font-size="80"','font-size="68"').replace('font-size="30"','font-size="24"').replace('從向量的關係，理解空間的結構。','同一個向量，不同的描述。')
(root/'website/assets/lecture6/cover.svg').write_text(cover,encoding='utf-8')
print('Configured two units, saved metadata, custom cover and script registration.')
