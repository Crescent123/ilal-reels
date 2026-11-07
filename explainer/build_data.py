import json,sys
# usage: python3 build_data.py tr.json out.json  (ep01 phrase list + scene/cut indices)
tr=json.load(open(sys.argv[1])); seg=[(s['start'],s['end']) for s in tr['segments']]
dar=["علاش البداية ديما كتكون زوينة…","ومن بعد كيتبدل كلشي؟","فاش كتبدا العلاقة،","الدماغ ديالك كيطلق كوكتيل ديال الهرمونات","Dopamine، Adrenaline…","بحال شي دوا.","كتولي كتفكر فيه نهار وليل،","كتشوف غير الزوين،","والعيوب ما كتبانش.","هاد المرحلة سماوها الباحثين","Limerence","كتطلع بزربة،","وكتوصل للقمة مع ستة شهور.","ومن بعد، بين عام وعام ونص،","الدوا كيسالي.","الهرمونات كيرجعو نورمال…","وكتبدا تشوف الشخص كيف ما هو بصح.","هنا كتبان العيوب،","وهنا كيبداو المشاكل الصغار.","بزاف ديال الناس كيحسبو هادي هي النهاية:","«ما بقاش كيبغيني»، «تبدلات».","وكيقلبو على شي واحد جديد…","باش يعاودو نفس الدوا من الأول.","ولكن كاين واحد الخط آخر","كيبدا تحت،","وكيطلع بشوية:","التعلق والثقة.","هادشي ما كيعطيكش الفراشات فالكرش…","ولكن هو اللي كيخلي الناس يكملو عشرين عام مع بعضيتهم.","الحب الحقيقي","ماشي ملي كتطيح فيه…","هو ملي الدوا كيسالي،","وكتبقى."]
end=seg[-1][1]
if len(seg)==len(dar): st=[s[0] for s in seg]
else:  # fallback: proportional by characters over the spoken span
    print('segment count',len(seg),'!= phrases',len(dar),'-> proportional timing')
    L=[len(x) for x in dar]; tot=sum(L); st=[]; acc=0
    for l in L: st.append(seg[0][0]+(end-seg[0][0])*acc/tot); acc+=l
nx=lambda i: st[i+1] if i+1<len(st) else end+.8
cap=[]
for i,p in enumerate(dar):
    a,b=st[i],nx(i); w=p.split()
    if len(p)>24 and len(w)>=3:
        h=len(w)//2; p1,p2=' '.join(w[:h]),' '.join(w[h:]); m=a+(b-a)*len(p1)/len(p)
        cap+= [[a,m,p1],[m,b,p2]]
    else: cap.append([a,b,p])
I=lambda i: st[i]
D={'s':[0,I(2),I(9),I(13),I(19),I(23),I(29)],
   'cut':[I(5),I(6),I(7),I(8),I(12),I(16),I(18),I(21),I(20),I(22),I(28)],
   'pl':[I(29),I(30),I(31),I(32)],'cap':cap,'dur':end+1.2}
json.dump(D,open(sys.argv[2],'w'),ensure_ascii=False); print('ok',round(end,2))
