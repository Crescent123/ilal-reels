# Couples explainer maker — runbook (one run = make up to 5 episodes from backlog.json and queue them)

Hilal (7 Nov 2026): "make at least 50 of these", all go straight to the trial queue (no daily drip). Budget OK'd:
~700 ElevenLabs credits per episode, ONE take each. Never print, store or ask for any API key.

Read first: explainer/SAFE_ZONES.md (layout + language rules), explainer/engine/SPEC.md (ep.json format),
explainer/ep05/ep.json (approved engine example). Episodes 2–4 are hand-made references for tone.

## 0. Lock (one run at a time)
`git pull`. If explainer/maker.lock exists and its ISO time is < 90 min old → stop. Else write the current UTC time
to explainer/maker.lock, commit + push. Delete it (commit + push) when the run ends, whatever happened.

## 1. Pick
Take the first 5 entries of explainer/backlog.json with "status":"todo" (lowest "ep" first). If none → delete the
lock, report "backlog done", stop. For each: mkdir explainer/epNN (NN = two digits).

## 2. Script → explainer/epNN/ep.json
- Moroccan DARIJA, 45–60 s spoken = about 650–800 characters, 17–24 phrases of 2–4 s each.
- ADAPT the "angle" for Moroccan couples; never translate the source. Balanced: no hate toward women or men; when a
  point is gendered, show it on both sides or turn it into a debate question. Keep debate → end with a question
  ("ونتوما؟ …") + cta "قولوها فالكومونطير 👇".
- Line 1 = the hook (a question or a surprising claim), it is also the title topic.
- LANGUAGE (Hilal, 6 Nov — the voice switch "is so bad, avoid maximum"): NO Latin letters anywhere in the voice text.
  Psych/science ideas in Darija/Arabic (عقلية الضحية، تحمّل المسؤولية، الحدود، العبء الذهني، التعوّد…). Only if no Arabic
  word exists, spell the English in Arabic letters (ليمرانس، غوتمان). Same rule for on-screen text.
- Voice text = the phrases' "t" joined with spaces (that's exactly what you send to ElevenLabs).
- Visual beats ("v") per phrase — see SPEC.md. Something must change on EVERY phrase (pose, bubble, emoji, top text,
  meter, fx, layout). Change layout every 3–5 phrases. Phrase 0: layout couple + a moving fx/pose (frame 1 already
  moves and shows the couple). Last phrase: layout "cta".

## 3. Voice
ElevenLabs creative_generate_speech: voice_id VZa0K5GwwOGE09GqMDa9 ("ilal Stories"), model eleven_v4,
generations_count 1, prompt = voice text. Never retry a generation (it charges again). Wait ~30 s, then
creative_get_generations(flow_id, [generation_id]) → full_res_url (repeat the get, not the generate, if still generating).
Start all 5 voices first, then fetch them.

## 4. Audio + timings
`bash explainer/engine/fetch.sh explainer/epNN '<full_res_url>'` (GitHub Actions; ~2 min). Prints duration + segment
count. Duration must be 40–62 s; outside → fix the script for the NEXT episode, keep this one if ≥38 s.

## 5. Check
`bash explainer/engine/check.sh explainer/epNN` → explainer/epNN/sheet.png (one still per phrase, green = safe area
x80–920 y240–1480, yellow = caption box). Read the sheet. Fix ep.json if: text/emoji crosses the green box, things
overlap (bubbles on heads, text on text), a phrase looks identical to the previous one, or a beat contradicts the line.
Re-run check after edits (max 2 rounds).

## 6. Render + queue
`bash explainer/engine/render.sh explainer/epNN` → out.mp4. Then from the repo root:
`bash tools/queue_add.sh $PWD/explainer/epNN/out.mp4 explainer_s9_<slug>` (ABSOLUTE path). Instagram trial only,
posted by the poster chat; never post yourself.

## 7. Log
- backlog.json: set "status":"queued", "date_queued":"YYYY-MM-DD".
- episodes.json: append {"ep","slug","topic" (title + one-line angle),"source_reel","made","status":"queued","date_queued"}.
- Commit explainer/epNN/{ep.json,data.json} + backlog.json + episodes.json (NOT frames/work/out.mp4), push.
- Report one line per episode: ep, title, seconds, credits. If ElevenLabs refuses (credits/quota), stop and report.
