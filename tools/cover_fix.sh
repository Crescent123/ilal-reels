#!/bin/bash
# usage: cover_fix.sh in.mp4 out.mp4  -> prepends the best mid-video frame (1 frame) so Instagram's default cover isn't black
set -e
IN="$1"; OUT="$2"; W=$(mktemp -d)
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$IN")
best=""; bestv=-1
for p in 0.30 0.40 0.50 0.60 0.70; do
  t=$(python3 -c "print(round($D*$p,2))")
  ffmpeg -loglevel error -y -ss $t -i "$IN" -frames:v 1 "$W/c_$p.png"
  v=$(python3 -c "from PIL import Image,ImageStat;im=Image.open('$W/c_$p.png').convert('L');s=ImageStat.Stat(im);print(round(s.mean[0]*0.5+s.stddev[0],1))")
  python3 -c "import sys;sys.exit(0 if $v>$bestv else 1)" && { best="$W/c_$p.png"; bestv=$v; }
done
SR=$(ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate -of csv=p=0 "$IN"); SR=${SR:-44100}
WH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$IN")
ffmpeg -loglevel error -y -loop 1 -i "$best" -frames:v 2 -r "$FPS" -vf "scale=${WH%x*}:${WH#*x},setsar=1,format=yuv420p" -c:v libx264 -preset veryfast -crf 18 "$W/cover.mp4"
CD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$W/cover.mp4"); MS=$(python3 -c "print(int(round($CD*1000)))")
ffmpeg -loglevel error -y -i "$W/cover.mp4" -i "$IN" -filter_complex \
 "[0:v]setsar=1,fps=$FPS,format=yuv420p[c];[1:v]setsar=1,fps=$FPS,format=yuv420p[m];[c][m]concat=n=2:v=1:a=0[v];[1:a]adelay=$MS:all=1[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$OUT"
echo "cover score $bestv from $(basename $best)"
