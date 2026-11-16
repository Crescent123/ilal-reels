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

## Round 2 (14 Nov) — the opening rule
Round 1 (topic only): day 1 = mean 63K / median 9.6K (pass); day 2 = mean ~6K (fail). Topic filters out losers but doesn't make winners.
Frame-by-frame look at the first 8 s of 51 posted clips (5–13 Nov): forbidden moment in caption 1 + 2nd beat raises the danger
→ median 56K, 73 % 20K+, 55 % 50K+ (n=11) vs median 4–6.5K for everything else (Mann-Whitney p=0.0001). Caveat: coded after
seeing the views, so it must prove itself on clips scored BLIND: on 14 Nov all 77 queued story clips were scored from their
frames at 1.5 s and 6 s without views (9 = both, 8, 7, 6, 5). Judge the 9s and 8s posted 14–16 Nov vs the same bar.

## Verdict on Rounds 1–2 (16 Nov 01:50Z) — FAILED
Same insights pull for every post (lifetime, 16 Nov): Nov 12 mean 64.5K / median 9.6K / 3 of 9 past 20K; Nov 13 mean 7.0K /
median 3.8K / 1 of 9; Nov 14 mean 8.8K / median 1.9K / 2 of 9; Nov 15 (≈5 h old) mean 3.9K / median 2.6K / 0 of 8.
Nov 12–14 together: mean 26.8K / median 4.2K / 22 % past 20K vs baseline 22.6K / 4.2K / 19 % → no real change; Nov 12 was
carried by one 429K clip. Round 2 blind rule-9s (14 Nov): 1.3K, 1.7K, 1.8K, 1.9K, 15.7K — the "forbidden moment + danger"
rule does not hold when scored blind. Round-2 8s did better (28K, 22K, 4.3K, 1.7K).
Live clip test (hangout #5 "flight", 15 Nov 18:02Z): 145 plays at 8 h, 18 % watched, 59 % skip — the podcast-clip format
does not work as a non-follower trial.

## Round 3 (16 Nov) — the curiosity rule
Frames at 0.3/1.5/3/5/8 s of the 8 clips past 15K vs the 8 under 2.1K (12–15 Nov). Winners: title asks what someone CLOSE
is secretly doing, narrator is the witness, that person is on screen in frame 1, playful tone (or a light comic twist).
Losers: narrator's own wrongdoing at risk of being caught, partner betrayal, heavy or sensitive topics. Winners avg 51 %
watched / 28 % skip / 8.6 shares per 1K; losers 34 % / 37 % / 3.6. Small sample (8 vs 8) → this is a hypothesis.
- storyreel/RUNBOOK.md 10a/10b rewritten (9 = family member's secret, narrator witnesses; 6 = narrator's own wrongdoing /
  partner drama; red flags still cap at 5).
- tools/queue_scores.json: 60 queued story clips rescored blind from their 1.5 s frame: 2 nines, 3 eights, 8 sevens,
  27 sixes, 20 fives.
- JUDGE: the 9s/8s/7s posted 16–18 Nov vs the 6s posted alongside them, at the same age (24 h / 72 h). PASS = the 7+ group has
  ≥2x the median and a higher 20K+ rate. Volume, platforms, formats unchanged.
