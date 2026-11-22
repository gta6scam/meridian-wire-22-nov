#!/usr/bin/env python3
"""THE MERIDIAN WIRE - Sunday 22 November 2026 in one page.

Compose program for the make.fun news-image-20261122 entry (account 1,
@yutulboy). Draws a 1024x1024 front page (entry.png, next to this file)
with Pillow only: flat layered shapes, a real-polygon world map, and a
sourced card for every pictured story. Deterministic: no randomness,
no clocks, no network. Facts were re-verified against the wires on
22 Nov: the morning digest pool had misdated most of its items, so
only wire-confirmed Sunday stories appear as cards; every older item
is named in DATE CHECK with its true date.

Revision note: the data sections below (cards, briefs, figures,
timeline) were restructured by the reviser session into a single
dict-based card table plus zipped parallel lists. Storage shape only -
every fact, headline and number on the page is unchanged.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mapdata import WORLD  # noqa: E402

FONT_DIR = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MX = 16                      # page margin
CW = W - 2 * MX              # content width = 992

PAPER = (247, 241, 227)      # cream #F7F1E3
CARD_BG = (253, 250, 242)
INK = (20, 33, 61)           # navy #14213D
RED = (176, 58, 46)          # accent #B03A2E
NAVY = (22, 40, 63)          # caption band / map sea #16283F
LAND = (104, 124, 98)
GREY = (90, 86, 76)
FAINT = (203, 192, 164)
WHITE = (255, 255, 255)

REGION_RGB = {
    "EUROPE": (176, 58, 46),
    "ASIA": (29, 111, 184),
    "MIDEAST": (125, 60, 152),
    "AFRICA": (30, 132, 73),
    "AMERICAS": (202, 111, 30),
    "OCEANIA": (20, 143, 119),
    "GLOBAL": (93, 109, 126),
    "SPORT": (178, 124, 20),
}

SERIF = "PlayfairDisplay-900.ttf"
SANSB = "Archivo-Bold.ttf"
SANSM = "Archivo-Medium.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

_cache = {}


def F(name, size):
    key = (name, int(size))
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), int(size))
    return _cache[key]


def tw(text, font):
    return d.textlength(text, font=font)


def fit_size(text, name, start, target_w, floor=10):
    """Largest size <= start at which text fits target_w."""
    s = start
    while s > floor and tw(text, F(name, s)) > target_w:
        s -= 1
    return s


def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_in(x, y, text, font, fill, anchor="la"):
    d.text((x, y), text, font=font, fill=fill, anchor=anchor)


def centre(x0, x1, y, text, font, fill):
    d.text(((x0 + x1) / 2, y), text, font=font, fill=fill, anchor="ma")


# ----------------------------------------------------------------- data
# FACT STATE (re-verified against the wires 22 Nov, pool v3): the
# morning digest pool misdated most of its items. Every card and brief
# on this page is a 22 Nov event with a wire timestamp; every older
# story is named in DATE CHECK with its true date - never dressed fresh.
#
# Storage shape (reviser's layout): all ten pictured stories live in
# ONE table, CARDS, built by the _card() helper as dicts with named
# fields. The drawing code consumes plain tuples, so _tuples() adapts
# the table: the first three rows become LEADS, the other seven MINIS.
# Briefs are bare lines, numbered by enumerate from 11. The figures
# strip and the timeline are zipped from parallel lists. Facts are
# identical to the previous build; only how they are kept has changed.

def _card(n, region, tag, head, deck, caption, chip):
    return {"n": n, "region": region, "tag": tag, "head": head,
            "deck": deck, "caption": caption, "chip": chip}


CARDS = [
    _card(1, "MIDEAST", "REUTERS",
          "IRAN STRIKES US BASES ACROSS THE GULF",
          "IRGC claims joint missile-and-drone strikes on 2 US Patriot "
          "radar sites. A Bahrain industrial plant burns; drones at "
          "Kuwait's Ali Al Salem are downed - the first since September.",
          "BAHRAIN - KUWAIT - THE GULF", "2 RADARS HIT"),
    _card(2, "GLOBAL", "REUTERS",
          "COP31: FINAL TEXT TABLED IN ANTALYA",
          "President Kurum tables the final package after Friday's "
          "suspended close: objections shut at 03:00 GMT and the "
          "approval plenary sits at 06:00 GMT Sunday.",
          "ANTALYA - CLIMATE SUMMIT", "06:00 GMT VOTE"),
    _card(3, "MIDEAST", "REUTERS",
          "TANKERS HIT OFF OMAN AS CLASH WIDENS",
          "Tankers are struck off Oman and Iran's Qeshm island sits "
          "inside the clash zone, as the Gulf fighting jumps from bases "
          "to the sea lanes the world's oil moves through.",
          "OMAN - QESHM - THE STRAIT", "SEA LANES HIT"),
    _card(4, "ASIA", "NCS",
          "M4.1 QUAKE WAKES MYANMAR",
          "The NCS logs a magnitude-4.1 quake at 02:35 IST, 95 km down "
          "at 24.4N, 94.6E by the India border. No damage reported.",
          "MYANMAR - NCS LOG", "M4.1 - 95 KM"),
    _card(5, "AMERICAS", "F1",
          "LAS VEGAS GP: LIGHTS OUT 04:00 GMT",
          "The Strip night race starts 20:00 Saturday Vegas time - "
          "04:00 UTC Sunday - as round 22 of the title fight runs "
          "under the lights.",
          "LAS VEGAS - STRIP CIRCUIT", "ROUND 22"),
    _card(6, "SPORT", "WIRES",
          "TURIN FINAL: ALCARAZ v ZVEREV",
          "The ATP Finals end today in Turin: Alcaraz, who fought back "
          "past Shelton, meets Zverev for the season's last big title.",
          "TURIN - ATP FINALS", "TITLE TODAY"),
    _card(7, "MIDEAST", "ANADOLU",
          "HOOTHI MISSILE DOWNED OVER MECCA REGION",
          "Saudi civil defence sounds the Mecca alert at 23:43 local; "
          "the coalition confirms the interception at 01:42 Sunday.",
          "MECCA REGION - SAUDI ARABIA", "01:42 SUNDAY"),
    _card(8, "EUROPE", "PREMIER LEAGUE",
          "ANFIELD SUNDAY: LIVERPOOL v UNITED",
          "Matchweek 11 closes at Anfield, 16:30 GMT Sunday, after "
          "Hull host Brighton in the early game.",
          "ANFIELD - LIVERPOOL", "16:30 GMT"),
    _card(9, "ASIA", "AFP",
          "INDIA'S 720: A WELLINGTON RECORD",
          "India declare on 720/9 - the highest Test total ever made "
          "in New Zealand - on Rahul's 136 and Pant's 128, day four "
          "at the Basin.",
          "WELLINGTON - BASIN RESERVE", "720/9 DECLARED"),
    _card(10, "AMERICAS", "SPACEX",
          "FALCON 9 LIFTS SPY SATELLITES",
          "NROL-136 rides a Falcon 9 out of Vandenberg in Sunday's "
          "12:16 UTC window - the NRO constellation's 15th batch.",
          "VANDENBERG - CALIFORNIA", "12:16 UTC"),
]


def _tuples(rows):
    """Adapt card dicts to the tuple shape the drawing code consumes."""
    return [(c["n"], c["region"], c["tag"], c["head"], c["deck"],
             c["caption"], c["chip"]) for c in rows]


LEADS = _tuples(CARDS[:3])
MINIS = _tuples(CARDS[3:])

# ALSO ON briefs: bare lines here, numbered on from the cards (11..36)
# by the enumerate below - one line each, all from Sunday.
BRIEF_LINES = [
    "ANTALYA - final text haggled line by line",
    "BAHRAIN - smoke rises over the industrial zone",
    "KUWAIT - first drone interception since September",
    "QESHM - island bases inside the clash zone",
    "TEHRAN - IRGC claims the joint operation",
    "MECCA - civil defence alert sounds at 23:43 local",
    "TURIN - Alcaraz fights back past Shelton to the final",
    "WELLINGTON - Nicholls' 175 anchors New Zealand's 368",
    "NAPLES - Kim leads Thitikul by one into Sunday",
    "FUKUOKA - Onosato, Wakamotoharu tied at 12-2",
    "SEA ISLAND - washout pushes RSM round 3 to Sunday",
    "VANDENBERG - booster B1097 returns to Landing Zone 4",
    "MANAMA - Bahrain demands the Security Council act",
    "WELLINGTON - Bumrah takes 4-92 in the first innings",
    "NAYPYIDAW - quake logged 95 km deep, no damage",
    "LAS VEGAS - 50 laps under the Strip lights",
    "KANSAS CITY - Chiefs host Cardinals in the NFL slate",
    "HORMUZ - tankers struck near the strait (UKMTO)",
    "FUKUOKA - Atamifuji one win back at 11-3",
    "NAPLES - $4 million awaits Sunday's LPGA winner",
    "DETROIT - Lions host Buccaneers in the early window",
    "TURIN - the season's last title decided tonight",
    "SEA ISLAND - three tied at 9 under into Sunday",
    "WELLINGTON - six Indian batters pass fifty",
    "BUFFALO - Bills host Dolphins in Sunday's slate",
    "HULL - Brighton visit the MKM in the early game",
]
BRIEFS = [(11 + i, line) for i, line in enumerate(BRIEF_LINES)]

# Figures strip: values and their card-bound labels, kept as two
# parallel lists and zipped - every figure names the card it is from.
FIGURE_VALUES = ["2", "06:00", "M4.1", "720/9", "12:16", "16:30"]
FIGURE_LABELS = [
    "PATRIOT RADARS - CARD 1",
    "GMT COP31 VOTE - CARD 2",
    "MYANMAR QUAKE - CARD 4",
    "INDIA'S RECORD - CARD 9",
    "UTC FALCON 9 - CARD 10",
    "GMT AT ANFIELD - CARD 8",
]
NUMBERS = list(zip(FIGURE_VALUES, FIGURE_LABELS))

# UTC timeline: slot labels and what happens in them, zipped pairwise.
SLOT_LABELS = ["OVERNIGHT", "05:42 WIB", "06:00 GMT", "11:00 WIB",
               "EVENING"]
SLOT_EVENTS = [
    "Iran strikes Gulf bases",
    "Mecca interception confirmed",
    "COP31 approval vote, Antalya",
    "Las Vegas GP lights out",
    "Alcaraz v Zverev, Turin",
]
TIMELINE = list(zip(SLOT_LABELS, SLOT_EVENTS))

DATE_CHECK = [
    "PERU QUAKE M6.9 - 20/21 NOV",
    "400-DRONE BARRAGE - 19-20 NOV",
    "LVIV STRIKE, 2 DEAD - 20 NOV",
    "RIYADH MISSILES DOWNED - 21 NOV",
    "EU-INDONESIA DEAL SIGNED - 21 NOV",
    "CYCLONE AKVAN AT RANCHI - 21 NOV",
    "GAZA AID STATEMENT - 15 NOV",
    "NORWAY OIL RULING - 13 NOV",
    "VENEZUELA $12.26BN FILE - 12 NOV",
    "GHANA HERITAGE NOTES - 12 NOV",
    "KENYA LAST EBOLA PATIENT - 11 NOV",
    "FRANCE 4TH WEEKEND - 7 NOV",
    "EISENKOT GETS MANDATE - 7 NOV",
    "ECB RACE OPENS - 6 NOV",
    "AL-SHABAAB CLAIM - 27 OCT",
]

# pin lon/lat for the 10 cards; dots for briefs
PINS = {
    1: (51.0, 26.8), 2: (30.7, 36.9), 3: (58.4, 23.6), 4: (94.6, 24.4),
    5: (-115.2, 36.1), 6: (7.7, 45.1), 7: (39.8, 21.4), 8: (-2.96, 53.43),
    9: (174.8, -41.3), 10: (-120.5, 34.7),
}
DOTS = [
    (96.0, 21.9), (45.0, 5.0), (-83.0, 42.3), (30.7, 36.9), (85.3, 23.3),
    (-2.96, 53.43), (78.0, 21.0), (130.4, 33.6), (46.7, 24.6), (-78.9, 42.9),
    (58.4, 23.6), (-115.2, 36.1), (-94.6, 39.1), (7.7, 45.1), (-81.8, 26.1),
    (39.8, 21.4), (174.8, -41.3), (-120.5, 34.7), (78.0, 35.0),
]


# ------------------------------------------------------------- drawing
def strip_art(x, y, w, h, num, colour, caption, chip):
    """Flat layered strip: tinted scene, one data chip, caption band."""
    d.rectangle([x, y, x + w, y + h], fill=colour)
    # layered shapes: horizon band + sun/disc + silhouette blocks
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=NAVY)
    r = h * 0.30
    cx, cy = x + w * (0.16 + 0.07 * (num % 5)), y + h * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 197, 24))
    for i in range(3):
        bx = x + w * (0.45 + 0.16 * i)
        bh = h * (0.30 + 0.13 * ((num + i) % 3))
        d.rectangle([bx, y + h - 13 - bh, bx + w * 0.11, y + h - 13],
                    fill=(14, 24, 44))
    d.rectangle([x, y, x + w, y + 3], fill=RED if num <= 3 else colour)
    # data chip, top right
    cf = F(SANSB, 9)
    cw_ = tw(chip, cf) + 12
    d.rounded_rectangle([x + w - cw_ - 4, y + 5, x + w - 4, y + 20],
                        radius=7, fill=NAVY)
    text_in(x + w - cw_ + 2, y + 7, chip, cf, WHITE)
    # caption band along the strip's bottom edge
    d.rectangle([x, y + h - 13, x + w, y + h], fill=NAVY)
    centre(x, x + w, y + h - 11, caption, F(SANSB, 9), WHITE)


def card(x, y, w, h, item, lead=False):
    num, region, tag, head, deck, caption, chip = item
    colour = REGION_RGB[region]
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=INK, width=1)
    sh = 62 if lead else 40
    strip_art(x + 1, y + 1, w - 2, sh, num, colour, caption, chip)
    ly = y + sh + 5
    text_in(x + 7, ly, "%d - %s" % (num, region), F(SANSB, 10), colour)
    tf = F(SANSB, 9)
    text_in(x + w - 7 - tw(tag, tf), ly + 1, tag, tf, GREY)
    hy = ly + 15
    hf = F(SERIF, 17 if lead else 14)
    for ln in wrap(head, hf, w - 14)[:3 if lead else 2]:
        text_in(x + 7, hy, ln, hf, INK)
        hy += (21 if lead else 17)
    df = F(SANSM, 12)
    for ln in wrap(deck, df, w - 14)[:5 if lead else 3]:
        text_in(x + 7, hy + 2, ln, df, (46, 46, 40))
        hy += 15


# ---------------------------------------------------------------- page
# top bar: the date lives here, small - the paper's name is the anchor
text_in(MX, 8, "SUNDAY - 22 NOVEMBER 2026", F(SANSB, 12), INK)
_r = "WIRE SERVICE - ONE PAGE, THE WHOLE DAY"
text_in(W - MX - tw(_r, F(SANSB, 12)), 8, _r, F(SANSB, 12), GREY)
d.line([MX, 28, W - MX, 28], fill=INK, width=2)

# masthead: the name, Playfair Black, as wide as the page allows
_m = "THE MERIDIAN WIRE"
_ms = fit_size(_m, SERIF, 76, CW)
centre(MX, W - MX, 34, _m, F(SERIF, _ms), INK)
d.line([MX, 104, W - MX, 104], fill=INK, width=3)
d.line([MX, 108, W - MX, 108], fill=INK, width=1)

# kicker counts
_k = "36 STORIES - 10 CARDS - EVERY STORY FROM SUNDAY 22 NOVEMBER 2026"
centre(MX, W - MX, 113, _k, F(SANSB, 12), RED)

# red hook band: the day's three biggest stories, read first
HY = 130
d.rectangle([MX, HY, W - MX, HY + 40], fill=RED)
hooks = [
    "1 - IRAN STRIKES US BASES IN THE GULF",
    "2 - COP31 FINAL TEXT TABLED IN ANTALYA",
    "3 - TANKERS HIT OFF OMAN",
]
_hw = CW // 3
for i, hk in enumerate(hooks):
    hf = F(SANSB, 12)
    lines = wrap(hk, hf, _hw - 18)
    yy = HY + (40 - len(lines) * 15) // 2
    for ln in lines:
        centre(MX + i * _hw, MX + (i + 1) * _hw, yy, ln, hf, WHITE)
        yy += 15
    if i:
        d.line([MX + i * _hw, HY + 6, MX + i * _hw, HY + 34], fill=WHITE,
               width=1)

# UTC timeline strip
TY = 176
d.rectangle([MX, TY, W - MX, TY + 30], fill=NAVY)
_tw5 = CW // 5
for i, (slot, ev) in enumerate(TIMELINE):
    x0 = MX + i * _tw5
    centre(x0, x0 + _tw5, TY + 3, slot, F(SANSB, 10), (245, 197, 24))
    ef = F(SANSM, 10)
    for j, ln in enumerate(wrap(ev, ef, _tw5 - 10)[:1]):
        centre(x0, x0 + _tw5, TY + 16, ln, ef, WHITE)
    if i:
        d.line([x0, TY + 5, x0, TY + 25], fill=(90, 110, 140), width=1)

# lead row: three big cards
LY = 212
_lw = (CW - 2 * 12) // 3
for i, item in enumerate(LEADS):
    card(MX + i * (_lw + 12), LY, _lw, 180, item, lead=True)

# mini grid: seven cards - a row of four, then a row of three wider ones
GY = 398
_w4 = (CW - 3 * 10) // 4
for c in range(4):
    card(MX + c * (_w4 + 10), GY, _w4, 148, MINIS[c])
_w3 = (CW - 2 * 10) // 3
for c in range(3):
    card(MX + c * (_w3 + 10), GY + 154, _w3, 148, MINIS[4 + c])


# numbers strip: six figures, every one bound to a card or brief
NY = 706
d.rectangle([MX, NY, W - MX, NY + 38], fill=(238, 231, 210))
_nw = CW // 6
for i, (big, lab) in enumerate(NUMBERS):
    x0 = MX + i * _nw
    centre(x0, x0 + _nw, NY + 2, big, F(SERIF, 20), RED)
    centre(x0, x0 + _nw, NY + 26, lab, F(SANSB, 9), INK)
    if i:
        d.line([x0, NY + 5, x0, NY + 33], fill=FAINT, width=1)

# bottom row: map (left) + ALSO ON briefs (right)
BY = 750
MAPW = 500
d.rectangle([MX, BY, MX + MAPW, BY + 196], fill=NAVY, outline=INK, width=1)
centre(MX, MX + MAPW, BY + 4, "WHERE IT HAPPENED - SUNDAY 22 NOVEMBER",
       F(SANSB, 11), WHITE)
map_box = (MX + 8, BY + 22, MX + MAPW - 8, BY + 158)


def proj(lon, lat):
    x = map_box[0] + (lon + 168) / 360.0 * (map_box[2] - map_box[0])
    y = map_box[1] + (80 - lat) / 136.0 * (map_box[3] - map_box[1])
    return x, y


for _name, polys in WORLD.items():
    for ring in polys.split("|"):
        pts = []
        for pair in ring.split(","):
            lo, la = pair.split(":")
            pts.append(proj(float(lo), float(la)))
        if len(pts) > 2:
            d.polygon(pts, fill=LAND, outline=(70, 88, 66))

REGION_OF = {it[0]: it[1] for it in LEADS + MINIS}
for lon, lat in DOTS:
    x, y = proj(lon, lat)
    d.ellipse([x - 2.5, y - 2.5, x + 2.5, y + 2.5], fill=(230, 225, 205))
for num, (lon, lat) in PINS.items():
    x, y = proj(lon, lat)
    col = REGION_RGB[REGION_OF[num]]
    d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=col, outline=WHITE, width=1)
    d.text((x, y), str(num), font=F(SANSB, 10), fill=WHITE, anchor="mm")
centre(MX, MX + MAPW, BY + 162,
       "NUMBERED PINS = THE 10 PICTURED CARDS", F(SANSB, 9), WHITE)
centre(MX, MX + MAPW, BY + 176,
       "SMALL DOTS = ALSO ON BRIEFS - PIN COLOURS MATCH CARD REGIONS",
       F(SANSB, 9), (200, 205, 215))

AX = MX + MAPW + 12
AW = W - MX - AX
d.rectangle([AX, BY, AX + AW, BY + 196], fill=CARD_BG, outline=INK, width=1)
text_in(AX + 8, BY + 5, "ALSO ON THE WIRE - 26 MORE FROM SUNDAY",
        F(SANSB, 11), INK)
d.line([AX + 8, BY + 22, AX + AW - 8, BY + 22], fill=RED, width=2)
bf = F(SANSM, 10)
col_w = (AW - 24) // 2
for i, (num, line) in enumerate(BRIEFS):
    cx = AX + 8 + (i // 13) * (col_w + 8)
    cy = BY + 27 + (i % 13) * 12.6
    s = "%d - %s" % (num, line)
    while tw(s, bf) > col_w and " " in s:
        s = s[:s.rfind(" ")]
    text_in(cx, cy, s, bf, (46, 46, 40))

# DATE CHECK: older stories, named and dated - deliberately out
DY = 950
d.rectangle([MX, DY, W - MX, DY + 46], fill=(253, 250, 242),
            outline=RED, width=2)
text_in(MX + 8, DY + 4, "DATE CHECK - NOT TODAY:", F(SANSB, 10), RED)
_dw = (CW - 158 - 8) // 3
for i, item in enumerate(DATE_CHECK):
    cx = MX + 158 + (i // 5) * _dw
    cy = DY + 3 + (i % 5) * 8.6
    text_in(cx, cy, item, F(SANSB, 9), (120, 40, 30))

# footer: the verification sentence + sources
centre(MX, W - MX, 1000,
       "Lead stories are Sunday's own; older stories are named in "
       "Date Check, never dressed as today's.",
       F(SANSM, 10), GREY)
centre(MX, W - MX, 1013,
       "Sources: Reuters - Anadolu - AFP - IANS - NCS - Premier League - "
       "SpaceX. Original drawings.", F(SANSB, 9), GREY)

img.save(OUT, optimize=True)
_size = os.path.getsize(OUT)
if _size > 165000:  # palette-compress for the bytes tie-break
    img.quantize(colors=256, method=Image.MEDIANCUT).save(OUT,
                                                          optimize=True)
    _size = os.path.getsize(OUT)
print("entry.png bytes:", _size)
