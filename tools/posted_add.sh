#!/bin/bash
# usage: tools/posted_add.sh <local mp4> <file name>  -> keeps a copy of a posted reel on branch "trial-posted"
# (squashed orphan, like trial-queue) so proven clips can be reused on Facebook / TikTok.
F="$1"; N="$2"; REPO=$(cd "$(dirname "$0")/.." && pwd); ORIGIN=$(git -C "$REPO" remote get-url origin)
for try in 1 2 3 4 5 6; do
  W=$(mktemp -d); trap 'rm -rf "$W"' EXIT; cd "$W"
  if git clone -q --depth 1 --branch trial-posted "$ORIGIN" p 2>/dev/null; then cd p; OLD=$(git rev-parse HEAD); LEASE="--force-with-lease=trial-posted:$OLD"
  else mkdir p; cd p; git init -q; git remote add origin "$ORIGIN"; LEASE="--force"; fi
  cp "$F" "$N"; git add -A; git checkout -q --orphan tmp 2>/dev/null
  git -c user.name=Hilal -c user.email=ilal-bot@users.noreply.github.com commit -qm "posted reels" --allow-empty
  git push -q $LEASE origin tmp:trial-posted && { echo "archived $N"; exit 0; }; cd /; rm -rf "$W"; sleep $((5 + RANDOM % 20))
done
echo "archive FAILED for $N (non-fatal)"; exit 0
