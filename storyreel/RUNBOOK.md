# 2D story reel runbook (ilal Stories → Instagram Trial Reels)

Goal per run: turn ONE new story from the Drive folder "Stories audio" into a 30–50 s vertical 2D reel in Hilal's own
voice and ADD IT TO THE SHARED TRIAL QUEUE (branch "trial-queue"). Several story makers run in parallel; the poster task
publishes the queue as MANUAL Trial Reels with NO caption, as many as Instagram allows. Story makers never publish.
No limit on making: always make one reel per run, however many are already waiting (Hilal's instruction). Only the
poster is limited, by Instagram.

## IDs
- Drive "Stories audio" folder: 1hPvjdeaN20sSWffO9aWRsN53lnWtJGCt (shared by link). Files are named "<YouTubeID> - <title>.m4a".
- OpenAI key: private Drive file 1Wdl0gkAK6qjvUhuhIGQwOblE67YAlbTR (read with Google Drive download_file_content, base64-decode, export as OPENAI_API_KEY). Never print it, never write it to the repo.
- Instagram platformAccountId (vidIQ): 28479362468423214.
- Pause marker shared with the other posting task: Drive file 1To5qPzsP_PVtqHPfC31ShBlz_BaLCl_1 (title "reels-trial-state: active" or "… paused until <ISO>").
- Used-story log: storyreel/used.json in this repo (video_id → {date, queued|permalink}). Push it after every reel.

## Steps
1. (Instagram pauses never stop story makers: always keep filling the queue.)
2. List the "Stories audio" folder (page through everything). Ignore .webm/.part and non-audio files. Pick the
   NEWEST-uploaded story whose YouTube ID is not in used.json. Skip anything that is not a storytime (titles with
   podcast, Bad advice, vlog, حلويات, tests of food, Q&A).
2b. CLAIM THE STORY FIRST (two story makers run in parallel). Immediately add
   "<youtube_id>": {"date": "<today>", "status": "reserved", "at": "<UTC ISO time>"} to storyreel/used.json, commit and
   push (git pull --rebase first). If the push is rejected or someone else already has that id, pick another story.
   Treat a "reserved" entry older than 3 hours as abandoned (a failed run) and free to take.
   Never claim more than one story per run.
3. `bash storyreel/fetch.sh <drive_file_id> <youtube_id> work` → work/story.m4a and work/thumb.jpg.
4. `bash storyreel/transcribe.sh work/story.m4a work/tr.json` → read work/tr_segments.txt.
5. CHOOSE THE CLIP (most important):
   - ONE continuous passage of the narration, 30–50 s. Do not stitch the video's first sentence onto a later part
     (Hilal hated that). Extra cuts only to drop a digression such as the membership/Patreon/Discord plug, and only
     at sentence boundaries.
   - Start at the beginning of a sentence that sets up the situation on its own (who/what), ideally a strong moment.
   - End on a cliffhanger right before a reveal. Never reveal the ending/twist.
   - Prefer the middle-to-late build-up (the discovery, the trap, the betrayal setting up), not the channel intro.
   - Use the word timestamps in work/tr.json to set start/end just before the first word and just after the last word.
6. Verify the cut: extract the clip audio (ffmpeg -ss start -to end) and transcribe it again; first and last words
   must be complete. Adjust by ±0.05–0.15 s if a word is clipped or a neighbour word leaks in.
7. Plan 7–9 scenes, one per phrase, each ≥2.5 s. For each: "at" = original-audio time where the scene starts
   (first = clip start; others just before a phrase begins), a short Darija caption (2–5 words, Arabic script,
   no French words), and a scene description that shows ACTION (who does what, where, emotion).
   Characters: define 2–4 recurring characters with very distinctive modern outfits in "chars"
   (e.g. "MOHAMED: a young man wearing a navy zip work jacket with orange reflective stripes, grey cargo trousers"),
   and reuse exactly those strings. Moroccan settings (city named in the story when known).
8. `OPENAI_API_KEY=… python3 storyreel/gen_images.py work/scenes.json` (writes work/n1.png…). Look at a contact
   sheet; regenerate a scene only if it is clearly wrong (text in image, wrong character, nonsense). Max 2 retries total.
9. Write work/spec.json and run `python3 storyreel/build.py work/spec.json`:
   {"audio":"work/story.m4a","video_id":ID,"video_title":<YouTube title from the file name>,"thumb":"work/thumb.jpg",
    "title":<short hook, ≤6 words, Darija>,"pieces":[[start,end]],"scenes":[...],"music":"music/suspense_<1-4>.mp3"
    (rotate),"out":"work/reel.mp4"}
10. Check: grab frames at several times and look at them (text not clipped, no text over faces, end slide fine).
11. Queue it: `bash tools/queue_add.sh work/reel.mp4 story_<youtube_id>` (keep the file under ~45 MB). Do NOT publish.
12. Replace your reservation in storyreel/used.json with {"date": ..., "queued": "<queued file name>"}, commit and push.

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
