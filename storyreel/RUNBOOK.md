# 2D story reel runbook (ilal Stories → Instagram Trial Reels)

Goal per run: turn ONE new story from the Drive folder "Stories audio" into a 30–50 s vertical 2D reel in Hilal's own
voice (40–55 s; see Experiment 1 for the build arm) and ADD IT TO THE SHARED TRIAL QUEUE (branch "trial-queue"). Several story makers run in parallel; the poster task
publishes the queue as MANUAL Trial Reels with NO caption, as many as Instagram allows. Story makers never publish.
Daily target: 12 clips a day (Toronto date) while Experiment 1 runs (the slate posts 9 a day and needs a few spare; 18 Nov fix: the old target = posting cap of 7 starved the 9-clip slate).
While Instagram posting is paused (pause marker title "paused until <time>" with that time in the future), the target is
4 per day. Before starting, read the pause marker (Google Drive get_file_metadata) and count today's clips (America/Toronto date):
moments with "status": "queued" and "date" today in storyreel/moments.json, plus live reservations (younger than 3 h). If the count is at or above
today's target (12, or 4 while paused), stop: today's target is reached. Otherwise make one.

## IDs
- Drive "Stories audio" folder: 1hPvjdeaN20sSWffO9aWRsN53lnWtJGCt (shared by link). Files are named "<YouTubeID> - <title>.m4a".
- AI steps (Whisper transcription and gpt-image-2 images) run in GitHub Actions through `tools/ai.sh`; the OpenAI key is
  a GitHub repo secret. NEVER download, read, print or export the OpenAI key in this session (the old Drive key file is
  retired; touching it gets the run blocked). If tools/ai.sh prints "AI ERRORS: OPENAI_API_KEY secret is not set",
  release your reservation and stop with that message. If anything else blocks the run, release the reservation
  (if the push still works) and stop with a one-line reason.
- Instagram platformAccountId (vidIQ): 28479362468423214.
- Pause marker shared with the other posting task: Drive file 1To5qPzsP_PVtqHPfC31ShBlz_BaLCl_1 (title "reels-trial-state: active" or "… paused until <ISO>").
- Used-story log: storyreel/used.json in this repo (video_id → {date, queued|permalink}). Push it after every reel.

## Steps
1. (An Instagram pause does not stop story makers; it only lowers today's target to 10.)
2. PICK A STORY — EVERY STORY HOLDS SEVERAL CLIPS (Hilal, 16 Nov: "a story could have lotta clips about lotta shit,
   even personal takes"). One story is no longer "used" after one clip. Order of choice:
   a) a story in "Stories audio" whose YouTube ID is in neither storyreel/used.json nor storyreel/moments.json (new upload);
   b) a story in storyreel/moments.json that still has a "todo" moment that is not a hard reject (make the one with the highest v4 estimate — skip steps 3–5).
      No limit per story: Hilal (16 Nov) — make as many as are good, each clip is seen on its own;
   c) a story not yet in moments.json, in the order of storyreel/story_rank.json (stories whose FIRST clip passed the
      retention gate — watched ≥48% and skip ≤33% — first, then family topic), then the rest of used.json, newest first.
      Never re-cut a passage that was already posted (Instagram limits repeated trials).
   Skip anything that is not a storytime (titles with podcast, Bad advice, vlog, حلويات, tests of food, Q&A).
2b. CLAIM THE STORY FIRST (story makers run in parallel). Add "<youtube_id>": {"reserved": "<UTC ISO time>"} to
   storyreel/moments.json (keep any existing moments), commit and push (git pull --rebase first). If the push is rejected
   or someone else holds a reservation younger than 3 hours, pick another story. Never claim more than one story per run.
2c. MINE THE WHOLE STORY (case a or c, after steps 3–4): read ALL of work/tr_segments.txt and list every passage that
   can stand alone as a 30–50 s clip, in story order, without overlapping each other or the earlier clip of this story
   (if you can't tell where the earlier clip was, assume it covered the first 90 s). Types: "secret" (a family member /
   someone close hides something and the narrator finds out — the best kind), "twist" (a funny or shocking turn),
   "conflict" (a fight or confrontation in the family/home), "take" (Hilal's own opinion or comment about what happened —
   end it on a debate question in Darija), "advice". Give each a rough v4 total (tools/RUBRIC_V4.md) to order them; hard rejects are marked "skip". Save them in moments.json as
   "<youtube_id>": {"mined": "<date>", "moments": [{"k": 1, "start": s, "end": e, "type": "...", "score": n,
   "hook": "<planned title>", "status": "todo"}, ...]}. A long story usually gives 3–8 moments. Then make the best
   todo moment in this run; the others wait for later runs (case b).
3. `bash storyreel/fetch.sh <drive_file_id> <youtube_id> work` → work/story.m4a and work/thumb.jpg.
4. `bash tools/ai.sh transcribe https://raw.githubusercontent.com/Crescent123/ilal-reels/drive-cache/<youtube_id>.m4a work`
   → work/tr.json and work/tr_segments.txt (takes 1–3 min). Read work/tr_segments.txt.
