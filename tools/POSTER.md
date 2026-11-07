# Trial-reel poster runbook (one run = drain the queues at a human pace)

Posts Instagram Trial Reels to @_ilal_ from TWO queues, oldest first, as many as Instagram allows:
- A) Google Drive folder "Reels trial" 1rGW63KerCj3EQRGRk-mDWn1dVkU1onyK (videos Hilal drops in).
- B) GitHub branch "trial-queue" of this repo (reels made by the story makers "story_*" and the vlog task "vlog_*"). `bash tools/queue_list.sh` prints
  "<file> <raw url>" per waiting reel; file names start with a unix time (= when queued).
Every post: Trial Reel never shared to followers, NO caption (posted with Upload-Post, see step 3).
Instagram platformAccountId (vidIQ): 28479362468423214.
Pause marker: Drive file 1To5qPzsP_PVtqHPfC31ShBlz_BaLCl_1, title "reels-trial-state: active" or
"reels-trial-state: paused until <ISO time>".

## Steps
0. BURST TIMING (Hilal, 30 Oct: "post one after the other until the limit; maybe the limit is a number, not timing"
   — and a block hit early in the day ends sooner). Get the Toronto time (TZ=America/Toronto date). Post only between
   10:00 and 23:59 Toronto (the 00:xx hour would start the next day's batch at midnight); outside that window stop right away (no post, nothing logged). No random skip, no random wait:
   every run inside the window posts until today's cap is reached (step 3).
0a. DAILY CAP RAMP (Hilal, 30 Oct: "6 posts with no problem → next day try 7, keep going until stopped, then go back"). The
   current cap lives in tools/post_cap.json ("cap"). On the FIRST run of each Toronto day (no "history" entry for
   yesterday yet): count yesterday's (Toronto date) Instagram "posted" and "error" lines in post_log.jsonl (platform "instagram" or missing) and append
   {"day": yesterday, "cap": cap, "posted": n, "block": true|false} to "history". Then:
   - if yesterday had a block (2 failures in a row / block pause): cap = max(4, cap - 1) and "hold_until" = today + 2 days
     (no probing while holding);
   - else if yesterday reached the cap (posted >= cap), had no Instagram refusals (tooling errors like a failed download or GitHub hiccup don't count), and today is past "hold_until": cap = cap + 1;
   - otherwise keep the cap.
   BLOCK PAUSE LENGTH ("pause_hours" in post_cap.json, start 20; Hilal 30 Oct: shrink it by 2 h each time it works):
   - if the most recent block before yesterday was followed by a clean day (yesterday: no block, posted >= cap) and
     "pause_tested" is not already true for that block: pause_hours = max(2, pause_hours - 2), set "pause_tested": true;
   - if a block happens within 3 posts after a pause ended (the pause was too short): pause_hours = pause_hours + 2
     and keep it there ("pause_floor" = that value; never shrink below it again).
   A new block resets "pause_tested" to false.
   Commit/push tools/post_cap.json. Use this cap everywhere below instead of a fixed number.
0b. ONE RUN AT A TIME (3 Nov: a long burst overlapped with the next hourly run and the same clip got posted twice).
   `git pull`; if tools/poster.lock exists and its time (one ISO line) is less than 50 minutes old, another run is still
   posting → stop right away. Otherwise write the current UTC time to tools/poster.lock, commit and push it (if the push
   is rejected, pull and re-check). Delete the lock (commit + push) when this run ends, whatever happened.
1. Read the marker title (Google Drive get_file_metadata). If paused and that time is in the future, stop.
2. QUALITY FIRST (Hilal, 23 Oct: post only the reels most likely to go viral; Instagram allows ~12/day).
   Each queue B item has a hook score 1–10: from tools/queue_scores.json ("scores"[file]) or from its file name
   ("..._s8_..." = 8); no score = 5. Drive folder items (Hilal's own videos, e.g. "As2ila b3qlha" Q&A) are always
   score 10. Only items scoring 7+ may be posted; lower ones stay in the queue as reserve (never delete them).
   Pick the HIGHEST score first; ties → oldest first. If nothing scores 7+, post nothing this run.
   Build the list: Drive folder video files (search parentId = folder, not trashed; ignore non-video files) with their
   createdTime, plus queue B items with time = the unix prefix. Order by score (above), then age. Nothing eligible → stop.
3. PACING (Instagram blocks the account when too many go out at once: 21 Oct after a burst, 22 Oct after 12 posts in
   2 h). TODAY ONLY — 2026-11-07 (Toronto date), Hilal: "today post just those": post ONLY queue files with "_explainer_" in the name (best/oldest first), nothing else (no story reels, no Drive videos), up to the normal rolling/cap limits. From 2026-11-08 back to the normal mix below. EXPLAINERS (6 Nov, Drive or queue): Hilal will put ~50 couples-explainer reels in the Drive "Reels trial" folder (file names start with "explainer"). Post at most 3 explainers per day — Drive or queue "_explainer_" files — (mixed into the batch, spaced, not all first) so story reels and Hilal's own clips still go out; log them with "src": "explainer" and "file": <Drive file name>. Other Drive videos (his own clips) keep first place. TREND + EXPLAINER REELS (5–6 Nov): queue files named *_trend_s9_* or *_explainer_s9_* are Hilal's face trend reels — Instagram trials ONLY (never Facebook/TikTok), score 9 so they go right after Drive videos; log them with "type" and "src" = "trend" or "explainer". SKIP LIST: never post a queue file listed in tools/social_skip.json (clips Hilal/Claude judged too weird for any platform). ROLLING LIMIT (4 Nov: blocks came at ~10–11 Instagram posts in any 24 h, e.g. 5 on Nov 4 right after 11 on Nov 3): also count Instagram "posted" lines in the LAST 24 HOURS; if that is 9 or more, stop (post the rest later in the day once older posts drop out of the window). Count "posted" lines in tools/post_log.jsonl from TODAY (Toronto date) whose "platform" is "instagram" or missing (Facebook / TikTok lines never count): if cap or more (tools/post_cap.json), stop.
   Otherwise post items back to back in this same run (wait a random 3–6 minutes between posts) until today's count
   reaches the cap, nothing eligible is left, or an error happens (then follow the error rules). Re-pick the best item
   (step 2) before each post and commit/push the log after each post.
   POSTING TOOL (Hilal, 2 Nov): Instagram trial reels go through Upload-Post (tools/post.sh), no longer vidIQ.
   Job file for one reel (profile is "default"; no caption; never shared to followers):
     {"user":"default","platforms":["instagram"],"video":"<public url>","title":"",
      "fields":{"share_mode":"TRIAL_REELS_DONT_SHARE_TO_FOLLOWERS"}}
   Run `bash tools/post.sh job.json` (takes 1-3 min). It prints result.json: PUBLISHED = results.instagram.success true
   (or status_poll ... "success": true) with a post_url = the permalink. Anything else = error (error rules below;
   a message mentioning limit / quota / rate / "too many" = limit).
   For a Drive item:
     a. Fetch it through vidIQ first (this container's network can't download from Drive):
        vidiq_video_upload(url="https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t") → videoUrl.
        Then cover fix (prevents black covers): `URL=$(bash tools/fix_and_host.sh "<videoUrl from vidIQ>" "<short name>")`.
     b. Post URL with the job above.
     c. Only after PUBLISHED: trash the Drive file (Google Drive trash_file). Never trash anything not published.
   For a queue B item (already has a good cover, no fix needed):
     a. Post the item's raw URL with the job above.
     b. Only after PUBLISHED: `bash tools/queue_rm.sh <file>`.
   FALLBACK: if tools/post.sh itself breaks (GitHub Actions down, job never finishes, auth error — not an Instagram
   refusal), post that item the old way: vidiq_video_upload(url) → vidiq_instagram_publish_reel(platformAccountId,
   videoUrl, trialParams {"graduationStrategy":"MANUAL"}, no caption), poll until PUBLISHED.
4. If publishing fails with a limit / quota / rate / "too many" error: rename the marker to
   "reels-trial-state: paused until <now + 3 h, ISO>" and stop (leave the item where it is).
   Any other error on an item: skip that item this run (leave it), continue with the next — and log it (see Post log,
   event "error" with the first ~150 characters of the message in "note"). If 2 items in a row fail the same way, stop the
   run (Instagram is refusing posts) instead of trying the rest, AND treat it as a block: rename the marker to
   "reels-trial-state: paused until <now + pause_hours (tools/post_cap.json, default 20) h, ISO>".
5. If the run published at least one reel and the marker said paused (time passed), rename it back to
   "reels-trial-state: active".
6. End with one line: how many posted from Drive, how many from the vlog queue, how many still waiting.

## Post log (all posting tasks)
After every PUBLISHED trial reel, and whenever Instagram returns a limit error, append ONE line to tools/post_log.jsonl
and push (git pull --rebase first):
{"t": "<UTC ISO time>", "src": "drive" | "vlog" | "story" (queue files: story_* = story, vlog_* = vlog), "event": "posted" | "limit" | "error", "permalink": "<url or empty>", "file": "<queue file name or Drive file title>", "platform": "instagram", "note": "<error text, only for error>"}

## Waiting for results (IMPORTANT — 4 Nov: runs got killed while waiting and never logged their posts)
`tools/post.sh` can wait up to 30 min (Upload-Post sometimes hands a post to its "background" worker). Never let a
shell timeout kill it silently: run it as `bash tools/post.sh job.json` with the longest tool timeout (10 min). It
prints "post job <stamp> submitted" first. If the call times out or ends without a result, run
`bash tools/post_wait.sh <stamp>` (≤8 min each) again until it prints the result. A result with
"handed off ... background" is final only once result.json has status_poll.status "completed": the permalink is
status_poll.results[0].post_url. Log every post (even ones found late) BEFORE starting the next one.
