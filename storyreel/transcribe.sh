#!/bin/bash
# usage: storyreel/transcribe.sh audio_file out.json   (needs OPENAI_API_KEY). Files over 24 MB are re-encoded smaller first.
set -e; IN="$1"; OUT="$2"; F="$IN"
if [ $(stat -c%s "$IN") -gt 24000000 ]; then F="${OUT%.json}_small.m4a"; ffmpeg -loglevel error -y -i "$IN" -ac 1 -b:a 48k "$F"; fi
code=$(curl -s -o "$OUT" -w "%{http_code}" https://api.openai.com/v1/audio/transcriptions -H "Authorization: Bearer $OPENAI_API_KEY" -F model=whisper-1 -F file=@"$F" -F language=ar -F response_format=verbose_json -F "timestamp_granularities[]=segment" -F "timestamp_granularities[]=word")
if [ "$code" != 200 ]; then echo "OpenAI HTTP $code: $(head -c 400 "$OUT")" >&2; exit 1; fi
python3 -c "
import json;d=json.load(open('$OUT'))
for s in d['segments']: print(f\"{s['start']:7.2f}-{s['end']:7.2f} {s['text']}\")" > "${OUT%.json}_segments.txt"
echo "segments: ${OUT%.json}_segments.txt"
