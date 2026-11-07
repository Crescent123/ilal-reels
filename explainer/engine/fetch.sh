#!/bin/bash
# usage: engine/fetch.sh <epdir> <elevenlabs content_url>  -> <epdir>/work/voice.mp3 + tr.json (via GitHub Actions ai job)
set -e; E=$(realpath "$1"); U="$2"; REPO=$(cd "$(dirname "$0")/../.." && pwd); S="$(date +%s)_$(basename $E)"
python3 -c "import json,sys;json.dump({'type':'transcribe','keep_audio':True,'url':sys.argv[1]},open(sys.argv[2],'w'))" "$U" "$REPO/ai/jobs/$S.json"
cd "$REPO"; for i in 1 2 3 4 5 6; do git pull -q --rebase origin main||true; git add "ai/jobs/$S.json"; git -c user.name=Hilal -c user.email=hilalmillali@gmail.com commit -qm "ai job $S"||true; git push -q origin HEAD:main && break; sleep $((3+RANDOM%10)); done
RAW=https://raw.githubusercontent.com/Crescent123/ilal-reels/ai-out/$S; sleep 40
for i in $(seq 1 60); do [ "$(curl -s -o /dev/null -w '%{http_code}' "$RAW/done.txt?$i$RANDOM")" = 200 ] && break; sleep 15; done
ERR=$(curl -s "$RAW/done.txt?e$RANDOM"); mkdir -p "$E/work"
curl -sfL -o "$E/work/voice.mp3" "$RAW/audio.mp3?$S"; curl -sfL -o "$E/work/tr.json" "$RAW/tr.json?$S"
[ -n "$ERR" ] && { echo "AI ERRORS: $ERR"; exit 1; }
echo "fetched $(basename $E): $(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/work/voice.mp3)s, $(python3 -c "import json;print(len(json.load(open('$E/work/tr.json'))['segments']))") segments"
