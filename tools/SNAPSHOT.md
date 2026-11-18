# Snapshot task runbook (measurement fix, second-opinion doc, 17 Nov)
Every Instagram post is measured at FIXED AGES: 3 h, 24 h, 72 h and 7 days (168 h). Retention (watched %, skip %) is read
at 24 h, plays at 72 h. Never compare clips of different ages. Also log the follower count once a day.

Runs hourly at :52. One run:
1. `git pull`. Read tools/post_log.jsonl: Instagram "posted" lines of the last 8 days (permalink → shortcode).
2. Read tools/snapshots.jsonl (one line per snapshot: {"sc","file","posted","target_h","age_h","taken","plays","watch",
   "skip","shares","saves","likes","comments","dur","pos","pick","v4","arm"}). For each post, the targets 3/24/72/168 h
   whose age has been reached and that have no line yet are DUE. Take a due snapshot only if the post's age is within
   +2 h of the target for 3 h, +3 h for 24 h, +6 h for 72 h, +12 h for 168 h; if it is later than that, still take it
   but add "late": true.
3. Fetch only what is due: vidiq_instagram_owner_insights (platformAccountId 28479362468423214, mode "reels",
   limit 25, since = the post's publish date, until = the next day) for each publish date that has a due post; match by
   shortcode. Append one line per due snapshot (copy pos/pick/v4/arm from the post_log line; story ID and moment are
   in tools/clip_meta.json under the file name).
4. Once per Toronto day (first run after 12:00 Toronto, if tools/followers.jsonl has no line for today): append
   {"date": "<Toronto date>", "t": UTC, "followers": followersCount from the same insights call}.
5. Commit + push (`git pull --rebase` first, retry on conflict). Nothing due → no commit. Never message Hilal from this
   task unless vidIQ is down for 6 runs in a row (then one line).

## Winners stock (tools/WINNERS.md)
Every run: any trial whose plays in a snapshot or insights reach 400K+ → add/update it in tools/winners.json as a
"candidate" (ig_plays, sc, file from post_log, src). Once a day, for candidates at least 7 days past a TikTok post,
read TikTok views (vidIQ) and apply WINNERS.md rule 2; mark "approved" or keep "candidate". When the number of
"approved" first reaches 5, send Hilal one line with the list and the planned public start date.
