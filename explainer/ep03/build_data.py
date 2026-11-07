import json
# ep03 «لا قاصح، لا مسكين» — one phrase per Whisper segment
tr=json.load(open('work/tr.json')); seg=[s['start'] for s in tr['segments']]; END=tr['segments'][-1]['end']
dar=["علاش الشخص اللي كيقول «واخا» لكلشي…","هو اللي كيتخلاو عليه الأول؟","فالعلاقة، كاينين جوج أنواع ديال الناس كيفشلو:",
"الأول قاصح:","بارد،","كيعطي غير الأوامر،","والحنان ما كيبانش عليه.","الثاني مسكين:","كيقول «واخا» لكلشي،",
"غير باش ما يزعف حتى واحد.","الأول كيخوّف…","والثاني ما كيبقاش كيتحترم.","وكاين نوع ثالث،","هو اللي كيتبغى بصح:",
"Warm but firm","حنين فالكلام،","ولكن عندو Boundaries واضحين.","كيقول «لا» بلا ما يغوت،","وبلا ما يعتذر عشرين مرة.",
"مثلا:","«كنبغيك،","ولكن هاد الطريقة ديال الهضرة ما مقبولاش عندي.»","الحنان كيعطي الأمان،","والحزم كيعطي الاحترام.",
"وإلا طاح واحد فيهم…","العلاقة كتميل.","ماشي خاصك تختار واش تكون حنين ولا تكون قوي…","خاصك تكون بجوج.",
"ونتوما؟","شكون فيكم الحنين…","وشكون الحازم؟"]
assert len(dar)==len(seg),(len(dar),len(seg))
nx=lambda i: seg[i+1] if i+1<len(seg) else END+.6
cap=[]
for i,p in enumerate(dar):
    a,b=seg[i],nx(i); w=p.split()
    if len(p)>24 and len(w)>=3:
        h=len(w)//2; p1,p2=' '.join(w[:h]),' '.join(w[h:]); m=a+(b-a)*len(p1)/len(p)
        cap+=[[a,m,p1],[m,b,p2]]
    else: cap.append([a,b,p])
D={'s':[0,seg[2],seg[12],seg[19],seg[22],seg[26]],'t':seg,'cap':cap,'dur':END+1.3}
json.dump(D,open('data.json','w'),ensure_ascii=False); print('ok',round(END,2),len(cap))
