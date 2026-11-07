# Slow caption harvest of @thejakeabdo (Hilal, 7 Nov: "slowly take what we need… who knows he deletes his acc")

Goal: fill "topic" (the reel caption) for every reel in explainer/source_list.json, a little at a time, so future
explainer batches have topics ready. Text only — never download or store his videos. Read-only on Instagram: never
like, follow, comment or message.

## One run (≈100 captions, ~10 min)
1. `git pull` in the repo. Pick the next 100 reels with "topic": null and no "caption_try", highest "views" first.
2. Claude in Chrome: if several browsers are connected pick **Browser 2** (deviceId 132154f2-1868-433a-815c-e08096890da5,
   the Mac signed in to Instagram). tabs_context_mcp → new tab → https://www.instagram.com/ . If Instagram shows the
   login page, stop and report (Hilal must log in himself; never type credentials).
3. In that tab run JavaScript in chunks of ≤8 reels per call (each call must finish < 40 s), ONE request at a time with
   a 3–5 s random pause between requests:
   `const r=await fetch('/reel/'+code+'/'); const h=await r.text();` → status; caption = the `og:title` meta content of
   the parsed HTML, minus the leading "Jake Abdo sur Instagram : " / "Jake Abdo on Instagram: ". Keep results in
   `window.__H` = {code: caption}. If any status is 429 or the HTML has no og:title for 3 reels in a row → stop
   fetching for this run (Instagram is rate-limiting; try again next run).
4. Read the results back as JSON arrays (`JSON.stringify(Object.entries(window.__H))`) — never "code=value" text (the
   tool blocks it as cookie-like). Big results: put them in a <pre> on the page and use get_page_text.
5. Write into source_list.json: "topic" = caption ("" if empty/promo), "caption_try" = today's date (also on failures
   so they aren't retried forever), and "series_90days" = true if the caption matches /Day \d|Stick Figure/.
   For new series reels, add "pick": "use" | "reframe" | "skip" + "couples_angle" (couples-friendly, no hate toward
   women or men; skip pickup/sex tactics) — same style as the existing picks. Re-run `python3 explainer/mark_used.py`.
6. Close your tab. Commit source_list.json ("harvest: +N captions"), pull --rebase, push.
7. When no reel is left with topic null and no caption_try → report "harvest complete" and stop.
Report one line: captions added, remaining, new series reels found.
