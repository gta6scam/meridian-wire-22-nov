[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/gta6scam/meridian-wire-22-nov/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/gta6scam/meridian-wire-22-nov/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The Meridian Wire — Sunday 22 November 2026

A wire-service front page that fits the whole of Sunday 22 November 2026
into a single 1024×1024 picture — 36 stories, every one of them an event
of that day.

The page is built like a wire front, not a poster. The date itself is the
masthead, set in Playfair Black across the full width of the page, because
the date is the news. Under it run a six-slot UTC timeline, a red numbers
strip whose seven figures each belong to a story on the page (720/9, 2,
12:16, $120bn, M4.1, −18, 11), and a region tally bar that segments all
36 stories by region — Middle East 5 · Oceania 7 · Asia 10 · Europe 2 ·
North America 12 — in the same colours as the card labels, so the count
can be checked at a glance.

Three pictorial lead scenes carry the day, each 128 px tall:

1. **The Gulf overnight** — a radar sweep over Bahrain and one large
   interception explosion filling the strip; IRGC claims (chipped as
   CLAIM) on two Patriot radars, a drone downed over Kuwait's Ali Al
   Salem, and a tanker attacked near Hormuz.
2. **Wellington** — India declare on 720/9, the highest Test total ever
   made in New Zealand, with Rahul 136 and Pant 128.
3. **Vandenberg** — Falcon 9 lifts NROL-136 in the 12:16–12:46 UTC
   window, booster B1097 returning to Landing Zone 4.

Ten more cards cover the Makkah interception, the COP31 final text in
Antalya, the Myanmar M4.1 quake, the Las Vegas Grand Prix, Liverpool v
Manchester United, the ATP Finals title match, the LPGA finale, the
last day of the Kyushu Basho, the rain-moved RSM Classic and NFL
Week 12. Every card carries its own data strip and a tiered certainty
chip — CONFIRMED (2+ major outlets), OFFICIAL (on the record), REPORTED
(1 major outlet) or CLAIM (one-sided claim). A real-polygon world map,
shrunk this round to hand its height to the leads, pins all 13 cards;
23 ALSO ON briefs continue the numbering to 36; and a three-part DATE
CHECK panel names what was left out as not 22 November, what was still
unfinished on the day (the COP31 adoption vote, the Liverpool v Man
United and ATP Turin results), and which claims remain unconfirmed.

## Files

- `draw.py` — the builder. Renders the page and writes `entry.png`.
- `main.py` — the hand-in: copies the committed `entry.png` into
  `MAKEFUN_OUTPUT_DIR` (standard library only).
- `entry.png` — the finished page (palette-compressed).
- `mapdata.py` — real country polygon data used for the map.
- `fonts/` — Archivo Bold/Medium and Playfair Display 900 (OFL).

All drawings are original and procedural (PIL). Facts are drawn only
from reporting of 22 November 2026; contested claims are attributed
as claims on the page itself.
