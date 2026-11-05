"""Rebuild this unit from reviewed JSON without changing source PDF or other lessons."""
from pathlib import Path
import json,hashlib,re
from urllib.parse import quote
R=Path(__file__).resolve().parents[3];U=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
M=read(U/'config.json');P=read(U/'content.json');S=read(U/'slides.json')
assert [p['page'] for p in P]==list(range(1,M['expectedPages']+1))
assert [s['number'] for s in S]==list(range(1,len(S)+1))
assert all(p['title'] and p['translation'] and p['explanation'] for p in P)
version=re.search(r'^standard_version: "([^"]+)"',(R/'wiki/standards/PDF課程教材製作標準.md').read_text(encoding='utf-8'),re.M).group(1)
ids=[M['sourceId'],M['externalSourceId']]
def write(path,body):
    p=R/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body,encoding='utf-8')
pdf=quote(M['pdf'],safe='/');note='notes/assembly-language/chapter-8.md'
head=f'''---
title: "組合語言 第八章：進階程序與堆疊框架"
course: assembly-language
unit: chapter-8
created: 2026-11-05
updated: 2026-11-05
status: reviewed
standard_version: "{version}"
source_ids: [{', '.join(ids)}]
coverage: "PDF pp. 1–51；完整逐頁翻譯與講解；無未完成頁段"
---

# 組合語言 第八章：進階程序與堆疊框架

[Wiki](../../wiki/index.md) · [原始 PDF](../../{pdf}) · [來源與勘誤](../../{M['sourceWiki']}) · [網站](../../index.html#/{M['key']}/pages/1)

## 來源與閱讀說明

按 PDF 實體頁序一頁一節。原頁尾編號因混編而不連續，逐頁另列；引用一律使用 PDF 頁序。
以繁體中文完整意譯，保留程式關鍵語法；重複頁尾不逐次抄寫。原文、觀念講解與選用補充分開；教學修正明示，不改原 PDF。遮住答案的頁面依可見內容呈現，下一頁揭露答案。
主要適用 32 位元 MASM／Irvine 教學模型。程式未經 MASM／Irvine32 原生組譯執行，Python 模型測試只核對演算法與位移。原作者 Kip R. Irvine，封面為 2015 第七版，含 2007 版與課堂增補；講義發布日期未知。

## 逐頁目錄

'''
notes=head+'\n'.join(f'- [PDF p. {p["page"]}：{p["title"]}](#pdf-p-{p["page"]})' for p in P)+'\n\n'
printed=[None]+list(range(2,9))+list(range(10,22))+list(range(23,32))+list(range(33,55))
assert len(printed)==51
for p,pn in zip(P,printed):
    n=p['page'];label=f'（內文 p. {pn}）' if pn and pn!=n else ('（封面無印刷頁碼）' if pn is None else f'（內文 p. {pn}）')
    p['printedPage']=pn
    notes+=f'<a id="pdf-p-{n}"></a>\n## PDF p. {n}｜{p["title"]}\n\n來源：[原 PDF 第 {n} 頁](../../{pdf}#page={n}){label} · [Wiki 來源](../../{M["sourceWiki"]})\n\n### 中文翻譯\n\n{p["translation"]}\n\n### 觀念講解\n\n{p["explanation"]}\n\n'
    if p['supplement']:notes+=f'### 教學補充／提醒\n\n{p["supplement"]}\n\n'
notes+='## 參考文獻\n\n### 已使用並納入 Wiki\n\n'
for r in M['references']:
    link=r['url'] if '://' in r['url'] else '../../'+quote(r['url'],safe='/')
    notes+=f'- [{r["title"]}]({link})：{r["detail"]}。\n'
notes+='\n[外部查證的實際範圍](../../wiki/sources/'+M['externalSourceId']+'.md)。外部連結需連網。\n\n### 延伸閱讀／待匯入\n\n目前無另列候選；未閱讀的官方手冊段落不作正文證據。\n\n## 進度與限制\n\n51 頁全部閱讀，翻譯與講解完整對應；來源勘誤與未原生執行的限制見上方說明及 [交付紀錄](../../teaching/assembly-language/chapter-8/delivery.md)。\n'
write(note,notes)
deck='# 組合語言第八章｜16 張精簡簡報\n\n以教學主線合併 PDF 多頁；完整內容見 [逐頁 notes](../../../notes/assembly-language/chapter-8.md)。\n\n'
speaker='# 組合語言第八章｜16 張逐張講稿\n\n對應 slides.md；每張交代目的、講解順序與易錯處。\n\n'
for s in S:
    ref=s['refs'];n=int(re.search(r'\d+',ref).group())
    backlink=f'../../../notes/assembly-language/chapter-8.md#pdf-p-{n}'
    deck+=f'## 投影片 {s["number"]}｜{s["title"]}\n\n'+'\n'.join('- '+x for x in s['bullets'])+f'\n\n依據：PDF pp. {ref}；[notes 對應頁段]({backlink})。\n\n'
    speaker+=f'## 投影片 {s["number"]}｜{s["title"]}\n\n{s["speaker"]}\n\n依據：PDF pp. {ref}；[notes 對應頁段]({backlink})。\n\n'
for name,body in [('slides',deck),('speaker-notes',speaker)]:
    write('presentations/assembly-language/chapter-8/'+name+'.md',body)
    # Downloads are two levels below root, whereas the source deck is three.
    write('website/downloads/assembly-chapter-8-'+name+'.md',body.replace('../../../','../../'))
write('website/downloads/assembly-chapter-8-notes.md',notes)
data=dict(meta=M,pages=P,slides=S,notes=notes,references=M['references'])
write('teaching/assembly-language/chapter-8/lesson.json',json.dumps(data,ensure_ascii=False,indent=2))
write(M['script'],'window.LESSONS=window.LESSONS||{};window.LESSONS['+json.dumps(M['key'])+']='+json.dumps(data,ensure_ascii=False)+';\n')
inputs=[U/'config.json',U/'content.json',U/'slides.json',U/'build.py',R/M['pdf'],R/'wiki/standards/PDF課程教材製作標準.md',R/'raw/web/microsoft-masm-procedures-20261105.md']
inputs += [R/'wiki/sources'/f'{sid}.md' for sid in ids]
inputs += [R/'wiki/concepts/堆疊框架與呼叫慣例.md',R/'wiki/concepts/值與位址及MASM定址.md',R/'wiki/topics/組合語言.md',R/'wiki/questions/CountMatches如何區分位置與跨位置匹配.md']
inputs += [U/'check_models.py',R/'website/assembly-diagrams.js',R/'website/assets/assembly-ch8/cover.svg',R/'presentations/assembly-language/chapter-8/diagrams.md',R/'website/app.js',R/'website/reader.css',R/'index.html']
manifest=dict(standard_version=version,updated='2026-11-05',course=M['course'],unit=M['unit'],source_ids=ids,pdf_pages=len(P),slides=len(S),coverage='PDF pp. 1–51',native_masm_execution=False,inputs={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs})
write('teaching/assembly-language/chapter-8/manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
print('Built 51 pages, 16 slides, speaker notes, downloads and website data.')
