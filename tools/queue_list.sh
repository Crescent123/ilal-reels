#!/bin/bash
# usage: tools/queue_list.sh -> one line per waiting reel: "<file> <raw url>" (oldest first; names start with a unix time)
REPO=$(cd "$(dirname "$0")/.." && pwd)
git -C "$REPO" ls-remote --exit-code origin trial-queue >/dev/null 2>&1 || exit 0
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT; git clone -q --depth 1 --filter=blob:none --no-checkout --branch trial-queue "$(git -C "$REPO" remote get-url origin)" "$W/q"
git -C "$W/q" ls-tree --name-only HEAD | grep '\.mp4$' | sort | while read f; do echo "$f https://raw.githubusercontent.com/Crescent123/ilal-reels/trial-queue/$f"; done
