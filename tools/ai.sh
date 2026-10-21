#!/bin/bash
# usage: tools/ai.sh transcribe <audio_url> <outdir>        -> <outdir>/tr.json + tr_segments.txt
#        tools/ai.sh images <scenes.json> <outdir>          -> <outdir>/<name>.png for each scene
# scenes.json for images: {"chars":{...},"scenes":[{"out":"work/n1.png" or "name":"n1.png","chars":[..],"scene":"..."}]}
# The OpenAI key lives ONLY in the GitHub repo secret; this script never needs it. Prints "AI ERRORS: ..." on failure.
set -e; T="$1"; IN="$2"; OUT="$3"; REPO=$(cd "$(dirname "$0")/.." && pwd); ORIG="$PWD"; mkdir -p "$OUT"
[ "$T" = images ] && IN=$(realpath "$IN")
S="$(date +%s)_$RANDOM$RANDOM"
python3 - "$T" "$IN" "$REPO/ai/jobs/$S.json" <<'P'
import json,sys,os
t,i,o=sys.argv[1:4]
if t=='transcribe': j={"type":"transcribe","url":i}
else:
    d=json.load(open(i)); j={"type":"images","chars":d['chars'],"scenes":[{"name":s.get('name') or os.path.basename(s['out']),"chars":s['chars'],"scene":s['scene']} for s in d['scenes']]}
json.dump(j,open(o,'w'),ensure_ascii=False)
P
cd "$REPO"
for try in 1 2 3 4 5 6; do
  git pull -q --rebase origin main || true
  git add "ai/jobs/$S.json"; git -c user.name=Hilal -c user.email=hilalmillali@gmail.com commit -qm "ai job $S" || true
  git push -q origin HEAD:main && break; sleep $((3 + RANDOM % 10))
done
RAW=https://raw.githubusercontent.com/Crescent123/ilal-reels/ai-out/$S
cd "$ORIG"; echo "ai job $S submitted, waiting..."
sleep 45
for i in $(seq 1 120); do [ "$(curl -s -o /dev/null -w '%{http_code}' "$RAW/done.txt?$i")" = 200 ] && break; sleep 15; done
[ "$(curl -s -o /dev/null -w '%{http_code}' "$RAW/done.txt?x")" = 200 ] || { echo "AI ERRORS: timed out (no result after 30 min)"; exit 1; }
ERR=$(curl -s "$RAW/done.txt?y")
if [ "$T" = transcribe ]; then
  curl -sfL -o "$OUT/tr.json" "$RAW/tr.json?$S" || true
  curl -sfL -o "$OUT/tr_segments.txt" "$RAW/tr_segments.txt?$S" || true
  [ -s "$OUT/tr_segments.txt" ] && echo "segments: $OUT/tr_segments.txt"
else
  python3 -c "
import json,os,sys;d=json.load(open('$IN'))
for s in d['scenes']: print((s.get('name') or os.path.basename(s['out'])), s.get('out') or '$OUT/'+s['name'])" | while read -r n dest; do
    curl -sfL -o "$dest" "$RAW/$n?$S" && echo "$dest ok" || echo "$dest MISSING"
  done
fi
[ -n "$ERR" ] && { echo "AI ERRORS: $ERR"; exit 1; }; exit 0
