# @ilalstories = the LAB for @_ilal_ (Hilal, 26 Nov 2026: "use this account to help the main account — testing, approving,
# posting the rest, pushing limits — with a self-learning loop on both, connected").

## Roles
1. TEST: anything unproven goes to @ilalstories first — new topics, new moment types, new title styles, lengths, new
   stories (first clip of a story never seen on either account). @_ilal_ only gets proven types + winner-story clips.
2. APPROVE: a clip that reaches ≥15K plays at 24 h on @ilalstories (or top 2 of its day) is APPROVED:
   - its story goes on the winner list (RUNBOOK "COPY THE WINNERS") → the makers dig it for @_ilal_;
   - its pattern/hypothesis gets a +1 win in tools/HYPOTHESES.md;
   - the clip itself may go to @_ilal_ as 1 slot a day ("pick": "approved"), never earlier than 48 h after its lab post.
3. THE REST: clips not in @_ilal_'s 9 fill @ilalstories (after the day's test clips).
4. PUSH LIMITS: @ilalstories probes Instagram's daily cap so @_ilal_ never has to. Ramp: 9 a day now; +1 every 3 clean
   days (no block, no "limit" error, no reach crash = median 3 h plays not below half of the previous 3 days). At the first
   block: log it, drop back 2 and hold 7 days. Current cap lives in tools/lab_state.json {"cap":9,"clean_days":0,
   "last_block":null}. When the lab holds a cap ≥ N+2 cleanly for 7 days, @_ilal_ may go up by 1 (from 9) — the daily
   learning check decides and logs it. Extra lab slots run 16:14–17:54 (one per run, 20 min apart).

## Daily lab slate (tools/slate/<date>-stories.json), built after @_ilal_'s slate
- First: TEST clips — clip_meta entries whose "test" names an ACTIVE hypothesis in tools/HYPOTHESES.md (up to 6).
- Then: approved-candidate re-checks are NOT re-posted here (no duplicates on the same account).
- Then: the rest by ws (max 2 per story). Never Hilal's face videos. Never a file already posted on either account,
  except an "approved" clip moving lab → main.

## Self-learning loop (both accounts, connected) — run by the daily learning check (21:45 Toronto)
analyze both accounts → update tools/HYPOTHESES.md (evidence per hypothesis) → decide only with enough data
(≥15 clips or 2 days in a row, or a clear effect) → apply (RUNBOOK / POSTER / ws / lab cap) → log in tools/LEARNINGS.md
→ queue new hypotheses as lab tests (status "active", the makers tag clips for them) → repeat.
Never re-test a hypothesis marked "kept" or "dropped" unless the ledger says why (stops us circling back).
