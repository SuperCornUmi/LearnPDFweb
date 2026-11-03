from fractions import Fraction as F
from pathlib import Path
import hashlib,json

def det(rows):
    a=[[F(x) for x in r] for r in rows]
    value=F(1)
    for i in range(len(a)):
        pivot=next((j for j in range(i,len(a)) if a[j][i]),None)
        if pivot is None:return F(0)
        if pivot!=i:a[i],a[pivot]=a[pivot],a[i];value=-value
        d=a[i][i];value*=d
        for j in range(i+1,len(a)):
            k=a[j][i]/d
            for c in range(i,len(a)):a[j][c]-=k*a[i][c]
    return value
def combo(vs,cs):return [sum(c*v[i] for c,v in zip(cs,vs)) for i in range(len(vs[0]))]
assert combo([(1,-1,2),(-2,3,1),(-1,3,8)],[3,2,-1])==[0,0,0]
assert combo([(1,2,3),(1,0,0),(0,1,0),(0,0,1)],[1,-1,-2,-3])==[0,0,0]
assert combo([(1,2,3),(1,0,0),(0,1,0),(0,0,1)],[1,2,3,-1])!=[0,0,0]
assert combo([(1,2,4),(2,1,3),(4,-1,1)],[2,-3,1])==[0,0,0]
assert det([[4,2,2],[2,3,-5],[3,1,3]])==0
assert combo([(4,2,3),(2,3,1),(2,-5,3)],[2,-3,-1])==[0,0,0]
assert combo([(1,-1,2,3),(-2,3,1,-2),(1,0,7,7)],[-3,-1,1])==[0,0,0,0]
assert det([[1,2,1],[-2,1,8],[3,8,7]])==0
assert combo([(1,-2,3),(2,1,8),(1,8,7)],[3,-2,1])==[0,0,0]
assert det([[1,0,2],[1,1,0],[1,1,1]])==1
assert det([[1,1,1],[1,1,0],[1,0,1]])==-1
assert det([[1,-2,1],[2,1,0],[3,0,1]])==2
for v in [(1,-2,1,0),(-1,1,0,1)]:
    assert v[0]+v[1]+v[2]==0 and 2*v[0]+v[1]+v[3]==0
root=Path(__file__).resolve().parents[1]
meta=json.loads((root/'raw/metadata/src-20261103-ce2005-lecture-5.json').read_text(encoding='utf-8-sig'))
assert hashlib.sha256((root/'raw/pdfs/CE2005_Lecture_5.pdf').read_bytes()).hexdigest()==meta['sha256']
notes=(root/'notes/linear-algebra/lecture-5.md').read_text(encoding='utf-8')
assert all(f'## PDF p. {n}｜' in notes for n in range(1,88))
assert notes.count('## PDF p. ')==87
print('PASS: numeric dependence relations, determinant examples, null-space vectors, source integrity and 87-page coverage.')