5. CHOOSE THE CLIP (most important; it is the moment you picked in 2c/2b):
   - ONE continuous passage of the narration, 30–50 s. Do not stitch the video's first sentence onto a later part
     (Hilal hated that). Extra cuts only to drop a digression such as the membership/Patreon/Discord plug, and only
     at sentence boundaries.
   - Start at the beginning of a sentence that sets up the situation on its own (who/what), ideally a strong moment.
   - End on a cliffhanger right before a reveal. Never reveal the ending/twist.
   - Prefer the middle-to-late build-up (the discovery, the trap, the betrayal setting up), not the channel intro.
   - Use the word timestamps in work/tr.json to set start/end just before the first word and just after the last word.
5b. EXPERIMENT 1 ARM + RUBRIC v4 (17 Nov – see "Experiment 1" below and tools/RUBRIC_V4.md). Before spending anything
   on images: (1) claim your Exp1 slot in tools/exp1.json (lowest slot with "file": null; set "taken_by": "<maker letter>-<UTC>",
   commit, push; on a rejected push, pull and claim the next one). The slot's "build" and "ending" decide how you cut and
   build this clip — never change them. (2) Plan the cut for that arm, then apply the v4 HARD REJECTS (name in title or
   first 8 s, set abroad, part x / needs an earlier clip, outside 40–55 s). A rejected moment is marked "skip" in
   moments.json and you take the next moment (keep the same slot). Do not filter on score otherwise: the poster needs
   low scores too (3 random slots a day). (3) Score the eight v4 items honestly from what frame 1, the title and the
   transcript of your cut will be, before building (no plays, no story history).
6. Check the cut with the word timestamps in work/tr.json: start just before the first word and end just after the
   last word of a complete sentence (build.py snaps to the quietest point within 0.12 s). No re-transcription needed.
7. Plan 7–9 scenes, one per phrase, each ≥2.5 s. For each: "at" = original-audio time where the scene starts
   (first = clip start; others just before a phrase begins), a short Darija caption (2–5 words, Arabic script,
   no French words), and a scene description that shows ACTION (who does what, where, emotion).
   Characters: define 2–4 recurring characters with very distinctive modern outfits in "chars"
   (e.g. "MOHAMED: a young man wearing a navy zip work jacket with orange reflective stripes, grey cargo trousers"),
   and reuse exactly those strings. Moroccan settings (city named in the story when known).
8. `bash tools/ai.sh images work/scenes.json work` (writes work/n1.png… — the "out" paths in scenes.json; 2–5 min). Look at a contact
   sheet; regenerate a scene only if it is clearly wrong (text in image, wrong character, nonsense). Max 2 retries total.
9. Write work/spec.json and run `python3 storyreel/build.py work/spec.json`:
   {"audio":"work/story.m4a","video_id":ID,"video_title":<YouTube title from the file name>,"thumb":"work/thumb.jpg",
    "title":<short hook, ≤6 words, Darija>,"pieces":[[start,end]],"scenes":[...],"music":"music/suspense_<1-4>.mp3"
    (rotate),"out":"work/reel.mp4"}
10. Check: grab frames at several times and look at them (text not clipped, no text over faces, end slide fine).
10a. SCORING = tools/RUBRIC_V4.md ONLY (frozen 18 Nov – 2 Dec). Earlier rubrics (topic, opening rule, curiosity rule)
   are retired; their history is in tools/EXPERIMENT.md. Write the clip's entry in tools/clip_meta.json (fields in
   RUBRIC_V4.md: story, moment, v4 items + total + tier + reject, arm {build, ending}, exp1_slot, length, made) and set
   the slot's "file" in tools/exp1.json to the queued file name, in the same commit as step 12.
