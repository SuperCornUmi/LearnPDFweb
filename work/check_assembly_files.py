from pathlib import Path
import json,re,hashlib
from urllib.parse import unquote
R=Path(__file__).resolve().parent.parent;U=R/'teaching/assembly-language/chapter-8'
data=json.loads((U/'lesson.json').read_text(encoding='utf-8'))
assert len(data['pages'])==51 and len(data['slides'])==16
assert [p['page'] for p in data['pages']]==list(range(1,52))
notes=(R/'notes/assembly-language/chapter-8.md').read_text(encoding='utf-8')
assert len(re.findall(r'^## PDF p\. \d+｜',notes,re.M))==51
assert notes.count('### 中文翻譯')==51 and notes.count('### 觀念講解')==51
assert notes.count('### 教學補充／提醒')==sum(bool(p['supplement']) for p in data['pages'])
for p in data['pages']:assert p['translation'].count('```')%2==0 and p['explanation'].count('```')%2==0
for name in ['slides','speaker-notes']:
    text=(R/f'presentations/assembly-language/chapter-8/{name}.md').read_text(encoding='utf-8')
    assert len(re.findall(r'^## 投影片 \d+｜',text,re.M))==16
assert (R/'website/downloads/assembly-chapter-8-notes.md').read_bytes()==(R/'notes/assembly-language/chapter-8.md').read_bytes()
assert len(list((R/'website/assets/assembly-ch8').glob('*.webp')))==50
assert (R/'website/assets/assembly-ch8/cover.svg').exists()
sha=hashlib.sha256((R/'raw/pdfs/1151 ch8.pdf').read_bytes()).hexdigest()
assert sha==hashlib.sha256(Path('C:/Users/miu99/Downloads/1151 ch8.pdf').read_bytes()).hexdigest()
assert sha==json.loads((R/'raw/metadata/src-20261105-assembly-ch8.json').read_text(encoding='utf-8'))['sha256']
broken=[];files=list((R/'wiki').rglob('*.md'))+list((R/'notes/assembly-language').glob('*.md'))+list((R/'presentations/assembly-language').rglob('*.md'))+list(U.glob('*.md'))+list((R/'website/downloads').glob('assembly-chapter-8-*.md'))+[R/'README.md',R/'website/README.md']
for p in files:
    body=re.sub(r'```[\s\S]*?```','',p.read_text(encoding='utf-8-sig'))
    body=re.sub(r'`[^`]*`','',body)
    for target in re.findall(r'\]\(([^)]+)\)',body):
        if '://' in target or target.startswith('#'):continue
        target=unquote(target.split('#')[0])
        if not (p.parent/target).exists():broken.append((str(p.relative_to(R)),target))
assert not broken,broken
index=(R/'wiki/index.md').read_text(encoding='utf-8')
for path in ['sources/src-20261105-assembly-ch8.md','sources/web-20261105-microsoft-masm-procedures.md','topics/組合語言.md','concepts/堆疊框架與呼叫慣例.md','concepts/值與位址及MASM定址.md','questions/CountMatches如何區分位置與跨位置匹配.md']:assert path in index
manifest=json.loads((U/'manifest.json').read_text(encoding='utf-8'))
for path,sha in manifest['inputs'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==sha,path
result=dict(date='2026-11-05',pages=51,slides=16,images=51,markdown_files_checked=len(files),broken_links=broken,source_hash_match=True,manifest_hashes_match=True)
(R/'work/src-20261105-assembly-ch8/file-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
