#!/bin/bash
# usage: bash tools/tiktok_run.sh [count=2]
# Picks the next TikTok clips by fixed rules and pushes Upload-Post jobs; the workflow logs each post itself.
# Order: archived IG-proven clips (tools/ig_plays.json, most plays first) -> queue s8 -> queue s7. Story clips only.
# Skips: tools/social_skip.json, anything already on TikTok (post_log or post/jobs). Never trend/drive files.
N=${1:-2}; cd "$(dirname "$0")/.." || exit 1; git pull -q
git fetch -q origin trial-posted 2>/dev/null; ARCH=$(git ls-tree --name-only FETCH_HEAD 2>/dev/null)
Q=$(bash tools/queue_list.sh 2>/dev/null | awk '{print $1}')
PICKS=$(ARCH="$ARCH" Q="$Q" N="$N" python3 - <<'PY'
import json,glob,os,re
log=[json.loads(l) for l in open('tools/post_log.jsonl') if l.strip()]
done={d.get('file') for d in log if d.get('platform')=='tiktok'}
for f in glob.glob('post/jobs/*.json'):
    try: d=json.load(open(f))
    except Exception: continue
    if d.get('platforms')==['tiktok']: done.add(d['video'].split('/')[-1])
skip=set(json.load(open('tools/social_skip.json')))
plays=json.load(open('tools/ig_plays.json')).get('plays',{})
arch=os.environ['ARCH'].split(); q=os.environ['Q'].split()
ok=lambda f:('_story_' in f or '_explainer_' in f) and f not in done and f not in skip
st=[('trial-posted',f) for f in sorted([f for f in arch if ok(f) and '_story_' in f and plays.get(f,0)>=10000],key=lambda f:-plays[f])]
st+=[('trial-queue',f) for f in q if ok(f) and '_story_' in f and '_s8_' in f]
st+=[('trial-queue',f) for f in q if ok(f) and '_story_' in f and '_s7_' in f]
st+=[('trial-posted',f) for f in arch if ok(f) and '_story_' in f and re.search(r'_s[78]_',f) and ('trial-posted',f) not in st]
# explainers (Hilal, 8 Nov: "post the explainers on tiktok too"): already-on-Instagram ones first, then queued
ex=[('trial-posted',f) for f in sorted(arch) if ok(f) and '_explainer_' in f]+[('trial-queue',f) for f in q if ok(f) and '_explainer_' in f]
c=[]
while (st or ex) and len(c)<int(os.environ['N']):   # alternate: 1 explainer, 1 story
    if ex: c.append(ex.pop(0))
    if st and len(c)<int(os.environ['N']): c.append(st.pop(0))
for b,f in c: print(b,f)
PY
)
[ -n "$PICKS" ] || { echo "nothing eligible for TikTok"; exit 0; }
echo "$PICKS" | while read B F; do
  J=$(mktemp); python3 -c "
import json,sys;b,f=sys.argv[1],sys.argv[2]
json.dump({'user':'default','platforms':['tiktok'],'video':f'https://raw.githubusercontent.com/Crescent123/ilal-reels/{b}/{f}',
 'title':'القصة كاملة فيوتيوب: ilal Stories 🎧','fields':{'privacy_level':'PUBLIC_TO_EVERYONE'},
 'log':{'src':'explainer' if '_explainer_' in f else 'story','file':f,'platform':'tiktok','note':'tiktok_run.sh'}},open(sys.argv[3],'w'),ensure_ascii=False)" "$B" "$F" "$J"
  timeout 90 bash tools/post.sh "$J" | head -1; rm -f "$J"
  echo "pushed $F"; sleep $((120 + RANDOM % 120))
done
