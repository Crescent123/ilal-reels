#!/bin/bash
# usage: tools/queue_rm.sh <file name in trial-queue>   -> removes a posted reel from the shared trial queue
set -e; N="$1"; REPO=$(cd "$(dirname "$0")/.." && pwd); ORIGIN=$(git -C "$REPO" remote get-url origin)
for try in 1 2 3; do
  W=$(mktemp -d); cd "$W"; git clone -q --depth 1 --branch trial-queue "$ORIGIN" q; cd q
  OLD=$(git rev-parse HEAD); git rm -q "$N"; git checkout -q --orphan tmp
  git -c user.name=Hilal -c user.email=hilalmillali@gmail.com commit -qm "trial queue" --allow-empty
  git push -q --force-with-lease=trial-queue:$OLD origin tmp:trial-queue && { echo "removed $N"; exit 0; }; sleep 20
done
echo "FAILED to remove $N"; exit 1
