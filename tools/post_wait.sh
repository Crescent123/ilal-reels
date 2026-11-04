#!/bin/bash
# usage: tools/post_wait.sh <stamp>   (stamp = the "post job <stamp> submitted" id printed by tools/post.sh)
# Waits up to ~8 min for that job's result and prints it. Safe to run again if it says PENDING.
S="$1"; RAW="https://raw.githubusercontent.com/Crescent123/ilal-reels/post-out/$S"
for i in $(seq 1 32); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' "$RAW/done.txt?w$i$RANDOM")" = 200 ] && { curl -s "$RAW/result.json?r$RANDOM"; echo; echo "ERR: $(curl -s "$RAW/done.txt?z$RANDOM")"; exit 0; }
  sleep 15
done
echo "PENDING $S (run tools/post_wait.sh $S again)"
