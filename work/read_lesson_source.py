from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parents[1]
n=int(sys.argv[1]);a=int(sys.argv[2]);b=int(sys.argv[3])
base=root/f'work/src-20261103-ce2005-lecture-{n}'
if n==6:pages=json.loads((base/'pages.json').read_text(encoding='utf-8'))
else:pages=re.split(r'=== PDF PAGE \d+ ===', (base/'text.txt').read_text(encoding='utf-8'))[1:]
for i in range(a-1,b):
 lines=[s for s in pages[i].splitlines() if len(re.findall(r'[A-Za-z]{2,}',s))>=2 and not s.startswith('CE2005') and 'Chia-Ru' not in s]
 print(f'[{i+1}] '+' '.join(lines))
