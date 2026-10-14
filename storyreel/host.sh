#!/bin/bash
# usage: storyreel/host.sh file.mp4 [branch] -> prints a public raw URL (orphan branch, default "queue2", replaced each time)
set -e; F="$1"; B="${2:-queue2}"; W=$(mktemp -d); N="reel_$(date +%s).mp4"; REPO=$(cd "$(dirname "$0")/.." && pwd)
cp "$F" "$W/$N"; cd "$W"; git init -q; git checkout -q --orphan "$B"; git add "$N"
git -c user.name=Hilal -c user.email=hilalmillali@gmail.com commit -qm "$B"
git remote add origin "$(git -C "$REPO" remote get-url origin)"; git push -q -f origin "$B" >/dev/null 2>&1
echo "https://raw.githubusercontent.com/Crescent123/ilal-reels/$B/$N"
