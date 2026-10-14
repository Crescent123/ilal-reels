"""Vertical reel from a 1920x1080 vlog clip.  python3 vlogreel/build_vlog.py spec.json
spec: {"src": clip.mp4, "start": s, "end": e,               # seconds inside src
       "full_cx": [[t, cx], ...],                            # face centre x (0-1920) keyframes for single shots (t relative to start)
       "split": [[t0, t1, topX, topY, botX, botY], ...],     # two-shot windows: 960x600 crops (top-left corners) stacked
       "title": str, "captions": [[t0, t1, text], ...],
       "cta": {"line1":..., "line2":..., "pill":..., "thumb_t": t, "vtitle":..., "handle":...},
       "music": mp3 (end card only), "out": out.mp4}
All text stays in Hilal's safe zone: x 90-930, y 215-1630."""
import json, sys, os, subprocess, base64
from playwright.sync_api import sync_playwright
S=json.load(open(sys.argv[1])); R=os.path.dirname(os.path.abspath(__file__)); A=R+'/../storyreel/assets/'
wd=os.path.splitext(S['out'])[0]+'_work'; os.makedirs(wd,exist_ok=True)
W,H,FPS=1080,1920,30; D=S['end']-S['start']; END=3.6
def run(a): subprocess.run(a,check=True)
run(['ffmpeg','-loglevel','error','-y','-ss',str(S['start']),'-i',S['src'],'-t',f'{D:.3f}','-c:v','libx264','-preset','veryfast','-crf','14','-r',str(FPS),'-c:a','pcm_s16le',wd+'/src.mov'])
# piecewise-linear crop-x expression for the full 9:16 crop (608 wide)
kf=sorted(S['full_cx'])
def lin(kf):
    e=f"{kf[-1][1]}"
    for (t0,x0),(t1,x1) in reversed(list(zip(kf,kf[1:]))):
        e=f"if(lt(t,{t1}),{x0}+({x1}-{x0})*(t-{t0})/{max(t1-t0,0.01)},{e})"
    return f"if(lt(t,{kf[0][0]}),{kf[0][1]},{e})"
cx=lin(kf)
fc=(f"[0:v]split=3[a][b][c];"
    f"[a]scale=-2:{H},crop={W}:{H},gblur=sigma=40,eq=brightness=-0.25[bg];"
    f"[b]crop=608:1080:'max(0,min(1920-608,{cx}-304))':0,scale={W}:{H}:flags=lanczos[full];")
parts=["[full]"]; last="full"
for i,(t0,t1,tx,ty,bx,by) in enumerate(S.get('split',[])):
    fc+=(f"[c]split=2[c{i}][c]; [c{i}]split=2[p{i}][q{i}];"
         f"[p{i}]crop=960:630:{tx}:{ty},scale=1080:709:flags=lanczos[top{i}];[q{i}]crop=960:630:{bx}:{by},scale=1080:709:flags=lanczos[bot{i}];")
fc=fc.rstrip(';')
# simpler: build split canvas once per window
fc=(f"[0:v]split={2+2*len(S.get('split',[]))}" + "".join(f"[s{k}]" for k in range(2+2*len(S.get('split',[])))) + ";"
    f"[s0]crop=864:1080:'max(0,min(1920-864,{cx}-432))':0,scale=1080:1350:flags=lanczos[f0];"
    f"[s1]scale=-2:{H},crop={W}:{H},gblur=sigma=40,eq=brightness=-0.3[bg];[bg]split=2[bg][bgf];[bgf][f0]overlay=0:360[v0];")
cur="v0"; k=2
for i,(t0,t1,tx,ty,bx,by) in enumerate(S.get('split',[])):
    fc+=(f"[s{k}]crop=960:600:{tx}:{ty},scale=1080:675:flags=lanczos[top{i}];[s{k+1}]crop=960:600:{bx}:{by},scale=1080:675:flags=lanczos[bot{i}];"
         f"[bg]split=2[bg][bgi{i}];[bgi{i}][top{i}]overlay=0:360[m{i}];[m{i}][bot{i}]overlay=0:1045[sp{i}];"
         f"[{cur}][sp{i}]overlay=0:0:enable='between(t,{t0},{t1})'[o{i}];")
    cur=f"o{i}"; k+=2
