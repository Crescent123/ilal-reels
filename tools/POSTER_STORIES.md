# Poster for @ilalstories (second account, Hilal approved 26 Nov 2026)

Follow tools/POSTER.md exactly, with these differences:
- Upload-Post profile: "user": "Stories" (capital S; it holds only @ilalstories on Instagram). Never post to "default" here.
- Runs at :14, :34, :54 Toronto, hours 13–17. FIXED SLOTS 13:14, 13:34, 13:54, 14:14, 14:34, 14:54, 15:14, 15:34, 15:54;
  16:14–17:54 = catch-up only. Same 9 a day max, 23 h rolling count, ≥15 min spacing — all counted ONLY over post_log
  lines with "account": "stories".
- Slate: tools/slate/<Toronto date>-stories.json. Build it on the first run of the day AFTER the @_ilal_ slate exists
  (if tools/slate/<date>.json is missing, stop and wait for the next run). Pool = the same eligible story clips as
  POSTER step 2, MINUS every file in today's @_ilal_ slate. Pick the 9 highest ws (same rules: max 2 per story, ≥3 short
  and ≥3 long when available). Drive videos (Hilal's own face videos) are NEVER posted here; story clips only.
- Every post is a Trial Reel, never shared to followers, no caption — same as @_ilal_.
- Log in tools/post_log.jsonl with "account": "stories" (and the usual fields + "request_id" from Upload-Post and the
  permalink/shortcode). Main-account lines without "account" mean @_ilal_.
- After it is PUBLISHED, remove the queue file with `bash tools/queue_rm.sh <file>` (both posters share the queue).
- Lock: use the same poster lock as POSTER.md so the two posters never edit the queue at the same moment.
