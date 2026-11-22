#!/usr/bin/env python3
"""The Meridian Wire — round 3 REVISION for @yutulboy (News Image 20261122).

Revised in place after the parent's pixel-by-pixel dissection of the
actual #1 entry (BEDAH-TOP1.md), which overrides the earlier board
estimates wherever the two disagree. What the revision does:

  * certainty chips are GONE from every card (the #1 page has zero);
    each card instead carries a D1 slug bar in its region colour —
    white bold caps, PLACE/TOPIC + the card's biggest fact;
  * lead headlines return to ~18 px serif bold (pitch 19), mini
    headlines ~13 px serif bold in two lines, deck-less;
  * lead scenes are ~110 px with subjects >=70% of scene height;
    the redrawn Gulf lead (radar + big explosion) is kept, rescaled;
  * pictured cards rise to 21 (3 leads + 18 minis): eight briefs were
    promoted to deck-less minis with full-bleed ~45 px scenes, so the
    page still totals 36 stories (21 cards + 15 briefs);
  * every scene carries a numbered badge (D ~17 px, bottom-right)
    and the map pins ALL 36 stories by number — no plain dots;
  * a D4 subdeck (italic serif, the three lead headlines joined by
    " . ") sits under the date; the UTC timeline is kept, compressed;
  * briefs use the D5 format: coloured region number badge + bold
    coloured region label + one line + (source), pitch 13 px;
  * the tally stays 16 px with labels inside the segments, widths
    proportional, sum == 36 recounted from cards + briefs;
  * the map is lightened toward the #1 language (pale blue sea, tan
    land) at its shrunken ~205 px height;
  * artwork follows D12: flat vector, one sky gradient, at most three
    large elements per scene, in-scene labels only >=14 px, region
    colours mid-tone.

The three-part DATE CHECK is kept exactly as built (the dissection
calls the fleet's richer, dated DATE CHECK a genuine advantage).
Digits in the numbers strip stay as built. Facts come only from
POOL22-BARU v3. Written fresh for this revision; all artwork is
procedural PIL drawing.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mapdata import WORLD  # noqa: E402

PAGE = 1024
RED = (165, 40, 40)
INK = (24, 22, 18)
CREAM = (247, 242, 232)
CARD_BG = (252, 249, 242)
MUTE = (98, 92, 82)
NAVY = (20, 38, 62)
GOLD = (255, 213, 116)
SEA = (205, 225, 235)
LAND = (222, 205, 180)

FONT_DIR = os.path.join(HERE, "fonts")


def load_font(fname, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, fname), size)


def bold(size):
    return load_font("Archivo-Bold.ttf", size)


def med(size):
    return load_font("Archivo-Medium.ttf", size)


def serif(size):
    return load_font("PlayfairDisplay-900.ttf", size)


# ------------------------------------------------------------------ regions
# Mid-tone region colours in the #1 palette family (BEDAH-TOP1 section 4).
REG_ME = (181, 83, 39)      # Middle East — orange
REG_OC = (78, 128, 45)      # Oceania — green
REG_AS = (156, 46, 90)      # Asia — magenta
REG_EU = (45, 88, 146)      # Europe — blue
REG_NA = (54, 143, 145)     # North America — cyan-teal

# ------------------------------------------------------------------ cards
# slug = PLACE/TOPIC + BIGGEST FACT (D1). src = plain named sources,
# no certainty tiers anywhere on the page.
CARDS = [
    dict(num=1, region="MIDDLE EAST", rc=REG_ME, slug="BAHRAIN: 2 RADARS CLAIMED HIT",
         head="IRGC claims hits on two Bahrain radars",
         deck="Al-Riffa & Awali radars claimed; an industry site ablaze, a drone downed in Kuwait, a tanker hit near Hormuz.",
         src="IRGC statement · Bahrain ministry · UKMTO",
         scene="gulf", cap="1 · BAHRAIN · MIDDLE EAST", lon=50.6, lat=26.2),
    dict(num=2, region="OCEANIA", rc=REG_OC, slug="WELLINGTON: 720/9 DECLARED",
         head="India declare 720/9 — a NZ Test record",
         deck="166 overs: Rahul 136, Pant 128, Gill 98. NZ 368 (Nicholls 175, Bumrah 4-92); India lead by 352.",
         src="IANS · AFP",
         scene="india", cap="2 · WELLINGTON · OCEANIA", lon=174.8, lat=-41.3),
    dict(num=3, region="NORTH AMERICA", rc=REG_NA, slug="VANDENBERG: 12:16 WINDOW",
         head="Falcon 9 lifts NROL-136 Sunday",
         deck="Window 12:16–12:46 UTC, SLC-4E: 15th NRO batch with Northrop Grumman; B1097 returns to LZ4.",
         src="SpaceX · Vandenberg SFB",
         scene="falcon", cap="3 · VANDENBERG · NORTH AMERICA", lon=-120.6, lat=34.7),
    dict(num=4, region="MIDDLE EAST", rc=REG_ME, slug="MAKKAH: MISSILE DOWNED",
         head="Missile downed; sirens 23:43 Riyadh",
         deck="", src="MIDDLE EAST · ANADOLU",
         scene="makkah", lon=39.8, lat=21.4),
    dict(num=5, region="ASIA", rc=REG_AS, slug="ANTALYA: FINAL TEXT TABLED",
         head="COP31 text tabled; plenary 06:00",
         deck="", src="ASIA · REUTERS",
         scene="cop", lon=30.7, lat=36.9),
    dict(num=6, region="ASIA", rc=REG_AS, slug="MYANMAR: M4.1 · 95 KM DEEP",
         head="M4.1 quake, 95 km deep, in Myanmar",
         deck="", src="ASIA · NCS / ANI",
         scene="quake", lon=94.6, lat=24.4),
    dict(num=7, region="NORTH AMERICA", rc=REG_NA, slug="LAS VEGAS: LIGHTS 04:00 UTC",
         head="Vegas GP: 50 laps, lights 04:00 UTC",
         deck="", src="NORTH AMERICA · FORMULA 1",
         scene="vegas", lon=-115.2, lat=36.1),
    dict(num=8, region="EUROPE", rc=REG_EU, slug="ANFIELD: 16:30 UTC",
         head="Liverpool v Man Utd, Anfield 16:30",
         deck="", src="EUROPE · PREMIER LEAGUE",
         scene="prem", lon=-2.96, lat=53.4),
    dict(num=9, region="EUROPE", rc=REG_EU, slug="TURIN: TITLE MATCH",
         head="Alcaraz v Zverev, Turin title match",
         deck="", src="EUROPE · ATP / REUTERS",
         scene="atp", lon=7.7, lat=45.1),
    dict(num=10, region="NORTH AMERICA", rc=REG_NA, slug="NAPLES: KIM −18 LEADS",
         head="Kim −18 leads CME finale by one",
         deck="", src="NORTH AMERICA · LPGA / AP",
         scene="lpga", lon=-81.8, lat=26.1),
    dict(num=11, region="ASIA", rc=REG_AS, slug="FUKUOKA: TWO AT 12-2",
         head="Two at 12-2 into Kyushu final day",
         deck="", src="ASIA · JSA",
         scene="sumo", lon=130.4, lat=33.6),
    dict(num=12, region="NORTH AMERICA", rc=REG_NA, slug="RSM: THREE LEAD AT −9",
         head="RSM round 3 rained to Sunday; −9 leads",
         deck="", src="NORTH AMERICA · REUTERS",
         scene="rsm", lon=-81.4, lat=31.2),
    dict(num=13, region="NORTH AMERICA", rc=REG_NA, slug="NFL: 11 SUNDAY GAMES",
         head="11 NFL games; SNF Vikings @ 49ers",
         deck="", src="NORTH AMERICA · NFL",
         scene="nfl", lon=-98.0, lat=39.0),
    dict(num=14, region="OCEANIA", rc=REG_OC, slug="WELLINGTON: NICHOLLS 175",
         head="Nicholls 175 stands alone in NZ 368",
         deck="", src="OCEANIA · IANS / AFP",
         scene="nicholls", lon=174.8, lat=-41.3),
    dict(num=15, region="OCEANIA", rc=REG_OC, slug="WELLINGTON: BUMRAH 4-92",
         head="Bumrah 4-92 cuts NZ to 368",
         deck="", src="OCEANIA · IANS / AFP",
         scene="bumrah", lon=174.8, lat=-41.3),
    dict(num=16, region="MIDDLE EAST", rc=REG_ME, slug="BAHRAIN: SITE ABLAZE",
         head="Industry site ablaze, Bahrain says",
         deck="", src="MIDDLE EAST · BAHRAIN MINISTRY",
         scene="bahrain", lon=50.6, lat=26.2),
    dict(num=17, region="MIDDLE EAST", rc=REG_ME, slug="HORMUZ: TANKER ATTACKED",
         head="Tanker hit near Hormuz, UKMTO says",
         deck="", src="MIDDLE EAST · UKMTO",
         scene="hormuz", lon=56.3, lat=26.5),
    dict(num=18, region="MIDDLE EAST", rc=REG_ME, slug="KUWAIT: DRONE DOWNED",
         head="Drone downed; first since September",
         deck="", src="MIDDLE EAST · KUWAIT ARMY",
         scene="kuwait", lon=47.9, lat=29.3),
    dict(num=19, region="ASIA", rc=REG_AS, slug="ANTALYA: SHUT 03:00 GMT",
         head="Objections shut 03:00; text tabled",
         deck="", src="ASIA · REUTERS",
         scene="cop2", lon=30.7, lat=36.9),
    dict(num=20, region="NORTH AMERICA", rc=REG_NA, slug="NAPLES: $4M TO WINNER",
         head="$4m CME prize; Kim leads at −18",
         deck="", src="NORTH AMERICA · LPGA / AP",
         scene="cme", lon=-81.8, lat=26.1),
    dict(num=21, region="ASIA", rc=REG_AS, slug="FUKUOKA: YUSHO DECIDERS",
         head="Yusho day: Onosato v Hoshoryu",
         deck="", src="ASIA · JSA",
         scene="yusho", lon=130.4, lat=33.6),
]

# Numbers strip — every figure is bound to a card, noted in brackets.
NUMBERS = [
    ("720/9", "India declared, Wellington (2)"),
    ("2", "Patriot radars claimed hit (1)"),
    ("12:16", "UTC Falcon 9 window opens (3)"),
    ("$120bn", "COP31 target dropped (5)"),
    ("M4.1", "Myanmar quake, 95 km deep (6)"),
    ("−18", "Kim's lead, Naples (10)"),
    ("11", "NFL Sunday games (13)"),
]

TIMELINE = [
    ("OVERNIGHT", "IRGC claims Gulf strikes"),
    ("04:00 UTC", "Las Vegas GP lights out"),
    ("06:00 UTC", "COP31 approval plenary"),
    ("09:00 UTC", "Sumo deciders, Fukuoka"),
    ("12:16 UTC", "Falcon 9 window opens"),
    ("16:30 UTC", "Liverpool v Man United"),
]

# Briefs 22–36 (15) — D5 format data: text, region label, colour,
# source, and the map position of the parent story.
BRIEFS = [
    ("Rahul 136, top score in India's 720/9", "OCEANIA", REG_OC, "IANS", 174.8, -41.3),
    ("Pant 128, second century of the 720/9", "OCEANIA", REG_OC, "IANS", 174.8, -41.3),
    ("Jaiswal 85, a fourth fifty-plus score", "OCEANIA", REG_OC, "IANS", 174.8, -41.3),
    ("Padikkal 80 in the record 720/9", "OCEANIA", REG_OC, "IANS", 174.8, -41.3),
    ("Sunday night: Vikings @ 49ers, 20:20 ET", "N AMERICA", REG_NA, "NFL", -122.0, 37.4),
    ("Thorbjornsen shares RSM lead at −9", "N AMERICA", REG_NA, "Reuters", -81.4, 31.2),
    ("Penge shares the RSM lead at −9", "N AMERICA", REG_NA, "Reuters", -81.4, 31.2),
    ("Neergaard-Petersen shares RSM lead, −9", "N AMERICA", REG_NA, "Reuters", -81.4, 31.2),
    ("Onosato 12-2, joint leader at Fukuoka", "ASIA", REG_AS, "JSA", 130.4, 33.6),
    ("Wakamotoharu 12-2, joint leader", "ASIA", REG_AS, "JSA", 130.4, 33.6),
    ("Atamifuji 11-3, one win back", "ASIA", REG_AS, "JSA", 130.4, 33.6),
    ("Wakamotoharu v Atamifuji, yusho decider", "ASIA", REG_AS, "JSA", 130.4, 33.6),
    ("Thitikul −17, one back at CME finale", "N AMERICA", REG_NA, "AP", -81.8, 26.1),
    ("Yoshida −17, one back at Tiburón", "N AMERICA", REG_NA, "AP", -81.8, 26.1),
    ("COP31 draft recalls Dubai fossil-fuel deal", "ASIA", REG_AS, "Reuters", 30.7, 36.9),
]

# Region tally — recounted from the cards and briefs above:
# cards ME5 OC3 AS5 EU2 NA6 + briefs OC4 AS5 NA6 = ME5 OC7 AS10 EU2 NA12.
TALLY = [
    ("MIDDLE EAST", 5, REG_ME),
    ("OCEANIA", 7, REG_OC),
    ("ASIA", 10, REG_AS),
    ("EUROPE", 2, REG_EU),
    ("N AMERICA", 12, REG_NA),
]

DATE_LEFT_OUT = ("Lviv strike 20 Nov · Peru M6.9 quake 20/21 Nov · Riyadh missiles 21 Nov · "
                 "Hodeidah strike 21 Nov · CEPA signing 21 Nov · France march of 82,500 21 Nov · "
                 "ICJ ruling 19 Nov")
DATE_NOT_YET = ("COP31 final adoption — plenary set for 06:00 GMT, vote pending · "
                "Liverpool v Man Utd result — kickoff 16:30 UTC · "
                "ATP Turin final result — played Sunday evening")
DATE_UNCONFIRMED = ("IRGC claim: 2 Patriot radars destroyed — not independently verified · "
                    "Houthi interception claim near Makkah — coalition account, contested")


# ------------------------------------------------------------------ helpers
def wrap_lines(draw, text, font, max_width):
    out, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def vgrad(draw, box, top, bottom, steps=24):
    x0, y0, x1, y1 = box
    span = y1 - y0
    for i in range(steps):
        a, b = i / steps, (i + 1) / steps
        col = tuple(int(top[k] + (bottom[k] - top[k]) * a) for k in range(3))
        draw.rectangle([x0, y0 + int(span * a), x1, y0 + int(span * b) + 1], fill=col)


def slug_bar(draw, box, text, rc, height, size):
    x0, y0, x1, _ = box
    draw.rectangle([x0, y0, x1, y0 + height], fill=rc)
    f = bold(size)
    draw.text((x0 + 8, y0 + (height - size) // 2 - 1), text, font=f,
              fill=(255, 255, 255))


def badge(draw, x1, y1, num, rc):
    """Numbered badge, diameter ~17 px, bottom-right of a scene (D3)."""
    cx, cy, r = x1 - 12, y1 - 12, 8
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rc,
                 outline=(255, 255, 255), width=2)
    t = str(num)
    tf = bold(9 if num < 10 else 8)
    draw.text((cx - draw.textlength(t, font=tf) / 2, cy - 5), t, font=tf,
              fill=(255, 255, 255))


# ------------------------------------------------------------------ lead scenes (110 px)
def scene_gulf(img, box):
    """Kept redraw: radar sweep + one big interception explosion,
    rescaled to the 110 px strip; burst + rays span ~91% of height."""
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    vgrad(d, box, (30, 66, 132), (74, 112, 168))
    sea_y = y0 + h - 22
    d.polygon([(x0, sea_y + 5), (x0 + int(w * .38), sea_y - 10),
               (x0 + int(w * .52), sea_y + 5), (x0, sea_y + 5)], fill=(30, 40, 34))
    rx, ry = x0 + int(w * .20), sea_y - 10
    d.line([rx, ry, rx, ry - 34], fill=(235, 238, 240), width=5)
    d.arc([rx - 32, ry - 62, rx + 32, ry - 2], 195, 345, fill=(245, 245, 240), width=5)
    d.line([rx, ry - 34, rx + 24, ry - 47], fill=(245, 245, 240), width=4)
    sweep_cx, sweep_cy = rx + 20, ry - 40
    d.polygon([(sweep_cx, sweep_cy), (x0 + int(w * .86), y0 + 2),
               (x0 + int(w * .97), y0 + int(h * .44))], fill=(120, 230, 150, 66))
    for r in (22, 37, 52):
        d.arc([sweep_cx - r, sweep_cy - r, sweep_cx + r, sweep_cy + r],
              -38, 62, fill=(150, 240, 170, 150), width=2)
    for ox, oy in [(int(w * .55), 4), (int(w * .68), 0)]:
        pts = []
        for i in range(21):
            t = i / 20
            pts.append((x0 + ox + (int(w * .78) - ox) * t,
                        y0 + oy + (int(h * .40) - oy) * t + 38 * t * (1 - t)))
        d.line(pts, fill=(255, 176, 70), width=3)
    ex, ey = x0 + int(w * .78), y0 + int(h * .40)
    for k in range(12):
        ang = k * math.pi / 6 + 0.26
        d.line([ex, ey, ex + int(56 * math.cos(ang)), ey + int(50 * math.sin(ang))],
               fill=(255, 140, 36), width=5)
    d.ellipse([ex - 42, ey - 28, ex + 42, ey + 28], fill=(255, 116, 28))
    d.ellipse([ex - 27, ey - 18, ex + 27, ey + 18], fill=(255, 178, 58))
    d.ellipse([ex - 12, ey - 8, ex + 12, ey + 8], fill=(255, 242, 190))
    for k in range(8):
        ang = k * math.pi / 4 + 0.5
        d.line([ex + int(30 * math.cos(ang)), ey + int(20 * math.sin(ang)),
                ex + int(58 * math.cos(ang)), ey + int(52 * math.sin(ang))],
               fill=(255, 120, 30), width=4)
    for dx, dy in [(-30, 10), (24, 26), (8, -30)]:
        d.ellipse([ex + dx - 3, ey + dy - 3, ex + dx + 3, ey + dy + 3], fill=(90, 60, 50))
    for dx, dy in [(-48, -24), (36, -32), (50, 14), (-40, 28), (14, -40), (-16, 38)]:
        d.ellipse([ex + dx - 3, ey + dy - 3, ex + dx + 3, ey + dy + 3], fill=(255, 190, 80))
    d.rectangle([x0, sea_y + 5, x1, y1], fill=(22, 58, 104))
    tx = x0 + int(w * .60)
    d.polygon([(tx, sea_y + 13), (tx + 78, sea_y + 13), (tx + 69, sea_y + 20),
               (tx + 9, sea_y + 20)], fill=(10, 12, 16))
    d.rectangle([tx + 10, sea_y + 5, tx + 47, sea_y + 13], fill=(64, 70, 80))
    d.rectangle([tx + 51, sea_y + 1, tx + 59, sea_y + 13], fill=(44, 48, 56))


def scene_india(img, box):
    """Wellington cricket kept, batsman enlarged to ~73% of height."""
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    vgrad(d, box, (104, 182, 104), (36, 120, 56))
    d.arc([x0 + 6, y0 - 48, x1 - 6, y0 + 62], 0, 180, fill=(238, 242, 238), width=4)
    px0, px1 = x0 + int(w * .38), x0 + int(w * .62)
    d.polygon([(px0, y1), (px0 + 15, y0 + 34), (px1 - 15, y0 + 34), (px1, y1)],
              fill=(219, 199, 148))
    for gx in (px0 + 22, px1 - 26):
        for s in range(3):
            d.line([gx + s * 6, y0 + 44, gx + s * 6, y0 + 62], fill=(252, 242, 200), width=3)
    bx, by = x0 + int(w * .47), y0 + int(h * .58)
    d.ellipse([bx - 9, by - 40, bx + 9, by - 22], fill=(16, 26, 56))
    d.line([bx, by - 22, bx - 5, by + 8], fill=(16, 26, 56), width=8)
    d.line([bx - 5, by + 8, bx - 20, by + 38], fill=(246, 246, 246), width=8)
    d.line([bx - 5, by + 8, bx + 18, by + 36], fill=(246, 246, 246), width=8)
    d.line([bx, by - 18, bx + 28, by - 4], fill=(16, 26, 56), width=6)
    d.line([bx + 25, by - 6, bx + 48, by - 30], fill=(150, 108, 56), width=6)
    d.ellipse([x0 + int(w * .72), y0 + 30, x0 + int(w * .72) + 10, y0 + 40], fill=(196, 28, 38))
    d.text((x0 + 10, y0 + 6), "720/9", font=bold(26), fill=(255, 255, 255))


def scene_falcon(img, box):
    """Falcon 9 kept, rocket enlarged to ~80% of scene height."""
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    vgrad(d, box, (252, 186, 116), (104, 152, 204))
    gy = y0 + h - 20
    d.rectangle([x0, gy, x1, y1], fill=(94, 90, 82))
    tx = x0 + int(w * .18)
    d.rectangle([tx - 6, y0 + 10, tx + 6, gy], fill=(56, 60, 66))
    for i in range(5):
        d.line([tx - 6, y0 + 18 + i * 15, tx + 28, y0 + 26 + i * 15],
               fill=(56, 60, 66), width=3)
    rx, ry = tx + 54, y0 + 8
    d.polygon([(rx - 13, ry + 62), (rx - 13, ry + 16), (rx, ry - 2), (rx + 13, ry + 16),
               (rx + 13, ry + 62)], fill=(248, 248, 248), outline=(38, 40, 48), width=2)
    d.rectangle([rx - 13, ry + 42, rx + 13, ry + 49], fill=(28, 28, 32))
    d.polygon([(rx - 13, ry + 62), (rx - 21, ry + 72), (rx - 13, ry + 72)], fill=(120, 128, 140))
    d.polygon([(rx + 13, ry + 62), (rx + 21, ry + 72), (rx + 13, ry + 72)], fill=(120, 128, 140))
    d.polygon([(rx - 8, ry + 62), (rx + 8, ry + 62), (rx, ry + 88)], fill=(255, 148, 38))
    d.polygon([(rx - 4, ry + 62), (rx + 4, ry + 62), (rx, ry + 76)], fill=(255, 224, 130))
    pts = []
    for i in range(31):
        t = i / 30
        pts.append((rx + (w * .58) * t, ry - 92 * t * (1 - t) + (gy - 8 - ry) * t * t))
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=(255, 238, 175), width=2)
    lz = x0 + int(w * .85)
    d.ellipse([lz - 17, gy - 7, lz + 17, gy + 5], outline=(255, 255, 255), width=3)
    d.text((lz - 15, gy - 28), "LZ4", font=bold(14), fill=(255, 255, 255))


LEAD_SCENES = {"gulf": scene_gulf, "india": scene_india, "falcon": scene_falcon}


# ------------------------------------------------------------------ mini scenes (45 px, full-bleed)
# D12: flat colour field edge-to-edge, 1-3 large elements, labels >=14 px.
def dev_makkah(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (30, 62, 128), (62, 102, 168))
    pts = []
    for i in range(25):
        t = i / 24
        pts.append((x0 + 14 + (x1 - x0 - 60) * t, y0 + 34 - 40 * t * (1 - t) - 8 * t))
    d.line(pts, fill=(255, 176, 70), width=4)
    ex, ey = pts[-1]
    for dx, dy in [(-11, -8), (0, -12), (11, -8), (12, 3), (-12, 3)]:
        d.line([ex, ey, ex + dx, ey + dy], fill=(255, 232, 150), width=3)
    d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 240, 190))
    d.text((x0 + 8, y0 + 4), "01:42", font=bold(15), fill=(255, 255, 255))


def dev_cop(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (20, 118, 78), (36, 148, 96))
    d.rectangle([x0 + 10, y0 + 8, x0 + 52, y0 + 36], fill=(247, 242, 232))
    d.line([x0 + 16, y0 + 16, x0 + 46, y0 + 16], fill=(90, 84, 70), width=3)
    d.line([x0 + 16, y0 + 24, x0 + 40, y0 + 24], fill=(90, 84, 70), width=3)
    d.text((x0 + 62, y0 + 6), "06:00", font=bold(20), fill=(255, 255, 255))
    d.text((x0 + 62, y0 + 27), "PLENARY", font=bold(14), fill=GOLD)


def dev_quake(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (96, 42, 138), (70, 30, 108))
    mid = y0 + 22
    pts, n = [], 40
    for i in range(n):
        t = i / (n - 1)
        amp = 2 + 15 * max(0.0, 1 - abs(t - .34) * 4)
        pts.append((x0 + 6 + 74 * t, mid + (amp if i % 2 else -amp) * .85))
    d.line(pts, fill=(130, 238, 150), width=3)
    d.text((x0 + 88, y0 + 5), "M4.1", font=bold(22), fill=(255, 255, 255))


def dev_vegas(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (86, 30, 124), (54, 20, 88))
    pts = [(x0 + 8, y0 + 32), (x0 + 30, y0 + 32), (x0 + 38, y0 + 10), (x0 + 60, y0 + 10),
           (x0 + 68, y0 + 33), (x0 + 88, y0 + 33), (x0 + 94, y0 + 12)]
    d.line(pts + [pts[0]], fill=(255, 212, 92), width=4)
    d.text((x0 + 104, y0 + 7), "50", font=bold(24), fill=(255, 255, 255))
    d.text((x0 + 104, y0 + 30), "LAPS", font=bold(14), fill=GOLD)


def dev_prem(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (36, 134, 64), (26, 106, 50))
    d.rectangle([x0 + 8, y0 + 6, x0 + 82, y0 + 38], outline=(255, 255, 255), width=3)
    d.line([x0 + 45, y0 + 6, x0 + 45, y0 + 38], fill=(255, 255, 255), width=2)
    d.ellipse([x0 + 39, y0 + 16, x0 + 51, y0 + 28], outline=(255, 255, 255), width=2)
    d.text((x0 + 92, y0 + 5), "16:30", font=bold(19), fill=(255, 255, 255))
    d.text((x0 + 92, y0 + 26), "ANFIELD", font=bold(14), fill=(225, 242, 228))


def dev_atp(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (32, 84, 156), (24, 62, 122))
    d.rectangle([x0 + 8, y0 + 6, x0 + 82, y0 + 38], outline=(255, 255, 255), width=3)
    d.line([x0 + 45, y0 + 6, x0 + 45, y0 + 38], fill=(255, 255, 255), width=2)
    d.line([x0 + 8, y0 + 22, x0 + 82, y0 + 22], fill=(255, 255, 255), width=2)
    d.ellipse([x0 + 104, y0 + 10, x0 + 128, y0 + 34], outline=GOLD, width=4)
    d.line([x0 + 122, y0 + 30, x0 + 140, y0 + 42], fill=GOLD, width=4)


def dev_lpga(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (22, 122, 80), (30, 148, 98))
    d.text((x0 + 8, y0 + 5), "−18", font=bold(30), fill=(255, 255, 255))
    d.line([x0 + 96, y0 + 38, x0 + 96, y0 + 10], fill=(255, 255, 255), width=4)
    d.polygon([(x0 + 96, y0 + 10), (x0 + 122, y0 + 15), (x0 + 96, y0 + 21)], fill=RED)


def dev_sumo(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (204, 138, 62), (186, 118, 48))
    cx, cy = x0 + 26, y0 + 22
    d.ellipse([cx - 20, cy - 15, cx + 20, cy + 15], fill=(216, 178, 120),
              outline=(110, 78, 38), width=4)
    d.text((x0 + 56, y0 + 5), "12-2 · 12-2", font=bold(17), fill=(40, 30, 18))


def dev_rsm(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (16, 108, 98), (24, 132, 118))
    for i in range(3):
        yy = y0 + 8 + i * 11
        d.rectangle([x0 + 10, yy, x0 + 10 + 62, yy + 7],
                    fill=(255, 255, 255) if i == 0 else (170, 226, 205))
    d.text((x0 + 84, y0 + 7), "−9 ×3", font=bold(22), fill=GOLD)


def dev_nfl(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (34, 68, 144), (26, 52, 112))
    for r in range(2):
        for c in range(6):
            cx, cy = x0 + 16 + c * 14, y0 + 13 + r * 15
            idx = r * 6 + c
            d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5],
                      fill=(255, 192, 84) if idx < 11 else (110, 128, 168))
    d.text((x0 + 102, y0 + 6), "11", font=bold(26), fill=(255, 255, 255))
    d.text((x0 + 102, y0 + 30), "GAMES", font=bold(14), fill=GOLD)


def dev_nicholls(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (26, 108, 72), (36, 130, 84))
    d.text((x0 + 8, y0 + 4), "175", font=bold(32), fill=(255, 255, 255))
    for gx in (x0 + 108, x0 + 122, x0 + 136):
        d.line([gx, y0 + 10, gx, y0 + 34], fill=(252, 242, 200), width=4)


def dev_bumrah(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (24, 52, 112), (34, 68, 144))
    d.text((x0 + 8, y0 + 5), "4-92", font=bold(30), fill=(255, 255, 255))
    d.ellipse([x0 + 122, y0 + 10, x0 + 146, y0 + 34], fill=(196, 28, 38))


def dev_bahrain(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (150, 52, 30), (120, 40, 24))
    d.rectangle([x0 + 10, y0 + 24, x0 + 74, y0 + 42], fill=(30, 26, 24))
    d.rectangle([x0 + 82, y0 + 14, x0 + 90, y0 + 42], fill=(30, 26, 24))
    fx, fy = x0 + 40, y0 + 24
    d.polygon([(fx - 13, fy), (fx, fy - 20), (fx + 13, fy)], fill=(255, 116, 28))
    d.polygon([(fx - 6, fy), (fx, fy - 11), (fx + 6, fy)], fill=(255, 200, 80))
    d.text((x0 + 100, y0 + 8), "FIRE", font=bold(18), fill=(255, 255, 255))


def dev_hormuz(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (28, 92, 140), (22, 70, 110))
    ty = y0 + 18
    d.polygon([(x0 + 14, ty + 12), (x0 + 118, ty + 12), (x0 + 106, ty + 22),
               (x0 + 26, ty + 22)], fill=(12, 14, 18))
    d.rectangle([x0 + 26, ty, x0 + 78, ty + 12], fill=(90, 96, 108))
    d.rectangle([x0 + 84, ty - 6, x0 + 94, ty + 12], fill=(60, 64, 74))
    d.arc([x0 + 8, y0 + 30, x0 + 60, y0 + 46], 0, 180, fill=(255, 255, 255), width=3)
    d.arc([x0 + 84, y0 + 30, x0 + 136, y0 + 46], 0, 180, fill=(255, 255, 255), width=3)


def dev_kuwait(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (70, 96, 140), (52, 76, 112))
    cx, cy = x0 + 62, y0 + 20
    d.polygon([(cx - 34, cy), (cx - 8, cy - 7), (cx + 20, cy - 7), (cx + 38, cy + 4),
               (cx + 12, cy + 6), (cx - 16, cy + 6)], fill=(16, 18, 22))
    d.polygon([(cx + 2, cy - 7), (cx + 14, cy - 16), (cx + 22, cy - 7)], fill=(16, 18, 22))
    d.polygon([(x0 + 116, y0 + 6), (x0 + 124, y0 + 20), (x0 + 132, y0 + 6)], fill=(255, 150, 50))
    d.line([x0 + 124, y0 + 20, x0 + 124, y0 + 34], fill=(255, 150, 50), width=4)


def dev_cop2(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (128, 44, 84), (104, 36, 68))
    d.text((x0 + 8, y0 + 5), "03:00", font=bold(28), fill=(255, 255, 255))
    d.rectangle([x0 + 108, y0 + 9, x0 + 142, y0 + 37], outline=(255, 255, 255), width=3)
    d.line([x0 + 114, y0 + 18, x0 + 136, y0 + 18], fill=(255, 255, 255), width=3)
    d.line([x0 + 114, y0 + 27, x0 + 130, y0 + 27], fill=(255, 255, 255), width=3)


def dev_cme(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (140, 108, 30), (116, 88, 24))
    d.text((x0 + 8, y0 + 5), "$4M", font=bold(30), fill=(255, 255, 255))
    d.arc([x0 + 104, y0 + 8, x0 + 146, y0 + 34], 0, 180, fill=GOLD, width=5)
    d.rectangle([x0 + 121, y0 + 30, x0 + 129, y0 + 38], fill=GOLD)


def dev_yusho(d, box):
    x0, y0, x1, y1 = box
    vgrad(d, box, (120, 52, 96), (96, 42, 78))
    cx, cy = x0 + 30, y0 + 22
    d.ellipse([cx - 22, cy - 16, cx + 22, cy + 16], fill=(216, 178, 120),
              outline=(255, 255, 255), width=3)
    d.text((x0 + 62, y0 + 6), "FINAL", font=bold(19), fill=(255, 255, 255))
    d.text((x0 + 62, y0 + 26), "DAY", font=bold(14), fill=GOLD)


DEVICES = {"makkah": dev_makkah, "cop": dev_cop, "quake": dev_quake,
           "vegas": dev_vegas, "prem": dev_prem, "atp": dev_atp,
           "lpga": dev_lpga, "sumo": dev_sumo, "rsm": dev_rsm, "nfl": dev_nfl,
           "nicholls": dev_nicholls, "bumrah": dev_bumrah, "bahrain": dev_bahrain,
           "hormuz": dev_hormuz, "kuwait": dev_kuwait, "cop2": dev_cop2,
           "cme": dev_cme, "yusho": dev_yusho}


# ------------------------------------------------------------------ cards
def frame(img, box, rc):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=CARD_BG)
    d.line([x0, y1, x1, y1], fill=(198, 190, 170), width=1)
    d.line([x0, y0, x0, y1], fill=(216, 208, 190), width=1)
    d.line([x1, y0, x1, y1], fill=(216, 208, 190), width=1)


def lead_card(img, card, box):
    x0, y0, x1, y1 = box
    frame(img, box, card["rc"])
    d = ImageDraw.Draw(img)
    slug_bar(d, (x0, y0, x1, y0), card["slug"], card["rc"], 20, 12)
    sbox = (x0, y0 + 20, x1, y0 + 130)           # 110 px scene
    LEAD_SCENES[card["scene"]](img, sbox)
    d = ImageDraw.Draw(img)
    badge(d, sbox[2], sbox[3], card["num"], card["rc"])
    d.text((x0 + 10, y0 + 134), card["cap"], font=bold(10), fill=card["rc"])
    hy = y0 + 146
    for line in wrap_lines(d, card["head"], serif(18), x1 - x0 - 20)[:2]:
        d.text((x0 + 10, hy), line, font=serif(18), fill=INK)
        hy += 19
    dy = y0 + 185
    for line in wrap_lines(d, card["deck"], med(11), x1 - x0 - 20)[:2]:
        d.text((x0 + 10, dy), line, font=med(11), fill=(52, 48, 42))
        dy += 12
    d.text((x0 + 10, y0 + 209), card["src"], font=med(9), fill=MUTE)


def mini_card(img, card, box):
    x0, y0, x1, y1 = box
    frame(img, box, card["rc"])
    d = ImageDraw.Draw(img)
    slug_bar(d, (x0, y0, x1, y0), card["slug"], card["rc"], 15, 9)
    sbox = (x0, y0 + 15, x1, y0 + 60)            # 45 px full-bleed scene
    DEVICES[card["scene"]](d, sbox)
    d = ImageDraw.Draw(img)
    badge(d, sbox[2], sbox[3], card["num"], card["rc"])
    hy = y0 + 61
    for line in wrap_lines(d, card["head"], serif(13), x1 - x0 - 14)[:2]:
        d.text((x0 + 7, hy), line, font=serif(13), fill=INK)
        hy += 11
    d.text((x0 + 7, y0 + 88), card["src"], font=med(8), fill=MUTE)


# ------------------------------------------------------------------ header
def header(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, PAGE, 18], fill=INK)
    d.text((14, 3), "THE MERIDIAN WIRE · THE WORLD'S NEWS IN ONE PICTURE",
           font=bold(11), fill=(255, 255, 255))
    right = "36 STORIES · 21 CARDS · EVERY ONE DATED TODAY"
    d.text((PAGE - 14 - d.textlength(right, font=bold(11)), 3), right,
           font=bold(11), fill=GOLD)
    # R1: the DATE is the masthead — glyph height and width as built in r2/r3.
    layer = Image.new("RGBA", (2300, 230), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((10, 10), "SUNDAY 22 NOVEMBER 2026",
                               font=serif(118), fill=INK + (255,))
    layer = layer.crop(layer.getbbox())
    glyph_h = layer.height
    layer = layer.resize((952, glyph_h), Image.LANCZOS)
    img.paste(layer, ((PAGE - 952) // 2, 20), layer)
    # D4 subdeck: italic serif, the three lead headlines joined by " . ",
    # sheared for the italic fall, auto-fitted to one line (target ~19 px).
    d = ImageDraw.Draw(img)
    sub = " · ".join(c["head"] for c in CARDS[:3])
    size = 19
    while size > 13 and d.textlength(sub, font=serif(size)) > 980:
        size -= 1
    sub_layer = Image.new("RGBA", (1100, 40), (0, 0, 0, 0))
    ImageDraw.Draw(sub_layer).text((16, 4), sub, font=serif(size), fill=INK + (255,))
    sub_layer = sub_layer.transform(sub_layer.size, Image.AFFINE,
                                    (1, 0.22, -9, 0, 1, 0), resample=Image.BICUBIC)
    sub_layer = sub_layer.crop(sub_layer.getbbox())
    img.paste(sub_layer, ((PAGE - sub_layer.width) // 2, 111), sub_layer)
    d = ImageDraw.Draw(img)
    d.line([14, 131, PAGE - 14, 131], fill=INK, width=2)
    slot_w = (PAGE - 28) // 6
    for i, (when, what) in enumerate(TIMELINE):
        x = 14 + i * slot_w
        if i:
            d.line([x - 5, 137, x - 5, 153], fill=(190, 182, 164), width=1)
        d.text((x, 135), when, font=bold(10), fill=RED)
        d.text((x, 147), what, font=med(8), fill=MUTE)
    d.line([14, 158, PAGE - 14, 158], fill=(190, 182, 164), width=1)
    col_w = (PAGE - 28) // 7
    for i, (big, cap) in enumerate(NUMBERS):
        x = 14 + i * col_w
        if i:
            d.line([x - 6, 164, x - 6, 198], fill=(190, 182, 164), width=1)
        d.text((x, 162), big, font=bold(38), fill=RED)
        d.text((x, 202), cap, font=med(8), fill=MUTE)
    # Region tally — 16 px, labels inside segments, widths proportional.
    total = sum(n for _, n, _ in TALLY)
    assert total == len(CARDS) + len(BRIEFS), "tally must equal story total"
    tx = 14
    for name, count, colour in TALLY:
        seg_w = round((PAGE - 28) * count / total)
        d.rectangle([tx, 214, tx + seg_w - 2, 230], fill=colour)
        label = f"{name} {count}"
        for sz in (9, 8):
            lf = bold(sz)
            if d.textlength(label, font=lf) <= seg_w - 8:
                d.text((tx + 4, 217 if sz == 9 else 218), label, font=lf,
                       fill=(255, 255, 255))
                break
        tx += seg_w
    return glyph_h


# ------------------------------------------------------------------ bottom zone
def all_pins():
    pins = {}
    for c in CARDS:
        pins[c["num"]] = (c["lon"], c["lat"], c["rc"], True)
    for i, (_t, _r, rc, _s, lon, lat) in enumerate(BRIEFS):
        pins[len(CARDS) + 1 + i] = (lon, lat, rc, False)
    return pins


def draw_map(img, box):
    x0, y0, x1, y1 = box
    layer = Image.new("RGB", (x1 - x0, y1 - y0), SEA)
    d = ImageDraw.Draw(layer)
    pw, ph = x1 - x0, y1 - y0
    mx0, my0, mx1, my1 = 8, 6, pw - 8, ph - 22

    def project(lon, lat):
        return (mx0 + (lon + 180) / 360 * (mx1 - mx0),
                my0 + (58 - lat) / 118 * (my1 - my0))

    for _name, rings in WORLD.items():
        for ring in rings.split("|"):
            pts = []
            for pair in ring.split(","):
                lo, la = pair.split(":")
                pts.append(project(float(lo), float(la)))
            if len(pts) > 2:
                d.polygon(pts, fill=LAND)
    # Numbered pins for ALL 36 stories (D3); clustered pins are jittered
    # deterministically by story number so every number stays readable.
    for num, (lon, lat, rc, is_card) in sorted(all_pins().items()):
        jlon = lon + ((num * 7) % 5 - 2) * 1.1
        jlat = lat + ((num * 3) % 5 - 2) * 0.9
        px, py = project(jlon, jlat)
        r = 8 if is_card else 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=rc,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        tf = bold(8 if num >= 10 else 9)
        d.text((px - d.textlength(t, font=tf) / 2, py - 5), t, font=tf,
               fill=(255, 255, 255))
    d.text((8, ph - 18), "All 36 stories pinned by number",
           font=med(10), fill=INK)
    img.paste(layer, (x0, y0))


def bottom_zone(img):
    d = ImageDraw.Draw(img)
    d.text((14, 766), "WHERE IT HAPPENED · ALL 36 STORIES, PINNED BY NUMBER",
           font=bold(11), fill=INK)
    d.text((480, 766), "ALSO ON SUNDAY — 15 MORE STORIES", font=bold(11), fill=INK)
    draw_map(img, (14, 780, 470, 985))           # 456 x 205 panel
    d = ImageDraw.Draw(img)
    yy = 780
    for i, (text, region, rc, source, _lon, _lat) in enumerate(BRIEFS):
        num = len(CARDS) + 1 + i
        cx, cy = 488, yy + 6
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=rc)
        t = str(num)
        tf = bold(7)
        d.text((cx - d.textlength(t, font=tf) / 2, cy - 4), t, font=tf,
               fill=(255, 255, 255))
        x = 502
        d.text((x, yy + 1), region, font=bold(9), fill=rc)
        x += d.textlength(region, font=bold(9)) + 6
        body = f"{text} ({source})"
        d.text((x, yy), body, font=med(10), fill=(52, 48, 42))
        yy += 13
    # DATE CHECK — three parts, kept as built; no chip legend (chips gone).
    d.rectangle([14, 989, 1010, 1022], outline=RED, width=2)
    rows = [
        ("DATE CHECK · LEFT OUT", DATE_LEFT_OUT),
        ("NOT YET", DATE_NOT_YET),
        ("UNCONFIRMED", DATE_UNCONFIRMED),
    ]
    ry = 992.0
    for label, body in rows:
        d.text((24, ry), label, font=bold(9), fill=RED)
        lw = d.textlength(label, font=bold(9))
        d.text((24 + lw + 8, ry), "— " + body, font=med(9), fill=(52, 48, 42))
        ry += 10.5


# ------------------------------------------------------------------ compose
def compose():
    img = Image.new("RGB", (PAGE, PAGE), CREAM)
    glyph_h = header(img)
    lead_w = (PAGE - 28 - 16) // 3
    for i, card in enumerate(CARDS[:3]):
        x = 14 + i * (lead_w + 8)
        lead_card(img, card, (x, 236, x + lead_w, 236 + 218))
    d = ImageDraw.Draw(img)
    d.text((14, 458), "MORE FROM SUNDAY · STORIES 4–21", font=bold(11), fill=RED)
    mini_w = (PAGE - 28 - 40) // 6
    for r in range(3):
        for c in range(6):
            card = CARDS[3 + r * 6 + c]
            x = 14 + c * (mini_w + 8)
            y = 472 + r * 98
            mini_card(img, card, (x, y, x + mini_w, y + 96))
    bottom_zone(img)
    return img, glyph_h


def save_page(img, path):
    q = img.quantize(colors=256, method=Image.MEDIANCUT)
    q.save(path, optimize=True)
    if os.path.getsize(path) > 165_000:
        q = img.quantize(colors=192, method=Image.MEDIANCUT)
        q.save(path, optimize=True)
    return os.path.getsize(path)


def build(outdir=None):
    outdir = outdir or HERE
    img, glyph_h = compose()
    size = save_page(img, os.path.join(outdir, "entry.png"))
    img.resize((300, 300), Image.LANCZOS).save(os.path.join(outdir, "entry-300.png"))
    probe = ImageDraw.Draw(img)
    problems = []
    for card in CARDS[:3]:
        n = len(wrap_lines(probe, card["head"], serif(18), 306))
        m = len(wrap_lines(probe, card["deck"], med(11), 306))
        print(f"lead {card['num']} headline lines={n} deck lines={m}")
        if n > 2 or m > 2:
            problems.append(card["num"])
    for card in CARDS[3:]:
        n = len(wrap_lines(probe, card["head"], serif(13), 145))
        print(f"mini {card['num']} headline lines={n}")
        if n > 2:
            problems.append(card["num"])
    for i, (text, region, _rc, source, _lo, _la) in enumerate(BRIEFS):
        w = (d_w := probe.textlength(region, font=bold(9)) + 6
             + probe.textlength(f"{text} ({source})", font=med(10)))
        print(f"brief {len(CARDS) + 1 + i} width={w:.0f}")
        if 502 + w > 1012:
            problems.append(f"brief{len(CARDS) + 1 + i}")
    print(f"entry_bytes={size} masthead_glyph_h={glyph_h} "
          f"stories={len(CARDS) + len(BRIEFS)} pictured={len(CARDS)} "
          f"tally_sum={sum(n for _, n, _ in TALLY)} problems={problems}")
    return size


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else None)
