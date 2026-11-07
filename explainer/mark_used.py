#!/usr/bin/env python3
"""Mark every source reel already adapted (episodes.json + backlog.json non-todo) in source_list.json:
reel["used_in_ep"]=N, reel["used_slug"]=slug. Run after logging an episode. Picking new topics: skip reels with used_in_ep."""
import json,re
S='explainer/source_list.json'; d=json.load(open(S))
code=lambda u: (re.search(r'/reel/([^/]+)',u or '') or [None,None])[1]
used={}
for e in json.load(open('explainer/episodes.json')):
    c=code(e.get('source_reel'));
    if c: used[c]=(e['ep'],e['slug'])
for b in json.load(open('explainer/backlog.json')):
    c=code(b.get('source_reel'))
    if c and b['status']!='todo': used.setdefault(c,(b['ep'],b['slug']))
    if c and b['status']=='todo': used.setdefault(c,(b['ep'],b['slug']+' (planned)'))
n=0
for r in d['reels']:
    c=code(r['link'])
    if c in used: r['used_in_ep'],r['used_slug']=used[c]; n+=1
    else: r.pop('used_in_ep',None); r.pop('used_slug',None)
d['meta']['used_note']='used_in_ep = already adapted (or planned) as a couples explainer — do NOT reuse these topics; re-run explainer/mark_used.py after each new episode'
json.dump(d,open(S,'w'),ensure_ascii=False,indent=1); print('marked',n,'source reels')
