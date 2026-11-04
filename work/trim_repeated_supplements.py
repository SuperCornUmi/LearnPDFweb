from pathlib import Path
root=Path(__file__).resolve().parents[1]
for n,indices in [(5,{53}),(6,{56,110,137})]:
 path=root/f'teaching/linear-algebra/lecture-{n}/pages.txt'
 lines=path.read_text(encoding='utf-8').splitlines()
 for i in indices:
  row=lines[i-1].split('｜');row[3]='';lines[i-1]='｜'.join(row)
 path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
