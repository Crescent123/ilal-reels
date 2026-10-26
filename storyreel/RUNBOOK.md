# 2D story reel runbook (ilal Stories → Instagram Trial Reels)

Goal per run: turn ONE new story from the Drive folder "Stories audio" into a 30–50 s vertical 2D reel in Hilal's own
voice and ADD IT TO THE SHARED TRIAL QUEUE (branch "trial-queue"). Several story makers run in parallel; the poster task
publishes the queue as MANUAL Trial Reels with NO caption, as many as Instagram allows. Story makers never publish.
Daily target (26 Oct): about 7 reels made per day in total (Instagram lets only ~7 trial reels a day through).
While Instagram posting is paused (pause marker title "paused until <time>" with that time in the future), the target is
4 per day. Before starting, read the pause marker (Google Drive get_file_metadata) and count the entries in
storyreel/used.json whose "date" is today (America/Toronto date) — reserved ones included, "skip" ones NOT counted. If the count is at or above
today's target (7, or 4 while paused), stop: today's target is reached. Otherwise make one.

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
2. List the "Stories audio" folder (page through everything). Ignore .webm/.part and non-audio files. Pick the
   NEWEST-uploaded story whose YouTube ID is not in used.json. Skip anything that is not a storytime (titles with
   podcast, Bad advice, vlog, حلويات, tests of food, Q&A).
2b. CLAIM THE STORY FIRST (two story makers run in parallel). Immediately add
   "<youtube_id>": {"date": "<today>", "status": "reserved", "at": "<UTC ISO time>"} to storyreel/used.json, commit and
   push (git pull --rebase first). If the push is rejected or someone else already has that id, pick another story.
   Treat a "reserved" entry older than 3 hours as abandoned (a failed run) and free to take.
   Never claim more than one story per run.
3. `bash storyreel/fetch.sh <drive_file_id> <youtube_id> work` → work/story.m4a and work/thumb.jpg.
4. `bash tools/ai.sh transcribe https://raw.githubusercontent.com/Crescent123/ilal-reels/drive-cache/<youtube_id>.m4a work`
   → work/tr.json and work/tr_segments.txt (takes 1–3 min). Read work/tr_segments.txt.
5. CHOOSE THE CLIP (most important):
   - ONE continuous passage of the narration, 30–50 s. Do not stitch the video's first sentence onto a later part
     (Hilal hated that). Extra cuts only to drop a digression such as the membership/Patreon/Discord plug, and only
     at sentence boundaries.
   - Start at the beginning of a sentence that sets up the situation on its own (who/what), ideally a strong moment.
   - End on a cliffhanger right before a reveal. Never reveal the ending/twist.
   - Prefer the middle-to-late build-up (the discovery, the trap, the betrayal setting up), not the channel intro.
   - Use the word timestamps in work/tr.json to set start/end just before the first word and just after the last word.
5b. VIRALITY GATE (Hilal: only make what has viral potential, otherwise skip). Before spending anything on images,
   write the planned title + first caption + first scene and score them 1–10 with the rubric in step 10b. If it can't
   reach 7, skip the story now: mark it in used.json as {"date": ..., "skip": "weak hook"}, push, and stop (no images).
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
10b. SCORE THE HOOK honestly 1–10 with the "What goes viral" rules: 9–10 = familiar Moroccan role + forbidden/secret
   question + two people in open tension in the first frame (e.g. "المدير شدني مع بنتو؟"); 7–8 = strong question or scandal
   with a clear conflict (e.g. "شنو لقا فتليفون مراتو؟", "صاحبي بغا يقتلني فالليل"); 4–6 = intriguing but vague, or one
   person alone in the first frame; 1–3 = vague ("الليلة اللي قلبات حياتي"), routine, or set abroad. If below 7, improve
   the title / first scene (one rebuild max); if the story itself can't reach 7, don't queue it: mark it in used.json as
   {"date": ..., "skip": "weak hook"} and stop (the poster only posts 7+).
11. Queue it: `bash tools/queue_add.sh work/reel.mp4 story_s<score>_<youtube_id>` (e.g. story_s8_abc123) (keep the file under ~45 MB). Do NOT publish.
12. Replace your reservation in storyreel/used.json with {"date": ..., "queued": "<queued file name>"}, commit and push.

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
