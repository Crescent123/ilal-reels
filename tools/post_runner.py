# Runs one Upload-Post job (called by .github/workflows/post.yml). Job JSON:
# {"user":"default","platforms":["tiktok"],"video":"<public url>","title":"...","fields":{"privacy_level":"PUBLIC_TO_EVERYONE",...}}
# Writes <out>/result.json and <out>/done.txt (empty = ok). Never prints the API key.
import json,sys,os,subprocess,time
job=json.load(open(sys.argv[1])); out=sys.argv[2]; key=os.environ['UPLOADPOST_API_KEY'].strip()
if job.get('action')=='analytics':
    # {"action":"analytics","request_ids":[...]} -> per-post metrics (read-only)
    res={}
    for rid in job.get('request_ids',[])[:40]:
        s=subprocess.run(['curl','-sS','-m','60','https://api.upload-post.com/api/uploadposts/post-analytics/'+rid,'-H','Authorization: Apikey '+key],capture_output=True,text=True).stdout
        try: res[rid]=json.loads(s)
        except Exception: res[rid]={'raw':s[:300]}
        time.sleep(1)
    txt=json.dumps(res,indent=1).replace(key,'[key]')
    open(os.path.join(out,'result.json'),'w').write(txt); open(os.path.join(out,'done.txt'),'w').write(''); sys.exit(0)
if job.get('action')=='list_users':
    s=subprocess.run(['curl','-sS','-m','60','https://api.upload-post.com/api/uploadposts/users','-H','Authorization: Apikey '+key],capture_output=True,text=True).stdout
    try:
        d=json.loads(s); prof=d.get('profiles') or d.get('users') or []
        slim=[{'username':x.get('username'),'platforms':sorted(k for k,v in (x.get('social_accounts') or {}).items() if v)} for x in prof]
        res={'success':True,'profiles':slim,'keys':sorted(d.keys())}
    except Exception as e: res={'success':False,'err':str(e)[:200]}
    json.dump(res,open(os.path.join(out,'result.json'),'w'),indent=1); open(os.path.join(out,'done.txt'),'w').write(''); sys.exit(0)
args=['curl','-sS','-m','900','-X','POST','https://api.upload-post.com/api/upload','-H','Authorization: Apikey '+key,
      '-F','user='+job['user'],'-F','video='+job['video']]
for p in job['platforms']: args+=['-F','platform[]='+p]
if job.get('title') is not None: args+=['-F','title='+job['title']]
for k,v in (job.get('fields') or {}).items():
    if isinstance(v,list):
        for x in v: args+=['-F',f'{k}[]={x}']
    else: args+=['-F',f'{k}={str(v).lower() if isinstance(v,bool) else v}']
r=subprocess.run(args,capture_output=True,text=True)
txt=(r.stdout or '')+(r.stderr or '')
try: res=json.loads(r.stdout)
except Exception: res={'raw':txt[:3000]}
# poll async status if a request_id came back without a final result
rid=res.get('request_id') if isinstance(res,dict) else None
if rid and not res.get('results'):
    for i in range(60):
        time.sleep(20)
        s=subprocess.run(['curl','-sS','-m','60','https://api.upload-post.com/api/uploadposts/status?request_id='+rid,'-H','Authorization: Apikey '+key],capture_output=True,text=True).stdout
        try: st=json.loads(s)
        except Exception: st={'raw':s[:2000]}
        res['status_poll']=st
        if isinstance(st,dict) and str(st.get('status','')).lower() in ('completed','failed','error','success','done'): break
json.dump(res,open(os.path.join(out,'result.json'),'w'),ensure_ascii=False,indent=1)
ok=isinstance(res,dict) and (res.get('success') is True or res.get('request_id'))
open(os.path.join(out,'done.txt'),'w').write('' if ok else ('upload failed: '+json.dumps(res)[:800]))

# Optional "log": {...} in the job -> the workflow appends one tools/post_log.jsonl line itself (5 Nov: runs kept dying
# before logging). Fields given are kept; t/event/permalink are filled in here.
if job.get('log'):
    import datetime
    def _url(r):
        for src in (r, r.get('status_poll') or {}):
            rr=src.get('results') if isinstance(src,dict) else None
            for v in ((rr.values() if isinstance(rr,dict) else rr) or []):
                if isinstance(v,dict) and v.get('post_url'): return v['post_url']
        return ''
    u=_url(res) if isinstance(res,dict) else ''
    line=dict(job['log']); ok=bool(u) or (isinstance(res,dict) and res.get('success') is True)
    line.update({'t':datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),'event':'posted' if ok else 'error','permalink':u})
    if not u: line['note']=('url pending (background upload) | ' if ok else '')+(line.get('note','')+' | no post_url: '+json.dumps(res)[:200]).strip(' |')
    json.dump(line,open(os.path.join(out,'logline.json'),'w'),ensure_ascii=False)
