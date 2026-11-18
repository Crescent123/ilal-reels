# Trial-reel poster runbook (one run = at most one post from the day's slate; runs at :04/:24/:44)

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
   every run posts AT MOST ONE item from today's slate, 20+ minutes after the previous post (step 3 SPACING).
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
2. DAILY SLATE (second-opinion doc, 17 Nov; rubric v4 frozen until 2 Dec — tools/RUBRIC_V4.md). The day's posts are
   fixed ONCE per Toronto day in tools/slate/<YYYY-MM-DD>.json; later runs only post from it.
   If today's slate file does not exist yet, build it (then commit + push it before posting):
   a. ELIGIBLE queue B items: *_story_* files only (see INSTAGRAM MIX), not in tools/social_skip.json, with an entry in
      tools/clip_meta.json whose v4.reject is false and whose length is 40–55 s. HARD REJECTS are never posted, whatever
      their score: name in title/first 8 s, abroad, part x, outside 40–55 s. Files without a clip_meta entry are not
      eligible (the health check scores them). Drive folder videos (Hilal's own drops) stay eligible as before and are
      added on top as pick "drive" (they count toward the 9 but not toward the 6/3).
   b. POOL: during Experiment 1 (tools/exp1.json: until 63 slot files have been posted, 18–24 Nov) the pool is the
      eligible Exp1 clips (clip_meta "arm" not null). If fewer than 9 − (drive items) Exp1 clips are eligible, add the
      other eligible clips to the pool.
   c. PICK (18 Nov, Hilal approved: hard rejects + STORY SCORE = v4.T1+T2+T3, the items that held up in the blind backtest, see tools/RUBRIC_V4.md): the 6 highest story scores in the pool (ties: T1, then oldest) = pick "top6"; then 3 drawn uniformly at
      random from the REST of the pool = pick "random3", using python `random.Random("<date>")`. Fewer available → take
      what there is (top first). Never swap a random pick for a better one: the 3 random slots are the control group.
   d. ORDER: shuffle the day's list with `random.Random("<date>-order")`; store
      {"date":..,"built":UTC,"items":[{"pos":1,"file":..,"pick":"top6|random3|drive","v4":total,"story":T1+T2+T3,"arm":{..}|null}, ...]}.
   No slate item eligible → stop.
2e. REPOST TESTS (from 25 Nov, after Experiment 1): at most 1 of the 9 slots a day may be a repost test from
   tools/winners.json (see tools/WINNERS.md), pick "repost". Never during Experiment 1.
3. PACING (Instagram blocks the account when too many go out at once: 21 Oct after a burst, 22 Oct after 12 posts in
   2 h). INSTAGRAM MIX (Hilal, 9 Nov evening — replaces every earlier explainer/trend rule): Instagram trials are STORY CLIPS ONLY (queue *_story_* files, plus videos Hilal himself puts in the Drive "Reels trial" folder). NEVER post *_explainer_* files on Instagram (21 tested: median ~2K vs ~9K for story clips; they stay on TikTok via the TikTok task). NEVER post *_trend_* files (or any other non-story queue file) on Instagram unless Hilal approves that file in chat. SKIP LIST: never post a queue file listed in tools/social_skip.json (clips Hilal/Claude judged too weird for any platform). ROLLING LIMIT (4 Nov: blocks came at ~10–11 Instagram posts in any 24 h, e.g. 5 on Nov 4 right after 11 on Nov 3): also count Instagram "posted" lines in the LAST 23 HOURS; if that is 9 or more, stop. (18 Nov: 23 h, not 24 h, so yesterday's post in the same slot has always dropped out and the schedule never drifts later; with the FIXED DAILY SLOTS below that still means at most 9 in any 24 h, the same pace that ran clean 5–16 Nov.) Count "posted" lines in tools/post_log.jsonl from TODAY (Toronto date) whose "platform" is "instagram" or missing (Facebook / TikTok lines never count): if cap or more (tools/post_cap.json), stop.
   SPACING (second-opinion doc): post AT MOST ONE item per run — the lowest-"pos" slate item not yet posted — and only if
   the last Instagram "posted" line is at least 20 minutes old (else stop). Runs are scheduled at :04, :24 and :44, so the
   day's 9 go out 20 minutes apart in the slate's random order.
   FIXED DAILY SLOTS (18 Nov, Hilal: "it's not good to be blocked"): the 9 posts go out at the SAME times every day —
   13:04, 13:24, 13:44, 14:04, 14:24, 14:44, 15:04, 15:24, 15:44 Toronto — so each day's posts sit exactly where
   yesterday's did and the 24 h count never piles up. Runs from 16:04 to 17:44 are CATCH-UP ONLY: they post only if a
   slot was missed earlier today (error, missing file) and the rolling limit allows it. Never post outside 13:00–17:59.
   Never post two in one run, never make up missed slots by bunching. If the rolling limit stops a slot, wait for the
   next run; don't retry within the same run. If an item fails or vanished, mark it "skipped" in the
   slate (with the reason) and the next run takes the next one. Commit/push the log after the post.
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
Since 18 Nov also add to every Instagram "posted" line: "pos": <slate position 1–9>, "pick": "top6"|"random3"|"drive",
"v4": <total or null>, "arm": {"build":0|1,"ending":0|1} or null (from the slate). The snapshot task (tools/SNAPSHOT.md)
reads these.

## Waiting for results (IMPORTANT — 4 Nov: runs got killed while waiting and never logged their posts)
`tools/post.sh` can wait up to 30 min (Upload-Post sometimes hands a post to its "background" worker). Never let a
shell timeout kill it silently: run it as `bash tools/post.sh job.json` with the longest tool timeout (10 min). It
prints "post job <stamp> submitted" first. If the call times out or ends without a result, run
`bash tools/post_wait.sh <stamp>` (≤8 min each) again until it prints the result. A result with
"handed off ... background" is final only once result.json has status_poll.status "completed": the permalink is
status_poll.results[0].post_url. Log every post (even ones found late) BEFORE starting the next one.
