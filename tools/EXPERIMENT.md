# Story-clip formula test (Hilal, 11 Nov evening)
Goal: an AVERAGE of 50–100K views per Instagram trial clip. Slots are limited (9 IG trials/day), so every slot must go to
the best formula. Run 12–14 Nov (3 posting days), then learn and change the rules if it doesn't work.

## Hypothesis (fixed BEFORE the test — don't move the goalposts)
From all 149 story reels 14 Oct–9 Nov (week-controlled): family stories = 1.8x views; red flags (character name in hook,
set abroad, crime/violence, money/scam core, "PART x") = 0.43x. Question marks and cheating did NOT matter.
Baseline: all story clips mean 22.6K / median 4.2K / 11% 50K+ / 19% 20K+. Clean family: mean 71K / median 20K / 50% 20K+.

## What changed
- tools/queue_scores.json: 13 family/neighbor clips = 9 (post first; 5 wife clips first marked 9 were set back to 7 — wife stories show no edge), 23 red-flag clips = 5 (held, never delete).
- storyreel/RUNBOOK.md 10b: new hook scoring (family +2, wife/neighbor +1, gf/fiancée −1, any red flag caps at 5).
- Volume, platforms, formats: unchanged.

## How to judge (same age, same platform)
- Compare each test clip at 24h / 48h / 72h with the clips posted 9–11 Nov (old rules) at the SAME age. Pull both with
  vidiq_instagram_owner_insights (reels mode, free) at each check and append one line per clip to tools/experiment_log.jsonl:
  {"check": "<UTC>", "sc": shortcode, "posted": UTC, "age_h": n, "group": "test"|"before", "plays", "watch", "skip"}.
- PASS: test clips at 72h have mean ≥ 50K, or clearly beat the before group at the same age (≥2x median AND higher 20K+ rate).
- FAIL: no clear gap → the rules are wrong. Then re-tag the test clips + before clips, find what separates the
  winners (watch% / skip% first, then topic / first frame / first sentence), rewrite RUNBOOK 10b + rescore the queue,
  and tell Hilal plainly what failed and what changes.
- Watch% and skip% move before views do: report them too (≥50% watched / ≤28% skip = the clips that get pushed).