fc+=f"[bg]nullsink;[{cur}]null[vid]"
# text overlays
CSS=f"""@font-face{{font-family:Cairo;src:url('file://{A}Cairo.ttf');font-weight:200 1000}}@font-face{{font-family:Anton;src:url('file://{A}Anton.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{W}px;height:{H}px;background:transparent;overflow:hidden;position:relative}}
.t{{position:absolute;top:255px;left:120px;right:150px;text-align:center;direction:rtl;font-family:Cairo;font-weight:900;font-size:62px;color:#FFC426;text-shadow:0 3px 12px rgba(0,0,0,.95),0 0 4px #000}}
.c{{position:absolute;bottom:300px;left:120px;right:150px;line-height:1.25;text-align:center;direction:rtl;font-family:Cairo;font-weight:900;font-size:70px;color:#fff;text-shadow:0 4px 14px rgba(0,0,0,.95),0 0 4px #000}}
.gt{{position:absolute;top:0;left:0;right:0;height:480px;background:linear-gradient(rgba(0,0,0,.55),rgba(0,0,0,0))}}.gb{{position:absolute;bottom:0;left:0;right:0;height:700px;background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.65) 55%)}}"""
FIT="document.fonts.ready.then(()=>{document.querySelectorAll('.t').forEach(e=>{let f=parseFloat(getComputedStyle(e).fontSize);e.style.whiteSpace='nowrap';e.style.width='max-content';e.style.margin='0 auto';while(e.getBoundingClientRect().width>800&&f>30){f-=2;e.style.fontSize=f+'px'}});document.querySelectorAll('.c').forEach(e=>{let f=parseFloat(getComputedStyle(e).fontSize);while(e.getBoundingClientRect().height>170&&f>40){f-=2;e.style.fontSize=f+'px'}})})"
run(['ffmpeg','-loglevel','error','-y','-ss',str(S['start']+S['cta']['thumb_t']),'-i',S['src'],'-frames:v','1',wd+'/thumb.jpg'])
c=S['cta']; OR,MA,BK='#FFAF32','#890219','#0F0F0F'
b64=lambda p,mt:f'data:{mt};base64,'+base64.b64encode(open(p,'rb').read()).decode()
CTA=f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:{OR}}}.txt{{position:absolute;top:280px;left:120px;right:150px;direction:rtl;text-align:center;font-family:Cairo;font-weight:900;color:{BK}}}
.l{{font-size:68px;line-height:1.3}}.a{{font-size:66px;line-height:1.25;width:max-content;margin:16px auto 0;color:#fff;background:{MA};padding:6px 36px 16px;border-radius:20px;transform:rotate(-1.5deg)}}
.th{{position:absolute;top:720px;left:110px;width:820px;height:461px;border:14px solid {BK};border-radius:30px;overflow:hidden;box-shadow:16px 16px 0 {MA};background:{BK}}}.th img{{width:100%;height:100%;object-fit:cover}}
.ti{{position:absolute;top:1225px;left:120px;right:150px;direction:rtl;text-align:center;font-family:Cairo;font-weight:900;font-size:46px;color:{BK}}}
.hd{{position:absolute;top:1340px;left:120px;right:150px;display:flex;justify-content:center}}.hd span{{background:{BK};color:{OR};font-family:Anton;font-size:56px;padding:8px 38px 12px;border-radius:60px;line-height:1}}
</style></head><body><div class=txt><div class=l>{c['line1']}</div><div class=l>{c['line2']}</div><div class=a>{c['pill']}</div></div>
<div class=th><img src="{b64(wd+'/thumb.jpg','image/jpeg')}"></div><div class=ti>{c['vtitle']}</div><div class=hd><span>{c['handle']}</span></div></body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':H})
    for i,(t0,t1,txt) in enumerate(S['captions']):
        open(wd+'/o.html','w').write(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body><div class=gt></div><div class=gb></div><div class=t>{S['title']}</div><div class=c>{txt}</div></body></html>")
        pg.goto('file://'+wd+'/o.html'); pg.wait_for_timeout(200); pg.evaluate(FIT); pg.wait_for_timeout(150); pg.screenshot(path=f'{wd}/ov{i}.png',omit_background=True)
    open(wd+'/o.html','w').write(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body><div class=gt></div><div class=gb></div><div class=t>{S['title']}</div></body></html>")
    pg.goto('file://'+wd+'/o.html'); pg.wait_for_timeout(200); pg.evaluate(FIT); pg.wait_for_timeout(150); pg.screenshot(path=f'{wd}/ovT.png',omit_background=True)
    open(wd+'/cta.html','w').write(CTA); pg.goto('file://'+wd+'/cta.html'); pg.wait_for_timeout(300); pg.screenshot(path=wd+'/cta.png'); b.close()
ins=['-i',wd+'/src.mov','-loop','1','-i',wd+'/ovT.png']
for i in range(len(S['captions'])): ins+=['-loop','1','-i',f'{wd}/ov{i}.png']
fc+=f";[vid][1:v]overlay=0:0[w0]"; cur="w0"
for i,(t0,t1,_) in enumerate(S['captions']):
    fc+=f";[{cur}][{i+2}:v]overlay=0:0:enable='between(t,{t0},{t1})'[w{i+1}]"; cur=f"w{i+1}"
fc+=f";[{cur}]format=yuv420p[v]"
run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',fc,'-map','[v]','-map','0:a','-t',f'{D:.3f}','-r',str(FPS),'-c:v','libx264','-preset','medium','-crf','17','-c:a','pcm_s16le',wd+'/main.mov'])
mus=S.get('music') or R+'/../music/suspense_1.mp3'
run(['ffmpeg','-loglevel','error','-y','-loop','1','-i',wd+'/cta.png','-i',mus,'-filter_complex',f"[1:a]atrim=0:{END},volume=-16dB,afade=t=in:d=0.4,afade=t=out:st={END-1}:d=1,aformat=sample_rates=48000:channel_layouts=stereo[a]",'-map','0:v','-map','[a]','-t',str(END),'-r',str(FPS),'-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','pcm_s16le',wd+'/end.mov'])
run(['ffmpeg','-loglevel','error','-y','-i',wd+'/main.mov','-i',wd+'/end.mov','-filter_complex',"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=out:st="+f"{D-0.3:.2f}"+":d=0.3[a0];[0:v]setsar=1,format=yuv420p,fps=30[v0];[1:v]setsar=1,format=yuv420p,fps=30[v1];[v0][a0][v1][1:a]concat=n=2:v=1:a=1[v][a]",
     '-map','[v]','-map','[a]','-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','256k','-movflags','+faststart',S['out']])
print(json.dumps({'out':S['out'],'seconds':round(D+END,2)}))
