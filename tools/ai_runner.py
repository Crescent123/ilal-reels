"""Runs one AI job inside GitHub Actions. python3 tools/ai_runner.py ai/jobs/<stamp>.json <outdir>
Job types:
 {"type":"transcribe","url":"https://...m4a"}            -> tr.json, tr_segments.txt
 {"type":"images","chars":{...},"scenes":[{"name":"n1.png","chars":[..],"scene":"..."}]} -> <name>.png ...
Writes <outdir>/done.txt at the end: empty when everything worked, else the errors."""
import json, sys, os, subprocess, urllib.request, tempfile
J=json.load(open(sys.argv[1])); O=sys.argv[2]; os.makedirs(O,exist_ok=True); errs=[]
R=os.path.dirname(os.path.abspath(__file__))+'/..'
if J['type']=='transcribe':
    a=tempfile.mktemp(suffix='.m4a')
    for i in range(3):
        try: urllib.request.urlretrieve(J['url'],a); break
        except Exception as e: err=str(e)
    else: errs.append('download failed: '+err)
    if not errs:
        r=subprocess.run(['bash',R+'/storyreel/transcribe.sh',a,O+'/tr.json'],capture_output=True,text=True)
        if r.returncode or not os.path.exists(O+'/tr_segments.txt'): errs.append('transcribe failed: '+(r.stderr or r.stdout)[-400:])
elif J['type']=='images':
    sc={"chars":J['chars'],"scenes":[{"out":O+'/'+s['name'],"chars":s['chars'],"scene":s['scene']} for s in J['scenes']]}
    f=tempfile.mktemp(suffix='.json'); json.dump(sc,open(f,'w'))
    r=subprocess.run(['python3',R+'/storyreel/gen_images.py',f],capture_output=True,text=True)
    errs+=[l for l in r.stdout.splitlines() if ' ERR ' in l]
    if r.returncode: errs.append(r.stderr[-400:])
else: errs.append('unknown job type')
open(O+'/done.txt','w').write('\n'.join(errs))
