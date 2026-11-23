#!/usr/bin/env python3
"""The Meridian Wire - NI22 round 4 for @yutulboy.

Round 4 iterates on the round 3 structure (21 pictured cards, region
slug bars, numbered badges and map pins, tally, subdeck, three-part
DATE CHECK) with ONE correction: colour is pulled down toward the
measured #1 profile.  Scene fields are now pale, low-range tones
(blends of the sampled mid-tone region colours with the paper cream);
only deliberate accent shapes carry the full mid-tone colour, so the
step-2 colour-area measurement (channel range > 70 and max > 90)
lands near #1's 11.8% page / 19.7% mid-band instead of round 3's
25.7% / 47.4%.

Architecture is data-driven and written for this round: every scene
is a list of primitive ops (rect / ellipse / polygon / line / text)
in normalised coordinates, interpreted by one small renderer.  Lead
subjects still span >=70% of their scene height.  Facts come only
from this account's own story pool (POOL22-BARU v3, as carried in
rounds 2-3); contested claims stay attributed as claims.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mapdata import WORLD  # noqa: E402

W = 1024
PAPER = (247, 242, 232)
CARD = (252, 249, 242)
BLACK = (24, 22, 18)
GREY = (98, 92, 82)
BODY = (52, 48, 42)
RED = (165, 40, 40)
GOLD_TXT = (255, 213, 116)
MAP_SEA = (205, 225, 235)
MAP_LAND = (222, 205, 180)

# Mid-tone region colours sampled from the #1 page (BEDAH-TOP1 s.4).
C_TEAL = (17, 107, 88)
C_BLUE = (45, 88, 146)
C_ORANGE = (181, 83, 39)
C_MAGENTA = (156, 46, 90)
C_CYAN = (54, 143, 145)
C_GREEN = (78, 128, 45)
C_GOLD = (160, 130, 47)

REGIONS = {
    "MIDDLE EAST": C_ORANGE,
    "OCEANIA": C_GREEN,
    "ASIA": C_MAGENTA,
    "EUROPE": C_BLUE,
    "N AMERICA": C_CYAN,
}
SHORT = {"MIDDLE EAST": "MIDDLE EAST", "OCEANIA": "OCEANIA", "ASIA": "ASIA",
         "EUROPE": "EUROPE", "N AMERICA": "N AMERICA"}

FONT_DIR = os.path.join(HERE, "fonts")


def f_sans(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "Archivo-Bold.ttf"), size)


def f_med(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "Archivo-Medium.ttf"), size)


def f_serif(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "PlayfairDisplay-900.ttf"), size)


def blend(colour, other, frac):
    """frac of `other` mixed into `colour`."""
    return tuple(int(colour[k] + (other[k] - colour[k]) * frac) for k in range(3))


def pale(colour, frac=0.72):
    """Pastel version of a mid-tone colour: blended toward paper cream.
    Such tones keep channel range <= 70, i.e. they read as colour on
    the page without counting as saturated area in the measurement."""
    return blend(colour, PAPER, frac)


# ---------------------------------------------------------------- stories
# (num, region, slug, headline, deck, source line, scene key, caption,
#  lon, lat)  -- leads carry a deck; minis are deck-less, so their
# headlines carry two facts wherever the line allows it.
LEADS = [
    (1, "MIDDLE EAST", "BAHRAIN: 2 RADARS CLAIMED HIT",
     "IRGC claims hits on two Bahrain radars",
     "Al-Riffa & Awali radars claimed; an industry site ablaze, a drone downed in Kuwait, a tanker hit near Hormuz.",
     "IRGC statement · Bahrain ministry · UKMTO", "gulf",
     "1 · BAHRAIN · MIDDLE EAST", 50.6, 26.2),
    (2, "OCEANIA", "WELLINGTON: 720/9 DECLARED",
     "India declare 720/9 — a NZ Test record",
     "166 overs: Rahul 136, Pant 128, Gill 98. NZ 368 (Nicholls 175, Bumrah 4-92); India lead by 352.",
     "IANS · AFP", "cricket",
     "2 · WELLINGTON · OCEANIA", 174.8, -41.3),
    (3, "N AMERICA", "VANDENBERG: 12:16 WINDOW",
     "Falcon 9 lifts NROL-136 Sunday",
     "Window 12:16–12:46 UTC, SLC-4E: 15th NRO batch with Northrop Grumman; B1097 returns to LZ4.",
     "SpaceX · Vandenberg SFB", "falcon",
     "3 · VANDENBERG · NORTH AMERICA", -120.6, 34.7),
]

MINIS = [
    (4, "MIDDLE EAST", "MAKKAH: MISSILE DOWNED",
     "Missile downed; sirens 23:43 Riyadh", "", "MIDDLE EAST · ANADOLU",
     "makkah", 39.8, 21.4),
    (5, "ASIA", "ANTALYA: FINAL TEXT TABLED",
     "COP31 text tabled; plenary 06:00", "", "ASIA · REUTERS",
     "cop", 30.7, 36.9),
    (6, "ASIA", "MYANMAR: M4.1 · 95 KM DEEP",
     "M4.1 quake, 95 km deep, Myanmar", "", "ASIA · NCS / ANI",
     "quake", 94.6, 24.4),
    (7, "N AMERICA", "LAS VEGAS: LIGHTS 04:00 UTC",
     "Vegas GP: 50 laps, lights 04:00 UTC", "", "NORTH AMERICA · FORMULA 1",
     "vegas", -115.2, 36.1),
    (8, "EUROPE", "ANFIELD: 16:30 UTC",
     "Liverpool v Man Utd, Anfield 16:30", "", "EUROPE · PREMIER LEAGUE",
     "prem", -2.96, 53.4),
    (9, "EUROPE", "TURIN: TITLE MATCH",
     "Alcaraz v Zverev, Turin title match", "", "EUROPE · ATP / REUTERS",
     "atp", 7.7, 45.1),
    (10, "N AMERICA", "NAPLES: KIM −18 LEADS",
     "Kim −18 leads CME finale by one", "", "NORTH AMERICA · LPGA / AP",
     "lpga", -81.8, 26.1),
    (11, "ASIA", "FUKUOKA: TWO AT 12-2",
     "Two at 12-2 into Kyushu final day", "", "ASIA · JSA",
     "sumo", 130.4, 33.6),
    (12, "N AMERICA", "RSM: THREE LEAD AT −9",
     "RSM round 3 rained to Sunday; −9 leads", "", "NORTH AMERICA · REUTERS",
     "rsm", -81.4, 31.2),
    (13, "N AMERICA", "NFL: 11 SUNDAY GAMES",
     "11 NFL games; SNF Vikings @ 49ers", "", "NORTH AMERICA · NFL",
     "nfl", -98.0, 39.0),
    (14, "OCEANIA", "WELLINGTON: NICHOLLS 175",
     "Nicholls 175 stands alone in NZ 368", "", "OCEANIA · IANS / AFP",
     "nicholls", 174.8, -41.3),
    (15, "OCEANIA", "WELLINGTON: BUMRAH 4-92",
     "Bumrah 4-92 cuts NZ to 368 all out", "", "OCEANIA · IANS / AFP",
     "bumrah", 174.8, -41.3),
    (16, "MIDDLE EAST", "BAHRAIN: SITE ABLAZE",
     "Industry site ablaze, Bahrain says", "", "MIDDLE EAST · BAHRAIN MINISTRY",
     "bahrain", 50.6, 26.2),
    (17, "MIDDLE EAST", "HORMUZ: TANKER ATTACKED",
     "Tanker hit near Hormuz, UKMTO says", "", "MIDDLE EAST · UKMTO",
     "hormuz", 56.3, 26.5),
    (18, "MIDDLE EAST", "KUWAIT: DRONE DOWNED",
     "Drone downed; first since September", "", "MIDDLE EAST · KUWAIT ARMY",
     "kuwait", 47.9, 29.3),
    (19, "ASIA", "ANTALYA: SHUT 03:00 GMT",
     "Objections shut 03:00; text tabled", "", "ASIA · REUTERS",
     "cop2", 30.7, 36.9),
    (20, "N AMERICA", "NAPLES: $4M TO WINNER",
     "$4m CME prize; Kim leads at −18", "", "NORTH AMERICA · LPGA / AP",
     "cme", -81.8, 26.1),
    (21, "ASIA", "FUKUOKA: YUSHO DECIDERS",
     "Yusho day: Onosato v Hoshoryu", "", "ASIA · JSA",
     "yusho", 130.4, 33.6),
]

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

# (text, region, source, lon, lat) -- stories 22..36
BRIEFS = [
    ("Rahul 136, top score in India's 720/9", "OCEANIA", "IANS", 174.8, -41.3),
    ("Pant 128, second century of the 720/9", "OCEANIA", "IANS", 174.8, -41.3),
    ("Jaiswal 85, a fourth fifty-plus score", "OCEANIA", "IANS", 174.8, -41.3),
    ("Padikkal 80 in the record 720/9", "OCEANIA", "IANS", 174.8, -41.3),
    ("Sunday night: Vikings @ 49ers, 20:20 ET", "N AMERICA", "NFL", -122.0, 37.4),
    ("Thorbjornsen shares RSM lead at −9", "N AMERICA", "Reuters", -81.4, 31.2),
    ("Penge shares the RSM lead at −9", "N AMERICA", "Reuters", -81.4, 31.2),
    ("Neergaard-Petersen shares RSM lead, −9", "N AMERICA", "Reuters", -81.4, 31.2),
    ("Onosato 12-2, joint leader at Fukuoka", "ASIA", "JSA", 130.4, 33.6),
    ("Wakamotoharu 12-2, joint leader", "ASIA", "JSA", 130.4, 33.6),
    ("Atamifuji 11-3, one win back", "ASIA", "JSA", 130.4, 33.6),
    ("Wakamotoharu v Atamifuji, yusho decider", "ASIA", "JSA", 130.4, 33.6),
    ("Thitikul −17, one back at CME finale", "N AMERICA", "AP", -81.8, 26.1),
    ("Yoshida −17, one back at Tiburón", "N AMERICA", "AP", -81.8, 26.1),
    ("COP31 draft recalls Dubai fossil-fuel deal", "ASIA", "Reuters", 30.7, 36.9),
]

# Recounted from the lists above: leads ME1 OC1 NA1; minis ME4 OC2 AS5
# EU2 NA5; briefs OC4 AS5 NA6  ->  ME5 OC7 AS10 EU2 NA12 = 36.
TALLY = [("MIDDLE EAST", 5), ("OCEANIA", 7), ("ASIA", 10),
         ("EUROPE", 2), ("N AMERICA", 12)]

DC_LEFT = ("Lviv strike 20 Nov · Peru M6.9 quake 20/21 Nov · Riyadh missiles 21 Nov · "
           "Hodeidah strike 21 Nov · CEPA signing 21 Nov · France march of 82,500 21 Nov · "
           "ICJ ruling 19 Nov")
DC_NOTYET = ("COP31 final adoption — plenary set for 06:00 GMT, vote pending · "
             "Liverpool v Man Utd result — kickoff 16:30 UTC · "
             "ATP Turin final result — played Sunday evening")
DC_UNCONF = ("IRGC claim: 2 Patriot radars destroyed — not independently verified · "
             "Houthi interception claim near Makkah — coalition account, contested")


# ---------------------------------------------------------------- scenes
# Scene spec: (top colour, bottom colour, [ops]).  Ops use normalised
# coordinates (0..1 across the scene box).  Op kinds:
#   ("r", x, y, x2, y2, colour)            rectangle
#   ("e", x, y, x2, y2, colour)            ellipse
#   ("eo", x, y, x2, y2, colour, width)    ellipse outline
#   ("p", [(x, y), ...], colour)           polygon
#   ("l", [(x, y), ...], colour, width)    polyline, width as frac of height
#   ("t", x, y, text, sizefrac, colour)    bold text, size as frac of height
# Fields are pale blends (channel range <= 70, uncounted); accents use
# the full mid-tone colours and cover a deliberate minority of each
# scene.  Subjects are drawn large in dark / white / low-range tones.

WHITE = (255, 255, 255)
SLATE = (38, 44, 54)
CHAR = (28, 26, 24)
SAND = (198, 170, 138)
SKIN = (222, 205, 180)

LEAD_SCENES = {
    # Gulf: pale dusk sky, dark sea, one big saturated burst (subject
    # ~90% of height: burst + rays), radar mast and tanker in slate.
    "gulf": (pale(C_BLUE, 0.52), pale(C_ORANGE, 0.62), [
        ("r", 0.0, 0.80, 1.0, 1.0, (44, 62, 84)),
        ("l", [(0.06, 0.80), (0.06, 0.42)], WHITE, 0.045),
        ("l", [(0.06, 0.42), (0.16, 0.30)], WHITE, 0.04),
        ("p", [(0.10, 0.36), (0.84, 0.06), (0.94, 0.38), (0.10, 0.44)],
         blend(C_GREEN, PAPER, 0.68)),
        ("l", [(0.30, 0.62), (0.62, 0.30)], (255, 176, 70), 0.03),
        ("e", 0.56, 0.06, 0.90, 0.62, C_ORANGE),
        ("e", 0.615, 0.145, 0.845, 0.535, (255, 178, 58)),
        ("e", 0.665, 0.225, 0.795, 0.455, (255, 242, 190)),
        ("p", [(0.60, 0.86), (0.84, 0.86), (0.81, 0.93), (0.63, 0.93)], CHAR),
        ("r", 0.635, 0.79, 0.755, 0.86, (96, 102, 112)),
    ]),
    # Wellington: alternating field stripes (one stripe family in full
    # green), tan pitch, batsman silhouette ~75% of height.
    "cricket": (pale(C_GREEN, 0.66), pale(C_GREEN, 0.5), [
        ("r", 0.125, 0.0, 0.25, 1.0, C_GREEN),
        ("r", 0.375, 0.0, 0.50, 1.0, C_GREEN),
        ("r", 0.625, 0.0, 0.75, 1.0, C_GREEN),
        ("r", 0.875, 0.0, 1.0, 1.0, C_GREEN),
        ("p", [(0.40, 1.0), (0.45, 0.30), (0.58, 0.30), (0.63, 1.0)], SAND),
        ("e", 0.415, 0.10, 0.475, 0.26, SLATE),
        ("l", [(0.445, 0.26), (0.43, 0.55)], SLATE, 0.075),
        ("l", [(0.43, 0.55), (0.36, 0.92)], WHITE, 0.07),
        ("l", [(0.43, 0.55), (0.52, 0.90)], WHITE, 0.07),
        ("l", [(0.44, 0.32), (0.56, 0.44)], SLATE, 0.055),
        ("l", [(0.55, 0.43), (0.66, 0.22)], (150, 108, 56), 0.05),
        ("e", 0.70, 0.26, 0.735, 0.335, RED),
        ("t", 0.03, 0.05, "720/9", 0.24, WHITE),
    ]),
    # Vandenberg: pale dawn sky, rocket in white/slate ~80% of height,
    # saturated flame, gold landing-zone ring.
    "falcon": (pale(C_ORANGE, 0.58), pale(C_BLUE, 0.6), [
        ("r", 0.0, 0.84, 1.0, 1.0, (104, 100, 92)),
        ("r", 0.135, 0.08, 0.165, 0.84, (70, 74, 82)),
        ("l", [(0.15, 0.18), (0.24, 0.26)], (70, 74, 82), 0.03),
        ("l", [(0.15, 0.36), (0.24, 0.44)], (70, 74, 82), 0.03),
        ("l", [(0.15, 0.54), (0.24, 0.62)], (70, 74, 82), 0.03),
        ("p", [(0.225, 0.66), (0.225, 0.20), (0.26, 0.06), (0.295, 0.20),
               (0.295, 0.66)], WHITE),
        ("r", 0.225, 0.50, 0.295, 0.565, CHAR),
        ("p", [(0.24, 0.66), (0.28, 0.66), (0.26, 0.94)], C_ORANGE),
        ("p", [(0.247, 0.66), (0.273, 0.66), (0.26, 0.82)], (255, 224, 130)),
        ("eo", 0.80, 0.70, 0.90, 0.92, C_GOLD, 0.035),
        ("t", 0.815, 0.44, "LZ4", 0.15, WHITE),
    ]),
}

MINI_SCENES = {
    "makkah": (pale(C_BLUE, 0.5), pale(C_BLUE, 0.66), [
        ("l", [(0.05, 0.78), (0.30, 0.72), (0.52, 0.38), (0.68, 0.30)],
         (255, 176, 70), 0.07),
        ("e", 0.63, 0.16, 0.75, 0.44, C_ORANGE),
        ("e", 0.655, 0.205, 0.725, 0.395, (255, 220, 150)),
        ("r", 0.80, 0.0, 1.0, 1.0, pale(C_BLUE, 0.3)),
        ("t", 0.815, 0.18, "01:42", 0.34, WHITE),
    ]),
    "cop": (pale(C_TEAL, 0.62), pale(C_TEAL, 0.5), [
        ("r", 0.04, 0.14, 0.34, 0.86, WHITE),
        ("r", 0.04, 0.14, 0.34, 0.32, C_TEAL),
        ("l", [(0.08, 0.48), (0.30, 0.48)], GREY, 0.05),
        ("l", [(0.08, 0.64), (0.26, 0.64)], GREY, 0.05),
        ("t", 0.42, 0.10, "06:00", 0.42, WHITE),
        ("t", 0.42, 0.56, "PLENARY", 0.28, blend(C_GOLD, WHITE, 0.35)),
    ]),
    "quake": (pale(C_MAGENTA, 0.55), pale(C_MAGENTA, 0.68), [
        ("l", [(0.03, 0.5), (0.14, 0.5), (0.20, 0.16), (0.27, 0.84),
               (0.33, 0.30), (0.40, 0.5), (0.50, 0.5)], (130, 238, 150), 0.06),
        ("r", 0.56, 0.0, 1.0, 1.0, pale(C_MAGENTA, 0.34)),
        ("t", 0.60, 0.16, "M4.1", 0.46, WHITE),
        ("t", 0.60, 0.62, "95 KM", 0.26, WHITE),
    ]),
    "vegas": (pale(C_MAGENTA, 0.5), pale(C_BLUE, 0.55), [
        ("l", [(0.04, 0.74), (0.20, 0.74), (0.27, 0.24), (0.42, 0.24),
               (0.48, 0.76), (0.62, 0.76), (0.67, 0.30), (0.04, 0.74)],
         C_GOLD, 0.07),
        ("t", 0.74, 0.08, "50", 0.52, WHITE),
        ("t", 0.74, 0.60, "LAPS", 0.27, blend(C_GOLD, WHITE, 0.3)),
    ]),
    "prem": (pale(C_GREEN, 0.6), pale(C_GREEN, 0.48), [
        ("eo", 0.03, 0.10, 0.55, 0.90, WHITE, 0.05),
        ("l", [(0.29, 0.10), (0.29, 0.90)], WHITE, 0.04),
        ("eo", 0.225, 0.32, 0.355, 0.68, WHITE, 0.04),
        ("r", 0.66, 0.0, 1.0, 1.0, pale(C_GREEN, 0.3)),
        ("t", 0.685, 0.12, "16:30", 0.38, WHITE),
        ("t", 0.685, 0.56, "ANFIELD", 0.25, WHITE),
    ]),
    "atp": (pale(C_BLUE, 0.58), pale(C_BLUE, 0.46), [
        ("eo", 0.03, 0.10, 0.55, 0.90, WHITE, 0.05),
        ("l", [(0.29, 0.10), (0.29, 0.90)], WHITE, 0.04),
        ("l", [(0.03, 0.50), (0.55, 0.50)], WHITE, 0.04),
        ("eo", 0.66, 0.14, 0.83, 0.66, C_GOLD, 0.08),
        ("l", [(0.80, 0.58), (0.93, 0.88)], C_GOLD, 0.08),
        ("r", 0.0, 0.86, 1.0, 1.0, C_BLUE),
    ]),
    "lpga": (pale(C_TEAL, 0.58), pale(C_GREEN, 0.55), [
        ("t", 0.04, 0.08, "−18", 0.62, WHITE),
        ("l", [(0.66, 0.88), (0.66, 0.14)], WHITE, 0.06),
        ("p", [(0.66, 0.14), (0.86, 0.26), (0.66, 0.40)], RED),
        ("r", 0.0, 0.88, 1.0, 1.0, C_GREEN),
    ]),
    "sumo": (pale(C_GOLD, 0.55), pale(C_GOLD, 0.42), [
        ("e", 0.03, 0.12, 0.30, 0.88, SKIN),
        ("eo", 0.03, 0.12, 0.30, 0.88, (110, 78, 38), 0.07),
        ("t", 0.38, 0.14, "12-2 · 12-2", 0.36, CHAR),
        ("r", 0.38, 0.66, 0.97, 0.80, C_ORANGE),
    ]),
    "rsm": (pale(C_CYAN, 0.6), pale(C_CYAN, 0.48), [
        ("r", 0.05, 0.14, 0.48, 0.30, WHITE),
        ("r", 0.05, 0.38, 0.48, 0.54, blend(C_CYAN, WHITE, 0.45)),
        ("r", 0.05, 0.62, 0.48, 0.78, blend(C_CYAN, WHITE, 0.45)),
        ("t", 0.58, 0.14, "−9 ×3", 0.46, blend(C_GOLD, WHITE, 0.25)),
        ("r", 0.58, 0.68, 0.97, 0.82, C_CYAN),
    ]),
    "nfl": (pale(C_BLUE, 0.55), pale(C_BLUE, 0.66), [
        ("e", 0.04, 0.12, 0.115, 0.42, (255, 192, 84)),
        ("e", 0.135, 0.12, 0.21, 0.42, (255, 192, 84)),
        ("e", 0.23, 0.12, 0.305, 0.42, (255, 192, 84)),
        ("e", 0.325, 0.12, 0.40, 0.42, (255, 192, 84)),
        ("e", 0.04, 0.56, 0.115, 0.86, (255, 192, 84)),
        ("e", 0.135, 0.56, 0.21, 0.86, (255, 192, 84)),
        ("e", 0.23, 0.56, 0.305, 0.86, (255, 192, 84)),
        ("e", 0.325, 0.56, 0.40, 0.86, (255, 192, 84)),
        ("t", 0.52, 0.06, "11", 0.56, WHITE),
        ("t", 0.70, 0.24, "GAMES", 0.30, blend(C_GOLD, WHITE, 0.3)),
        ("r", 0.52, 0.70, 0.97, 0.84, C_BLUE),
    ]),
    "nicholls": (pale(C_GREEN, 0.58), pale(C_GREEN, 0.46), [
        ("t", 0.04, 0.06, "175", 0.68, WHITE),
        ("l", [(0.70, 0.16), (0.70, 0.84)], (252, 242, 200), 0.07),
        ("l", [(0.79, 0.16), (0.79, 0.84)], (252, 242, 200), 0.07),
        ("l", [(0.88, 0.16), (0.88, 0.84)], (252, 242, 200), 0.07),
        ("r", 0.0, 0.86, 1.0, 1.0, C_GREEN),
    ]),
    "bumrah": (pale(C_BLUE, 0.52), pale(C_BLUE, 0.64), [
        ("t", 0.04, 0.08, "4-92", 0.60, WHITE),
        ("e", 0.78, 0.18, 0.94, 0.78, RED),
        ("r", 0.0, 0.86, 1.0, 1.0, C_MAGENTA),
    ]),
    "bahrain": (pale(C_ORANGE, 0.6), pale(C_ORANGE, 0.7), [
        ("r", 0.04, 0.52, 0.50, 0.92, CHAR),
        ("r", 0.54, 0.30, 0.62, 0.92, CHAR),
        ("p", [(0.16, 0.52), (0.27, 0.06), (0.38, 0.52)], C_ORANGE),
        ("p", [(0.21, 0.52), (0.27, 0.24), (0.33, 0.52)], (255, 200, 80)),
        ("t", 0.68, 0.16, "FIRE", 0.38, WHITE),
        ("r", 0.68, 0.64, 0.97, 0.78, C_ORANGE),
    ]),
    "hormuz": (pale(C_BLUE, 0.6), pale(C_CYAN, 0.62), [
        ("p", [(0.06, 0.56), (0.74, 0.56), (0.66, 0.78), (0.14, 0.78)], CHAR),
        ("r", 0.16, 0.36, 0.52, 0.56, (96, 102, 112)),
        ("r", 0.56, 0.24, 0.64, 0.56, (64, 68, 78)),
        ("l", [(0.04, 0.88), (0.20, 0.80), (0.36, 0.88), (0.52, 0.80),
               (0.68, 0.88), (0.84, 0.80)], WHITE, 0.05),
        ("r", 0.82, 0.0, 1.0, 1.0, C_ORANGE),
    ]),
    "kuwait": (pale(C_BLUE, 0.58), pale(C_CYAN, 0.6), [
        ("p", [(0.10, 0.46), (0.30, 0.30), (0.58, 0.30), (0.74, 0.52),
               (0.50, 0.60), (0.24, 0.60)], CHAR),
        ("p", [(0.40, 0.30), (0.50, 0.12), (0.58, 0.30)], CHAR),
        ("p", [(0.80, 0.10), (0.86, 0.42), (0.92, 0.10)], (255, 150, 50)),
        ("l", [(0.86, 0.42), (0.86, 0.78)], (255, 150, 50), 0.07),
        ("r", 0.0, 0.86, 1.0, 1.0, C_BLUE),
    ]),
    "cop2": (pale(C_MAGENTA, 0.58), pale(C_MAGENTA, 0.68), [
        ("t", 0.04, 0.08, "03:00", 0.56, WHITE),
        ("eo", 0.70, 0.14, 0.94, 0.84, WHITE, 0.06),
        ("l", [(0.75, 0.36), (0.89, 0.36)], WHITE, 0.06),
        ("l", [(0.75, 0.58), (0.85, 0.58)], WHITE, 0.06),
        ("r", 0.0, 0.86, 1.0, 1.0, C_MAGENTA),
    ]),
    "cme": (pale(C_GOLD, 0.5), pale(C_GOLD, 0.62), [
        ("t", 0.04, 0.08, "$4M", 0.60, WHITE),
        ("eo", 0.68, 0.14, 0.95, 0.72, blend(C_GOLD, WHITE, 0.2), 0.09),
        ("r", 0.785, 0.62, 0.845, 0.86, blend(C_GOLD, WHITE, 0.2)),
        ("r", 0.0, 0.86, 1.0, 1.0, C_GOLD),
    ]),
    "yusho": (pale(C_MAGENTA, 0.6), pale(C_ORANGE, 0.66), [
        ("e", 0.03, 0.10, 0.32, 0.90, SKIN),
        ("eo", 0.03, 0.10, 0.32, 0.90, WHITE, 0.06),
        ("t", 0.42, 0.12, "FINAL", 0.38, WHITE),
        ("t", 0.42, 0.54, "DAY", 0.28, blend(C_GOLD, WHITE, 0.3)),
        ("r", 0.42, 0.82, 0.97, 0.94, C_MAGENTA),
    ]),
}


# ---------------------------------------------------------------- renderer
def paint_scene(img, box, spec):
    """Interpret one scene spec inside box = (x0, y0, x1, y1)."""
    top, bottom, ops = spec
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d = ImageDraw.Draw(img, "RGBA")
    steps = 20
    for i in range(steps):
        a = i / steps
        col = tuple(int(top[k] + (bottom[k] - top[k]) * a) for k in range(3))
        d.rectangle([x0, y0 + int(h * a), x1, y0 + int(h * (i + 1) / steps) + 1],
                    fill=col)

    def px(nx):
        return x0 + nx * w

    def py(ny):
        return y0 + ny * h

    for op in ops:
        kind = op[0]
        if kind == "r":
            d.rectangle([px(op[1]), py(op[2]), px(op[3]), py(op[4])], fill=op[5])
        elif kind == "e":
            d.ellipse([px(op[1]), py(op[2]), px(op[3]), py(op[4])], fill=op[5])
        elif kind == "eo":
            d.ellipse([px(op[1]), py(op[2]), px(op[3]), py(op[4])],
                      outline=op[5], width=max(2, int(op[6] * h)))
        elif kind == "p":
            d.polygon([(px(a), py(b)) for a, b in op[1]], fill=op[2])
        elif kind == "l":
            pts = [(px(a), py(b)) for a, b in op[1]]
            d.line(pts, fill=op[2], width=max(2, int(op[3] * h)), joint="curve")
        elif kind == "t":
            size = max(9, int(op[4] * h))
            d.text((px(op[1]), py(op[2])), op[3], font=f_sans(size), fill=op[5])
    return ImageDraw.Draw(img)


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def slug(d, x0, y0, x1, text, colour, height, size):
    d.rectangle([x0, y0, x1, y0 + height], fill=colour)
    d.text((x0 + 8, y0 + (height - size) // 2 - 1), text,
           font=f_sans(size), fill=WHITE)


def badge(d, x1, y1, num, colour):
    cx, cy, r = x1 - 12, y1 - 12, 8
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour,
              outline=WHITE, width=2)
    t = str(num)
    tf = f_sans(9 if num < 10 else 8)
    d.text((cx - d.textlength(t, font=tf) / 2, cy - 5), t, font=tf, fill=WHITE)


def card_frame(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=CARD)
    d.line([x0, y1, x1, y1], fill=(198, 190, 170), width=1)
    d.line([x0, y0, x0, y1], fill=(216, 208, 190), width=1)
    d.line([x1, y0, x1, y1], fill=(216, 208, 190), width=1)


def lead_card(img, story, box):
    num, region, slugtxt, head, deck, src, key, cap, _lon, _lat = story
    colour = REGIONS[region]
    x0, y0, x1, _y1 = box
    d = ImageDraw.Draw(img)
    card_frame(d, box)
    slug(d, x0, y0, x1, slugtxt, colour, 20, 12)
    sbox = (x0, y0 + 20, x1, y0 + 130)
    d = paint_scene(img, sbox, LEAD_SCENES[key])
    badge(d, sbox[2], sbox[3], num, colour)
    d.text((x0 + 10, y0 + 134), cap, font=f_sans(10), fill=colour)
    y = y0 + 146
    for line in wrap(d, head, f_serif(18), x1 - x0 - 20)[:2]:
        d.text((x0 + 10, y), line, font=f_serif(18), fill=BLACK)
        y += 19
    y = y0 + 185
    for line in wrap(d, deck, f_med(11), x1 - x0 - 20)[:2]:
        d.text((x0 + 10, y), line, font=f_med(11), fill=BODY)
        y += 12
    d.text((x0 + 10, y0 + 209), src, font=f_med(9), fill=GREY)


def mini_card(img, story, box):
    num, region, slugtxt, head, _deck, src, key, _lon, _lat = story
    colour = REGIONS[region]
    x0, y0, x1, _y1 = box
    d = ImageDraw.Draw(img)
    card_frame(d, box)
    slug(d, x0, y0, x1, slugtxt, colour, 15, 9)
    sbox = (x0, y0 + 15, x1, y0 + 60)
    d = paint_scene(img, sbox, MINI_SCENES[key])
    badge(d, sbox[2], sbox[3], num, colour)
    y = y0 + 61
    for line in wrap(d, head, f_serif(13), x1 - x0 - 14)[:2]:
        d.text((x0 + 7, y), line, font=f_serif(13), fill=BLACK)
        y += 11
    d.text((x0 + 7, y0 + 88), src, font=f_med(8), fill=GREY)


# ---------------------------------------------------------------- header
def header(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 18], fill=BLACK)
    d.text((14, 3), "THE MERIDIAN WIRE · THE WORLD'S NEWS IN ONE PICTURE",
           font=f_sans(11), fill=WHITE)
    right = "36 STORIES · 21 CARDS · EVERY ONE DATED TODAY"
    d.text((W - 14 - d.textlength(right, font=f_sans(11)), 3), right,
           font=f_sans(11), fill=GOLD_TXT)
    # The date is the masthead.
    layer = Image.new("RGBA", (2300, 230), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((10, 10), "SUNDAY 22 NOVEMBER 2026",
                               font=f_serif(118), fill=BLACK + (255,))
    layer = layer.crop(layer.getbbox())
    glyph_h = layer.height
    layer = layer.resize((952, glyph_h), Image.LANCZOS)
    img.paste(layer, ((W - 952) // 2, 20), layer)
    # Subdeck: the three lead headlines, italic-sheared serif, one line.
    d = ImageDraw.Draw(img)
    sub = " · ".join(s[3] for s in LEADS)
    size = 19
    while size > 13 and d.textlength(sub, font=f_serif(size)) > 980:
        size -= 1
    sub_layer = Image.new("RGBA", (1100, 40), (0, 0, 0, 0))
    ImageDraw.Draw(sub_layer).text((16, 4), sub, font=f_serif(size),
                                   fill=BLACK + (255,))
    sub_layer = sub_layer.transform(sub_layer.size, Image.AFFINE,
                                    (1, 0.22, -9, 0, 1, 0),
                                    resample=Image.BICUBIC)
    sub_layer = sub_layer.crop(sub_layer.getbbox())
    img.paste(sub_layer, ((W - sub_layer.width) // 2, 111), sub_layer)
    d = ImageDraw.Draw(img)
    d.line([14, 131, W - 14, 131], fill=BLACK, width=2)
    slot_w = (W - 28) // 6
    for i, (when, what) in enumerate(TIMELINE):
        x = 14 + i * slot_w
        if i:
            d.line([x - 5, 137, x - 5, 153], fill=(190, 182, 164), width=1)
        d.text((x, 135), when, font=f_sans(10), fill=RED)
        d.text((x, 147), what, font=f_med(8), fill=GREY)
    d.line([14, 158, W - 14, 158], fill=(190, 182, 164), width=1)
    col_w = (W - 28) // 7
    for i, (big, cap) in enumerate(NUMBERS):
        x = 14 + i * col_w
        if i:
            d.line([x - 6, 164, x - 6, 198], fill=(190, 182, 164), width=1)
        d.text((x, 162), big, font=f_sans(38), fill=RED)
        d.text((x, 202), cap, font=f_med(8), fill=GREY)
    # Region tally: 16 px, labels inside, widths proportional to counts.
    total = sum(n for _name, n in TALLY)
    assert total == len(LEADS) + len(MINIS) + len(BRIEFS)
    tx = 14
    for name, count in TALLY:
        seg_w = round((W - 28) * count / total)
        colour = REGIONS[name]
        d.rectangle([tx, 214, tx + seg_w - 2, 230], fill=colour)
        label = f"{name} {count}"
        for sz in (9, 8):
            lf = f_sans(sz)
            if d.textlength(label, font=lf) <= seg_w - 8:
                d.text((tx + 4, 217 if sz == 9 else 218), label, font=lf,
                       fill=WHITE)
                break
        tx += seg_w
    return glyph_h


# ---------------------------------------------------------------- bottom
def pin_positions():
    pins = {}
    for s in LEADS:
        pins[s[0]] = (s[8], s[9], REGIONS[s[1]])
    for s in MINIS:
        pins[s[0]] = (s[7], s[8], REGIONS[s[1]])
    for i, b in enumerate(BRIEFS):
        pins[len(LEADS) + len(MINIS) + 1 + i] = (b[3], b[4], REGIONS[b[1]])
    return pins


def draw_map(img, box):
    x0, y0, x1, y1 = box
    pw, ph = x1 - x0, y1 - y0
    layer = Image.new("RGB", (pw, ph), MAP_SEA)
    d = ImageDraw.Draw(layer)
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
                d.polygon(pts, fill=MAP_LAND)
    for num, (lon, lat, colour) in sorted(pin_positions().items()):
        jlon = lon + ((num * 7) % 5 - 2) * 1.1
        jlat = lat + ((num * 3) % 5 - 2) * 0.9
        px_, py_ = project(jlon, jlat)
        r = 7
        d.ellipse([px_ - r, py_ - r, px_ + r, py_ + r], fill=colour,
                  outline=WHITE, width=1)
        t = str(num)
        tf = f_sans(8 if num >= 10 else 9)
        d.text((px_ - d.textlength(t, font=tf) / 2, py_ - 5), t, font=tf,
               fill=WHITE)
    d.text((8, ph - 18), "All 36 stories pinned by number",
           font=f_med(10), fill=BLACK)
    img.paste(layer, (x0, y0))


def bottom_zone(img):
    d = ImageDraw.Draw(img)
    d.text((14, 766), "WHERE IT HAPPENED · ALL 36 STORIES, PINNED BY NUMBER",
           font=f_sans(11), fill=BLACK)
    d.text((480, 766), "ALSO ON SUNDAY — 15 MORE STORIES",
           font=f_sans(11), fill=BLACK)
    draw_map(img, (14, 780, 470, 985))
    d = ImageDraw.Draw(img)
    yy = 780
    for i, (text, region, source, _lon, _lat) in enumerate(BRIEFS):
        num = len(LEADS) + len(MINIS) + 1 + i
        colour = REGIONS[region]
        cx, cy = 488, yy + 6
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=colour)
        t = str(num)
        tf = f_sans(7)
        d.text((cx - d.textlength(t, font=tf) / 2, cy - 4), t, font=tf,
               fill=WHITE)
        x = 502
        d.text((x, yy + 1), region, font=f_sans(9), fill=colour)
        x += d.textlength(region, font=f_sans(9)) + 6
        d.text((x, yy), f"{text} ({source})", font=f_med(10), fill=BODY)
        yy += 13
    d.rectangle([14, 989, 1010, 1022], outline=RED, width=2)
    rows = [("DATE CHECK · LEFT OUT", DC_LEFT), ("NOT YET", DC_NOTYET),
            ("UNCONFIRMED", DC_UNCONF)]
    ry = 992.0
    for label, body in rows:
        d.text((24, ry), label, font=f_sans(9), fill=RED)
        lw = d.textlength(label, font=f_sans(9))
        d.text((24 + lw + 8, ry), "— " + body, font=f_med(9), fill=BODY)
        ry += 10.5


# ---------------------------------------------------------------- compose
def compose():
    img = Image.new("RGB", (W, W), PAPER)
    glyph_h = header(img)
    lead_w = (W - 28 - 16) // 3
    for i, story in enumerate(LEADS):
        x = 14 + i * (lead_w + 8)
        lead_card(img, story, (x, 236, x + lead_w, 236 + 218))
    d = ImageDraw.Draw(img)
    d.text((14, 458), "MORE FROM SUNDAY · STORIES 4–21", font=f_sans(11),
           fill=RED)
    mini_w = (W - 28 - 40) // 6
    for r in range(3):
        for c in range(6):
            story = MINIS[r * 6 + c]
            x = 14 + c * (mini_w + 8)
            y = 472 + r * 98
            mini_card(img, story, (x, y, x + mini_w, y + 96))
    bottom_zone(img)
    return img, glyph_h


def colour_stats(img):
    """Step-2 sampling; colour = channel range > 70 AND max > 90."""
    rgb = img.convert("RGB")
    px = rgb.load()
    w, h = rgb.size

    def band(y0, y1):
        hit = tot = 0
        for yy in range(y0, y1, 2):
            for xx in range(0, w, 2):
                r, g, b = px[xx, yy]
                tot += 1
                if max(r, g, b) - min(r, g, b) > 70 and max(r, g, b) > 90:
                    hit += 1
        return 100.0 * hit / tot

    return band(0, h), band(470, 760)


def build(outdir=None):
    outdir = outdir or HERE
    img, glyph_h = compose()
    q = img.quantize(colors=256, method=Image.MEDIANCUT)
    entry_path = os.path.join(outdir, "entry.png")
    q.save(entry_path, optimize=True)
    size = os.path.getsize(entry_path)
    if size > 165_000:
        q = img.quantize(colors=192, method=Image.MEDIANCUT)
        q.save(entry_path, optimize=True)
        size = os.path.getsize(entry_path)
    img.resize((300, 300), Image.LANCZOS).save(
        os.path.join(outdir, "entry-300.png"))
    # Measure on the committed (quantised) image, as the board method does.
    committed = Image.open(entry_path)
    page_col, mid_col = colour_stats(committed)
    probe = ImageDraw.Draw(img)
    problems = []
    for s in LEADS:
        n = len(wrap(probe, s[3], f_serif(18), 306))
        m = len(wrap(probe, s[4], f_med(11), 306))
        print(f"lead {s[0]} headline_lines={n} deck_lines={m}")
        if n > 2 or m > 2:
            problems.append(s[0])
    for s in MINIS:
        n = len(wrap(probe, s[3], f_serif(13), 145))
        print(f"mini {s[0]} headline_lines={n}")
        if n > 2:
            problems.append(s[0])
    for i, b in enumerate(BRIEFS):
        width = (probe.textlength(b[1], font=f_sans(9)) + 6
                 + probe.textlength(f"{b[0]} ({b[2]})", font=f_med(10)))
        print(f"brief {22 + i} width={width:.0f}")
        if 502 + width > 1012:
            problems.append(f"brief{22 + i}")
    print(f"entry_bytes={size} masthead_glyph_h={glyph_h} "
          f"stories={len(LEADS) + len(MINIS) + len(BRIEFS)} "
          f"pictured={len(LEADS) + len(MINIS)} "
          f"tally_sum={sum(n for _nm, n in TALLY)} problems={problems}")
    print(f"colour_page={page_col:.2f}% colour_mid={mid_col:.2f}%")
    return size


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else None)
