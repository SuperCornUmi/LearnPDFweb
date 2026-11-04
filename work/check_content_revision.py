from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[1]
protected=json.loads((root/'work/content-revision-protected.json').read_text(encoding='utf-8'))
for path,expected in protected.items():
 assert hashlib.sha256((root/path).read_bytes()).hexdigest()==expected,('unrelated file changed',path)
for n,total,expected_supplements in [(5,87,9),(6,152,11)]:
 unit=root/f'teaching/linear-algebra/lecture-{n}'
 data=json.loads((unit/'lesson.json').read_text(encoding='utf-8'))
 pages=data['pages'];assert [p['page'] for p in pages]==list(range(1,total+1))
 old=(root/f'work/lecture-{n}-pages-before-detail-revision.txt').read_text(encoding='utf-8').splitlines()
 assert all(p['explanation']!=before.split('｜')[2] for p,before in zip(pages,old))
 assert all(p['translation'] and p['explanation'] for p in pages)
 assert sum(bool(p['supplement']) for p in pages)==expected_supplements
 assert len(set(p['explanation'] for p in pages))==total
 notes=(root/f'notes/linear-algebra/lecture-{n}.md').read_text(encoding='utf-8')
 assert re.findall(r'^## PDF p\. (\d+)｜',notes,re.M)==list(map(str,range(1,total+1)))
 assert notes.count('### 教學補充／提醒')==expected_supplements
 for p in pages:
  assert p['explanation'] in notes
  assert p['translation'].replace('`','') in notes.replace('`','')
 assert (root/f'website/downloads/lecture-{n}-notes.md').read_text(encoding='utf-8')==notes
 manifest=json.loads((unit/'manifest.json').read_text(encoding='utf-8'))
 for path,digest in manifest['inputs'].items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest,path
 print(f'PASS Lecture {n}: {total} individually revised explanations, {expected_supplements} optional supplements, Markdown/site data/downloads and hashes agree.')
print(f'PASS: {len(protected)} protected source, Wiki, standards, slide, image and style files unchanged.')
