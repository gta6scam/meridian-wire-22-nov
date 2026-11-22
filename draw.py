#!/usr/bin/env python3
"""The Meridian Wire — News Image 20261122 challenger for @yutulboy.

Wire-service front page built to the first-glance study rules:
R1 date-as-masthead, R2 red numbers strip in the top 22%, R3 three
pictorial lead scenes >=85px with in-strip data labels, R4 a data
strip on every card, R5 a source/certainty tag on every strip,
R6 one red accent, R7 the 300px thumbnail gate, R8 cream field.

All facts come only from POOL22-BARU (13 verified 22 Nov 2026 events
plus its named discards). Three layout variants of this one concept
are rendered; the duel winner (see DUEL.md) becomes entry.png and
the losers are kept in variants/ as cadangan banding.
Original code, written for this build.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mapdata import WORLD

W = H = 1024
RED = (178, 30, 32)
INK = (26, 24, 20)
PAPER = (247, 242, 231)
PAPER2 = (251, 248, 240)
GREY = (96, 90, 80)
NAVY = (22, 40, 63)

FD = os.path.join(HERE, "fonts")
def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)
def fb(size): return F("Archivo-Bold.ttf", size)
def fm(size): return F("Archivo-Medium.ttf", size)
def fp(size): return F("PlayfairDisplay-900.ttf", size)

# ---------------------------------------------------------------- data
CARDS = [
 dict(n=1, region="GULF · CONFLICT", rc=(150, 84, 30), tag="CLAIM · IRGC",
      head="IRGC claims hits on two US Patriot radars in Bahrain",
      deck="Tehran says missiles and drones hit radars at Al-Riffa and Awali; an industry site burned, a drone fell in Kuwait, a tanker was hit near Hormuz.",
      facts=5, kind="gulf", cap="BAHRAIN · KUWAIT · HORMUZ"),
 dict(n=2, region="NEW ZEALAND · CRICKET", rc=(30, 110, 76), tag="IANS / AFP",
      head="India declare on 720/9 — a Test record in New Zealand",
      deck="720/9 in 166 overs — highest Test total in NZ: Rahul 136, Pant 128, Gill 98. NZ 368 (Nicholls 175); India lead 352.",
      facts=7, kind="india", cap="WELLINGTON · DAY FOUR"),
 dict(n=3, region="CALIFORNIA · SPACE", rc=(40, 84, 150), tag="VSFB OFFICIAL",
      head="Falcon 9 to lift NROL-136 from Vandenberg Sunday",
      deck="Window 12:16–12:46 UTC from SLC-4E: the 15th NRO constellation batch, with Northrop Grumman; booster B1097 returns to LZ4.",
      facts=5, kind="falcon", cap="VANDENBERG SLC-4E · LZ4"),
 dict(n=4, region="MAKKAH · AIR DEFENCE", rc=(150, 84, 30), tag="CONFIRMED · ANADOLU",
      head="Coalition downs Houthi missile near Makkah",
      deck="Sirens at 23:43 Riyadh; intercept confirmed ~01:42 Sunday.",
      facts=2, kind="makkah", cap="MAKKAH REGION"),
 dict(n=5, region="ANTALYA · CLIMATE", rc=(30, 110, 76), tag="REUTERS",
      head="COP31 final text tabled in Antalya",
      deck="Final text tabled; approval plenary 06:00 GMT Sunday.",
      facts=2, kind="cop", cap="ANTALYA"),
 dict(n=6, region="MYANMAR · EARTHQUAKE", rc=(120, 70, 130), tag="NCS VIA ANI",
      head="M4.1 quake recorded in Myanmar",
      deck="Logged 02:35:57 IST 22 Nov; epicentre 24.404N 94.616E.",
      facts=3, kind="quake", cap="24.404N · 94.616E"),
 dict(n=7, region="LAS VEGAS · FORMULA 1", rc=(178, 30, 32), tag="FORMULA1.COM",
      head="Las Vegas GP: lights out 04:00 UTC",
      deck="Round 22 at the Strip Circuit: 20:00 Sat local, 50 laps.",
      facts=3, kind="vegas", cap="STRIP CIRCUIT"),
 dict(n=8, region="ENGLAND · PREMIER LEAGUE", rc=(40, 84, 150), tag="PREMIERLEAGUE.COM",
      head="Liverpool v Man United at Anfield",
      deck="Matchweek 11: Anfield 16:30 UTC; Hull v Brighton 14:00 UTC.",
      facts=3, kind="prem", cap="ANFIELD · MW11"),
 dict(n=9, region="TURIN · TENNIS", rc=(30, 110, 76), tag="ATP · REUTERS",
      head="Alcaraz v Zverev: ATP Finals title match",
      deck="Turin final Sun ~16:00 UTC; Alcaraz rallied past Shelton.",
      facts=2, kind="atp", cap="TURIN"),
 dict(n=10, region="FLORIDA · GOLF", rc=(30, 110, 76), tag="LPGA.COM · AP",
      head="A Lim Kim leads CME finale at −18",
      deck="Kim −18 leads Thitikul & Yoshida by 1 at Tiburón, Naples.",
      facts=3, kind="lpga", cap="TIBURÓN · NAPLES"),
 dict(n=11, region="FUKUOKA · SUMO", rc=(120, 70, 130), tag="JSA · DAY 14",
      head="Kyushu Basho: two men at 12-2",
      deck="Onosato & Wakamotoharu 12-2, Atamifuji 11-3; deciders set.",
      facts=3, kind="sumo", cap="FUKUOKA"),
 dict(n=12, region="GEORGIA · PGA TOUR", rc=(40, 84, 150), tag="REUTERS",
      head="Rain moves RSM round three to Sunday",
      deck="Sat washout moved R3 to Sun, final Mon; 3 share lead −9.",
      facts=3, kind="rsm", cap="RSM CLASSIC"),
 dict(n=13, region="USA · NFL", rc=(150, 84, 30), tag="ESPN / NFL",
      head="NFL Week 12: 11 Sunday games",
      deck="11 Sunday games (US): 13:00 ET early, SNF 20:20 ET.",
      facts=3, kind="nfl", cap="WEEK 12 · SUN (US)"),
]

NUMBERS = [  # (big, caption lines, card) — all bound to cards on the page
 ("720/9", "India's declared total,", "Wellington (2)"),
 ("2", "Patriot radars IRGC says", "it hit (1)"),
 ("12:16", "UTC — Falcon 9 window", "opens (3)"),
 ("$120bn", "adaptation target dropped", "at COP31 (5)"),
 ("M4.1", "Myanmar quake, 95 km", "deep (6)"),
 ("−18", "A Lim Kim's lead score,", "Naples (10)"),
 ("11", "NFL Sunday games,", "Week 12 (13)"),
]

TIMELINE = [  # 6 slots, all 22 Nov 2026 events
 ("OVERNIGHT", "IRGC claims Gulf strikes"),
 ("04:00 UTC", "Las Vegas GP lights out"),
 ("06:00 UTC", "COP31 approval plenary"),
 ("09:00 UTC", "Sumo deciders, Fukuoka"),
 ("12:16 UTC", "Falcon 9 window opens"),
 ("16:30 UTC", "Liverpool v Man United"),
]

BRIEFS = [  # 14..40 — each carries a name and/or number, pool facts only
 "14 Rahul 136 — top score in India's 720/9 at Wellington",
 "15 Pant 128 — the innings' second century, Wellington",
 "16 Gill 98 — out two runs short of a hundred",
 "17 Jaiswal 85 — fifty in the record 720/9 total",
 "18 Padikkal 80 — fifth fifty-plus score of the innings",
 "19 Nicholls 175 — New Zealand's lone stand in their 368",
 "20 Bumrah 4-92 — best figures of the Wellington match",
 "21 NFL early window — Sunday games start 13:00 ET",
 "22 NFL late window — kickoffs 16:05–16:25 ET Sunday",
 "23 Sunday night — Vikings @ 49ers, 20:20 ET",
 "24 Thorbjornsen — shares the RSM lead at −9",
 "25 Penge — shares the RSM lead at −9",
 "26 Neergaard-Petersen — shares the RSM lead at −9",
 "27 RSM Classic — final round pushed to Monday",
 "28 Onosato 12-2 — joint leader into senshuraku",
 "29 Wakamotoharu 12-2 — joint leader into senshuraku",
 "30 Atamifuji 11-3 — one win back at Fukuoka",
 "31 Yusho decider — Onosato v Hoshoryu, final day",
 "32 Yusho decider — Wakamotoharu v Atamifuji",
 "33 Thitikul −17 — one shot back at the CME finale",
 "34 Yoshida −17 — one shot back at the CME finale",
 "35 CME prize — $4m to the winner at Tiburón",
 "36 Bahrain — civil industry site ablaze, ministry says",
 "37 Kuwait — drone downed at Ali Al Salem, first since Sept",
 "38 Hormuz — tanker attacked near the strait (UKMTO)",
 "39 COP31 — objections to final text closed 03:00 GMT",
 "40 COP31 — third draft recalls Dubai fossil-fuel deal",
]

DATECHECK = ("Left out as NOT 22 Nov: Lviv strike (20 Nov) · Peru M6.9 quake (20/21 Nov) · "
 "3 missiles on Riyadh (21 Nov) · Saudi strike on Hodeidah (21 Nov) · CEPA signing (21 Nov) · "
 "France march of 82,500 (21 Nov) · ICJ ruling (19 Nov). Not yet: Davis Cup final (29 Nov).")

PINS = {1: (50.6, 26.2), 2: (174.8, -41.3), 3: (-120.6, 34.7), 4: (39.8, 21.4),
        5: (30.7, 36.9), 6: (94.6, 24.4), 7: (-115.2, 36.1), 8: (-2.96, 53.4),
        9: (7.7, 45.1), 10: (-81.8, 26.1), 11: (130.4, 33.6), 12: (-81.4, 31.2),
        13: (-122.0, 37.4)}
BRIEF_DOTS = [(174.8, -41.3), (174.8, -41.3), (-81.4, 31.2), (130.4, 33.6),
              (130.4, 33.6), (-81.8, 26.1), (50.6, 26.2), (45.0, 24.0),
              (30.7, 36.9), (-100.0, 38.0), (-122.0, 37.4), (55.0, 25.3)]

# ---------------------------------------------------------------- helpers
def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def chip(draw, x, y, text, fill, txt=(255, 255, 255), size=11, pad=7):
    f = fb(size)
    tw = draw.textlength(text, font=f)
    draw.rounded_rectangle([x, y, x + tw + pad * 2, y + size + 9], 5, fill=fill)
    draw.text((x + pad, y + 3), text, font=f, fill=txt)
    return tw + pad * 2

def caption_band(draw, box, text, tag, dark=NAVY):
    x0, y0, x1, y1 = box
    bh = 16
    draw.rectangle([x0, y1 - bh, x1, y1], fill=dark)
    draw.text((x0 + 7, y1 - bh + 3), text, font=fb(10), fill=(255, 255, 255))
    tf = fb(9)
    tw = draw.textlength(tag, font=tf)
    draw.text((x1 - tw - 7, y1 - bh + 4), tag, font=tf, fill=(255, 214, 120))

def grad(draw, box, top, bot, steps=24):
    x0, y0, x1, y1 = box
    h = y1 - y0
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        c = tuple(int(top[k] + (bot[k] - top[k]) * t0) for k in range(3))
        draw.rectangle([x0, y0 + int(h * t0), x1, y0 + int(h * t1) + 1], fill=c)

# ---------------------------------------------------------------- lead scenes
def scene_gulf(img, box, style):
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    grad(d, box, (16, 26, 52), (58, 74, 110))
    for sx, sy in [(30, 14), (90, 30), (180, 10), (250, 26), (60, 44), (300, 40)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(255, 255, 255, 200))
    sea_y = y0 + int(h * 0.72)
    d.rectangle([x0, sea_y, x1, y1], fill=(24, 52, 84))
    d.polygon([(x0, sea_y), (x0 + int(w * .42), sea_y - 16), (x0 + int(w * .55), sea_y), (x1, sea_y)], fill=(38, 44, 40))
    rx = x0 + int(w * .30)
    d.line([rx, sea_y - 14, rx, sea_y - 44], fill=(230, 230, 220), width=3)
    d.arc([rx - 26, sea_y - 66, rx + 26, sea_y - 14], 200, 340, fill=(240, 240, 230), width=4)
    d.line([rx, sea_y - 44, rx + 20, sea_y - 56], fill=(240, 240, 230), width=3)
    if style == "B":
        d.arc([rx + 96, sea_y - 58, rx + 140, sea_y - 16], 200, 340, fill=(170, 175, 185), width=3)
        d.line([rx + 118, sea_y - 16, rx + 118, sea_y - 40], fill=(170, 175, 185), width=3)
    fx = x0 + int(w * .47)
    d.ellipse([fx - 16, sea_y - 26, fx + 16, sea_y + 2], fill=(255, 120, 40, 190))
    d.ellipse([fx - 8, sea_y - 18, fx + 8, sea_y + 2], fill=(255, 190, 60, 220))
    for ox, oy, ex, ey in [(int(w * .06), 6, int(w * .30), int(h * .34)), (int(w * .16), 2, int(w * .44), int(h * .30))]:
        pts = []
        for i in range(21):
            t = i / 20
            pts.append((x0 + ox + (ex - ox) * t, y0 + oy + (ey - oy) * t + 52 * t * (1 - t)))
        d.line(pts, fill=(255, 170, 60), width=3)
        d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4], fill=(255, 220, 130))
    tx = x0 + int(w * .68)
    d.polygon([(tx, sea_y + 14), (tx + 96, sea_y + 14), (tx + 86, sea_y + 25), (tx + 10, sea_y + 25)], fill=(12, 14, 18))
    d.rectangle([tx + 14, sea_y + 5, tx + 60, sea_y + 14], fill=(70, 76, 84))
    d.rectangle([tx + 64, sea_y + 1, tx + 74, sea_y + 14], fill=(50, 54, 62))
    chip(d, x0 + 8, y0 + 8, "2 RADARS CLAIMED HIT", RED, size=11)
    d.text((x0 + 10, y0 + h - 38), "HORMUZ TANKER", font=fb(9), fill=(255, 255, 255))
    caption_band(d, box, CARDS[0]["cap"], CARDS[0]["tag"])

def scene_india(img, box, style):
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    grad(d, box, (120, 178, 120), (52, 128, 66))
    d.arc([x0 + 10, y0 - 46, x1 - 10, y0 + 66], 0, 180, fill=(235, 240, 235), width=3)
    for i in range(9):
        cx = x0 + 26 + i * (w - 52) // 8
        d.ellipse([cx, y0 + 12 + (i % 3) * 5, cx + 4, y0 + 16 + (i % 3) * 5], fill=(240, 240, 240, 170))
    px0, px1 = x0 + int(w * .40), x0 + int(w * .60)
    d.polygon([(px0, y1), (px0 + 16, y0 + 34), (px1 - 16, y0 + 34), (px1, y1)], fill=(216, 196, 148))
    for gx in (px0 + 22, px1 - 26):
        for s in range(3):
            d.line([gx + s * 5, y0 + 44, gx + s * 5, y0 + 62], fill=(250, 240, 200), width=2)
    bx, by = x0 + int(w * .47), y0 + int(h * .52)
    d.ellipse([bx - 6, by - 26, bx + 6, by - 14], fill=(20, 30, 60))
    d.line([bx, by - 14, bx - 4, by + 8], fill=(20, 30, 60), width=5)
    d.line([bx - 4, by + 8, bx - 14, by + 26], fill=(245, 245, 245), width=5)
    d.line([bx - 4, by + 8, bx + 12, by + 24], fill=(245, 245, 245), width=5)
    d.line([bx, by - 12, bx + 20, by - 2], fill=(20, 30, 60), width=4)
    d.line([bx + 18, by - 4, bx + 34, by - 22], fill=(150, 110, 60), width=4)
    d.ellipse([x0 + int(w * .70), y0 + 30, x0 + int(w * .70) + 7, y0 + 37], fill=(190, 30, 40))
    if style == "B":
        d.ellipse([x0 + 14, y0 + h - 44, x0 + 74, y0 + h - 30], outline=(255, 255, 255, 140), width=2)
        d.text((x0 + 22, y0 + h - 41), "BASIN RES.", font=fb(8), fill=(255, 255, 255, 200))
    chip(d, x0 + 8, y0 + 8, "720/9 DECLARED", RED, size=11)
    chip(d, x1 - 118, y0 + 8, "RAHUL 136", NAVY, size=11)
    caption_band(d, box, CARDS[1]["cap"], CARDS[1]["tag"])

def scene_falcon(img, box, style):
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    grad(d, box, (250, 196, 130), (120, 160, 210))
    gy = y0 + int(h * .78)
    d.rectangle([x0, gy, x1, y1], fill=(96, 92, 84))
    tx = x0 + int(w * .20)
    d.rectangle([tx - 5, y0 + 18, tx + 5, gy], fill=(60, 64, 70))
    for i in range(4):
        d.line([tx - 5, y0 + 26 + i * 16, tx + 26, y0 + 34 + i * 16], fill=(60, 64, 70), width=2)
    rx, ry = tx + 44, y0 + int(h * .20)
    d.polygon([(rx - 9, ry + 34), (rx - 9, ry), (rx, ry - 16), (rx + 9, ry), (rx + 9, ry + 34)], fill=(245, 245, 245))
    d.rectangle([rx - 9, ry + 22, rx + 9, ry + 27], fill=(30, 30, 34))
    d.polygon([(rx - 6, ry + 34), (rx + 6, ry + 34), (rx, ry + 50)], fill=(255, 150, 40))
    d.polygon([(rx - 3, ry + 34), (rx + 3, ry + 34), (rx, ry + 42)], fill=(255, 220, 120))
    pts = []
    for i in range(31):
        t = i / 30
        pts.append((rx + (w * .62) * t, ry - 104 * t * (1 - t) + (gy - 8 - ry) * t * t))
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=(255, 235, 170), width=2)
    lz = x0 + int(w * .84)
    d.ellipse([lz - 15, gy - 6, lz + 15, gy + 4], outline=(255, 255, 255), width=2)
    d.text((lz - 13, gy - 22), "LZ4", font=fb(11), fill=(255, 255, 255))
    if style == "B":
        d.ellipse([x0 + int(w * .55), y0 + 12, x0 + int(w * .55) + 26, y0 + 38], fill=(255, 240, 200, 160))
    chip(d, x0 + 8, y0 + 8, "12:16–12:46 UTC", RED, size=11)
    chip(d, x1 - 128, y0 + 8, "B1097 → LZ4", NAVY, size=11)
    caption_band(d, box, CARDS[2]["cap"], CARDS[2]["tag"])

# ---------------------------------------------------------------- mini devices (strip 30px, band takes bottom 12)
def dev_makkah(d, box):
    x0, y0, x1, y1 = box
    grad(d, box, (24, 34, 64), (70, 88, 130))
    pts = []
    for i in range(25):
        t = i / 24
        pts.append((x0 + 8 + (x1 - x0 - 66) * t, y0 + 15 - 13 * t * (1 - t) * 2.4 - 3 * t))
    d.line(pts, fill=(255, 170, 60), width=2)
    ex, ey = pts[-1]
    for dx, dy in [(0, -6), (6, -4), (7, 2), (-6, -4)]:
        d.line([ex, ey, ex + dx, ey + dy], fill=(255, 230, 150), width=2)
    d.text((x0 + 8, y0 + 2), "INTERCEPT 01:42", font=fb(9), fill=(255, 255, 255))

def dev_cop(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(232, 238, 230))
    cx, cy, r = x0 + 12, y0 + 9, 7
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    d.line([cx, cy, cx, cy - 5], fill=RED, width=2); d.line([cx, cy, cx + 4, cy + 2], fill=INK, width=2)
    d.text((x0 + 26, y0 + 0), "06:00 GMT PLENARY", font=fb(9), fill=INK)
    d.text((x0 + 26, y0 + 9), "$120bn FELL THU", font=fb(9), fill=RED)

def dev_quake(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(30, 30, 36))
    mid = y0 + 9
    pts, n = [], 40
    for i in range(n):
        t = i / (n - 1)
        amp = 1 + 8 * max(0.0, 1 - abs(t - .42) * 4)
        pts.append((x0 + 5 + (x1 - x0 - 86) * t, mid + (amp if i % 2 else -amp) * .8))
    d.line(pts, fill=(120, 230, 140), width=2)
    d.text((x1 - 70, y0 + 2), "M4.1", font=fb(12), fill=(255, 255, 255))

def dev_vegas(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(26, 24, 40))
    pts = [(x0 + 8, y0 + 14), (x0 + 34, y0 + 14), (x0 + 42, y0 + 3), (x0 + 66, y0 + 3),
           (x0 + 74, y0 + 15), (x0 + 96, y0 + 15), (x0 + 102, y0 + 5)]
    d.line(pts + [pts[0]], fill=(255, 210, 90), width=2)
    d.text((x1 - 66, y0 + 0), "50 LAPS", font=fb(11), fill=(255, 255, 255))
    d.text((x1 - 66, y0 + 10), "04:00 UTC", font=fb(8), fill=(255, 210, 120))

def dev_prem(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(52, 128, 66))
    d.rectangle([x0 + 6, y0 + 2, x0 + 56, y0 + 16], outline=(255, 255, 255), width=2)
    d.line([x0 + 31, y0 + 2, x0 + 31, y0 + 16], fill=(255, 255, 255), width=1)
    d.text((x0 + 64, y0 + 0), "16:30 ANFIELD", font=fb(9), fill=(255, 255, 255))
    d.text((x0 + 64, y0 + 9), "14:00 HULL", font=fb(9), fill=(230, 240, 230))

def dev_atp(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(36, 74, 120))
    d.rectangle([x0 + 6, y0 + 2, x0 + 56, y0 + 16], outline=(255, 255, 255), width=2)
    d.line([x0 + 31, y0 + 2, x0 + 31, y0 + 16], fill=(255, 255, 255), width=1)
    d.line([x0 + 6, y0 + 9, x0 + 56, y0 + 9], fill=(255, 255, 255), width=1)
    d.text((x0 + 64, y0 + 0), "FINAL · SUNDAY", font=fb(9), fill=(255, 255, 255))
    d.text((x0 + 64, y0 + 9), "≈16:00 UTC", font=fb(9), fill=(200, 220, 245))

def dev_lpga(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(238, 242, 236))
    d.text((x0 + 6, y0 + 2), "−18", font=fb(15), fill=RED)
    d.rectangle([x0 + 44, y0 + 6, x0 + 44 + 62, y0 + 12], fill=RED)
    d.rectangle([x0 + 44 + 58, y0 + 3, x0 + 44 + 60, y0 + 15], fill=NAVY)
    d.text((x0 + 112, y0 + 4), "$4M PRIZE", font=fb(9), fill=RED)

def dev_sumo(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(226, 208, 178))
    cx, cy = x0 + 13, y0 + 9
    d.ellipse([cx - 10, cy - 8, cx + 10, cy + 8], fill=(206, 184, 148), outline=(120, 90, 50), width=2)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(60, 50, 40))
    d.text((x0 + 30, y0 + 0), "12-2 · 12-2 · 11-3", font=fb(9), fill=INK)
    d.text((x0 + 30, y0 + 9), "YUSHO DECIDERS", font=fb(9), fill=GREY)

def dev_rsm(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(240, 244, 238))
    for i in range(3):
        yy = y0 + 2 + i * 5.5
        d.rectangle([x0 + 6, yy, x0 + 6 + 52, yy + 4], fill=(30, 110, 76) if i == 0 else (110, 155, 125))
    d.text((x0 + 66, y0 + 3), "3 LEADERS", font=fb(9), fill=INK)
    d.text((x1 - 46, y0 + 3), "−9 ×3", font=fb(12), fill=RED)

def dev_nfl(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(30, 44, 74))
    for r in range(2):
        for c in range(6):
            cx, cy = x0 + 10 + c * 11, y0 + 5 + r * 9
            d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 190, 80) if (r * 6 + c) < 11 else (90, 100, 130))
    d.text((x0 + 80, y0 + 0), "11 GAMES", font=fb(10), fill=(255, 255, 255))
    d.text((x0 + 80, y0 + 10), "SNF 20:20 ET", font=fb(8), fill=(255, 200, 120))

DEVICES = {"makkah": dev_makkah, "cop": dev_cop, "quake": dev_quake, "vegas": dev_vegas,
           "prem": dev_prem, "atp": dev_atp, "lpga": dev_lpga, "sumo": dev_sumo,
           "rsm": dev_rsm, "nfl": dev_nfl}
SCENES = {"gulf": scene_gulf, "india": scene_india, "falcon": scene_falcon}

# ---------------------------------------------------------------- cards
def shadow(img, box):
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x0 + 4, y0 + 5, x1 + 4, y1 + 5], 6, fill=(40, 32, 20, 110))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(4))).convert("RGB"), (0, 0))

def card_frame(img, box, style, rc):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    if style == "B":
        shadow(img, box)
        d.rounded_rectangle(box, 6, fill=PAPER2, outline=(190, 180, 160), width=1)
    else:
        d.rectangle(box, fill=PAPER2)
        d.line([x0, y0, x1, y0], fill=rc, width=3)
        d.line([x0, y1, x1, y1], fill=(200, 192, 172), width=1)

def lead_card(img, card, box, style, scene_h, head_pitch=22, deck_pitch=14):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    card_frame(img, box, style, card["rc"])
    d.text((x0 + 10, y0 + 5), f"{card['n']}  {card['region']}", font=fb(11), fill=card["rc"])
    sbox = (x0 + 8, y0 + 23, x1 - 8, y0 + 23 + scene_h)
    SCENES[card["kind"]](img, sbox, style)
    d = ImageDraw.Draw(img)
    hy = sbox[3] + 6
    for ln in wrap(d, card["head"], fb(19), x1 - x0 - 20):
        d.text((x0 + 10, hy), ln, font=fb(19), fill=INK); hy += head_pitch
    hy += 3
    for ln in wrap(d, card["deck"], fm(12), x1 - x0 - 20):
        d.text((x0 + 10, hy), ln, font=fm(12), fill=(52, 48, 42)); hy += deck_pitch

def mini_card(img, card, box, style):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    card_frame(img, box, style, card["rc"])
    d.text((x0 + 8, y0 + 4), f"{card['n']}  {card['region']}", font=fb(9), fill=card["rc"])
    sbox = (x0 + 6, y0 + 15, x1 - 6, y0 + 45)
    DEVICES[card["kind"]](d, sbox)
    d = ImageDraw.Draw(img)
    d.rectangle([sbox[0], sbox[3] - 12, sbox[2], sbox[3]], fill=NAVY)
    d.text((sbox[0] + 5, sbox[3] - 10), card["cap"], font=fb(8), fill=(255, 255, 255))
    tf = fb(8); tw = d.textlength(card["tag"], font=tf)
    d.text((sbox[2] - tw - 5, sbox[3] - 10), card["tag"], font=tf, fill=(255, 214, 120))
    hy = sbox[3] + 4
    for ln in wrap(d, card["head"], fb(14), x1 - x0 - 16)[:2]:
        d.text((x0 + 8, hy), ln, font=fb(14), fill=INK); hy += 15
    hy += 1
    for ln in wrap(d, card["deck"], fm(12), x1 - x0 - 16)[:2]:
        d.text((x0 + 8, hy), ln, font=fm(12), fill=(52, 48, 42)); hy += 12

# ---------------------------------------------------------------- header
def header(img, style):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 20], fill=INK)
    d.text((14, 4), "THE MERIDIAN WIRE · THE WORLD'S NEWS IN ONE PICTURE", font=fb(11), fill=(255, 255, 255))
    rt = "40 STORIES · 13 CARDS · EVERY ONE DATED TODAY"
    d.text((W - 14 - d.textlength(rt, font=fb(11)), 4), rt, font=fb(11), fill=(255, 214, 120))
    # R1: the DATE is the masthead. Rendered as its own layer at full
    # glyph height (88px ink) and condensed horizontally to 952px wide
    # (93% of page) so the caps stay >=80px tall AND >=90% wide.
    layer = Image.new("RGBA", (2200, 220), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((10, 10), "SUNDAY 22 NOVEMBER 2026", font=fp(118), fill=INK + (255,))
    layer = layer.crop(layer.getbbox())
    glyph_h = layer.height
    layer = layer.resize((952, glyph_h), Image.LANCZOS)
    if style == "B":
        sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        sh.paste((150, 40, 40, 120), (0, 0), layer)
        img.paste(sh, ((W - 952) // 2 + 3, 29), sh)
    img.paste(layer, ((W - 952) // 2, 26), layer)
    d = ImageDraw.Draw(img)
    d.line([14, 120, W - 14, 120], fill=INK, width=2)
    # UTC timeline — 6 slots, all 22 Nov events
    sw = (W - 28) // 6
    for i, (t, ev) in enumerate(TIMELINE):
        x = 14 + i * sw
        if i: d.line([x - 5, 128, x - 5, 148], fill=(190, 182, 164), width=1)
        d.text((x, 126), t, font=fb(12), fill=RED)
        d.text((x, 141), ev, font=fm(9), fill=GREY)
    d.line([14, 156, W - 14, 156], fill=(190, 182, 164), width=1)
    # R2: numbers strip in the top 22% — digit ink 30px, single red accent
    nw = (W - 28) // 7
    for i, (big, c1, c2) in enumerate(NUMBERS):
        x = 14 + i * nw
        if i: d.line([x - 6, 162, x - 6, 202], fill=(190, 182, 164), width=1)
        d.text((x, 160), big, font=fb(38), fill=RED)
        d.text((x, 202), c1, font=fm(9), fill=GREY)
        d.text((x, 213), c2, font=fm(9), fill=GREY)
    return 224, glyph_h

# ---------------------------------------------------------------- bottom
def draw_map(img, box):
    # rendered on its own layer and pasted, so high-latitude polygons
    # are clipped to the panel and can never paint over other zones
    x0, y0, x1, y1 = box
    layer = Image.new("RGB", (x1 - x0, y1 - y0), (26, 52, 44))
    d = ImageDraw.Draw(layer)
    mx0, my0, mx1, my1 = 8, 6, (x1 - x0) - 8, (y1 - y0) - 24
    def proj(lon, lat):
        return (mx0 + (lon + 180) / 360 * (mx1 - mx0), my0 + (58 - lat) / 118 * (my1 - my0))
    for name, s in WORLD.items():
        for ring in s.split("|"):
            pts = []
            for pair in ring.split(","):
                lo, la = pair.split(":")
                pts.append(proj(float(lo), float(la)))
            if len(pts) > 2:
                d.polygon(pts, fill=(74, 122, 92))
    for lon, lat in BRIEF_DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=(210, 200, 170))
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=CARDS[n - 1]["rc"], outline=(255, 255, 255), width=1)
        t = str(n); tf = fb(10)
        d.text((px - d.textlength(t, font=tf) / 2, py - 6), t, font=tf, fill=(255, 255, 255))
    d.text((8, (y1 - y0) - 19), "Numbered pins = the 13 cards · small dots = the briefs", font=fm(10), fill=(235, 240, 230))
    img.paste(layer, (x0, y0))

def bottom(img, y, swapped=False):
    d = ImageDraw.Draw(img)
    map_box = (14, y, 520, y + 292) if not swapped else (504, y, 1010, y + 292)
    al_box = (534, y, 1010, y + 292) if not swapped else (14, y, 490, y + 292)
    d.text((map_box[0], y), "WHERE IT HAPPENED", font=fb(13), fill=INK)
    draw_map(img, (map_box[0], y + 18, map_box[2], map_box[3]))
    d = ImageDraw.Draw(img)
    ax0 = al_box[0]
    d.text((ax0, y), "ALSO ON SUNDAY — 27 MORE STORIES", font=fb(13), fill=INK)
    yy = y + 21
    for b in BRIEFS:
        num, rest = b.split(" ", 1)
        d.text((ax0, yy), num, font=fb(10), fill=RED)
        d.text((ax0 + 24, yy), rest, font=fm(10), fill=(52, 48, 42))
        yy += 10.2
    dy = y + 300
    d.rectangle([14, dy, 1010, dy + 32], outline=RED, width=2)
    d.text((24, dy + 10), "DATE CHECK", font=fb(11), fill=RED)
    for j, ln in enumerate(wrap(d, DATECHECK, fm(10), 850)):
        d.text((118, dy + 4 + j * 12), ln, font=fm(10), fill=(52, 48, 42))
    fy = dy + 40
    left = "Every story happened, or was first reported, on Sunday 22 November 2026. Contested claims are attributed as claims."
    d.text((14, fy), left, font=fm(10), fill=GREY)
    rt = "Sources named on each card · Original drawings"
    d.text((W - 14 - d.textlength(rt, font=fm(10)), fy), rt, font=fm(10), fill=GREY)

# ---------------------------------------------------------------- composers
def compose_A(style="A"):
    img = Image.new("RGB", (W, H), PAPER)
    y, gh = header(img, style)
    cw = (W - 28 - 16) // 3
    for i, card in enumerate(CARDS[:3]):
        lead_card(img, card, (14 + i * (cw + 8), y, 14 + i * (cw + 8) + cw, y + 216), style, 92)
    my = y + 224
    mw = (W - 28 - 32) // 5
    for r in range(2):
        for c in range(5):
            mini_card(img, CARDS[3 + r * 5 + c], (14 + c * (mw + 8), my + r * 108, 14 + c * (mw + 8) + mw, my + r * 108 + 106), style)
    bottom(img, my + 224)
    return img, gh

def compose_C(style="C"):
    img = Image.new("RGB", (W, H), PAPER)
    y, gh = header(img, style)
    # asymmetric hero row: wide Gulf lead, narrower India + Falcon
    lead_card(img, CARDS[0], (14, y, 474, y + 228), style, 120, head_pitch=20, deck_pitch=13)
    lead_card(img, CARDS[1], (482, y, 744, y + 228), style, 92, head_pitch=20, deck_pitch=13)
    lead_card(img, CARDS[2], (752, y, 1010, y + 228), style, 92, head_pitch=20, deck_pitch=13)
    my = y + 228
    mw = (W - 28 - 32) // 5
    for r in range(2):
        for c in range(5):
            mini_card(img, CARDS[3 + r * 5 + c], (14 + c * (mw + 8), my + r * 108, 14 + c * (mw + 8) + mw, my + r * 108 + 106), style)
    bottom(img, my + 220, swapped=True)
    return img, gh

WINNER = "A"  # R7 duel verdict — see variants/DUEL.md

def render(style):
    return compose_C("C") if style == "C" else compose_A(style)

def save_entry(img, path):
    q = img.quantize(colors=256, method=Image.MEDIANCUT)
    q.save(path, optimize=True)
    if os.path.getsize(path) > 165_000:
        q = img.quantize(colors=192, method=Image.MEDIANCUT)
        q.save(path, optimize=True)
    return os.path.getsize(path)

def build(outdir=None):
    outdir = outdir or HERE
    os.makedirs(os.path.join(outdir, "variants"), exist_ok=True)
    imgs, glyph = {}, {}
    for s in ("A", "B", "C"):
        imgs[s], glyph[s] = render(s)
    size = save_entry(imgs[WINNER], os.path.join(outdir, "entry.png"))
    imgs[WINNER].resize((300, 300), Image.LANCZOS).save(os.path.join(outdir, "entry-300.png"))
    for s in ("A", "B", "C"):
        if s != WINNER:
            save_entry(imgs[s], os.path.join(outdir, "variants", f"variant-{s}.png"))
            imgs[s].resize((300, 300), Image.LANCZOS).save(os.path.join(outdir, "variants", f"variant-{s}-300.png"))
    print(f"winner={WINNER} entry_bytes={size} glyph_h={glyph}")
    return size, glyph

if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else None)
