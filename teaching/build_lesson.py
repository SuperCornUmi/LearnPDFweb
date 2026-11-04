"""Generate one course unit from its reviewed source data; no network required."""
from pathlib import Path
import json,sys,hashlib,re
ROOT=Path(__file__).resolve().parent.parent
standard_text=(ROOT/'wiki/standards/PDF課程教材製作標準.md').read_text(encoding='utf-8')
standard_version=re.search(r'^standard_version: "([^"]+)"$',standard_text,re.M).group(1)
unit=Path(sys.argv[1]).resolve()
assert unit.is_relative_to(ROOT/'teaching')
meta=json.loads((unit/'config.json').read_text(encoding='utf-8'))
pages=[]
for n,line in enumerate((unit/'pages.txt').read_text(encoding='utf-8').strip().splitlines(),1):
    fields=line.split('｜')
    assert len(fields)==4 and all(fields[:3]),(n,fields)
    pages.append(dict(zip(['page','title','translation','explanation','supplement'],[n]+fields)))
assert len(pages)==meta['expectedPages']
slides=[]
for n,line in enumerate((unit/'slides.txt').read_text(encoding='utf-8').strip().splitlines(),1):
    title,bullets,speaker,refs=line.split('｜')
    slides.append(dict(number=n,title=title,bullets=bullets.split(';'),speaker=speaker,refs=refs))
course,slug=meta['course'],meta['unit']
notes_dir=ROOT/'notes'/course
deck_dir=ROOT/'presentations'/course/slug
downloads=ROOT/'website/downloads'
for folder in [notes_dir,deck_dir,downloads,ROOT/'website/lessons']:folder.mkdir(parents=True,exist_ok=True)
intro=f'''---
title: "{meta['courseName']} {meta['label']}：{meta['title']}"
course: {course}
unit: {slug}
created: 2026-11-03
updated: 2026-11-04
standard_version: "{standard_version}"
source_ids: [{meta['sourceId']}, web-20261104-mit-coordinates-spaces]
coverage: "PDF pp. 1–{len(pages)}；每頁翻譯與講解，必要時補充"
---

# {meta['courseName']} {meta['label']}：{meta['title']}

[Wiki 索引](../../wiki/index.md) · [原始 PDF](../../{meta['pdf']}) · [來源摘要](../../{meta['sourceWiki']}) · [HTML 閱讀入口](../../index.html#/{course}/{slug}/pages/1)

本筆記按 PDF 實體頁序完整翻譯與講解，採繁體中文意譯並保留數學內容，重複頁尾不逐次抄寫。row 指橫列、column 指直欄；矩陣以逐列列表表示。原文與觀念講解分段，講解展開推理與計算；只在有助理解當頁時加補充。原文錯誤另標勘誤，不改原 PDF。封面在網站以自製圖呈現，原作者與日期保留於來源資料。

## 逐頁目錄

'''
toc='\n'.join(f'- [PDF p. {p["page"]}：{p["title"]}](#pdf-p-{p["page"]})' for p in pages)
body=[]
for p in pages:
    n=p['page']
    supplement_md=('\n### 教學補充／提醒\n\n'+p['supplement']+'\n') if p['supplement'] else ''
    body.append(f'''<a id="pdf-p-{n}"></a>
## PDF p. {n}｜{p['title']}

來源：[原 PDF 第 {n} 頁](../../{meta['pdf']}#page={n}) · [Wiki 來源](../../{meta['sourceWiki']})

### 中文翻譯

{p['translation']}

### 觀念講解

{p['explanation']}

{supplement_md}
''')
refs='## 參考文獻\n\n### 已使用並納入 Wiki\n\n'
for r in meta['references']:
    refs+=f'- [{r["title"]}]({r["url"] if "://" in r["url"] else "../../"+r["url"]})：{r["detail"]}。\n'
refs+='\n外部來源使用範圍與交叉核對見 [Wiki 查證](../../wiki/sources/web-20261104-mit-coordinates-spaces.md)。\n\n### 延伸閱讀／待完整匯入\n\nMIT 逐字稿其餘頁與影片尚未完整匯入，本教材不使用未讀內容。\n'
notes=intro+toc+'\n\n'+'\n'.join(body)+'\n'+refs
(notes_dir/(slug+'.md')).write_text(notes,encoding='utf-8')
deck=f'# {meta["label"]}：{meta["title"]}｜精簡簡報\n\n依對應 notes 提煉，共 {len(slides)} 張，並非每個 PDF 頁面一張。\n\n'
speaker=f'# {meta["label"]}｜逐張講解稿\n\n對應 {len(slides)} 張精簡簡報，完整逐頁講解另見 notes。\n\n'
for s in slides:
    deck+=f'## 投影片 {s["number"]}｜{s["title"]}\n\n'+'\n'.join('- '+b for b in s['bullets'])+f'\n\n依據：PDF pp. {s["refs"]}；notes 對應頁段。\n\n'
    speaker+=f'## 投影片 {s["number"]}｜{s["title"]}\n\n{s["speaker"]}\n\n回查：PDF pp. {s["refs"]}。\n\n'
(deck_dir/'slides.md').write_text(deck,encoding='utf-8')
(deck_dir/'speaker-notes.md').write_text(speaker,encoding='utf-8')
for name,text in [('notes',notes),('slides',deck),('speaker-notes',speaker)]:
    (downloads/(slug+'-'+name+'.md')).write_text(text,encoding='utf-8')
data=dict(meta=meta,pages=pages,slides=slides,notes=notes,references=meta['references'])
(unit/'lesson.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
js='window.LESSONS=window.LESSONS||{};window.LESSONS['+json.dumps(meta['key'])+']='+json.dumps(data,ensure_ascii=False)+';\n'
(ROOT/meta['script']).write_text(js,encoding='utf-8')
manifest=dict(standard_version=standard_version,course=course,unit=slug,updated='2026-11-04',pdf_pages=len(pages),slides=len(slides),source_ids=[meta['sourceId'],'web-20261104-mit-coordinates-spaces'],inputs={})
for p in [unit/'pages.txt',unit/'slides.txt',unit/'config.json',ROOT/meta['pdf']]+list((ROOT/'wiki').rglob('*.md')):
    manifest['inputs'][p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(unit/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Built {meta["label"]}: {len(pages)} pages, {len(slides)} slides.')