11. Queue it: `bash tools/queue_add.sh work/reel.mp4 story_s<v4 total>_<youtube_id>_m<k>` (e.g. story_s12_abc123_m3) (keep the file under ~45 MB). Do NOT publish.
12. In storyreel/moments.json set that moment to {"status": "queued", "date": "<today>", "file": "<queued file name>"}, drop the "reserved" key, commit and push. (used.json stays as the record of first clips; don't add to it.)

## Experiment 1 (18–24 Nov, 63 clips; verdict not before 25 Nov — no rule changes before then)
Each clip's arm comes from its tools/exp1.json slot (seeded, balanced in blocks of 4). Both ending arms use the same kind of
moment; only the end cut moves.

BUILD arm 0 = the current maker (steps 6–9 as written: 7–9 scenes ≥2.5 s each, gentle zoom, 40–55 s).
BUILD arm 1 = "fast open + hold" spec:
- Start cut: the clip starts on the sentence that NAMES THE PERSON AND THE ODD ACT; at most 7 words before the verb;
  leading silence under 0.1 s; no greeting, no "one day", no scene-setting.
- Frame 1: the person in the title caught MID-ACT, seen from where the witness stands (doorway, stairs, window),
  head-to-waist framing, face visible, at most 2 characters. No establishing shot of a house or street.
- Motion: put "fast_open": true in spec.json (build.py pushes scene 1 in 100%→112% over 2 s). Scene 2 starts by 2.5 s;
  at least 3 scenes in the first 8 s (those early scenes may be 2–3 s, still cut in pauses). After second 8, a scene
  lasts at least 5 s.
- Title: on frame 1 (build.py shows it at full opacity, no fade); at most 6 words on 2 lines: relationship word + concrete
  act + when/where ("شنو بغات مرات خويا فالليل؟" is the pattern; "What happened?" is not).
- First caption: the odd act itself, on screen at 0.0 s. The title asks; caption and voice show.
- Sound: voice at full level from the first frame (build.py does this); no sting, logo or intro card.
- Hold: count beats in the transcript before cutting: at least 6 new facts or turns and no stretch longer than 8 s without
  one; a new question or reversal lands between 12 and 18 s (if the passage has none, pick another passage);
  self-contained for a stranger (no "as I told you", no unexplained "he"); length 44–54 s.

ENDING arm 0 = cut before the reveal (cliffhanger, as today).
ENDING arm 1 = the reveal happens INSIDE the clip, then Hilal's own take or a debate line from his narration closes it
(still one continuous passage of his voice, only cut; 40–55 s total, 44–54 s if build arm 1).

Never change a slot's arm. If a story has no moment that can satisfy the slot's arm, release the slot (taken_by: null)
and pick another story. Log every clip in tools/clip_meta.json with its arm.

## What goes viral (from 65 story reels, 16–21 Oct; views track watch % (r=0.66) and skip rate (r=-0.65), not length)
Winners (40K–433K views, 50–67 % watched, skip ≤30 %): "شنو كان كيدير الفقيه؟", "هاكا فيسبوك ديال جارتو",
"بيكالا غيرات ليا حياتي", "خطة المدير ضد البرهوش", "ليفرور البيتزا طاح فالحب", "الميكانيكي وبنت المعلم", "ماما كتخبي عليا شي حاجة".
Losers (1–2K views, 20–30 % watched, skip 45–54 %): "ليلة فطنجة", "ليلة سودا فالبرازيل", "تعرف على بنت فالقسم", "ماماه مرضات",
"جمعات الباليزة ورجعات للدار", "عرضة غريبة فدار الوكيل", stories set abroad (Brazil, Bahamas, America).
So, BEFORE claiming a story, judge whether it can carry a winning hook; skip stories that can't (just pick the next one):
- The title names a SPECIFIC familiar Moroccan role (الفقيه، الجارة، المدير، الميكانيكي، ليفرور، مول الحانوت، الأستاذ، ماما/بابا، البوليسي)
  plus a forbidden / secret / scandal / "what was he doing?" angle. A question is best. Never a vague "a night in X".
- Moroccan settings beat stories abroad.
- The FIRST image (first 2 s) shows two characters in open tension or a shocking situation, not one person on a phone or a
  bed. The first caption states the conflict ("الفقيه جا عند مو"), not background.
- Start the clip at the most intriguing sentence, not at the setup; length 40–50 s; end on the cliffhanger.
- Update 28 Oct (18 filtered reels): the hits are FUNNY / awkward taboo situations ("دار راسو مثلي وسط البنات" 158K,
  "المدير شدني مع بنتو؟" 27K, "شنو وقع مع صاحب خوها؟" 24K). Dark hooks about violence, crime or death flopped every time
  ("يوتوبر لقا صاحبتو مقتولة", "صاحبي بغا يقتلني فالليل", "خطيبتي ضربتني بالركبة", "صاحب الجارة دق عليها فالليل": 1.4–2K).
  So score violence / murder / crime / beating hooks at most 6 (skip them); prefer embarrassing, cheeky or romantic-scandal
  situations with a comic first image.
- Series test (12 parts of 60–83 s, 22 Oct): 16–30 % watched — don't make long multi-part series.

## Style rules (from Hilal)
- Voice: never EQ/denoise/compress/speed-change. Only cut. build.py already does this.
- Image changes only in pauses (build.py snaps to the quietest point). Slow gentle zoom only, plain cuts.
- No text inside images. Captions never over faces (build.py places them below the image).
- Music well under the voice (build.py: −24 dB + ducking).

## Instagram safe zone + composition (Hilal's lines, measured on his phone)
- Text (title, captions, CTA, end card) stays inside x 90–930, y 215–1630 of the 1080x1920 frame: title just under the
  top line (~y 255), captions sit right above the bottom line (bottom edge ~y 1620). Nothing near the right ~150px (buttons).
- Images are FULL-SCREEN vertical (gen_images.py makes 1024x1536, build.py fills the frame). The picture can run to every
  edge; only the main subjects/action must sit in the central area. Edges = calm background. Never let a subject look cut.
- Captions may overlap legs/floor but never faces; build.py adds dark gradients top and bottom for readability.
- When checking frames, reject a reel if text leaves that box or a face is under a caption.

## Post log (all posting tasks)
After every PUBLISHED trial reel, and whenever Instagram returns a limit error, append ONE line to tools/post_log.jsonl
and push (git pull --rebase first):
{"t": "<UTC ISO time>", "src": "drive" | "vlog" | "story", "event": "posted" | "limit", "permalink": "<url or empty>"}
