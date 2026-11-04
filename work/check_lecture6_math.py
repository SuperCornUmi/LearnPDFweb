from fractions import Fraction as F
from pathlib import Path
import json,hashlib
def matrix(a):return [[F(x) for x in row] for row in a]
def mul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def inverse(a):
    n=len(a);r=[list(map(F,row))+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for i in range(n):
        j=next(j for j in range(i,n) if r[j][i]);r[i],r[j]=r[j],r[i]
        d=r[i][i];r[i]=[v/d for v in r[i]]
        for k in range(n):
            if k!=i:
                q=r[k][i];r[k]=[x-q*y for x,y in zip(r[k],r[i])]
    return [row[n:] for row in r]
def rref(a):
    r=matrix(a);row=0;pivots=[]
    for c in range(len(r[0])):
        p=next((i for i in range(row,len(r)) if r[i][c]),None)
        if p is None:continue
        r[row],r[p]=r[p],r[row];v=r[row][c];r[row]=[x/v for x in r[row]]
        for i in range(len(r)):
            if i!=row:
                v=r[i][c];r[i]=[x-v*y for x,y in zip(r[i],r[row])]
        pivots.append(c);row+=1
        if row==len(r):break
    return r,pivots
U=[[1,1,1],[1,2,2],[0,0,1]];V=[[1,2,1],[1,3,5],[1,2,4]]
S=mul(inverse(U),V);assert S==matrix([[1,1,-3],[-1,-1,0],[1,2,4]])
assert mul(S,[[3],[2],[-1]])==[[8],[-5],[3]]
assert mul(S,[[1],[-3],[2]])==[[-8],[2],[3]]
A=[[1,2,-1,1],[2,4,-3,0],[1,2,1,5]]
assert rref(A)[0]==matrix([[1,2,0,3],[0,0,1,2],[0,0,0,0]])
assert mul(A,[[-2,-3],[1,0],[0,-2],[0,1]])==[[0,0],[0,0],[0,0]]
A4=[[1,-2,1,1,2],[-1,3,0,2,-2],[0,1,1,3,4],[1,2,5,13,5]]
assert rref(A4)[1]==[0,1,4]
X=[[1,2,2,3],[2,5,4,8],[-1,-3,-2,-5],[0,2,0,4]];assert rref(X)[1]==[0,1]
B=[[1,1,1],[0,1,1],[0,0,1]];images=[[2,1],[3,4],[-1,2]]
assert mul(inverse(B),images)==matrix([[-1,-3],[4,2],[-1,2]])
P=[[1,0,-2],[0,2,0],[0,0,4]];D0=[[0,1,0],[0,0,2],[0,0,0]]
assert mul(mul(inverse(P),D0),P)==[[0,2,0],[0,0,4],[0,0,0]]
assert mul(mul(P,D0),inverse(P))==matrix([[0,F(1,2),0],[0,0,1],[0,0,0]])
A=[[2,2,0],[1,1,2],[1,1,2]];S=[[1,-2,1],[-1,1,1],[0,1,1]]
assert mul(mul(inverse(S),A),S)==[[0,0,0],[0,1,0],[0,0,4]]
assert inverse(S)==matrix([[0,-1,1],[F(-1,3),F(-1,3),F(2,3)],[F(1,3),F(1,3),F(1,3)]])
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'teaching/linear-algebra/lecture-6/lesson.json').read_text(encoding='utf-8'))
assert [p['page'] for p in data['pages']]==list(range(1,153))
assert len(data['slides'])==20 and all(p[k] for p in data['pages'] for k in ['translation','explanation'])
meta=json.loads((root/'raw/metadata/src-20261103-ce2005-lecture-6.json').read_text(encoding='utf-8'))
assert hashlib.sha256((root/meta['stored_path']).read_bytes()).hexdigest()==meta['sha256']
assert hashlib.sha256(Path(meta['original_path']).read_bytes()).hexdigest()==meta['sha256']
print('PASS: exact rational checks for coordinates, inverses, row/column pivots, kernel bases, representation matrices, both similarity examples and errata; 152 pages, 20 slides, PDF hash unchanged.')
