import json,sys
# ep02 «شكون الغالط؟» — phrases with their start times (Whisper segments; English terms fill the gaps Whisper skipped)
tr=json.load(open('work2/tr.json')); seg=[s['start'] for s in tr['segments']]; END=tr['segments'][-1]['end']
dar=["فاش كتوقع شي مشكلة بيناتكم…","شكون فيكم اللي كيقول","«سمح ليا» الأول؟","بزاف ديال الكوبلات كيدخلو فواحد اللعبة:",
"هو كيقول «نتي اللي بديتي»،","هي كتقول «نتا اللي خليتيني ندير هكا».","وكل واحد كيلعب دور الضحية…","هادشي كيسميوه عقلية الضحية.",
"المشكل ماشي فالغلطة،","المشكل فاللي ما بغاش يشدها.","حيت ملي ما كاينش تحمّل المسؤولية،","نفس الخصومة كترجع…","كل سيمانة.",
"القاعدة ساهلة:","حتى إلا كانت الغلطة 90% ديالو،","شد الـ10% ديالك نتا.","«أنا غلطت فهادي.»","بلا «ولكن».",
"وشوف شنو كيوقع:","ملي واحد كيعترف،","الآخر كيطيح السلاح،","وكيبدا حتى هو يعترف بالجهة ديالو.",
"ولكن رد البال:","المحاسبة ماشي تبقى تحاسب الآخر كل نهار.","اللي كيحاسب بزاف","كيولي قاضي…","ماشي شريك.",
"العلاقة اللي كتعيش","ماشي اللي ما فيهاش الغلط…","هي اللي فيها جوج كيقولو:","«أنا».","ونتوما؟","شكون فيكم اللي كيعتذر الأول؟"]
assert len(dar)==len(seg),(len(dar),len(seg))
ph=list(zip(seg,dar))
ph.sort()
st=[p[0] for p in ph]; txt=[p[1] for p in ph]
nx=lambda i: st[i+1] if i+1<len(st) else END+.6
cap=[]
for i,p in enumerate(txt):
    a,b=st[i],nx(i); w=p.split()
    if len(p)>24 and len(w)>=3:
        h=len(w)//2; p1,p2=' '.join(w[:h]),' '.join(w[h:]); m=a+(b-a)*len(p1)/len(p)
        cap+=[[a,m,p1],[m,b,p2]]
    else: cap.append([a,b,p])
I={t:s for s,t in ph}
k=lambda s: I[s]
D={'s':[0,k(dar[3]),k(dar[8]),k(dar[13]),k(dar[18]),k(dar[22]),k(dar[27])],
   'c':{ 'sorry':k(dar[1]),'sorry2':k(dar[2]),'w':k(dar[4]),'r':k(dar[5]),'victim':k(dar[6]),'vm':k(dar[7])+1.1,
     'hold':k(dar[9]),'noacc':k(dar[10]),'acc':k(dar[10])+1.0,'again':k(dar[11]),'week':k(dar[12]),
     'bar':k(dar[14]),'take':k(dar[15]),'ana':k(dar[16]),'bla':k(dar[17]),
     'adm':k(dar[19]),'drop':k(dar[20]),'both':k(dar[21]),
     'check':k(dar[23]),'judge':k(dar[24]),'qadi':k(dar[25]),'partner':k(dar[26]),
     'p1':k(dar[28]),'p2':k(dar[29]),'p3':k(dar[30]),'q1':k(dar[31]),'q2':k(dar[32])},
   'cap':cap,'dur':END+1.3}
json.dump(D,open('data.json','w'),ensure_ascii=False); print('ok',round(END,2),len(cap))
