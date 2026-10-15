#!/bin/bash
# usage: tools/queue_add.sh file.mp4 <name>   -> adds the reel to the shared trial queue (branch "trial-queue")
# The branch always holds exactly the reels still waiting to be posted (history squashed to 1 commit).
set -e; F="$1"; NAME=$(echo "${2:-reel}" | tr -cd 'A-Za-z0-9_-' | cut -c1-40); REPO=$(cd "$(dirname "$0")/.." && pwd)
ORIGIN=$(git -C "$REPO" remote get-url origin); N="$(date +%s)_${NAME}.mp4"
for try in 1 2 3 4 5 6 7 8; do
  W=$(mktemp -d); cd "$W"
  if git clone -q --depth 1 --branch trial-queue "$ORIGIN" q 2>/dev/null; then cd q; else mkdir q; cd q; git init -q; git remote add origin "$ORIGIN"; fi
  OLD=$(git rev-parse --verify -q HEAD 2>/dev/null || echo none)
  cp "$F" "$N"; git checkout -q --orphan tmp; git add -A
  git -c user.name=Hilal -c user.email=hilalmillali@gmail.com commit -qm "trial queue"
  if [ "$OLD" = none ]; then git push -q origin tmp:trial-queue && { echo "queued $N"; exit 0; }
  else git push -q --force-with-lease=trial-queue:$OLD origin tmp:trial-queue && { echo "queued $N"; exit 0; }; fi
  sleep $((10 + RANDOM % 30))
done
echo "FAILED to queue $N"; exit 1
