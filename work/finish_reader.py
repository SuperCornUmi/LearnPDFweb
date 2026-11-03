from pathlib import Path
p=Path('website/app.js')
s=p.read_text(encoding='utf-8')
s=s.replace("location.hash.replace(/^#/?/,'')",'location.hash.slice(1)')
s=s.replace('requestAnimationFrame(()=>jump(n));','requestAnimationFrame(()=>{fitReader();jump(n)});')
# Source uses a double closing parenthesis for the callback invocation.
s=s.replace('requestAnimationFrame(()=>jump(n));','requestAnimationFrame(()=>{fitReader();jump(n)});')
if 'function fitReader()' not in s:
    s=s.replace('function pageImage(n)',"function fitReader(){const stream=document.getElementById('reader-stream');if(stream)stream.style.height=Math.max(280,innerHeight-stream.getBoundingClientRect().top-14)+'px';}\nwindow.addEventListener('resize',()=>{fitReader();if(readerJump&&state.mode==='pages')readerJump(state.page)});\nfunction pageImage(n)")
p.write_text(s,encoding='utf-8')
print('Reader sizing and route syntax updated.')
