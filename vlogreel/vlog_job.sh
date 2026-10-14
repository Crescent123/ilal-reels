#!/bin/bash
# usage: vlogreel/vlog_job.sh "<job line>" ["<job line>" ...]   then waits for GitHub and downloads results into $OUT (default work/)
# job lines: "prep <driveId> <tag>" (audio + contact sheets in ONE pass) | "cut <driveId> <tag> <start> <end>"
set -e; REPO=$(cd "$(dirname "$0")/.." && pwd); OUT=${OUT:-work}; mkdir -p "$OUT"; cd "$REPO"
git pull -q --rebase origin main || true
printf "%s\n" "$@" > vlog/job.txt; echo "# $(date +%s)" >> vlog/job.txt
git add vlog/job.txt && git commit -qm "vlog job" && git push -q origin main
STAMP=$(date +%s); sleep 60
RAW=https://raw.githubusercontent.com/Crescent123/ilal-reels/vlog-cache
want=(); for l in "$@"; do set -- $l; case $1 in prep|audio) want+=("$3.m4a" "$3_sheet_01.jpg");; sheet) want+=("$3_sheet_01.jpg");; cut) want+=("$3.mp4");; esac; done
for i in $(seq 1 400); do
  ok=1; for f in "${want[@]}"; do [ "$(curl -s -o /dev/null -w '%{http_code}' "$RAW/$f?$i")" = 200 ] || ok=0; done
  [ "$(curl -s -o /dev/null -w '%{http_code}' "$RAW/errors.txt?$i")" = 200 ] && { curl -s "$RAW/errors.txt"; exit 1; }
  [ $ok = 1 ] && break; sleep 20
done
for f in "${want[@]}"; do curl -sfL -o "$OUT/$f" "$RAW/$f"; done
for w in "${want[@]}"; do case "$w" in *_sheet_01.jpg) b=${w%_sheet_01.jpg}; for n in 02 03 04 05; do curl -sfL -o "$OUT/${b}_sheet_$n.jpg" "$RAW/${b}_sheet_$n.jpg" 2>/dev/null || true; done;; esac; done
ls -la "$OUT"
