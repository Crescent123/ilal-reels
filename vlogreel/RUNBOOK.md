# Vlog reel runbook (ilal Vlogs → Instagram Trial Reels)

Goal per run: cut EVERY remaining good moment (no limit) from the public ilal Vlogs videos into ~35–55 s vertical reels with Hilal's real
footage and voice, and add them to the shared trial queue (branch "trial-queue"). The poster task publishes everything
in that queue as MANUAL Trial Reels at a human pace — this task never publishes by itself.
No caps: Hilal wants every good moment clipped until the vlogs are finished. Keep going vlog after vlog until no
ingested vlog has good moments left (Drive quota permitting for new ingests). Queue each reel as soon as it is done
(don't wait until the end) and push used.json after each one, so nothing is lost if the run is cut short.
Hilal's verdict on the first one (Budapest, "بودابست ولا مدريد؟"): "perfect". Copy that recipe exactly:
vlogreel/example_budapest_spec.json.

## IDs
- Drive folder "Vlogs Public": 1UphkYpkRv9huLmcl2cDN7u2IvXVZP3Mg (shared by link). Use ONLY files whose title
  contains "public" (case-insensitive). NEVER use files with "members" in the title (paid members' content).
- Instagram platformAccountId (vidIQ): 28479362468423214.
- Pause marker shared with the other posting tasks: Drive file 1To5qPzsP_PVtqHPfC31ShBlz_BaLCl_1.
- Log of used moments: vlogreel/used.json  {driveFileId: [{title, clip:[start,end], date, permalink}]}.
- Per-vlog cache in the repo: vlogreel/cache/<driveFileId>/ (tr.json, tr_segments.txt, *_sheet_*.jpg), made once at ingest.
- Per-vlog 1080p master: GitHub release "src-<driveFileId>" (made once at ingest; clips are cut from it).
- OpenAI key (only for Whisper): private Drive file 1Wdl0gkAK6qjvUhuhIGQwOblE67YAlbTR (download_file_content, base64-
  decode, export OPENAI_API_KEY). Never print it, never write it into the repo.

## How the big files are reached (IMPORTANT — Google Drive has a download quota per file)
The vlogs are 4–13 GB 4K files and this workspace cannot reach Drive, so GitHub Actions (.github/workflows/vlog.yml)
does the heavy work. Streaming a big file from Drive more than about once a day trips Google's "Download quota exceeded"
(it happened on 14 Oct and blocked both vlogs for up to 24 h). So each vlog is read from Drive ONLY ONCE:
- `ingest <id> <tag> [<copyId>]` reads the Drive file once and makes: a 1080p master stored as GitHub release
  "src-<id>" (10-minute parts), <tag>.m4a (mono audio) and <tag>_sheet_NN.jpg contact sheets (a frame every 10 s).
  Takes ~20–60 min. `gh api repos/Crescent123/ilal-reels/releases/tags/src-<id>` (REST; succeeds once a vlog is ingested — `gh release view` is blocked in these sessions).
- `cut <id> <tag> <start> <end>` then cuts from that master (never touches Drive), ~2–4 min.
`OUT=work bash vlogreel/vlog_job.sh "<line>" ["<line>"...]` writes vlog/job.txt, pushes, waits for the job's own
done marker and downloads the results; it prints "JOB ERRORS: …" if anything failed. Make tags unique (append $(date +%s)).
If an ingest fails with "Quota exceeded" / "Invalid data", Drive is throttling that file: leave it, work on another
ingested vlog, and try the ingest again on a later run (the quota resets within 24 h). Never retry more than once per run.

## Steps
1. List "Vlogs Public" (page through). Candidates = "public" files (ignore "members" and "TEMP" files). Prefer vlogs
   that are already ingested and still have moments left; among those pick the one with the FEWEST entries in
   used.json. A vlog is finished when it has no more good, non-overlapping moments: then add {"done": true} as the
   last element of its list in used.json. If every public vlog is finished, stop (nothing left).
   List ALL remaining good moments of the vlog first, then cut them in batches of ~5 `cut` lines per job.
3. If the chosen vlog has no release "src-<id>" yet: run `ingest <id> <tag>` (only once per run), transcribe with
   `bash storyreel/transcribe.sh work/<tag>.m4a work/tr.json`, copy tr.json, tr_segments.txt and the sheets into
   vlogreel/cache/<id>/ and commit. If the cache already exists, just use it.
4. CHOOSE THE MOMENT (most important). Read tr_segments.txt (Whisper often turns Darija into MSA; read for meaning)
   and look at the contact sheets. Good moments: an opinion / hot take / comparison, a reaction, a funny exchange,
   a surprising price or fact, a strong view with talking. Hilal or a friend should be on camera talking.
   - ONE continuous passage 35–55 s, starting on the start of a sentence that works on its own (a question is ideal),
     ending right BEFORE the punchline/verdict/answer (cliffhanger) so people go watch the vlog.
   - No overlap with moments already in used.json for this vlog. Skip intros/outros, "subscribe", sponsor talk,
     long silent b-roll, and anything private (documents, addresses, kids' faces up close).
   - Use word timestamps in tr.json for exact start/end.
5. `cut <id> <tag> <start-6> <end+6>` (a margin on each side; cut from the release master). In the downloaded clip the moment starts at 6.0 s
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
9. Queue it: `bash tools/queue_add.sh work/reel.mp4 vlog_<city>_<start>` (keep the file under ~45 MB; if bigger,
   rebuild with a higher crf). Do NOT publish.
10. Append to vlogreel/used.json (title, clip in ORIGINAL vlog seconds, date, "queued": <file name>), commit, push
    (git pull --rebase first; other tasks push to this repo too).
