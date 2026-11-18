# Approved winners → public posts (Hilal, 18 Nov 2026)

Nothing is shared to followers until there is a good stock of APPROVED WINNERS. Hilal's rule:

A clip is an APPROVED WINNER when BOTH hold:
1. As an Instagram trial it reached **400K+ plays** (any snapshot, or insights at any age), AND
2. it proved itself a second time: **either** it outperformed on TikTok (views ≥ 3x the median of our TikTok story
   posts from the same 7 days, and at least 50K), **or** it was reposted as a new Instagram trial and that repost
   ALSO reached 400K+.

tools/winners.json = {"candidates": {<file or shortcode>: {"ig_plays":n, "sc":.., "tiktok": {"permalink":..,"views":n,
"median7d":n} | null, "repost": {"sc":..,"plays":n} | null, "status": "candidate|approved|failed", "src":"story|drive"}}}
- The snapshot task adds every trial that passes 400K as a "candidate" and keeps ig_plays updated.
- TikTok check: if the candidate's file was not on TikTok yet, it is eligible for TikTok (story clips only; drive videos only
  if Hilal OKs). Read TikTok views with vidIQ (vidiq_tiktok_profile_videos, @_ilal_) after 7 days.
- Repost test: the poster may use 1 of the 9 daily slots for a repost test (pick "repost", from 25 Nov, never during
  Experiment 1). The file must still exist (trial-queue/trial-posted branch, or Drive).
- Status approved → counts toward the stock. Failed both second chances → "failed".

STOCK READY = 5 approved winners. When the stock first reaches 5, message Hilal (one line, with the list). Public
posting starts only then (up to 2 a day, each with a linked part 2, per the second-opinion doc) — say the start date in
that message so he can say wait. Until then: no trial is ever shared to followers.

Seed (from insights Oct 14–Nov 10, trials ≥400K): DekNY5tCqsN 2.11M (drive), De2oYp5DwHn 539K (drive),
Derd7LnERcu 462K (story), Denn0haj_rH 444K (story), DfSPBSyjk_7 425K (drive). None on TikTok yet; no repost yet.
