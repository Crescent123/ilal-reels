#!/bin/bash
# usage: tools/fix_and_host.sh <video_url> <name>
# downloads the video, prepends a bright mid-video frame as the cover, force-pushes it to the orphan
# branch "queue" and prints the public raw URL.
set -e
URL="$1"; NAME="${2:-reel}"; W=$(mktemp -d); trap 'rm -rf "$W"' EXIT; REPO=$(cd "$(dirname "$0")/.." && pwd)
curl -sfL -o "$W/in.mp4" "$URL"
bash "$REPO/tools/cover_fix.sh" "$W/in.mp4" "$W/out.mp4" >&2
mkdir "$W/q"; cd "$W/q"; git init -q; git checkout -q --orphan queue
F="$(echo "$NAME" | tr -cd 'A-Za-z0-9_-' | cut -c1-40)_$(date +%s).mp4"
cp "$W/out.mp4" "$F"; git add "$F"
git -c user.name=Hilal -c user.email=hilalmillali@gmail.com commit -qm "queue $F"
git remote add origin "$(git -C "$REPO" remote get-url origin)"
git push -q -f origin queue >&2
echo "https://raw.githubusercontent.com/Crescent123/ilal-reels/queue/$F"
