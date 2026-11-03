from pathlib import Path
root=Path(__file__).resolve().parents[1]
old=root/'website/index.html'
new=root/'index.html'
assert old.resolve().parent==root/'website'
assert not new.exists(), 'Root index.html already exists; inspect before replacing.'
html=old.read_text(encoding='utf-8')
for name in ['styles.css','reader.css','lesson-data.js','app.js']:
    html=html.replace('"'+name+'"','"website/'+name+'"')
html=html.replace('"../wiki/','"wiki/').replace('"../notes/','"notes/')
old.rename(new)
new.write_text(html,encoding='utf-8')
p=root/'website/app.js'
s=p.read_text(encoding='utf-8')
s=s.replace('../raw/','raw/').replace('../wiki/','wiki/')
s=s.replace('assets/lecture5/','website/assets/lecture5/').replace('"downloads/','"website/downloads/')
p.write_text(s,encoding='utf-8')
p=root/'teaching/linear-algebra/lecture-5/build.py'
s=p.read_text(encoding='utf-8').replace('website/index.html','index.html').replace("url='../raw/","url='raw/")
p.write_text(s,encoding='utf-8')
docs=[root/'README.md',root/'AGENTS.md',root/'website/README.md']+list((root/'wiki').rglob('*.md'))
for p in docs:
    if p.name=='log.md':continue
    s=p.read_text(encoding='utf-8').replace('website/index.html','index.html')
    p.write_text(s,encoding='utf-8')
for name in ['check-reader-v2.cjs','check-website.cjs']:
    p=root/'work'/name
    if p.exists():p.write_text(p.read_text(encoding='utf-8').replace("path.resolve('website/index.html')","path.resolve('index.html')"),encoding='utf-8')
(root/'.nojekyll').touch()
print('Moved root entry and adjusted document-relative URLs, build source, documentation and browser checks.')
