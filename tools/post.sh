#!/bin/bash
# usage: tools/post.sh <job.json>   -> pushes the job, waits, prints result.json. Key stays in the repo secret.
set -e; J="$1"; REPO=$(cd "$(dirname "$0")/.." && pwd); S="$(date +%s)_$RANDOM"
mkdir -p "$REPO/post/jobs"; cp "$J" "$REPO/post/jobs/$S.json"; cd "$REPO"
for t in 1 2 3 4 5; do git pull -q --rebase origin main || true; git add "post/jobs/$S.json"; git -c user.name=Hilal -c user.email=ilal-bot@users.noreply.github.com commit -qm "post job $S" || true; git push -q origin HEAD:main && break; sleep 5; done
RAW=https://raw.githubusercontent.com/Crescent123/ilal-reels/post-out/$S
echo "post job $S submitted"; sleep 40
for i in $(seq 1 120); do [ "$(curl -s -o /dev/null -w '%{http_code}' "$RAW/done.txt?$i")" = 200 ] && break; sleep 15; done
curl -s "$RAW/result.json?$S"; echo; echo "ERR: $(curl -s "$RAW/done.txt?z")"
