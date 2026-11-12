# tiny-chess-01: readable fixed-node negamax engine, <4 KB.
import json,os,urllib.request as U
EU=os.environ.get("MAKEFUN_ENV_URL","")
V=(0,100,320,330,500,900,0)
ND_=(-21,-19,-12,-8,8,12,19,21);BD_=(-9,-11,9,11);RD_=(-10,-1,1,10)
KD=BD_+RD_
CAST={95:((1,97,(96,97),(95,96,97)),(2,93,(92,93,94),(93,94,95))),
 25:((4,27,(26,27),(25,26,27)),(8,23,(22,23,24),(23,24,25)))}
CR={91:2,98:1,21:8,28:4}
M=100000;N=0
class TO(Exception):pass
def att(bd,s,w):
 g=1 if w else -1
 if g in (bd[s+9*g],bd[s+11*g]):return 1
 for o in ND_:
  if bd[s+o]==2*g:return 1
 for o in KD:
  j=s+o;q=bd[j]
  if q==6*g:return 1
  while q==0:j+=o;q=bd[j]
  if q==g*(3 if abs(o) in (9,11) else 4) or q==5*g:return 1
 return 0
def bad(bd,w):
 return att(bd,bd.index(6 if w else -6),not w)
def gen(st,cap=0):
 bd,side,cast,ep=st
 g=1 if side else -1
 ms=[];ap=ms.append
 for i in range(21,99):
  p=bd[i]
  if p==99 or p*g<=0:continue
  t=p*g
  if t==1:
   d=-10*g;j=i+d
   if bd[j]==0:
    if j<29 or j>90:ap((i,j,5))
    elif not cap:
     ap((i,j,0))
     if i//10 in (3,8) and bd[j+d]==0:ap((i,j+d,0))
   for dd in (d-1,d+1):
    j=i+dd;q=bd[j]
    if q!=99 and q*g<0:ap((i,j,5 if j<29 or j>90 else 0))
    elif j==ep:ap((i,j,0))
  else:
   for o in (0,0,ND_,BD_,RD_,KD,KD)[t]:
    j=i+o
    while bd[j]==0:
     if not cap:ap((i,j,0))
     if t in (2,6):break
     j+=o
    q=bd[j]
    if q!=99 and q*g<0:ap((i,j,0))
   if t==6 and not cap:
    K0=95 if side else 25
    for bit,to,emp,safe in CAST[K0]:
     if cast&bit and all(bd[x]==0 for x in emp) and not any(att(bd,x,not side) for x in safe):ap((K0,to,0))
 return ms
def mk(st,m):
 bd=st[0][:]
 i,j,pr=m;p=bd[i];cap=bd[j];csq=j
 if abs(p)==1 and cap==0 and i%10!=j%10:
  csq=j+10 if p>0 else j-10;cap=bd[csq];bd[csq]=0
 bd[j]=(pr if p>0 else -pr) if pr else p;bd[i]=0
 if abs(p)==6 and abs(j-i)==2:
  r=(i+3,i+1) if j>i else (i-4,i-1);bd[r[1]]=bd[r[0]];bd[r[0]]=0
 c=st[2]
 if abs(p)==6:c&=12 if p>0 else 3
 for x in (i,csq):c&=~CR.get(x,0)&15
 return [bd,not st[1],c,(i+j)//2 if abs(p)==1 and abs(j-i)==20 else 0]
def ev(st):
 bd=st[0];s=0
 for i in range(21,99):
  p=bd[i]
  if not p or p==99 or abs(p)==6:continue
  t=abs(p);rn=10-i//10;k=min(i%10,9-i%10)+min(rn,9-rn)-4
  v=V[t]+(6*(rn-1 if p>0 else 8-rn) if t==1 else (0,0,9,4,0,2)[t]*k)
  s+=v if p>0 else -v
 return s if st[1] else -s
def sr(st,d,a,b):
 global N
 N+=1
 if N>12000:raise TO
 bd=st[0];side=st[1];chk=bad(bd,side);quiet=d<=0 and not chk
 best=ev(st) if quiet else -M-1
 if quiet:
  if best>=b:return best
  if best>a:a=best
 for m in sorted(gen(st,1 if quiet else 0),reverse=True,key=lambda m:
   10000+V[abs(bd[m[1]])] if bd[m[1]] else 0):
  ns=mk(st,m)
  if bad(ns[0],side):continue
  s=-sr(ns,d-1,-b,-a)
  if s>best:best=s
  if s>a:
   a=s
   if a>=b:break
 if best==-M-1 and (d>0 or chk):return -M-d if chk else 0
 return best
def choose(st):
 global N
 ms=[m for m in gen(st) if not bad(mk(st,m)[0],st[1])]
 bm=ms[0];N=0
 for d in range(1,64):
  a=-M-1;cb=bm
  try:
   for m in ms:
    s=-sr(mk(st,m),d-1,-M-1,-a)
    if s>a:a=s;cb=m
  except TO:break
  bm=cb;ms.remove(bm);ms.insert(0,bm)
 return bm
def uci(m):
 f=lambda i:chr(96+i%10)+str(10-i//10)
 return f(m[0])+f(m[1])+("nbrq"[m[2]-2] if m[2] else "")
def parse(fen):
 bd=[0 if 20<i<99 and 0<i%10<9 else 99 for i in range(120)]
 w=fen.split();i=21
 for ch in w[0]:
  if ch=="/":i+=2
  elif ch.isdigit():i+=int(ch)
  else:
   t="pnbrqk".index(ch.lower())+1;bd[i]=t if ch.isupper() else -t;i+=1
 c=sum(1<<"KQkq".index(ch) for ch in w[2] if ch in "KQkq")
 e=21+(8-int(w[3][1]))*10+ord(w[3][0])-97 if w[3]!="-" else 0
 return [bd,w[1]=="w",c,e]
def post(p,b):
 r=U.urlopen(U.Request(EU+p,data=json.dumps(b).encode()))
 return json.load(r)
def main():
 while 1:
  g=post("/game",{})
  if g.get("status")=="done":break
  while g.get("status")=="your_move":
   try:m=choose(parse(g["fen"]))
   except Exception:m=None
   try:g=post("/move",{"game":g["game"],"move":uci(m) if m else g["legal_moves"][0]})
   except Exception:g=post("/game",{})
if __name__=="__main__":main()
# tiny-chess-01 @urelkdubdqwr
# deterministic fixed-node search
