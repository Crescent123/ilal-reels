# Poster for @ilalstories (second account, Hilal approved 26 Nov 2026)

Follow tools/POSTER.md exactly, with these differences:
- Upload-Post profile: "user": "Stories" (capital S; it holds only @ilalstories on Instagram). Never post to "default" here.
- Runs at :14, :34, :54 Toronto, hours 13–17. FIXED SLOTS 13:14, 13:34, 13:54, 14:14, 14:34, 14:54, 15:14, 15:34, 15:54;
  16:14–17:54 = catch-up only. Daily max = tools/lab_state.json "cap" (lab ramp, see tools/LAB.md), 23 h rolling count, ≥15 min spacing — all counted ONLY over post_log
  lines with "account": "stories".
- Slate: tools/slate/<Toronto date>-stories.json. Build it on the first run of the day AFTER the @_ilal_ slate exists
  (if tools/slate/<date>.json is missing, stop and wait for the next run). Pool = the same eligible story clips as
  POSTER step 2, MINUS every file in today's @_ilal_ slate. Build it as tools/LAB.md says (test clips first, then the rest by ws; max 2 per story).
  Size = tools/lab_state.json "cap" (starts at 9). Slots beyond 9 run 16:14–17:54, one per run. Drive videos (Hilal's own face videos) are NEVER posted here; story clips only.
- Every post is a Trial Reel, never shared to followers, no caption — same as @_ilal_.
- Log in tools/post_log.jsonl with "account": "stories" (and the usual fields + "request_id" from Upload-Post and the
  permalink/shortcode). Main-account lines without "account" mean @_ilal_.
- After it is PUBLISHED: FIRST archive it (28 Nov fix — 3 lab posts lost their archive copy, and an approved lab clip can only
  move to @_ilal_ from the archive): download https://raw.githubusercontent.com/Crescent123/ilal-reels/trial-queue/<file>,
  run `bash tools/posted_add.sh <local mp4> <file>`, confirm the file is listed on branch trial-posted (retry up to 3 times),
  THEN `bash tools/queue_rm.sh <file>` (both posters share the queue). If the archive still fails, keep the file in the
  queue and log "archive_failed" — never remove an unarchived lab clip.
- Lock: use the same poster lock as POSTER.md so the two posters never edit the queue at the same moment.

- 28 Nov: after the test clips, order the rest like POSTER step 2c (ws ≥ 5 filter, winner-list stories first, then random) — ws is not a ranking any more.
