import json
# ep04 «العقد القديم» — one phrase per Whisper segment
tr=json.load(open('work/tr.json')); seg=[s['start'] for s in tr['segments']]; END=tr['segments'][-1]['end']
dar=["زمان، الراجل والمرا كانو موقعين واحد العقد…","حتى واحد ما كتبو.","هو كيخدم ويجيب الفلوس،","وهي كتدبر الدار والولاد.",
"ماشي ديما كان عادل…","ولكن كل واحد كان عارف شنو كيتسنى منو.","دابا، بجوج خدامين، بجوج عيانين،","وبجوج راجعين للدار على سبعة.",
"والعقد القديم؟ تقطع…","وما تكتبش بلاصتو حتى عقد جديد.","وهنا كيبدا الحساب فالسر:","«أنا خدمت كثر»، «أنا تعبت كثر».",
"الباحثين كيسميو هادشي","Mental load","الشغل اللي ما كيبانش،","بحال التفكير فشنو غادي ناكلو،","وشكون غادي يخلص الضو.",
"المشكل ماشي فالمرا اللي خدامة،","وماشي فالراجل اللي تبدل.","المشكل أننا عايشين بقواعد جديدة…","بعقد قديم.",
"جلسو وكتبو العقد ديالكم:","شكون كيدير شنو.","حيت اللي ما كيتقالش… كيتحسب.","ونتوما؟","عندكم العقد القديم… ولا الجديد؟"]
assert len(dar)==len(seg),(len(dar),len(seg))
nx=lambda i: seg[i+1] if i+1<len(seg) else END+.6
cap=[]
for i,p in enumerate(dar):
    a,b=seg[i],nx(i); w=p.split()
    if len(p)>24 and len(w)>=3:
        h=len(w)//2; p1,p2=' '.join(w[:h]),' '.join(w[h:]); m=a+(b-a)*len(p1)/len(p)
        cap+=[[a,m,p1],[m,b,p2]]
    else: cap.append([a,b,p])
D={'s':[0,seg[2],seg[6],seg[10],seg[17],seg[21]],'t':seg,'cap':cap,'dur':END+1.3}
json.dump(D,open('data.json','w'),ensure_ascii=False); print('ok',round(END,2),len(cap))
