# Blind scoring rubric v4 (second-opinion doc, 17 Nov). The ONLY rubric until 2 Dec 2026 (14 days). Frozen.

The scorer sees ONLY frame 1, the title (on frame 1) and the clip's transcript with timings. It never sees plays, the
story's past results, or which experiment arm the clip is in.

## Step 1 — hard rejects (never post; reject=true)
- A person's NAME in the title or in the first 8 s (spoken or on screen).
- Set ABROAD.
- "Part x", or the clip needs an earlier clip to make sense.
- Shorter than 40 s or longer than 55 s (the clip's video length).

## Step 2 — eight items, 0–2 each (max 16)
| item | 2 | 1 | 0 |
|---|---|---|---|
| T1 whose secret | family or household member, in-law, neighbour | wife, stranger, workplace | girlfriend, fiancée, friend |
| T2 narrator's role | witness | involved, not at fault | does the wrong thing himself |
| T3 tone | light, curious, comic | tense | heavy: illness, death, humiliation, crime, the narrator's own drinking/drugs |
| H1 frame 1 | the title's person mid-act, face visible, ≤2 characters | person visible but passive | room, street, crowd |
| H2 words in 0–3 s | relationship word AND the odd act | one of the two | greeting or setup |
| H3 title | ≤6 words, relationship + concrete act | a question, but generic | reveals the outcome, or >8 words |
| D1 beats | ≥6 new facts/turns, no gap >8 s without one | 4–5 | ≤3 |
| D2 second hook | a new question/reversal lands at 12–18 s | lands later | none |

Total = sum (0–16). Tiers: A ≥12, B 9–11, C ≤8. Ties: T1, then D1.

## Where scores live
`tools/clip_meta.json` → `"<queue file name>": {"story": "<youtube id>", "moment": k, "v4": {"T1":..,"T2":..,"T3":..,"H1":..,
"H2":..,"H3":..,"D1":..,"D2":.., "total": n, "tier": "A|B|C", "reject": false, "reject_why": ""}, "arm": {"build": 0|1,
"ending": 0|1} or null, "exp1_slot": n or null, "length": seconds, "made": "<UTC>"}`.
The poster never posts `reject: true`.

## Blind backtest result (18 Nov 2026) → FALLBACK IN FORCE
62 recoverable posted clips (19 gate passes), scored blind by a separate agent from frame 1 + transcript + length only.
AUC of v4 total vs gate pass = 0.59 (95% bootstrap CI 0.45–0.72), below the 0.70 bar. Per the doc, ranking falls back
to: hard rejects + T1. The poster ranks by `v4.T1` (ties: oldest first). Makers still score and log ALL eight items
(needed for the forward test and the 120-clip refit). Per-item AUCs: T1 0.62, T2 0.67, T3 0.72, H1 0.50, H2 0.49,
H3 0.38, D1 0.39, D2 0.47; T1+T2+T3 0.78 (post hoc, not adopted without Hilal's OK). Details: tools/EXPERIMENT.md.

## Tests it must pass (never change the rubric because of day-to-day results)
- Blind backtest: tools/EXPERIMENT.md "Rubric v4 backtest".
- Forward test, 14 days: with 3 random clips a day in the mix, rank correlation between score and watched % ≥ 0.25 at
  120 clips, and the top-6 pass rate beats the random-3 pass rate.
- Refit at 120 scored and posted clips: fit pass ~ the eight items; keep the items that hold their sign. Never add an item
  from a best-vs-worst comparison.
