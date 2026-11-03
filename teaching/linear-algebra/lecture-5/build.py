"""Build the lesson's local, dependency-free reading artifacts."""
from pathlib import Path
import json, hashlib, re

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SITE = ROOT / 'website'
NOTES = ROOT / 'notes/linear-algebra'
DECK = ROOT / 'presentations/linear-algebra/lecture-5'
for folder in (SITE, NOTES, DECK, SITE/'downloads'):
    folder.mkdir(parents=True, exist_ok=True)

lines = HERE.joinpath('pages.txt').read_text(encoding='utf-8').strip().splitlines()
assert len(lines) == 87, f'Expected 87 pages, found {len(lines)}'
pages=[]
for n, line in enumerate(lines, 1):
    parts=line.split('｜')
    assert len(parts)==4, (n, len(parts))
    title, translation, explanation, supplement=parts
    assert all(parts)
    pages.append(dict(page=n,title=title,translation=translation,explanation=explanation,supplement=supplement))

slides=[]
for n,line in enumerate(HERE.joinpath('slides.txt').read_text(encoding='utf-8').strip().splitlines(),1):
    title,bullets,speaker,refs=line.split('｜')
    slides.append(dict(number=n,title=title,bullets=bullets.split(';'),speaker=speaker,refs=refs))

refs='''## 參考文獻與補充來源

### 已使用並納入 Wiki

1. 鍾佳儒，CE2005 Lecture 5: Linear Independence and Bases，2026-10-14，PDF pp. 1–87。[來源摘要](../../wiki/sources/src-20261103-ce2005-lecture-5.md)。
2. Gilbert Strang，MIT OCW 18.06，Lecture 9 官方逐字稿，僅核對 PDF pp. 1–3。查閱日 2026-11-03。[官方來源](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/0fab20a14c050d85ef29563cd6c52d37_MIT18_06S10_L09.pdf) · [Wiki 查證](../../wiki/sources/web-20261103-mit-lecture9.md)。用於 p. 36 的自由變數補充，沒有把其餘未讀內容當作依據。
3. [教學補充與條件](../../wiki/concepts/線性代數教學補充.md)：記錄依原講義直接展開的推導、勘誤與例子。

### 待匯入的延伸閱讀

- [MIT 18.06SC：Independence, Basis and Dimension 課程摘要入口](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/resources/mit18_06scf11_ses1-9sum/)：已確認官方資源入口；尚未完整閱讀摘要 PDF，本版不使用其內容。可供後續比較講法。
'''

intro='''---
title: "線性代數 Lecture 5：逐頁中文講解"
course: linear-algebra
unit: lecture-5
created: 2026-11-03
updated: 2026-11-03
standard_version: "1.0"
source_ids: [src-20261103-ce2005-lecture-5, web-20261103-mit-lecture9]
coverage: "PDF pp. 1–87；每頁皆有對應章節"
---

# 線性代數 Lecture 5：線性獨立與基底

[Wiki 索引](../../wiki/index.md) · [原始 PDF](../../raw/pdfs/CE2005_Lecture_5.pdf) · [HTML 閱讀入口](../../website/index.html)

本筆記依 PDF 實體頁序逐頁翻譯、講解與補充。翻譯採忠實的中文意譯，保留各頁數學內容；頁尾重複課程資訊不逐次抄寫。講解與補充是教學重述及推導，不冒充原文。矩陣以逐列列表表示，例如 [[a,b],[c,d]]；ᵀ 表示轉置。封面、分隔頁與結尾頁均保留。

第 19 頁係數順序有原文勘誤；第 22、63、76、77 頁亦附閱讀條件或排字提醒。PDF 原檔保持不變。

## 逐頁目錄

'''
toc='\n'.join(f'- [PDF p. {p["page"]}：{p["title"]}](#pdf-p-{p["page"]})' for p in pages)
chunks=[]
for p in pages:
    translation_md=p['translation'].replace('W[f₁,…,fₙ](x)', '`W[f₁,…,fₙ](x)`')
    chunks.append(f'''<a id="pdf-p-{p['page']}"></a>
## PDF p. {p['page']}｜{p['title']}

來源：[原始 PDF 第 {p['page']} 頁](../../raw/pdfs/CE2005_Lecture_5.pdf#page={p['page']}) · [Wiki 來源頁](../../wiki/sources/src-20261103-ce2005-lecture-5.md)

### 中文翻譯

{translation_md}

### 觀念講解

{p['explanation']}

### 教學補充／提醒

{p['supplement']}
''')
notes=intro+toc+'\n\n'+'\n\n'.join(chunks)+'\n\n'+refs
(NOTES/'lecture-5.md').write_text(notes,encoding='utf-8')

deck='# Lecture 5｜精簡簡報逐張內容\n\n依據 notes/linear-algebra/lecture-5.md；共 15 張，合併原 PDF 多頁。\n\n'
speaker='# Lecture 5｜簡報逐張講解稿\n\n本檔對應 15 張精簡簡報；完整 87 頁講解另見 notes。\n\n'
for s in slides:
    deck+=f'## {s["number"]}. {s["title"]}\n\n'+ '\n'.join('- '+b for b in s['bullets'])+f'\n\n來源：CE2005 PDF pp. {s["refs"]}；詳細說明見 notes 對應頁段。\n\n'
    speaker+=f'## {s["number"]}. {s["title"]}\n\n{s["speaker"]}\n\n來源：PDF pp. {s["refs"]}。\n\n'
(DECK/'slides.md').write_text(deck,encoding='utf-8')
(DECK/'speaker-notes.md').write_text(speaker,encoding='utf-8')
data=dict(pages=pages,slides=slides,notes=notes,references=[
    dict(title='CE2005 Lecture 5｜原始 PDF',url='../raw/pdfs/CE2005_Lecture_5.pdf',detail='主要來源 · 87 頁 · 鍾佳儒 · 2026-10-14'),
    dict(title='MIT Lecture 9｜官方逐字稿',url='https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/0fab20a14c050d85ef29563cd6c52d37_MIT18_06S10_L09.pdf',detail='已查證補充 · 僅 pp. 1–3 · 查閱 2026-11-03'),
    dict(title='MIT 18.06SC｜課程摘要入口',url='https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/resources/mit18_06scf11_ses1-9sum/',detail='延伸閱讀候選 · 未完整匯入 · 本版未使用其內容')])
(SITE/'lesson-data.js').write_text('window.LESSON = '+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8')
(HERE/'lesson.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for name,body in [('lecture-5-notes.md',notes),('lecture-5-slides.md',deck),('lecture-5-speaker-notes.md',speaker)]:
    (SITE/'downloads'/name).write_text(body,encoding='utf-8')
manifest=dict(standard_version='1.0',course='linear-algebra',unit='lecture-5',date='2026-11-03',pdf_pages=87,slides=len(slides),source_ids=['src-20261103-ce2005-lecture-5','web-20261103-mit-lecture9'],inputs={})
for path in [HERE/'pages.txt',HERE/'slides.txt',ROOT/'raw/pdfs/CE2005_Lecture_5.pdf']+list((ROOT/'wiki').rglob('*.md')):
    manifest['inputs'][path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
(HERE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Built {len(pages)} page lessons, {len(slides)} slides, Markdown notes and browser data.')
