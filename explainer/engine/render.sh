#!/bin/bash
# usage: engine/render.sh <epdir>  -> <epdir>/out.mp4 (frames + voice + music bed)
set -e; D=$(cd "$(dirname "$0")" && pwd); E=$(realpath "$1")
python3 $D/build.py "$E" >/dev/null; rm -rf "$E/frames"; node $D/render.js "$E" full
DUR=$(python3 -c "import json;print(json.load(open('$E/data.json'))['dur'])")
ffmpeg -y -v error -framerate 30 -i "$E/frames/f%05d.jpg" -i "$E/work/voice.mp3" -i "$D/../pad.wav" -filter_complex "[2:a]volume=0.10,afade=t=out:st=$(python3 -c "print($DUR-3)"):d=3[m];[1:a][m]amix=inputs=2:duration=first:normalize=0[a]" -map 0:v -map "[a]" -c:v libx264 -pix_fmt yuv420p -crf 20 -c:a aac -b:a 160k -shortest "$E/out.mp4"
rm -rf "$E/frames"; echo "rendered $E/out.mp4 $(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/out.mp4)s"
