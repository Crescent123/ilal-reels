# Vlog reel runbook (ilal Vlogs → Instagram Trial Reels)

Goal per run: cut ONE new moment from a public ilal Vlogs video into a ~35–55 s vertical reel with Hilal's real
footage and voice, and post it to Instagram @_ilal_ as a MANUAL Trial Reel with NO caption.
Hilal's verdict on the first one (Budapest, "بودابست ولا مدريد؟"): "perfect". Copy that recipe exactly:
vlogreel/example_budapest_spec.json.

## IDs
- Drive folder "Vlogs Public": 1UphkYpkRv9huLmcl2cDN7u2IvXVZP3Mg (shared by link). Use ONLY files whose title
  contains "public" (case-insensitive). NEVER use files with "members" in the title (paid members' content).
- Instagram platformAccountId (vidIQ): 28479362468423214.
- Pause marker shared with the other posting tasks: Drive file 1To5qPzsP_PVtqHPfC31ShBlz_BaLCl_1.
- Log of used moments: vlogreel/used.json  {driveFileId: [{title, clip:[start,end], date, permalink}]}.
- Per-vlog cache in the repo: vlogreel/cache/<driveFileId>/ (tr.json, tr_segments.txt, *_sheet_*.jpg). Create it the
  first time a vlog is used and commit it, so later runs skip the audio/sheet step.
- OpenAI key (only for Whisper): private Drive file 1Wdl0gkAK6qjvUhuhIGQwOblE67YAlbTR (download_file_content, base64-
  decode, export OPENAI_API_KEY). Never print it, never write it into the repo.

## How the big files are reached
The vlogs are 4–13 GB 4K files. This workspace cannot reach Drive, so GitHub Actions (.github/workflows/vlog.yml) streams
them straight from Drive with ffmpeg and pushes small results to the orphan branch vlog-cache.
`OUT=work bash vlogreel/vlog_job.sh "<line>" ["<line>"...]` writes vlog/job.txt, pushes, waits and downloads results.
Lines: `audio <id> <tag>` (mono m4a + info), `sheet <id> <tag>` (contact sheets, a frame every 10 s with timecodes),
`cut <id> <tag> <start> <end>` (1920x1080 mp4 of that range). ALWAYS make tags unique per run (append $(date +%s)).
Takes ~3–10 min per job; a cut of 70 s takes ~5 min.

## Steps
1. If the pause marker says paused and that time is still in the future, stop.
2. List "Vlogs Public" (page through). Candidates = "public" files. Pick the vlog with the FEWEST entries in used.json
   (oldest first on ties). If every public vlog already has 8 used moments, stop (nothing left).
3. If vlogreel/cache/<id>/ is missing: run one job with both `audio <id> <tag>` and `sheet <id> <tag>`, transcribe with
   `bash storyreel/transcribe.sh work/<tag>.m4a work/tr.json`, copy tr.json, tr_segments.txt and the sheets into the
   cache folder and commit.
4. CHOOSE THE MOMENT (most important). Read tr_segments.txt (Whisper often turns Darija into MSA; read for meaning)
   and look at the contact sheets. Good moments: an opinion / hot take / comparison, a reaction, a funny exchange,
   a surprising price or fact, a strong view with talking. Hilal or a friend should be on camera talking.
   - ONE continuous passage 35–55 s, starting on the start of a sentence that works on its own (a question is ideal),
     ending right BEFORE the punchline/verdict/answer (cliffhanger) so people go watch the vlog.
   - No overlap with moments already in used.json for this vlog. Skip intros/outros, "subscribe", sponsor talk,
     long silent b-roll, and anything private (documents, addresses, kids' faces up close).
   - Use word timestamps in tr.json for exact start/end.
5. `cut <id> <tag> <start-6> <end+6>` (a margin on each side). In the downloaded clip the moment starts at 6.0 s
   (adjust if the margin was clipped at 0). Re-transcribe [start,end] of the clip to confirm first/last words.
6. Face positions: make strips of the moment, 1 frame/s with a grid (ffmpeg fps=1,scale=384:-2,drawgrid=w=96 …,
   tile=5x3). Each grid column = 480 source px. Write down for every second where the speaking face(s) are.
   - Two people side by side (faces > ~700 px apart) for several seconds → a "split" window
     [t0, t1, topX, topY, botX, botY]: 960x600 crops, normally left person on top (x 0) and right person bottom (x 960);
     choose topY/botY so faces sit in the upper-middle of each crop (not under the bottom captions).
   - Otherwise "full_cx" keyframes [t, faceX] (piecewise-linear; for camera whips add two close keyframes to jump).
7. Spec (see example_budapest_spec.json) and `python3 vlogreel/build_vlog.py work/spec.json`:
   - title: short Darija hook ≤ 5 words, ideally the question of the clip (e.g. "بودابست ولا مدريد؟").
   - captions: 5–8 short Darija lines (2–6 words, Arabic script) that follow what is said, timed to the speech, gaps OK.
   - cta: line1 "الڤلوگ كامل كتسناك", line2 "فقناة ilal Vlogs", pill "قلب عليها فيوتيوب", vtitle "ڤلوگ <city>",
     handle "@ilalvlogs", thumb_t = a time (relative to start) with a nice wide frame of the place/people.
   - music: rotate music/suspense_1..4.mp3 (only plays under the end card). Original vlog audio is never processed.
8. Check frames at ~6 moments + end card: faces visible and not under text, no empty-sky frames, text inside the
   safe box x 90–930 / y 215–1630. Fix keyframes and rebuild if needed (max 2 rebuilds).
9. Post: `URL=$(bash storyreel/host.sh work/reel.mp4 queue3)` → vidiq_video_upload(url=URL) →
   vidiq_instagram_publish_reel(platformAccountId, videoUrl, NO caption, trialParams {"graduationStrategy":"MANUAL"}).
   Poll with containerId every ~20 s until PUBLISHED.
10. Append to vlogreel/used.json (title, clip in ORIGINAL vlog seconds, date, permalink), commit, push
    (git pull --rebase first; other tasks push to this repo too).
11. On a limit/quota/rate error when publishing: set the pause marker title to
    "reels-trial-state: paused until <now+3h ISO>", don't log the moment, stop.
