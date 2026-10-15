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
1. Read the marker title (Google Drive get_file_metadata). If paused and that time is in the future, stop.
2. Build the list: Drive folder video files (search parentId = folder, not trashed; ignore non-video files) with their
   createdTime, plus queue B items with time = the unix prefix. Sort oldest first. Nothing → stop.
3. Post at most 6 items this run. Between two posts wait a random 4–9 minutes (sleep in chunks ≤ 9 min).
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
   Any other error on an item: skip that item this run (leave it), continue with the next.
5. If the run published at least one reel and the marker said paused (time passed), rename it back to
   "reels-trial-state: active".
6. End with one line: how many posted from Drive, how many from the vlog queue, how many still waiting.

## Post log (all posting tasks)
After every PUBLISHED trial reel, and whenever Instagram returns a limit error, append ONE line to tools/post_log.jsonl
and push (git pull --rebase first):
{"t": "<UTC ISO time>", "src": "drive" | "vlog" | "story" (queue files: story_* = story, vlog_* = vlog), "event": "posted" | "limit", "permalink": "<url or empty>"}
