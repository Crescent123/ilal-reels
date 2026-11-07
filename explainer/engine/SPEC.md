# ep.json format (engine/anim.html)
{"slug","title" (short Darija, shown on top),"source","source_topic",
 "phrases":[{"t":"spoken + caption text","v":{beat}} ...]}

Captions = the "t" of each phrase (auto-split in 2 if > 24 chars). Hidden on layouts text/cta.

## Persistent beat fields (stay until changed)
- L: layout — couple (default) | apart | close (hug distance) | solo_w | solo_r | split (divider, small figures) |
  text (no captions, small figures, big words) | cta (end question) | list (figures on the sides, items stack in the middle)
- w / r: pose of the white man / red woman, space-separated words:
  arm: down up reach hug point cross chest lift wave head(hands on head)
  face/flags: smile sad angry shock tear walk nod shake away(turned away) small fade hide
- fx (continuous): hearts bolts snow rain q(question marks) zzz coins confetti sparks glow(ring on white) wall rope ; "" = none
## One-phrase fields (pop at the phrase start)
- top: ["text","color"]  line at y 480
- mid: ["emoji","label",size]  big emoji at the centre (y 600) + label
- bw / br: bubble over white / red ("text")
- sl / sr: labels left / right (split) ["text","color"]
- m: ["label",from,to,"color"] animated meter at the bottom (y 1185)
- x: true (red X) · ck: true (green check) · burst: "r"|"w" (heart burst) · broken: true (heart breaks)
- big: [["text","color",size,delay]...] stacked big lines (by = first y, default 600; gap default 150) — for text/cta
- item: "text" (list layout: adds a line that stays)
- cta: "small grey line at y 1260"
Colors: w r p(pink) g(gold) b(blue) gr(green) grey or any #hex.
Tips: keep top/big text ≤ ~22 characters; bubbles ≤ ~26; emoji labels ≤ 2–3 words. Use split for "X vs Y",
list for "3 signs / 3 rules", text for the punchline, cta last.
