from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'website/app.js'
s=p.read_text(encoding='utf-8')
start=s.index('function pageView(n)')
end=s.index('function slideView(n)')
s=s[:start]+r'''let readerJump=null;
function pageImage(n){return n===1?'assets/lecture5/cover.svg':`assets/lecture5/${String(n).padStart(3,'0')}.webp`;}
function pageSection(p){const n=p.page,cover=n===1;return `<article class="page-section" id="pdf-page-${n}" data-pdf-page="${n}" aria-labelledby="page-title-${n}"><header class="page-section-heading"><span class="eyebrow">PDF PAGE ${String(n).padStart(2,'0')}</span><h2 id="page-title-${n}">${cover?'學習封面':esc(p.title)}</h2></header><div class="page-columns"><div class="source-panel"><div class="panel-label"><span>${cover?'自製學習封面':'原始講義'} · PDF p. ${n}</span><a href="${original(n)}" target="_blank" rel="noopener">開啟原始 PDF ↗</a></div><button class="zoom-page" data-zoom="${n}" aria-label="放大第 ${n} 頁${cover?'自製封面':'原始講義'}"><img src="${pageImage(n)}" width="1600" height="900" loading="${n===1?'eager':'lazy'}" alt="${cover?'自製學習封面：線性獨立與基底':`原始 PDF 第 ${n} 頁：${esc(p.title)}`}"></button><div class="source-caption">${cover?'自製封面，保留原 PDF 第 1 頁的對應位置。':'原頁與右側中文逐頁對照。'} 可直接往下捲動繼續閱讀。</div></div><div class="page-explanations"><section class="explanation-card translation"><h3>01 ／ 中文翻譯</h3>${para(cover?'線性代數 Lecture 5：線性獨立與基底。本頁以自製學習封面呈現；原始講義的作者與日期保留在來源紀錄中。':p.translation)}</section><section class="explanation-card"><h3>02 ／ 觀念講解</h3>${para(p.explanation)}</section><section class="explanation-card supplement"><h3>03 ／ 教學補充・提醒</h3>${para(p.supplement)}</section></div></div></article>`;}
function pageView(n){
 const expanded=store.get('l5-directory','closed')==='open';
 shell('pages',`<div class="reading-workspace ${expanded?'directory-open':''}" id="reading-workspace"><div class="reader-tools"><button id="directory-toggle" aria-expanded="${expanded}" aria-controls="page-directory">${expanded?'收起目錄':'☰ 目錄／搜尋'}</button><button data-prev aria-label="上一個 PDF 頁面">← 上一頁</button><label for="page-select">跳至</label><select id="page-select">${D.pages.map(q=>`<option value="${q.page}">${q.page}. ${q.page===1?'學習封面':esc(q.title)}</option>`).join('')}</select><button data-next aria-label="下一個 PDF 頁面">下一頁 →</button><span class="page-counter" aria-live="polite">PDF <b id="current-page">${n}</b> / 87</span><span class="scroll-hint">在下方閱讀區捲動，可連續閱讀</span></div><div class="reading-layout"><aside class="page-sidebar" id="page-directory" aria-label="原始頁面目錄" ${expanded?'':'hidden'}><label class="tiny muted" for="page-search">搜尋標題或觀念</label><input id="page-search" type="search" placeholder="搜尋本講內容…"><nav class="page-list">${D.pages.map(q=>`<a href="${BASE}/pages/${q.page}" data-page="${q.page}"><span>${String(q.page).padStart(2,'0')}</span>${q.page===1?'學習封面':esc(q.title)}</a>`).join('')}</nav><p id="search-empty" class="tiny muted" hidden>沒有符合的頁面，請換個關鍵字。</p></aside><div class="reader-stream" id="reader-stream" tabindex="0" role="region" aria-label="87 頁連續講解閱讀區"><div class="page-sections">${D.pages.map(pageSection).join('')}</div><p class="stream-end">已到本講最後一頁 · 共 87 頁<br><a href="${BASE}/references/">來源與參考文獻 →</a></p></div></div></div>`);
 document.body.classList.add('reading-mode');
 const stream=document.getElementById('reader-stream'),sections=[...document.querySelectorAll('.page-section')];
 const setCurrent=(v,updateURL=true)=>{state.page=v;store.set('l5-page',v);document.getElementById('current-page').textContent=v;document.getElementById('page-select').value=String(v);document.querySelector('[data-prev]').disabled=v===1;document.querySelector('[data-next]').disabled=v===87;document.querySelectorAll('[data-page]').forEach(a=>{const active=+a.dataset.page===v;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});const link=document.querySelector('.mode-tabs a.active');if(link)link.href=`${BASE}/pages/${v}`;if(updateURL&&location.hash!==`${BASE}/pages/${v}`)history.replaceState(null,'',`${BASE}/pages/${v}`);};
 const jump=(v,smooth=false)=>{const target=sections[v-1];if(!target)return;setCurrent(v);stream.scrollTo({top:target.offsetTop,behavior:smooth?'smooth':'instant'});};
 readerJump=jump;
 let scheduled=false;
 stream.addEventListener('scroll',()=>{if(scheduled)return;scheduled=true;requestAnimationFrame(()=>{scheduled=false;const top=stream.scrollTop+60;let current=1;for(const section of sections){if(section.offsetTop<=top)current=+section.dataset.pdfPage;else break}setCurrent(current);})},{passive:true});
 document.getElementById('page-select').onchange=e=>navigatePage(+e.target.value);
 document.querySelector('[data-prev]').onclick=()=>navigatePage(state.page-1);
 document.querySelector('[data-next]').onclick=()=>navigatePage(state.page+1);
 document.getElementById('directory-toggle').onclick=e=>{const workspace=document.getElementById('reading-workspace'),open=!workspace.classList.contains('directory-open');workspace.classList.toggle('directory-open',open);document.getElementById('page-directory').hidden=!open;e.currentTarget.setAttribute('aria-expanded',String(open));e.currentTarget.textContent=open?'收起目錄':'☰ 目錄／搜尋';store.set('l5-directory',open?'open':'closed');requestAnimationFrame(()=>jump(state.page));};
 document.getElementById('page-search').oninput=e=>{const term=e.target.value.trim().toLowerCase();let found=0;document.querySelectorAll('[data-page]').forEach(a=>{const q=D.pages[+a.dataset.page-1];const match=[q.title,q.translation,q.explanation,q.supplement,String(q.page)].join(' ').toLowerCase().includes(term);a.hidden=!match;if(match)found++;});document.getElementById('search-empty').hidden=found>0;};
 document.querySelectorAll('[data-zoom]').forEach(button=>button.onclick=()=>{const v=+button.dataset.zoom,dialog=document.getElementById('image-dialog');document.getElementById('zoom-image').src=pageImage(v);document.getElementById('zoom-caption').textContent=`PDF p. ${v} · ${v===1?'自製學習封面':D.pages[v-1].title}`;dialog.showModal();});
 requestAnimationFrame(()=>jump(n));
}
function navigatePage(n){if(n>=1&&n<=87){if(readerJump&&document.getElementById('reader-stream')){history.pushState(null,'',`${BASE}/pages/${n}`);readerJump(n,true)}else location.hash=`${BASE}/pages/${n}`;}}
''' +s[end:]
start=s.index('function route()')
end=s.index("window.addEventListener('hashchange',route)")
s=s[:start]+r'''function route(){
 if(!D){main.innerHTML='<p class="error">教材資料未載入。請確認 lesson-data.js 與 index.html 放在同一資料夾。</p>';return;}
 const parts=location.hash.replace(/^#/?/,'').split('/').filter(Boolean),previousMode=state.mode;
 const mode=parts[0]==='linear-algebra'&&parts[1]==='lecture-5'?(parts[2]||'pages'):null;
 if(mode==='pages'&&previousMode==='pages'&&document.getElementById('reader-stream')){readerJump(Math.max(1,Math.min(87,parseInt(parts[3])||1)));return;}
 if(mode==='slides'&&previousMode==='slides'&&document.querySelector('.slide')){updateSlide(Math.max(1,Math.min(D.slides.length,parseInt(parts[3])||1)));return;}
 document.body.classList.remove('reading-mode');readerJump=null;window.scrollTo({top:0,behavior:'instant'});
 if(!parts.length){state.mode='home';home();return}if(parts[0]!=='linear-algebra'){location.hash='#/';return}if(parts.length===1){state.mode='course';course();return}if(parts[1]!=='lecture-5'){location.hash='#/linear-algebra';return}
 state.mode=mode;if(mode==='pages'){state.page=Math.max(1,Math.min(87,parseInt(parts[3])||1));pageView(state.page)}else if(mode==='slides'){state.slide=Math.max(1,Math.min(D.slides.length,parseInt(parts[3])||1));slideView(state.slide)}else if(mode==='notes')notesView();else if(mode==='diagrams')diagramsView();else if(mode==='references')referencesView();else location.hash=BASE+'/pages/1';
}
function updateSlide(n){
 state.slide=n;const s=D.slides[n-1],y=window.scrollY,focus=document.activeElement?.id,mainY=main.scrollTop;
 document.querySelector('.slide h2').textContent=s.title;
 document.querySelector('.slide ul').innerHTML=s.bullets.map(b=>`<li>${esc(b)}</li>`).join('');
 document.querySelector('.slide-footer').innerHTML=`<span>來源：原講義 PDF pp. ${esc(s.refs)}</span><span>${String(n).padStart(2,'0')} / ${D.slides.length}</span>`;
 document.getElementById('slide-select').value=String(n);
 document.getElementById('slide-prev').disabled=n===1;document.getElementById('slide-next').disabled=n===D.slides.length;
 document.querySelector('.speaker p').textContent=s.speaker;
 document.querySelector('.speaker a').href=`${BASE}/pages/${parseInt(s.refs)}`;
 document.querySelector('.mode-tabs a.active').href=`${BASE}/slides/${n}`;
 document.getElementById('slide-prev').onclick=()=>navigateSlide(state.slide-1);
 document.getElementById('slide-next').onclick=()=>navigateSlide(state.slide+1);
 if(focus)document.getElementById(focus)?.focus({preventScroll:true});
 window.scrollTo({top:y,behavior:'instant'});main.scrollTop=mainY;
}
''' +s[end:]
p.write_text(s,encoding='utf-8')
print('Updated continuous reader and in-place slide switching.')
