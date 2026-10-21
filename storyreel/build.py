"""Build a 2D story reel.  python3 storyreel/build.py spec.json
spec = {
 "audio": "work/story.m4a",            # full story audio
 "video_id": "H3Bzil3_UnI", "video_title": "...",   # for the end slide
 "thumb": "thumbs/H3Bzil3_UnI.jpg",
 "title": "short yellow top title (Darija)",
 "pieces": [[start,end], ...],          # ORIGINAL-audio seconds, usually ONE continuous piece
 "scenes": [{"at": orig_seconds, "image": "work/n1.png", "caption": "short Darija"} ...],  # first 'at' = pieces[0][0]
 "music": "music/suspense_1.mp3", "out": "work/reel.mp4",
 "badge": "PART 3"}                     # optional: yellow badge above the title (series parts)
Voice is only cut (10 ms fades), never processed. Scene changes snap to the quietest point within 0.12 s."""
import json, subprocess, numpy as np, base64, os, sys, tempfile
from PIL import Image, ImageFilter, ImageEnhance
from playwright.sync_api import sync_playwright
R=os.path.dirname(os.path.abspath(__file__)); A=R+'/assets/'
S=json.load(open(sys.argv[1])); W,H,FPS,GAP,END=1080,1920,30,0.22,3.8
wd=tempfile.mkdtemp()
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',S['audio'],'-ac','1','-ar','16000','-f','s16le',wd+'/pcm.raw'],check=True)
x=np.fromfile(wd+'/pcm.raw',dtype=np.int16).astype(np.float32); SR=16000
def rms(t,w=0.02):
    i=int(t*SR); n=int(w*SR); s=x[max(0,i-n//2):i+n//2]; return float(np.sqrt((s**2).mean()+1e-9))
def snap(t,win=0.12): return float(min(np.arange(t-win,t+win,0.005),key=rms))
P=[[snap(a),snap(b)] for a,b in S['pieces']]
for i,(a,b) in enumerate(P):
    d=b-a
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',f'{a:.3f}','-t',f'{d:.3f}','-i',S['audio'],'-af',f'afade=t=in:d=0.01,afade=t=out:st={d-0.01:.3f}:d=0.01'+(f',apad=pad_dur={GAP}' if i<len(P)-1 else ',apad=pad_dur=0.3'),'-ar','48000','-c:a','pcm_s16le',f'{wd}/p{i}.wav'],check=True)
open(wd+'/l.txt','w').write(''.join(f"file '{wd}/p{i}.wav'\n" for i in range(len(P))))
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',wd+'/l.txt','-c','copy',wd+'/voice.wav'],check=True)
VD=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',wd+'/voice.wav'],capture_output=True,text=True).stdout)
starts=[];t=0
for i,(a,b) in enumerate(P): starts.append(t); t+=b-a+GAP
def m(o):
    for (a,b),s in zip(P,starts):
        if a-0.2<=o<=b+0.2: return max(0,s+(min(max(o,a),b)-a))
    raise ValueError(f'scene time {o} not inside any piece')
sc=S['scenes']; bounds=[0]+[m(snap(s['at'])) for s in sc[1:]]+[VD]; TOTAL=VD+END
def b64(p,mt): return f'data:{mt};base64,'+base64.b64encode(open(p,'rb').read()).decode()
CSS=f"""@font-face{{font-family:Cairo;src:url('file://{A}Cairo.ttf');font-weight:200 1000}}@font-face{{font-family:Anton;src:url('file://{A}Anton.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{W}px;height:{H}px;background:transparent;overflow:hidden;position:relative}}
.t{{position:absolute;top:255px;left:120px;right:150px;text-align:center;direction:rtl;font-family:Cairo;font-weight:900;font-size:58px;color:#FFC426;text-shadow:0 3px 12px rgba(0,0,0,.95),0 0 4px #000}}
.c{{position:absolute;bottom:300px;left:120px;right:150px;line-height:1.25;text-align:center;direction:rtl;font-family:Cairo;font-weight:900;font-size:70px;color:#fff;text-shadow:0 4px 14px rgba(0,0,0,.95),0 0 4px #000}}
.pl{{position:absolute;top:226px;left:120px;right:150px;display:flex;justify-content:center}}.pl span{{background:#FFC426;color:#0F0F0F;font-family:Anton;font-size:50px;letter-spacing:3px;padding:4px 30px 8px;border-radius:14px;line-height:1.1;box-shadow:0 4px 14px rgba(0,0,0,.6)}}.bd .t{{top:312px}}
.gt{{position:absolute;top:0;left:0;right:0;height:520px;background:linear-gradient(rgba(0,0,0,.6),rgba(0,0,0,0))}}.gb{{position:absolute;bottom:0;left:0;right:0;height:760px;background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.7) 55%)}}"""
OR,MA,RD,BK='#FFAF32','#890219','#C00000','#0F0F0F'
CTA=f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:{OR}}}.txt{{position:absolute;top:280px;left:120px;right:150px;direction:rtl;text-align:center;font-family:Cairo;font-weight:900;color:{BK}}}
.l{{font-size:68px;line-height:1.3}}.a{{font-size:76px;line-height:1.25;width:max-content;margin:16px auto 0;color:#fff;background:{MA};padding:6px 36px 16px;border-radius:20px;transform:rotate(-1.5deg)}}
.th{{position:absolute;top:720px;left:110px;width:820px;height:461px;border:14px solid {BK};border-radius:30px;overflow:hidden;box-shadow:16px 16px 0 {MA};background:{BK}}}.th img{{width:100%;height:100%;object-fit:cover}}
.yb{{position:absolute;top:670px;left:80px;width:150px;height:106px;background:{RD};border-radius:32px;display:flex;align-items:center;justify-content:center;transform:rotate(-6deg);border:8px solid {BK}}}
.ti{{position:absolute;top:1225px;left:120px;right:150px;direction:rtl;text-align:center;font-family:Cairo;font-weight:900;font-size:42px;line-height:1.35;color:{BK};display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.hd{{position:absolute;top:1365px;left:120px;right:150px;display:flex;justify-content:center;align-items:center;gap:20px;direction:ltr}}
.hd img{{width:96px;height:96px;border-radius:50%;border:6px solid {BK}}}.hd span{{background:{BK};color:{OR};font-family:Anton;font-size:52px;padding:8px 34px 12px;border-radius:60px;line-height:1}}
</style></head><body><div class=txt><div class=l>القصة كاملة كتسناك</div><div class=l>فقناة ilal Stories</div><div class=a>الرابط فالبيو</div></div>
<div class=th>{'<img src="'+b64(S['thumb'],'image/jpeg')+'">' if S.get('thumb') and os.path.exists(S['thumb']) else ''}</div><div class=yb><svg width=60 height=60 viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="#fff"/></svg></div>
<div class=ti>{S.get('video_title','')}</div><div class=hd><img src="{b64(A+'avatar.png','image/png')}"><span>@ilalstories</span></div></body></html>"""
FIT="document.fonts.ready.then(()=>{document.querySelectorAll('.t,.l').forEach(e=>{let f=parseFloat(getComputedStyle(e).fontSize);e.style.whiteSpace='nowrap';e.style.width='max-content';e.style.margin='0 auto';while(e.getBoundingClientRect().width>800&&f>30){f-=2;e.style.fontSize=f+'px'}});document.querySelectorAll('.c').forEach(e=>{let f=parseFloat(getComputedStyle(e).fontSize);while(e.getBoundingClientRect().height>170&&f>40){f-=2;e.style.fontSize=f+'px'}})})"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':H})
    for i,s in enumerate(sc):
        open(wd+'/o.html','w').write(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body class={'bd' if S.get('badge') else 'n'}><div class=gt></div><div class=gb></div>{('<div class=pl><span>'+S['badge']+'</span></div>') if S.get('badge') else ''}<div class=t>{S['title']}</div><div class=c>{s['caption']}</div></body></html>")
        pg.goto('file://'+wd+'/o.html'); pg.wait_for_timeout(200); pg.evaluate(FIT); pg.wait_for_timeout(150); pg.screenshot(path=f'{wd}/ov{i}.png',omit_background=True)
    open(wd+'/cta.html','w').write(CTA); pg.goto('file://'+wd+'/cta.html'); pg.wait_for_timeout(300); pg.screenshot(path=wd+'/cta.png'); b.close()
segs=[]
for i,s in enumerate(sc):
    im=Image.open(s['image']).convert('RGB'); sc_=max(W/im.width,H/im.height); im=im.resize((round(im.width*sc_),round(im.height*sc_)),Image.LANCZOS); im=im.crop(((im.width-W)//2,(im.height-H)//2,(im.width-W)//2+W,(im.height-H)//2+H))
    bg=im.resize((H,H)).crop(((H-W)//2,0,(H-W)//2+W,H)).filter(ImageFilter.GaussianBlur(40)); ImageEnhance.Brightness(bg).enhance(0.45).save(f'{wd}/bg{i}.png')
    im.resize((2*W,2*H),Image.LANCZOS).save(f'{wd}/im{i}.png')
    n=max(1,round((bounds[i+1]-bounds[i])*FPS)); z=f"'1+0.045*on/{n}'" if i%2==0 else f"'1.045-0.045*on/{n}'"
    fc=f"[1:v]zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}[z];[0:v][z]overlay=0:0[a];[a][2:v]overlay=0:0,format=yuv420p[v]"
    subprocess.run(['ffmpeg','-loglevel','error','-y','-loop','1','-i',f'{wd}/bg{i}.png','-i',f'{wd}/im{i}.png','-loop','1','-i',f'{wd}/ov{i}.png','-filter_complex',fc,'-map','[v]','-frames:v',str(n),'-r',str(FPS),'-c:v','libx264','-preset','veryfast','-crf','17',f'{wd}/s{i}.mp4'],check=True); segs.append(f'{wd}/s{i}.mp4')
subprocess.run(['ffmpeg','-loglevel','error','-y','-loop','1','-i',wd+'/cta.png','-vf','format=yuv420p','-frames:v',str(round(END*FPS)),'-r',str(FPS),'-c:v','libx264','-preset','veryfast','-crf','17',wd+'/sE.mp4'],check=True); segs.append(wd+'/sE.mp4')
open(wd+'/v.txt','w').write(''.join(f"file '{s}'\n" for s in segs))
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',wd+'/v.txt','-c','copy',wd+'/video.mp4'],check=True)
mus=S.get('music') or R+'/../music/suspense_1.mp3'
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',wd+'/video.mp4','-i',wd+'/voice.wav','-stream_loop','-1','-i',mus,'-filter_complex',
 f"[2:a]atrim=0:{TOTAL:.2f},volume=-24dB,afade=t=in:d=0.5,afade=t=out:st={TOTAL-1.2:.2f}:d=1.2[mus];[1:a]apad=whole_dur={TOTAL:.2f},asplit=2[vo][sc];[mus][sc]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=400[duck];[vo][duck]amix=inputs=2:normalize=0:duration=first[a]",
 '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','320k','-movflags','+faststart','-t',f'{TOTAL:.2f}',S['out']],check=True)
subprocess.run(['cp',wd+'/voice.wav',os.path.splitext(S['out'])[0]+'_voice.wav'])
print(json.dumps({'out':S['out'],'voice_seconds':round(VD,2),'total':round(TOTAL,2),'scene_bounds':[round(b,2) for b in bounds]}))
