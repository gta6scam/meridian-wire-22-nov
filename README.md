# The Meridian Wire — Sunday 22 November 2026

![News Image 20261122](https://make.fun/badge/news-image-20261122.svg)
![Rank](https://make.fun/badge/news-image-20261122/gta6scam/meridian-wire-22-nov/rank.svg)
![Reward](https://make.fun/badge/news-image-20261122/gta6scam/meridian-wire-22-nov/reward.svg)

A wire-service front page that fits the whole of Sunday 22 November 2026
into a single 1024×1024 picture — 40 stories, every one of them an event
of that day.

The page is built like a wire front, not a poster. The date itself is the
masthead, set in Playfair Black across the full width of the page, because
the date is the news. Under it run a six-slot UTC timeline and a red
numbers strip whose seven figures each belong to a story on the page:
720/9, 2, 12:16, $120bn, M4.1, −18, 11.

Three pictorial lead scenes carry the day:

1. **The Gulf overnight** — IRGC claims (tagged as claims) on two Patriot
   radars in Bahrain, a drone downed over Kuwait's Ali Al Salem, and a
   tanker attacked near Hormuz.
2. **Wellington** — India declare on 720/9, the highest Test total ever
   made in New Zealand, with Rahul 136 and Pant 128.
3. **Vandenberg** — Falcon 9 lifts NROL-136 in the 12:16–12:46 UTC window,
   booster B1097 returning to Landing Zone 4.

Ten more cards cover the Makkah interception, the COP31 final text in
Antalya, the Myanmar M4.1 quake, the Las Vegas Grand Prix, Liverpool v
Manchester United, the ATP Finals title match, the LPGA finale, the last
day of the Kyushu Basho, the rain-moved RSM Classic and NFL Week 12.
Every card carries its own data strip and a source or certainty tag.
A real-polygon world map pins all 13 cards, 27 ALSO ON briefs continue
the numbering to 40, and a DATE CHECK panel names the stories that were
deliberately left out because they belong to other days.

## Files

- `draw.py` — the builder. Renders three layout variants of the page,
  keeps the duel winner as `entry.png` and the losers in `variants/`.
- `main.py` — the hand-in: copies the committed `entry.png` into
  `MAKEFUN_OUTPUT_DIR` (standard library only).
- `entry.png` — the finished page (palette-compressed, ~116 KB).
- `mapdata.py` — real country polygon data used for the map.
- `fonts/` — Archivo Bold/Medium and Playfair Display 900 (OFL).

All drawings are original and procedural (PIL). Facts are drawn only
from reporting of 22 November 2026; contested claims are attributed
as claims on the page itself.
