"""Check arithmetic and algorithm models; this does NOT execute MASM machine code."""
import json
from pathlib import Path
def positional(x,y):
    assert len(x)==len(y)
    count=0
    for a,b in zip(x,y):
        if a==b:count+=1
    return count
def cross_unique(x,y):
    assert len(set(x))==len(x) and len(set(y))==len(y)
    count=0
    for a in x:
        for b in y:
            if a==b:
                count+=1;break
    return count
examples=[([10,5,4,-6,2,11,12],[10,5,3,1,4,2,-6],2,5),([],[],0,0),([-2,0,3],[-2,0,3],3,3),([1,2],[3,4],0,0),([-1,2],[2,-1],0,2)]
for x,y,a,b in examples:assert (positional(x,y),cross_unique(x,y))==(a,b)
assert 30-14==16 and 5+6==11 and hex(50)=='0x32'
s=0x1000;stack={};esp=s
for value in [6,5,'return','old EBP']:
    esp-=4;stack[esp]=value
ebp=esp
assert stack[ebp+8]==5 and stack[ebp+12]==6 and stack[ebp+4]=='return'
esp=ebp-8
esp=ebp;esp+=4 # LEAVE model
esp+=4+8      # RET 8 model
assert esp==s
esp=0x19ff58;observed=[]
for size in [4,2,2,4]:esp-=size;observed.append(f'{esp:08X}')
assert observed==['0019FF54','0019FF52','0019FF50','0019FF4C']
def fill(buf,n,value):
    if n==0:return buf
    for i in range(n):buf[i]=value
    return buf
assert fill([0,0,0],3,7)==[7,7,7] and fill([],0,7)==[]
out=dict(date='2026-11-05',kind='Python arithmetic/algorithm models only',array_pairs=len(examples),results='passed',push_esp=observed,native_masm_execution=False)
(Path(__file__).parent/'model-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out))
