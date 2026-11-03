from pathlib import Path
import re
root=Path(__file__).resolve().parent.parent
p=root/'website/app.js'
s=p.read_text(encoding='utf-8').replace("await document.getElementById('deck').requestFullscreen()",'await main.requestFullscreen()')
p.write_text(s,encoding='utf-8')
p=root/'website/styles.css'
s=p.read_text(encoding='utf-8')
if '#main:fullscreen{' not in s:
    s+='\n[hidden]{display:none!important}#main:fullscreen{background:var(--bg);overflow:auto;padding:20px}#main:fullscreen .breadcrumbs,#main:fullscreen .unit-heading,#main:fullscreen .mode-tabs,#main:fullscreen .mode-description{display:none}#main:fullscreen .slide{min-height:65vh}\n'
p.write_text(s,encoding='utf-8')
broken=[]
for p in (root/'wiki').rglob('*.md'):
    body=re.sub(r'`[^`]*`','',p.read_text(encoding='utf-8-sig'))
    for target in re.findall(r'\]\(([^)]+)\)',body):
        if '://' in target or target.startswith('#'):continue
        if not (p.parent/target.split('#')[0]).exists():broken.append((str(p),target))
assert not broken,broken
print('Wiki links checked.')
