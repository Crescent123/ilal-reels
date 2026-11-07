# Couples explainer reels (Hilal's cloned voice) — template
Reference account: @the90daysofgame ("90 Days of Game"). Episode 1 = «قاعدة 18 شهر» (approved by Hilal, 6 Nov 2026).
Files: anim.html (scene engine, edit the scenes per episode), build_data.py (phrase list -> scene/cut times + captions),
render.js (`node render.js test '[t1,t2]'` stills / `node render.js full` frames), pad.wav (music bed), SAFE_ZONES.md (rules).
Fonts: copy storyreel/assets/Cairo.ttf next to anim.html.

## Pipeline per episode
1. Script in Darija (~45–60 s, ~800 chars). Hook in the first line. Terms in Darija/Arabic first; English only if no Arabic word exists, and then spelled in Arabic letters for the voice (see SAFE_ZONES.md).
2. Voice: ElevenLabs creative_generate_speech, voice_id VZa0K5GwwOGE09GqMDa9 ("ilal Stories", Hilal's PVC), model eleven_v4,
   1 generation (~800 credits).
3. The container can't download from elevenlabsusercontent.com, so fetch via GitHub Actions: push
   ai/jobs/<stamp>.json = {"type":"transcribe","keep_audio":true,"url":"<content_url>"} -> ai-out/<stamp>/audio.mp3 + tr.json
   (Whisper segments give the timing; text comes back in MSA, only use the times). Align segments to your phrases
   (merge extra segments by hand if counts differ — see ep01/tr_aligned.json).
4. Edit anim.html scenes for the new topic, build data.json, test stills at key times, check overlaps/safe zones, then
   render full frames and mux:
   ffmpeg -framerate 30 -i frames/f%05d.jpg -i voice.mp3 -i pad.wav -filter_complex "[2:a]volume=0.10,afade=t=out:st=<dur-3>:d=3[m];[1:a][m]amix=inputs=2:duration=first:normalize=0[a]" -map 0:v -map "[a]" -c:v libx264 -pix_fmt yuv420p -crf 20 -c:a aac -b:a 160k -shortest out.mp4
5. Queue: `bash tools/queue_add.sh out.mp4 explainer_s9_<slug>` (IG trial poster posts s9 right after Hilal's Drive clips;
   "explainer" files are Instagram-only — TikTok/Facebook take only `_story_` files).
