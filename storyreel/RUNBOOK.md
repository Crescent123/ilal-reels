# 2D story reel runbook (ilal Stories → Instagram Trial Reels)

Goal per run: turn ONE new story from the Drive folder "Stories audio" into a 30–50 s vertical 2D reel in Hilal's own
voice and ADD IT TO THE SHARED TRIAL QUEUE (branch "trial-queue"). Several story makers run in parallel; the poster task
publishes the queue as MANUAL Trial Reels with NO caption, as many as Instagram allows. Story makers never publish.
Daily target: the posting cap in tools/post_cap.json ("cap", currently ramping from 7; Instagram's real limit is being probed).
While Instagram posting is paused (pause marker title "paused until <time>" with that time in the future), the target is
4 per day. Before starting, read the pause marker (Google Drive get_file_metadata) and count today's clips (America/Toronto date):
moments with "status": "queued" and "date" today in storyreel/moments.json, plus live reservations (younger than 3 h). If the count is at or above
today's target (the cap, or 4 while paused), stop: today's target is reached. Otherwise make one.

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
   b) a story in storyreel/moments.json that still has a "todo" moment scoring 7+ AND fewer than 2 clips queued in the
      last 24 h (spread the stories out — the feed shouldn't get 4 clips of one story in a day) (make that moment — skip steps 3–5);
   c) a story not yet in moments.json, best first: the ones whose earlier clip got 20K+ plays (tools/ig_plays.json,
      match the YouTube ID in the file name), then the stories marked "skip" in used.json (their opening was weak, the
      rest was never looked at), then the rest of used.json, newest first.
   Skip anything that is not a storytime (titles with podcast, Bad advice, vlog, حلويات, tests of food, Q&A).
2b. CLAIM THE STORY FIRST (story makers run in parallel). Add "<youtube_id>": {"reserved": "<UTC ISO time>"} to
   storyreel/moments.json (keep any existing moments), commit and push (git pull --rebase first). If the push is rejected
   or someone else holds a reservation younger than 3 hours, pick another story. Never claim more than one story per run.
2c. MINE THE WHOLE STORY (case a or c, after steps 3–4): read ALL of work/tr_segments.txt and list every passage that
   can stand alone as a 30–50 s clip, in story order, without overlapping each other or the earlier clip of this story
   (if you can't tell where the earlier clip was, assume it covered the first 90 s). Types: "secret" (a family member /
   someone close hides something and the narrator finds out — the best kind), "twist" (a funny or shocking turn),
   "conflict" (a fight or confrontation in the family/home), "take" (Hilal's own opinion or comment about what happened —
   end it on a debate question in Darija), "advice". Score each with 10b. Save them in moments.json as
   "<youtube_id>": {"mined": "<date>", "moments": [{"k": 1, "start": s, "end": e, "type": "...", "score": n,
   "hook": "<planned title>", "status": "todo"}, ...]}. A long story usually gives 3–8 moments. Then make the best
   todo moment (score 7+) in this run; the others wait for later runs (case b).
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
5b. VIRALITY GATE (Hilal: only make what has viral potential, otherwise skip). Before spending anything on images,
   write the planned title + first caption + first scene and score them 1–10 with the rubric in step 10b. If it can't
   reach 7, mark that moment "skip" in moments.json and take the next todo moment of the same story (or stop if none).
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
10a. WHERE TO CUT — THE CURIOSITY RULE (Round 3, 16 Nov; replaces the 14 Nov "forbidden moment + danger" rule, which
   FAILED blind: the 5 rule-9 clips posted 14 Nov got 1.3K, 1.7K, 1.8K, 1.9K, 15.7K). From the real first 8 s of the
   35 story clips posted 12–15 Nov, the 8 clips past 15K vs the 8 under 2.1K:
   WINNERS (429K, 84K, 29K, 28K, 27K, 22K, 17K, 16K): the title asks WHAT SOMEONE CLOSE IS SECRETLY DOING and the
   narrator is the WITNESS — "شنو كانت كدير ختي وصاحبتها؟", "ماما لقات الحشيش فالدار؟", "شنو بغات ختو من مراتو؟",
   "شنو كانت كدير الخدامة فداري؟", "ماما خلات البنت تبات عندهم" — or a light comic twist ("العروبي طاح معايا... وأنا
   راجل!", "شكون شطح مع صاحبة الديجي؟"). Everyday Moroccan home, the other person on screen in frame 1, playful tone.
   LOSERS: the narrator is the one doing wrong and might get caught (party while dad travels, came home drunk, texting
   his girlfriend's friend, spying with a camera), partner betrayal ("مراتي كذبات عليا"), heavy topics (mom has cancer),
   sensitive ones (a gay guest). Numbers: winners avg 51 % watched / 28 % skip / 8.6 shares per 1K views; losers 34 % /
   37 % / 3.6. So: open on the OTHER person doing the odd/secret thing, caption 1 = what we see them do ("ختي وصاحبتها
   سدو الباب", "بابا كيكمي فالبالكون"), caption 2 = what we hear/notice next ("كنسمعو الحركة من الحيط"). Keep it
   curious and a bit funny, not scary. Never open on illness, plans, a job, a party being organised, or background.
   End before the reveal (as before).
10b. SCORE THE HOOK honestly 1–10:
   9 = title asks what a FAMILY/HOUSEHOLD member is secretly doing (ماما/بابا/ختي/خويا/الجد/مرت خويا/الخدامة/حماتي),
       narrator is the witness, that person is on screen in frame 1 — name the file _s9_.
   8 = family/home secret told another way, or a light comic twist where the narrator outsmarts someone.
   7 = curiosity about someone else (friend, neighbour, stranger at a wedding) or a playful romance situation.
   6 = narrator's own wrongdoing at risk of being caught, cheating / partner trust, girlfriend-fiancée drama.
       Below 7 → rework the cut once (start on the other person's secret); if it still can't reach 7, skip it.
   Hard caps at 5 (skip): a character NAME in title or captions, set abroad / foreign tourists, "PART x", money/scam/
   gambling core, crime/prison/police/violence, death/illness, alcohol. (149-reel analysis: red flags = 0.43x views.)
   Supply note: the queue has almost no 9s — when picking a story, prefer ones where a parent/sibling/grandparent/maid
   hides something and the narrator finds out.
11. Queue it: `bash tools/queue_add.sh work/reel.mp4 story_s<score>_<youtube_id>_m<k>` (e.g. story_s8_abc123_m3) (keep the file under ~45 MB). Do NOT publish.
12. In storyreel/moments.json set that moment to {"status": "queued", "date": "<today>", "file": "<queued file name>"}, drop the "reserved" key, commit and push. (used.json stays as the record of first clips; don't add to it.)

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
