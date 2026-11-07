#!/bin/bash
# usage: engine/check.sh <epdir>  -> build data.json + <epdir>/sheet.png (one still per phrase, safe-area guides)
set -e; D=$(cd "$(dirname "$0")" && pwd); E=$(realpath "$1")
python3 $D/build.py "$E"; rm -f "$E"/test_*.png
T=$(python3 -c "import json;d=json.load(open('$E/data.json'));print(json.dumps([round(min(p['a']+.9,(p['a']+p['b'])/2+.2),2) for p in d['ph']]))")
node $D/render.js "$E" test "$T"
python3 - "$E" <<'P'
import sys,glob;from PIL import Image,ImageDraw
E=sys.argv[1];fs=sorted(glob.glob(E+'/test_*.png'),key=lambda f:float(f.split('test_')[1][:-4]))
W,H=216,384;cols=8;rows=(len(fs)+cols-1)//cols;im=Image.new('RGB',(cols*W,rows*H),'#333')
for i,f in enumerate(fs):
    a=Image.open(f).convert('RGB').resize((W,H));d=ImageDraw.Draw(a);s=W/1080
    d.rectangle([80*s,240*s,920*s,1480*s],outline='#0f0');d.rectangle([80*s,1330*s,920*s,1460*s],outline='#ff0');d.text((4,4),str(i),fill='#0ff')
    im.paste(a,((i%cols)*W,(i//cols)*H))
im.save(E+'/sheet.png');print('sheet',E+'/sheet.png')
P
rm -f "$E"/test_*.png
