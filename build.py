"""Build entry.png: front page of world news for Wednesday 18 November 2026 (v3).

Layout: dated masthead, one large lead story (APEC in Shenzhen), 10 illustrated
story cards, a labelled world map with numbered pins, and briefs by region.
Run locally (needs Pillow and Windows system fonts): python build.py
Sources for every item are listed in SOURCES.md.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONTS = "C:/Windows/Fonts/"
INK = (24, 22, 20)
PAPER = (247, 242, 230)
CARD = (255, 253, 247)
RED = (178, 30, 30)
NAVY = (26, 50, 94)
GREY = (90, 85, 80)
SEA = (196, 220, 238)
LAND = (222, 206, 160)
WHITE = (255, 255, 255)
SKY = (214, 232, 246)
SKIN = (232, 192, 152)


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


F_MAST = font("georgiab.ttf", 46)
F_DATE = font("arialbd.ttf", 21)
F_TAG = font("arialbd.ttf", 13)
F_HEAD = font("arialbd.ttf", 19)
F_HERO = font("arialbd.ttf", 27)
F_SUB = font("arial.ttf", 13)
F_HSUB = font("arial.ttf", 15)
F_REG = font("arialbd.ttf", 13)
F_BRIEF = font("arial.ttf", 12)
F_PIN = font("arialbd.ttf", 12)
F_MAPL = font("arialbd.ttf", 10)
F_NAME = font("arialbd.ttf", 12)
F_FOOT = font("arial.ttf", 12)

HERO = ("CHINA · APEC SUMMIT", "SHENZHEN", "Xi welcomes Trump to APEC with a rare hug",
        "Xi holds talks with Putin before first three-way summit with Trump", (114, 22))

# (tag, big fact, headline, subline, icon, panel colour, (lon, lat) for the map pin)
CARDS = [
    ("EUROPE · UKRAINE", "€45bn", "EU proposes loan to keep Kyiv afloat",
     "Backed by joint EU borrowing", "euro", (222, 230, 245), (4, 50)),
    ("GAZA", "TANKS IN", "Israel crosses Gaza ceasefire line",
     "First such push since 2025 truce", "tank", (240, 226, 196), (34, 31)),
    ("WALL STREET", "-561", "Dow falls 1.1% to 50,198 points",
     "S&P 500 down 5th day; Nvidia swings", "chart", (232, 232, 232), (-74, 41)),
    ("VENEZUELA", "DEAL", "US and Venezuela restore military ties",
     "Hegseth signs pact in Caracas", "flags", SKY, (-67, 10)),
    ("COP31 · TURKIYE", "DEADLOCK", "UN climate talks stall in Antalya",
     "Countries launch 'climate reality check'", "globe", (226, 240, 222), (31, 37)),
    ("US SENATE", "FLIPPED", "Democrat Peltola wins Alaska seat",
     "Unseats Republican Dan Sullivan", "ballot", (226, 232, 244), (-150, 62)),
    ("TECH", "OUTAGE", "Apple Pay, iCloud and Gmail disrupted",
     "NSA internal network also down", "cloud", (230, 230, 240), (-122, 37)),
    ("GOLD", "$3,742", "Gold hits lowest price in over a year",
     "Worry for African gold producers", "gold", (246, 238, 214), (28, -26)),
    ("UK ECONOMY", "3.6%", "UK inflation rises as fuel prices climb",
     "Petrol and diesel costs up", "pound", (236, 228, 236), (-1, 52)),
    ("IRAQ · TURKEY", "OIL FLOWS", "Iraq pumps oil to Turkey after 12 years",
     "Route avoids Hormuz disruption", "barrel", (240, 232, 218), (44, 35)),
]

BRIEFS = [
    ("EUROPE", ["Deutsche Bank 15M-file leak probed", "Rally against Slovak PM Fico",
                "146,000 protest across France", "Record rain in Portugal", "Court probes Julio Iglesias"]),
    ("N. AMERICA", ["Jeffries wins 251 votes in Speaker bid", "Russian spy suspect held",
                    "Waymo pulls robotaxis off highways", "Trump must testify in BBC case",
                    "Warner, Paramount TV merge"]),
    ("LATIN AM.", ["Bukele strikes Haiti gang boss's home", "Ecuador fishermen sue US over strike",
                   "Brazil probes vote-meddling claim", "Mexico asks Xi for a panda",
                   "Hegseth heads on to Colombia"]),
    ("MIDEAST", ["Kahana elected Knesset speaker", "Iran army vows 'more crushing' reply",
                 "Activist Nabeel Rajab dies at 62", "UN: health crisis in Taiz, Yemen",
                 "Israel delays E1 settlement contracts"]),
    ("AFRICA", ["S. Africa mercenary case", "Medieval cathedral floor found in Sudan",
                "Amnesty: probe RSF drone strikes", "Nigeria frees 15 hostages",
                "Kenya antibiotic rules"]),
    ("S. ASIA", ["Bangladesh police clash with workers", "62 students hit by toxic gas, Kerala",
                 "Militant commander killed, Kashmir", "Pakistan pushes TAPI pipeline",
                 "India signs Rs 1,976cr IAI deal"]),
    ("ASIA-PAC", ["AI cheating scandal hits Korea exams", "Takaichi invites Lee to Japan",
                  "M5.8 quake near Madang, PNG", "Hanson: cut refugee intake 90%",
                  "Albanese arrives in Shenzhen"]),
]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-95, 72), (-80, 62), (-60, 50), (-80, 30), (-81, 25), (-97, 18), (-105, 22),
     (-117, 32), (-125, 48), (-150, 60)],
    [(-55, 60), (-20, 70), (-30, 82), (-70, 78)],
    [(-80, 10), (-60, 8), (-35, -7), (-40, -22), (-58, -38), (-70, -55), (-75, -40), (-72, -15), (-81, -3)],
    [(-10, 36), (-9, 44), (-5, 48), (5, 52), (8, 57), (25, 70), (40, 68), (45, 45), (28, 40), (15, 38)],
    [(-6, 50), (2, 51), (-3, 59), (-7, 56)],
    [(-17, 15), (-5, 35), (10, 37), (32, 31), (43, 12), (51, 11), (40, -15), (32, -28), (20, -35), (12, -18),
     (9, 4), (-8, 5)],
    [(45, 45), (40, 68), (70, 73), (110, 76), (140, 72), (170, 66), (142, 50), (122, 30), (108, 20), (100, 8),
     (80, 8), (72, 20), (57, 25), (48, 30), (35, 32), (28, 40)],
    [(114, -22), (130, -12), (142, -11), (153, -27), (146, -39), (135, -34), (115, -34)],
    [(130, 31), (141, 36), (142, 43), (138, 38)],
]
MAP_LABELS = [("N. AMERICA", (-110, 52)), ("S. AMERICA", (-60, -25)), ("EUROPE", (20, 63)),
              ("AFRICA", (18, 0)), ("ASIA", (95, 58)), ("OCEANIA", (134, -30))]

WARN = []


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def fit(d, text, name, size, width):
    while size > 12 and d.textlength(text, font=font(name, size)) > width:
        size -= 1
    return font(name, size)


def star(d, cx, cy, r, fill):
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.42
        a = -math.pi / 2 + math.pi * k / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


# ---------- flags ----------

def flag_china(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK)
    star(d, x + w * 0.24, y + h * 0.34, h * 0.24, (255, 222, 0))


def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE)
    hh = h / 7
    for k in range(0, 7, 2):
        d.rectangle([x, y + k * hh, x + w, y + (k + 1) * hh], fill=RED)
    d.rectangle([x, y, x + w * 0.42, y + 4 * hh], fill=NAVY)
    d.rectangle([x, y, x + w, y + h], outline=INK)


def flag_russia(d, x, y, w, h):
    for k, col in enumerate([WHITE, (0, 57, 166), (213, 43, 30)]):
        d.rectangle([x, y + k * h / 3, x + w, y + (k + 1) * h / 3], fill=col)
    d.rectangle([x, y, x + w, y + h], outline=INK)


def flag_venezuela(d, x, y, w, h):
    for k, col in enumerate([(250, 205, 0), (0, 50, 140), (205, 20, 40)]):
        d.rectangle([x, y + k * h / 3, x + w, y + (k + 1) * h / 3], fill=col)
    d.rectangle([x, y, x + w, y + h], outline=INK)


# ---------- the lead illustration: tarmac welcome in Shenzhen ----------

def person(d, cx, base, suit, tie, hair):
    d.rectangle([cx - 16, base - 62, cx + 16, base - 4], fill=suit, outline=INK, width=2)
    d.polygon([(cx - 4, base - 62), (cx + 4, base - 62), (cx, base - 40)], fill=tie)
    d.rectangle([cx - 15, base - 4, cx - 3, base], fill=INK)
    d.rectangle([cx + 3, base - 4, cx + 15, base], fill=INK)
    d.ellipse([cx - 13, base - 90, cx + 13, base - 62], fill=SKIN, outline=INK, width=2)
    d.chord([cx - 13, base - 92, cx + 13, base - 70], 180, 360, fill=hair)


def hero_art(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h * 0.7, x + w, y + h], fill=(150, 150, 150))
    d.line([x, y + h * 0.84, x + w, y + h * 0.84], fill=WHITE, width=3)
    # Air Force One on the tarmac
    px, py = x + w * 0.58, y + h * 0.46
    d.rounded_rectangle([px - 70, py - 9, px + 80, py + 9], radius=9, fill=WHITE, outline=INK, width=2)
    d.line([px - 66, py - 1, px + 76, py - 1], fill=(70, 120, 190), width=4)
    d.polygon([(px - 10, py), (px + 30, py), (px - 30, py + 32), (px - 44, py + 32)], fill=(225, 225, 230),
              outline=INK)
    d.polygon([(px - 70, py - 8), (px - 58, py - 8), (px - 70, py - 36), (px - 80, py - 36)], fill=(70, 120, 190),
              outline=INK)
    for k in range(8):
        d.ellipse([px - 40 + k * 13, py - 6, px - 35 + k * 13, py - 1], fill=NAVY)
    d.line([px + 64, py + 9, px + 64, y + h * 0.7], fill=INK, width=2)
    d.line([px - 20, py + 9, px - 20, y + h * 0.7], fill=INK, width=2)
    # host and guest flags
    for k, fl in enumerate([flag_china, flag_us, flag_russia]):
        fx = x + 10 + k * 44
        d.line([fx, y + 8, fx, y + h * 0.72], fill=INK, width=3)
        fl(d, fx + 2, y + 10, 36, 22)
    # Xi and Trump embrace, with name labels
    base = y + h * 0.96
    lx = x + w * 0.3
    person(d, lx, base, (40, 40, 48), RED, (30, 30, 30))
    person(d, lx + 30, base, NAVY, (200, 30, 40), (232, 200, 120))
    d.line([lx + 8, base - 50, lx + 24, base - 46], fill=(40, 40, 48), width=7)
    d.line([lx + 22, base - 54, lx + 6, base - 50], fill=NAVY, width=7)
    for nm, dx in (("XI", -30), ("TRUMP", 64)):
        tx = lx + dx
        d.rounded_rectangle([tx - 26, base - 114, tx + 26, base - 97], radius=4, fill=WHITE, outline=INK)
        d.text((tx, base - 105), nm, font=F_NAME, fill=INK, anchor="mm")
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


# ---------- card icons: each drawn inside box (x, y, s) ----------

def icon_euro(d, x, y, s):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 60, 150), outline=INK, width=3)
    for k in range(12):
        a = 2 * math.pi * k / 12
        star(d, cx + r * 0.78 * math.cos(a), cy + r * 0.78 * math.sin(a), 4, (250, 210, 40))
    d.text((cx, cy), "€", font=font("arialbd.ttf", int(s * 0.42)), fill=(250, 210, 40), anchor="mm")


def icon_tank(d, x, y, s):
    d.rectangle([x + 4, y + s * 0.5, x + s - 4, y + s * 0.74], fill=(95, 105, 70), outline=INK, width=2)
    d.rectangle([x + s * 0.26, y + s * 0.32, x + s * 0.64, y + s * 0.51], fill=(110, 120, 80), outline=INK, width=2)
    d.line([x + s * 0.6, y + s * 0.4, x + s - 1, y + s * 0.3], fill=INK, width=5)
    for k in range(5):
        wx = x + 12 + k * (s - 24) / 4
        d.ellipse([wx - 6, y + s * 0.74 - 4, wx + 6, y + s * 0.74 + 8], fill=GREY, outline=INK)
    d.line([x, y + s * 0.95, x + s, y + s * 0.95], fill=(230, 190, 40), width=5)


def icon_chart(d, x, y, s):
    d.rectangle([x + 2, y + 2, x + s - 2, y + s - 2], fill=WHITE, outline=INK, width=2)
    for k in range(1, 4):
        d.line([x + 4, y + s * k / 4, x + s - 4, y + s * k / 4], fill=(220, 220, 220))
    pts = [(x + 8, y + s * 0.25), (x + s * 0.3, y + s * 0.38), (x + s * 0.45, y + s * 0.32),
           (x + s * 0.65, y + s * 0.6), (x + s * 0.8, y + s * 0.55), (x + s - 12, y + s * 0.82)]
    d.line(pts, fill=RED, width=5)
    ex, ey = pts[-1]
    d.polygon([(ex - 4, ey + 9), (ex + 9, ey - 5), (ex - 12, ey - 8)], fill=RED)


def icon_flags(d, x, y, s):
    flag_us(d, x + 2, y + 6, s * 0.5, s * 0.34)
    flag_venezuela(d, x + s * 0.48, y + s * 0.56, s * 0.5, s * 0.34)
    d.line([x + s * 0.2, y + s * 0.84, x + s * 0.42, y + s * 0.5], fill=INK, width=3)
    d.ellipse([x + s * 0.36, y + s * 0.44, x + s * 0.48, y + s * 0.56], fill=SKIN, outline=INK)


def icon_globe(d, x, y, s):
    cx, cy, r = x + s * 0.4, y + s / 2, s * 0.38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(80, 150, 210), outline=INK, width=2)
    d.polygon([(cx - r * 0.6, cy - r * 0.4), (cx - r * 0.1, cy - r * 0.6), (cx, cy), (cx - r * 0.5, cy + r * 0.3)],
              fill=(90, 160, 80))
    d.polygon([(cx + r * 0.2, cy + r * 0.1), (cx + r * 0.7, cy - r * 0.1), (cx + r * 0.5, cy + r * 0.6)],
              fill=(90, 160, 80))
    tx = x + s * 0.88
    d.rounded_rectangle([tx - 6, y + 4, tx + 6, y + s - 16], radius=6, fill=WHITE, outline=INK, width=2)
    d.rectangle([tx - 2, y + s * 0.35, tx + 2, y + s - 16], fill=RED)
    d.ellipse([tx - 10, y + s - 24, tx + 10, y + s - 4], fill=RED, outline=INK)


def icon_ballot(d, x, y, s):
    d.rectangle([x + 6, y + s * 0.45, x + s - 6, y + s - 2], fill=(240, 240, 240), outline=INK, width=3)
    d.rectangle([x + s * 0.3, y + s * 0.45, x + s * 0.7, y + s * 0.5], fill=INK)
    d.rectangle([x + s * 0.3, y + 4, x + s * 0.7, y + s * 0.47], fill=WHITE, outline=INK, width=2)
    d.line([x + s * 0.37, y + s * 0.24, x + s * 0.46, y + s * 0.36, x + s * 0.63, y + s * 0.12], fill=NAVY, width=4)
    d.text((x + s / 2, y + s * 0.74), "AK", font=font("arialbd.ttf", 19), fill=NAVY, anchor="mm")


def icon_cloud(d, x, y, s):
    c = (180, 190, 205)
    d.ellipse([x + 2, y + s * 0.35, x + s * 0.5, y + s * 0.78], fill=c, outline=INK, width=2)
    d.ellipse([x + s * 0.28, y + s * 0.18, x + s * 0.8, y + s * 0.72], fill=c, outline=INK, width=2)
    d.ellipse([x + s * 0.55, y + s * 0.38, x + s - 2, y + s * 0.78], fill=c, outline=INK, width=2)
    d.rectangle([x + s * 0.2, y + s * 0.5, x + s * 0.8, y + s * 0.77], fill=c)
    d.line([x + s * 0.36, y + s * 0.38, x + s * 0.64, y + s * 0.7], fill=RED, width=7)
    d.line([x + s * 0.64, y + s * 0.38, x + s * 0.36, y + s * 0.7], fill=RED, width=7)


def icon_gold(d, x, y, s):
    gold, dark = (225, 180, 40), (150, 110, 20)

    def bar(bx, by, w, h):
        d.polygon([(bx, by + h), (bx + w, by + h), (bx + w - 8, by), (bx + 8, by)], fill=gold, outline=dark)
    bar(x + 2, y + s * 0.66, s * 0.46, s * 0.24)
    bar(x + s * 0.5, y + s * 0.66, s * 0.46, s * 0.24)
    bar(x + s * 0.26, y + s * 0.42, s * 0.46, s * 0.24)
    d.line([x + s * 0.8, y + 2, x + s * 0.8, y + s * 0.26], fill=RED, width=5)
    d.polygon([(x + s * 0.8 - 9, y + s * 0.22), (x + s * 0.8 + 9, y + s * 0.22), (x + s * 0.8, y + s * 0.36)],
              fill=RED)


def icon_pound(d, x, y, s):
    d.rectangle([x + s * 0.06, y + s * 0.5, x + s * 0.3, y + s * 0.95], fill=(60, 60, 64), outline=INK)
    d.rectangle([x + s * 0.09, y + s * 0.55, x + s * 0.27, y + s * 0.68], fill=(250, 220, 120))
    d.line([x + s * 0.3, y + s * 0.7, x + s * 0.42, y + s * 0.62], fill=INK, width=3)
    d.ellipse([x + s * 0.36, y + s * 0.08, x + s * 0.8, y + s * 0.52], fill=(205, 205, 210), outline=INK, width=3)
    d.text((x + s * 0.58, y + s * 0.3), "£", font=font("arialbd.ttf", int(s * 0.34)), fill=INK, anchor="mm")
    d.line([x + s * 0.9, y + s * 0.92, x + s * 0.9, y + s * 0.18], fill=RED, width=5)
    d.polygon([(x + s * 0.9 - 9, y + s * 0.22), (x + s * 0.9 + 9, y + s * 0.22), (x + s * 0.9, y + s * 0.06)],
              fill=RED)


def icon_barrel(d, x, y, s):
    d.rounded_rectangle([x + 4, y + s * 0.12, x + s * 0.46, y + s * 0.9], radius=8, fill=(40, 40, 44), outline=INK)
    for f in (0.32, 0.7):
        d.line([x + 4, y + s * f, x + s * 0.46, y + s * f], fill=(120, 120, 130), width=3)
    d.rectangle([x + s * 0.46, y + s * 0.55, x + s - 2, y + s * 0.67], fill=GREY, outline=INK)
    d.polygon([(x + s - 2, y + s * 0.48), (x + s - 2, y + s * 0.74), (x + s - 14, y + s * 0.61)], fill=RED)
    d.polygon([(x + s * 0.74, y + s * 0.16), (x + s * 0.66, y + s * 0.34), (x + s * 0.74, y + s * 0.42),
               (x + s * 0.82, y + s * 0.34)], fill=INK)


ICONS = dict(euro=icon_euro, tank=icon_tank, chart=icon_chart, flags=icon_flags, globe=icon_globe,
             ballot=icon_ballot, cloud=icon_cloud, gold=icon_gold, pound=icon_pound, barrel=icon_barrel)


def draw_map(d, x0, y0, w, h, pins):
    lon0, lon1, lat0, lat1 = -170, 180, -50, 80

    def p(lon, lat):
        return (x0 + (lon - lon0) / (lon1 - lon0) * w, y0 + (lat1 - lat) / (lat1 - lat0) * h)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA, outline=INK, width=2)
    for poly in CONTINENTS:
        d.polygon([p(a, b) for a, b in poly], fill=LAND, outline=(150, 135, 100))
    for name, ll in MAP_LABELS:
        d.text(p(*ll), name, font=F_MAPL, fill=(120, 105, 70), anchor="mm")
    placed = []
    for num, ll in pins:
        px, py = p(*ll)
        for _ in range(6):  # nudge a pin that would overlap an earlier one
            if all(math.hypot(px - qx, py - qy) >= 19 for qx, qy in placed):
                break
            py += -19 if py > y0 + 30 else 19
        placed.append((px, py))
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=2)
        d.text((px, py), str(num), font=F_PIN, fill=WHITE, anchor="mm")


def tag_bar(d, x, y, w, num, tag):
    d.rectangle([x, y, x + w, y + 20], fill=NAVY)
    d.ellipse([x + 4, y + 2, x + 20, y + 18], fill=RED)
    d.text((x + 12, y + 10), str(num), font=F_TAG, fill=WHITE, anchor="mm")
    d.text((x + 26, y + 10), tag, font=F_TAG, fill=WHITE, anchor="lm")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 58], fill=INK)
    d.text((W / 2, 30), "THE WORLD TODAY", font=F_MAST, fill=PAPER, anchor="mm")
    d.rectangle([0, 58, W, 84], fill=RED)
    d.text((W / 2, 71), "WEDNESDAY, 18 NOVEMBER 2026  ·  THE DAY'S WORLD NEWS ON ONE PAGE", font=F_DATE,
           fill=WHITE, anchor="mm")

    top, gap, ch = 90, 6, 200
    cw = (W - 16 - 3 * gap) / 4

    # lead story spans two columns of the first row
    hw = 2 * cw + gap
    d.rectangle([8, top, 8 + hw, top + ch], fill=CARD, outline=INK, width=2)
    tag_bar(d, 8, top, hw, 1, HERO[0])
    hero_art(d, 12, top + 24, 250, ch - 28)
    tx, tw = 270, 8 + hw - 270 - 6
    d.text((tx, top + 26), HERO[1], font=fit(d, HERO[1], "arialbd.ttf", 34, tw), fill=RED)
    ty = top + 66
    for ln in wrap(d, HERO[2], F_HERO, tw):
        d.text((tx, ty), ln, font=F_HERO, fill=INK)
        ty += 30
    sl = wrap(d, HERO[3], F_HSUB, tw)
    sy = top + ch - 8 - 18 * len(sl)
    if sy < ty:
        WARN.append("OVERLAP: lead story")
    for ln in sl:
        d.text((tx, sy), ln, font=F_HSUB, fill=GREY)
        sy += 18

    slots = [(2, 0), (3, 0)] + [(c, r) for r in (1, 2) for c in range(4)]
    for i, ((tag, fact, head, sub, ic, panel, _), (col, row)) in enumerate(zip(CARDS, slots)):
        cx = 8 + col * (cw + gap)
        cy = top + row * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD, outline=INK, width=2)
        tag_bar(d, cx, cy, cw, i + 2, tag)
        d.rounded_rectangle([cx + 5, cy + 25, cx + 91, cy + 109], radius=8, fill=panel)
        ICONS[ic](d, cx + 8, cy + 27, 80)
        ff = fit(d, fact, "arialbd.ttf", 30, cw - 102)
        d.text((cx + 94 + (cw - 98) / 2, cy + 67), fact, font=ff, fill=RED, anchor="mm")
        lines = wrap(d, head, F_HEAD, cw - 12)
        if len(lines) > 3:
            WARN.append(f"WRAP: card {i + 2} headline {len(lines)} lines")
        ty = cy + 114
        for ln in lines:
            d.text((cx + 6, ty), ln, font=F_HEAD, fill=INK)
            ty += 22
        sl = wrap(d, sub, F_SUB, cw - 12)
        if len(sl) > 1:
            WARN.append(f"WRAP: card {i + 2} subline {len(sl)} lines")
        if cy + ch - 20 < ty:
            WARN.append(f"OVERLAP: card {i + 2}")
        d.text((cx + 6, cy + ch - 20), sl[0], font=F_SUB, fill=GREY)

    # bottom: map (left) and briefs (right)
    by = top + 3 * ch + 2 * gap + 6
    bh = H - 26 - by
    mw = 400
    d.text((8, by), "WHERE THE 11 LEAD STORIES HAPPENED", font=F_REG, fill=RED)
    pins = [(1, HERO[4])] + [(i + 2, c[6]) for i, c in enumerate(CARDS)]
    draw_map(d, 8, by + 18, mw, bh - 20, pins)

    bx = mw + 18
    d.text((bx, by), "MORE NEWS FROM 18 NOVEMBER, BY REGION", font=F_REG, fill=RED)
    rh = (bh - 18) / len(BRIEFS)
    n = 1 + len(CARDS)
    for k, (reg, items) in enumerate(BRIEFS):
        ry = by + 18 + k * rh
        d.rectangle([bx, ry + 2, bx + 82, ry + rh - 3], fill=NAVY)
        d.text((bx + 41, ry + rh / 2), reg, font=F_REG, fill=WHITE, anchor="mm")
        lines = wrap(d, "  •  ".join(items), F_BRIEF, W - 8 - bx - 90)
        if len(lines) > 2:
            WARN.append(f"WRAP: briefs {reg} {len(lines)} lines")
        ly = ry + rh / 2 - 7.5 * len(lines)
        for ln in lines:
            d.text((bx + 90, ly), ln, font=F_BRIEF, fill=INK)
            ly += 15
        n += len(items)
        d.line([bx, ry + rh - 1, W - 8, ry + rh - 1], fill=(200, 192, 175), width=1)

    # footer
    d.rectangle([0, H - 22, W, H], fill=INK)
    d.text((W / 2, H - 11), f"DATE CHECK: Wednesday 18 Nov 2026 · {n} stories, 7 regions · Sources: AP, "
           "Guardian, Euronews, Democracy Now!, UN News, Al Jazeera, Africanews, The Hindu, ABC",
           font=F_FOOT, fill=PAPER, anchor="mm")

    assert n >= 40, n
    img.save("entry.png", optimize=True)
    print("stories:", n)
    for w in WARN:
        print(w)


if __name__ == "__main__":
    main()
