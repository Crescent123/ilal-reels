#!/bin/bash
# usage: storyreel/fetch.sh <drive_file_id> <video_id> <outdir>
# Asks the repo's GitHub workflows to pull the public Drive audio + the YouTube thumbnail, then downloads both.
set -e; FID="$1"; VID="$2"; OUT="$3"; REPO=$(cd "$(dirname "$0")/.." && pwd); mkdir -p "$OUT"
cd "$REPO"; git pull -q --rebase origin main || true
mkdir -p drive; echo "$FID $VID.m4a" > drive/wanted.txt
grep -qx "$VID" thumbs/wanted.txt || echo "$VID" >> thumbs/wanted.txt
git add drive/wanted.txt thumbs/wanted.txt; git -c user.name=Hilal -c user.email=hilalmillali@gmail.com commit -qm "fetch $VID" || true
git push -q origin main 2>/dev/null || { git pull -q --rebase origin main; git push -q origin main; }
for i in $(seq 1 40); do sleep 8; curl -sf -o "$OUT/story.m4a" "https://raw.githubusercontent.com/Crescent123/ilal-reels/drive-cache/$VID.m4a" && break; done
for i in $(seq 1 20); do curl -sf -o "$OUT/thumb.jpg" "https://raw.githubusercontent.com/Crescent123/ilal-reels/main/thumbs/$VID.jpg" && break; sleep 6; done
ls -la "$OUT"
