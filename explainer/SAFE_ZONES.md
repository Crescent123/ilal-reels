# Couples explainer reels — template rules (Hilal, 6 Nov)
Canvas 1080x1920. Instagram covers: top ~220 px (header), bottom ~420 px (caption/account/audio), right ~140 px (like/comment/share).
SAFE AREA for anything important: x 80–920, y 240–1480. Captions sit in y 1330–1460, ONE line at a time, never overlapping visuals.
Hook: frame 1 must already MOVE and show the topic (the couple), never a black screen with text. Title text inside the safe area.
Keep it dynamic: something changes every 1.5–3 s (cut, zoom, icon pop, figure action); slow camera push-in on every scene.
Captions: 2–5 words per chunk, timed to the voice, white box, black text, no wrapping (auto-shrink).
Voice: Hilal's PVC "ilal Stories" (VZa0K5GwwOGE09GqMDa9) on eleven_v4. ~800 credits per 55 s.
Pipeline: script -> ElevenLabs v4 -> fetch audio + Whisper timings via GitHub Actions (ai job, keep_audio) -> anim.html scenes -> Playwright frames -> ffmpeg + soft synth bed.
- Scientific terms (dopamine, limerence…) stay in English, in text AND voice (Hilal, 6 Nov): write them in Latin letters in the script so the clone says them the English way.
