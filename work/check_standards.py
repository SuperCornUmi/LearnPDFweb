from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[1]
broken=[]
targets=[root/'AGENTS.md',root/'README.md',root/'website/README.md']+list((root/'wiki').rglob('*.md'))+list((root/'teaching').rglob('README.md'))+list((root/'notes').rglob('*.md'))
for path in targets:
    body=path.read_text(encoding='utf-8-sig')
    body=re.sub(r'```.*?```','',body,flags=re.S)
    body=re.sub(r'`[^`]*`','',body)
    for target in re.findall(r'(?<!!)\[[^\[\]\n]+\]\(([^)]+)\)',body):
        if '://' in target or target.startswith('#'):continue
        if not (path.parent/target.split('#')[0]).exists():broken.append((str(path.relative_to(root)),target))
assert not broken,broken
standard='wiki/standards/PDF課程教材製作標準.md'
assert standard in (root/'AGENTS.md').read_text(encoding='utf-8')
assert 'standards/PDF課程教材製作標準.md' in (root/'wiki/index.md').read_text(encoding='utf-8')
for name in ['lesson-notes.md','page-explanation.md','lesson-slides.md','lesson-delivery.md']:
    assert (root/'templates'/name).exists()
manifest=json.loads((root/'teaching/linear-algebra/lecture-5/manifest.json').read_text(encoding='utf-8'))
assert manifest['standard_version']=='1.0'
assert standard in manifest['inputs']
assert manifest['pdf_pages']==87 and manifest['slides']==15
print(f'PASS: {len(targets)} Markdown files checked; all local links resolve; AGENTS/index/standard/templates connected; manifest v1.0 includes standard hash; 87 pages / 15 slides retained.')
