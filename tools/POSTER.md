# Trial-reel poster runbook (one run = drain the queues at a human pace)

Posts Instagram Trial Reels to @_ilal_ from TWO queues, oldest first, as many as Instagram allows:
- A) Google Drive folder "Reels trial" 1rGW63KerCj3EQRGRk-mDWn1dVkU1onyK (videos Hilal drops in).
- B) GitHub branch "trial-queue" of this repo (reels made by the story makers "story_*" and the vlog task "vlog_*"). `bash tools/queue_list.sh` prints
  "<file> <raw url>" per waiting reel; file names start with a unix time (= when queued).
Every post: Trial Reel with trialParams {"graduationStrategy":"MANUAL"} (never shared to followers), NO caption.
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
   yesterday yet): count yesterday's (Toronto date) "posted" and "error" lines in post_log.jsonl and append
   {"day": yesterday, "cap": cap, "posted": n, "block": true|false} to "history". Then:
   - if yesterday had a block (2 failures in a row / block pause): cap = max(4, cap - 1) and "hold_until" = today + 2 days
     (no probing while holding);
   - else if yesterday reached the cap (posted >= cap), had no errors, and today is past "hold_until": cap = cap + 1;
   - otherwise keep the cap.
   BLOCK PAUSE LENGTH ("pause_hours" in post_cap.json, start 20; Hilal 30 Oct: shrink it by 2 h each time it works):
   - if the most recent block before yesterday was followed by a clean day (yesterday: no block, posted >= cap) and
     "pause_tested" is not already true for that block: pause_hours = max(2, pause_hours - 2), set "pause_tested": true;
   - if a block happens within 3 posts after a pause ended (the pause was too short): pause_hours = pause_hours + 2
     and keep it there ("pause_floor" = that value; never shrink below it again).
   A new block resets "pause_tested" to false.
   Commit/push tools/post_cap.json. Use this cap everywhere below instead of a fixed number.
1. Read the marker title (Google Drive get_file_metadata). If paused and that time is in the future, stop.
2. QUALITY FIRST (Hilal, 23 Oct: post only the reels most likely to go viral; Instagram allows ~12/day).
   Each queue B item has a hook score 1–10: from tools/queue_scores.json ("scores"[file]) or from its file name
   ("..._s8_..." = 8); no score = 5. Drive folder items (Hilal's own videos, e.g. "As2ila b3qlha" Q&A) are always
   score 10. Only items scoring 7+ may be posted; lower ones stay in the queue as reserve (never delete them).
   Pick the HIGHEST score first; ties → oldest first. If nothing scores 7+, post nothing this run.
   Build the list: Drive folder video files (search parentId = folder, not trashed; ignore non-video files) with their
   createdTime, plus queue B items with time = the unix prefix. Order by score (above), then age. Nothing eligible → stop.
3. PACING (Instagram blocks the account when too many go out at once: 21 Oct after a burst, 22 Oct after 12 posts in
   2 h). Count "posted" lines in tools/post_log.jsonl from TODAY (Toronto date): if cap or more (tools/post_cap.json), stop.
   Otherwise post items back to back in this same run (wait a random 3–6 minutes between posts) until today's count
   reaches the cap, nothing eligible is left, or an error happens (then follow the error rules). Re-pick the best item
   (step 2) before each post and commit/push the log after each post.
   For a Drive item:
     a. vidiq_video_upload(url="https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t").
     b. Cover fix (prevents black covers): `URL=$(bash tools/fix_and_host.sh "<videoUrl from a>" "<short name>")`,
        then vidiq_video_upload(url=URL) to get the final videoUrl.
     c. vidiq_instagram_publish_reel(platformAccountId, videoUrl, trialParams MANUAL, no caption); poll with containerId
        every ~15–20 s until PUBLISHED.
     d. Only after PUBLISHED: trash the Drive file (Google Drive trash_file). Never trash anything not published.
   For a queue B item (already has a good cover, no fix needed):
     a. vidiq_video_upload(url=<raw url>) → videoUrl.
     b. Publish exactly as above and poll until PUBLISHED.
     c. Only after PUBLISHED: `bash tools/queue_rm.sh <file>`.
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
{"t": "<UTC ISO time>", "src": "drive" | "vlog" | "story" (queue files: story_* = story, vlog_* = vlog), "event": "posted" | "limit" | "error", "permalink": "<url or empty>", "note": "<error text, only for error>"}
