#!/usr/bin/env python3
"""ep dir -> data.json. Reads <ep>/ep.json (title, phrases[{t,v}]) + <ep>/work/tr.json (Whisper).
Phrase start times: if Whisper segment count == phrase count -> segment starts; else time-warp by characters
(Whisper segments as anchors) and snap to the nearest segment start within 0.35 s."""
import json,sys,bisect
E=sys.argv[1]; ep=json.load(open(f'{E}/ep.json')); tr=json.load(open(f'{E}/work/tr.json'))
segs=[(s['start'],s['end'],s['text'].strip()) for s in tr['segments']]; END=segs[-1][1]
ph=ep['phrases']; txt=[p['t'] for p in ph]
L=lambda s: len(s.replace(' ',''))
def dp_align(segs,txt):
    """phrase j starts at segment b_j (monotonic); minimise char mismatch of each phrase vs its segments."""
    n,m=len(txt),len(segs); sc=[L(s[2]) for s in segs]; pc=[L(x) for x in txt]
    k=sum(sc)/max(1,sum(pc)); pc=[c*k for c in pc]
    pre=[0]
    for c in sc: pre.append(pre[-1]+c)
    INF=1e18; best=[[INF]*(m+1) for _ in range(n+1)]; arg=[[0]*(m+1) for _ in range(n+1)]
    best[0][0]=0
    for j in range(1,n+1):
        for e in range(j,m-(n-j)+1):
            for b in range(j-1,e):
                if best[j-1][b]>=INF: continue
                c=best[j-1][b]+abs((pre[e]-pre[b])-pc[j-1])
                if c<best[j][e]: best[j][e]=c; arg[j][e]=b
    e=m; starts=[]
    for j in range(n,0,-1):
        b=arg[j][e]; starts.append(segs[b][0]); e=b
    return starts[::-1]
if len(segs)==len(ph): st=[s[0] for s in segs]
elif len(segs)>len(ph):
    st=dp_align(segs,txt); print('note: %d segments vs %d phrases -> DP alignment'%(len(segs),len(ph)))
else:

    # anchors: cumulative char fraction of whisper text at each segment start/end
    tot=sum(L(s[2]) for s in segs) or 1; F=[0.0]; Tm=[segs[0][0]]; acc=0
    for a,b,s in segs: acc+=L(s); F.append(acc/tot); Tm.append(b)
    tot2=sum(L(x) for x in txt); st=[]; acc=0
    for x in txt:
        f=acc/tot2; i=min(len(F)-2,max(0,bisect.bisect_right(F,f)-1)); seg_t=segs[i][0] if i<len(segs) else Tm[i]
        k=(f-F[i])/max(1e-6,F[i+1]-F[i]); tt=segs[i][0]+(segs[i][1]-segs[i][0])*k
        near=min(segs,key=lambda s:abs(s[0]-tt))[0]
        st.append(near if abs(near-tt)<.35 else tt); acc+=L(x)
    for i in range(1,len(st)): st[i]=max(st[i],st[i-1]+.4)
    print('note: %d segments vs %d phrases -> char time-warp'%(len(segs),len(ph)))
nx=lambda i: st[i+1] if i+1<len(st) else END+.6
cap=[]
for i,p in enumerate(txt):
    a,b=st[i],nx(i); w=p.split()
    if len(p)>24 and len(w)>=3:
        h=len(w)//2; p1,p2=' '.join(w[:h]),' '.join(w[h:]); m=a+(b-a)*len(p1)/len(p)
        cap+=[[a,m,p1],[m,b,p2]]
    else: cap.append([a,b,p])
D={'title':ep['title'],'ph':[{'a':st[i],'b':nx(i),'v':ph[i].get('v',{})} for i in range(len(ph))],'cap':cap,'dur':END+1.3}
json.dump(D,open(f'{E}/data.json','w'),ensure_ascii=False); print('built',E,round(END,2),'s',len(ph),'phrases')
