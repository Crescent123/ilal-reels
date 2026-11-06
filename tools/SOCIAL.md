# Facebook and TikTok posters (public posts) — Hilal, 2 Nov 2026

TWO SEPARATE scheduled tasks (Hilal, 3 Nov: "each its own program"): "TikTok reels" (10:41–20:41 Toronto = 16:41–02:41 Morocco, every 2 h) and
"Facebook reels" (12:53, 15:53, 17:53 Toronto = 18:53, 21:53, 23:53 Morocco; Moroccan evening is prime time). Each posts ONLY its own platform and never stops because of the other
platforms' pauses or errors. Instagram (POSTER.md) is a third, separate program.

Each run: up to TWO TikTok reels (5–10 min apart) and at most ONE Facebook reel. Hilal, 2 Nov: "TikTok you can blast; Facebook start slow and keep analysing it". Quality over count: skip the run on a platform when nothing good is left.
Hilal gave standing approval (2 Nov): pick and post without asking. Report only problems.
Posting tool: Upload-Post, `bash tools/post.sh job.json` (see POSTER.md / tools/post_runner.py). Profile "default".

## Hard rules (both platforms)
- Only story clips (file names `*_story_*`) — never `*_trend_*` (Hilal's face). NEVER Hilal's face (Drive "Reels trial" videos, Q&A, vlogs).
- Never anything gambling-related on TikTok. Never delete anything. The Instagram pause marker (POSTER.md step 1) is for Instagram blocks only and does NOT stop Facebook/TikTok — unless its title mentions "Hilal" (a pause he asked for), then post nothing anywhere.
- QUALITY FILTER (Hilal: "good clips overall, not only views"): look at a frame (ffmpeg at ~1.5 s, read the title text)
  and SKIP anything very weird, gross, sexual, involving minors in romance/marriage/abuse, extreme violence, or
  anything that could embarrass the page. Facebook audience criticises more: be stricter there. When unsure, skip.
  Write skipped files to tools/social_skip.json {"file": "reason"} so they're never reconsidered.
- Never post the same file twice on the same platform (check post_log.jsonl "file" + "platform").

## Speed (5 Nov: a TikTok run hung for 1 h+ and posted nothing)
- Posting runs must NOT page through Instagram insights. For Instagram plays, read tools/ig_plays.json only
  (the health check keeps it fresh). Keep each run short: pick, check one frame, post, log.

## Where clips come from
- trial-posted branch: copies of every reel already posted as an Instagram trial (raw URL:
  https://raw.githubusercontent.com/Crescent123/ilal-reels/trial-posted/<file>). tools/queue_rm.sh adds them automatically.
- trial-queue branch: reels not yet posted on Instagram (`bash tools/queue_list.sh`).
- Instagram views: vidiq_instagram_owner_insights (platformAccountId 28479362468423214), match the post_log line with
  platform instagram/missing + "file" to its permalink shortcode. Older lines without "file": match by time — queue_rm
  removes the file a few seconds BEFORE the log line is written.

## Facebook (published, NOT a trial — everyone sees it)
- PROTECT THE PAGE (Hilal, 4 Nov: "I don't want to lose traction on Facebook; stop if it's not working, even with proven
  clips — it's a big audience"). Facebook is on PROBATION until ~9 Nov. Before each post, read the stats of the earlier
  Facebook reels (analytics action below). STOP posting on Facebook (post nothing, tell Hilal in one line) if, once
  reels are 3+ days old, they average under 20,000 views (Hilal, 4 Nov: "I need minimum 20k views"), or any reel draws clearly negative comments/reactions, or
  Hilal's page reach drops. Never raise the Facebook count without his OK.
- Only clips that were Instagram trials with 20,000+ plays AND pass the quality filter, highest plays first.
  Wait at least 48 h after the Instagram trial before judging its plays.
- Job: {"user":"default","platforms":["facebook"],"video":"<raw url>","title":"<caption>",
        "fields":{"facebook_media_type":"REELS","video_state":"PUBLISHED","facebook_description":"<caption>"}}
- Caption: the clip's top question line in Darija (as shown in the video) + one emoji at most + 
  "القصة كاملة هنا: https://www.youtube.com/watch?v=<ID>" (ID = end of the file name). No hashtags.
- START SLOW: at most 3 Facebook reels a day for now (skip the run once 3 went out today). Facebook reach gets reviewed before raising it.
- If no eligible clip: post nothing (fine).

## TikTok (public)
- Pick from trial-posted (best Instagram plays first, 10K+), then trial-queue score 8 (`_s8_`), then 7.
- Job: {"user":"default","platforms":["tiktok"],"video":"<raw url>","title":"<question line> 😳 القصة كاملة فيوتيوب: ilal Stories",
        "fields":{"privacy_level":"PUBLIC_TO_EVERYONE"}}
- Up to 12 a day (2 per run). If TikTok returns a rate/limit/spam error, stop TikTok for the rest of the day and log it. All 650 old TikToks are "Only me": never change that.

## Log (5 Nov: the WORKFLOW logs now)
Put `"log": {"src":"story","file":"<file>","platform":"<tiktok|facebook>","note":"..."}` inside every job JSON.
The posting workflow appends the post_log line itself when the post finishes (even if your run dies), so you don't
have to wait for the result. "Never the same file twice" = check BOTH post_log.jsonl and post/jobs/*.json (a job
already pushed for that file + platform counts as posted). After pushing a job, wait ~1 min and move on.
Append to tools/post_log.jsonl: {"t","src":"story","event":"posted"|"error","permalink","file","platform":"facebook"|"tiktok","note"}.
The permalink is results[0].post_url in result.json (or status_poll.results). Commit + push after each post.
Any error: log it, don't retry the same item that run. 3 errors in a row on one platform → stop that platform and tell Hilal (SendUserMessage, one line).

## Waiting for results (IMPORTANT — 4 Nov: runs got killed while waiting and never logged their posts)
`tools/post.sh` can wait up to 30 min (Upload-Post sometimes hands a post to its "background" worker). Never let a
shell timeout kill it silently: run it as `bash tools/post.sh job.json` with the longest tool timeout (10 min). It
prints "post job <stamp> submitted" first. If the call times out or ends without a result, run
`bash tools/post_wait.sh <stamp>` (≤8 min each) again until it prints the result. A result with
"handed off ... background" is final only once result.json has status_poll.status "completed": the permalink is
status_poll.results[0].post_url. Log every post (even ones found late) BEFORE starting the next one.

## Stats (read-only)
`{"action":"analytics","request_ids":[...]}` through `bash tools/post.sh` returns Upload-Post per-post metrics
(TikTok: views, likes, shares, avg watch time, new followers; Facebook: views/reactions). Request ids are in
post-out/<stamp>/result.json of each post job. First read (4 Nov): on TikTok the Instagram-proven clips won by far
(R81K… 8.7K views, KjEr… 4.8K) vs ~300–1,100 for unproven ones → TikTok picks proven clips FIRST, then 8s.
