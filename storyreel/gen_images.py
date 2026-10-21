"""python3 storyreel/gen_images.py scenes.json   (needs OPENAI_API_KEY)
scenes.json = {"chars": {"M": "...outfit description...", ...}, "scenes": [{"out":"work/n1.png","chars":["M"],"scene":"..."}]}"""
import json, base64, sys, os, urllib.request, concurrent.futures as cf
KEY=os.environ['OPENAI_API_KEY'].strip()
STY=("2D cartoon illustration in a clean webcomic style: thick black outlines, flat colors with soft shading, a detailed painted muted realistic background. "
     "All people are simple stick-style characters with a big round plain BALD WHITE head (no hair, no ears), two black dot eyes, a simple line mouth, a thin white neck, round white mitten hands, normal clothes on a slim body. ")
D=json.load(open(sys.argv[1])); CH=D['chars']
def gen(j):
    p=STY+" ".join(CH[c] for c in j['chars'])+" SCENE: "+j['scene']+" Tall vertical portrait composition (phone screen). Put the characters and the action in the CENTRAL area of the picture: roughly the middle 60% of the height and the middle 75% of the width, fully visible, nothing important cut off. The top 15% is only calm background (wall, ceiling or sky), the bottom 25% is only calm floor/ground, and the far left and far right edges are only background scenery. Draw only these characters. No text, letters, numbers, logos or UI anywhere."
    body=json.dumps({"model":"gpt-image-2","prompt":p,"size":"1024x1536","quality":"medium","n":1}).encode()
    for attempt in range(2):
        try:
            req=urllib.request.Request("https://api.openai.com/v1/images/generations",data=body,headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json"})
            r=json.load(urllib.request.urlopen(req,timeout=400)); open(j['out'],'wb').write(base64.b64decode(r['data'][0]['b64_json'])); return j['out'],'ok'
        except urllib.error.HTTPError as e: err=e.read().decode()[:300]
        except Exception as e: err=str(e)
    return j['out'],'ERR '+err.replace(KEY,'[key]')
with cf.ThreadPoolExecutor(10) as ex:
    for res in ex.map(gen,D['scenes']): print(*res)
