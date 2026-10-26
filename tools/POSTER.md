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
0. HUMAN TIMING (Hilal, 24 Oct: "post like I would in my waking hours, randomly"). Get the Toronto time
   (TZ=America/Toronto date). Post only between 10:00 and 00:59 Toronto; outside that window stop right away (no post,
   nothing logged). Inside it, decide randomly whether this run posts: roll a number 1–100 (`echo $((RANDOM%100+1))`)
   and post only if it is ≤ 50 (≈7 posts spread over the 15 waking hours, never on a fixed rhythm) — exception: if
   fewer posts than (hours since 10:00 Toronto ÷ 2.2) have gone out today, post anyway so the day still reaches ~7.
   When posting, first wait a random 0–30 minutes (`sleep` in chunks ≤ 9 min) so posts don't land at the same
   minute every hour.
1. Read the marker title (Google Drive get_file_metadata). If paused and that time is in the future, stop.
2. QUALITY FIRST (Hilal, 23 Oct: post only the reels most likely to go viral; Instagram allows ~12/day).
   Each queue B item has a hook score 1–10: from tools/queue_scores.json ("scores"[file]) or from its file name
   ("..._s8_..." = 8); no score = 5. Drive folder items (Hilal's own videos, e.g. "As2ila b3qlha" Q&A) are always
   score 10. Only items scoring 7+ may be posted; lower ones stay in the queue as reserve (never delete them).
   Pick the HIGHEST score first; ties → oldest first. If nothing scores 7+, post nothing this run.
   Build the list: Drive folder video files (search parentId = folder, not trashed; ignore non-video files) with their
   createdTime, plus queue B items with time = the unix prefix. Order by score (above), then age. Nothing eligible → stop.
3. PACING (Instagram blocks the account when too many go out at once: 21 Oct after a burst, 22 Oct after 12 posts in
   2 h). Count "posted" lines in tools/post_log.jsonl from the last 24 h: if 7 or more, stop (daily cap; Instagram blocked at ~11/24 h on 24 Oct and at 9 posts in 8.5 h on 26 Oct). Also stop if the last post was less than 90 minutes ago. Otherwise post
   at most 1 item this run (the poster runs every hour, so posts spread over the day).
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
   "reels-trial-state: paused until <now + 20 h, ISO>".
5. If the run published at least one reel and the marker said paused (time passed), rename it back to
   "reels-trial-state: active".
6. End with one line: how many posted from Drive, how many from the vlog queue, how many still waiting.

## Post log (all posting tasks)
After every PUBLISHED trial reel, and whenever Instagram returns a limit error, append ONE line to tools/post_log.jsonl
and push (git pull --rebase first):
{"t": "<UTC ISO time>", "src": "drive" | "vlog" | "story" (queue files: story_* = story, vlog_* = vlog), "event": "posted" | "limit" | "error", "permalink": "<url or empty>", "note": "<error text, only for error>"}
