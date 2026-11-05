from pathlib import Path
R=Path(__file__).resolve().parent.parent
p=R/'index.html';s=p.read_text(encoding='utf-8')
s=s.replace('<script src="website/app.js" defer></script>','<script src="website/lessons/assembly-chapter-8.js" defer></script><script src="website/assembly-diagrams.js" defer></script><script src="website/app.js" defer></script>')
p.write_text(s,encoding='utf-8')
p=R/'website/app.js';s=p.read_text(encoding='utf-8')
s=s.replace("const para=s=>'<p>'+esc(s)+'</p>';",'''const para=s=>String(s).split(/(```[\\w-]*\\n[\\s\\S]*?```)/g).filter(Boolean).map(part=>part.startsWith('```')?'<pre class="lesson-code"><code>'+esc(part.replace(/^```[\\w-]*\\n/,'').replace(/```$/,''))+'</code></pre>':part.trim().split(/\\n\\s*\\n/).filter(Boolean).map(t=>'<p>'+esc(t)+'</p>').join('')).join('');''')
s=s.replace('<div class="card-art">${art}</div>', '<div class="card-art">${c.course===\'assembly-language\'?assemblyArt:art}</div>')
s=s.replace('<span class="eyebrow">MATHEMATICS · CE2005</span>','<span class="eyebrow">${esc(c.courseTag||\'MATHEMATICS · CE2005\')}</span>')
s=s.replace('<p>從向量的關係，理解空間的結構。</p>','<p>${esc(c.courseDescription||\'從向量的關係，理解空間的結構。\')}</p>')
s=s.replace('個章節 · 4 種學習模式','個章節 · 多種學習模式')
s=s.replace('<div class="eyebrow">CE2005 / LINEAR ALGEBRA</div>', '<div class="eyebrow">${esc(list[0].meta.courseTag||\'CE2005 / LINEAR ALGEBRA\')}</div>')
s=s.replace('用定義建立觀念，用推導理解關係。<br>從這裡選擇章節，找到適合當下的閱讀方式。', '${esc(list[0].meta.courseDescription||\'用定義建立觀念，用推導理解關係。\')}<br>從這裡選擇章節，找到適合當下的閱讀方式。')
s=s.replace('<p>CE2005 · ${esc(M.label)}', '<p>${esc(M.courseTag||\'CE2005\')} · ${esc(M.label)}')
s=s.replace("function diagramsView(){if(M.diagrams==='coordinates')", "function diagramsView(){if(M.diagrams==='assembly')assemblyDiagramsView();else if(M.diagrams==='coordinates')")
s=s.replace('para(cover?`${M.courseName}', "para(cover&&M.course!=='assembly-language'?`${M.courseName}")
# Keep the physical PDF page as the primary number, expose mixed original pagination.
s=s.replace('· PDF p. ${n}</span>', "· PDF p. ${n}${p.printedPage&&p.printedPage!==n?`（內文 p. ${p.printedPage}）`:''}</span>")
p.write_text(s,encoding='utf-8')
p=R/'website/reader.css';s=p.read_text(encoding='utf-8')
s+='''
/* Structured code and diagrams for programming lessons; text remains selectable. */
.lesson-code{max-width:100%;min-width:0;overflow:auto;white-space:pre;tab-size:4;background:#f1f4ee;border:1px solid #dce5d9;border-radius:8px;padding:14px;font:14px/1.7 Consolas,"Courier New",monospace;color:#173849;margin:12px 0 18px}.lesson-code code{font:inherit}.page-explanations,.explanation-card,.stack-layout>*{min-width:0}.explanation-card p{white-space:pre-line}.stack-layout{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:24px;margin:20px 0}.table-scroll{max-width:100%;overflow:auto}.match-inputs{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:14px 0}.match-inputs label{display:flex;flex-direction:column;gap:8px}.match-inputs input{min-width:0;width:100%;box-sizing:border-box;padding:11px;border:1px solid #b9cec0;border-radius:7px;background:#fffdf7;font:inherit}#stack-step{max-width:100%}#match-result{margin:16px 0}#stack-registers{overflow-wrap:anywhere;font-family:Consolas,monospace}#match-result{overflow-wrap:anywhere}@media(max-width:700px){.stack-layout,.match-inputs{grid-template-columns:1fr}.lesson-code{font-size:13px;padding:11px}.diagram-card{min-width:0}}
'''
p.write_text(s,encoding='utf-8')
print('Registered assembly lesson and adapted shared labels/code rendering.')
