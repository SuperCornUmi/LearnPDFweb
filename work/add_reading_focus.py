from pathlib import Path
p=Path('website/app.js')
s=p.read_text(encoding='utf-8')
old="if(stream)stream.style.height=Math.max(280,innerHeight-stream.getBoundingClientRect().top-14)+'px';"
new="if(stream){const height=Math.max(280,innerHeight-stream.getBoundingClientRect().top-10);stream.style.height=height+'px';stream.style.setProperty('--reader-height',height+'px');}"
assert old in s
s=s.replace(old,new,1)
needle=" document.body.classList.add('reading-mode');"
replacement=""" document.body.classList.add('reading-mode');
 document.querySelector('.site-header').id='site-header';
 document.querySelector('.reader .breadcrumbs').id='lesson-breadcrumbs';
 document.querySelector('.unit-heading').id='lesson-heading';
 document.querySelector('.mode-tabs').id='lesson-modes';
 const focusButton=document.createElement('button');
 focusButton.id='reading-focus-toggle';
 focusButton.setAttribute('aria-controls','site-header lesson-breadcrumbs lesson-heading lesson-modes');
 document.querySelector('.reader-tools').prepend(focusButton);
 const setFocus=focused=>{document.body.classList.toggle('reading-focus',focused);focusButton.textContent=focused?'展開導覽 ▾':'收起上方 ▴';focusButton.setAttribute('aria-expanded',String(!focused));store.set('reader-header',focused?'closed':'open');};
 setFocus(store.get('reader-header','closed')==='closed');
 focusButton.onclick=()=>{const stream=document.getElementById('reader-stream'),top=stream.scrollTop;setFocus(!document.body.classList.contains('reading-focus'));fitReader();stream.scrollTop=top;};"""
assert needle in s
s=s.replace(needle,replacement,1)
s=s.replace("document.body.classList.remove('reading-mode');","document.body.classList.remove('reading-mode','reading-focus');")
p.write_text(s,encoding='utf-8')
print('Added persistent, accessible reading header collapse control.')
