"""Build entry.png: front page of world news for Wednesday 18 November 2026 (v2).

Layout: dated masthead, 12 illustrated lead cards (each with one big key fact),
a world map with numbered pins for the cards, and briefs by region.
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
SEA = (200, 222, 238)
LAND = (222, 206, 160)
WHITE = (255, 255, 255)


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


F_MAST = font("georgiab.ttf", 46)
F_DATE = font("arialbd.ttf", 21)
F_TAG = font("arialbd.ttf", 13)
F_HEAD = font("arialbd.ttf", 19)
F_SUB = font("arial.ttf", 13)
F_REG = font("arialbd.ttf", 13)
F_BRIEF = font("arial.ttf", 13)
F_PIN = font("arialbd.ttf", 12)
F_FOOT = font("arial.ttf", 12)

# (tag, big fact, headline, subline, icon, (lon, lat) for the map pin)
CARDS = [
    ("CHINA · APEC", "SHENZHEN", "Xi greets Trump with a hug on the tarmac",
     "Xi-Putin talks before 3-way summit", "summit", (114, 22)),
    ("EUROPE · UKRAINE", "€45bn", "EU proposes loan to keep Kyiv afloat",
     "Backed by joint EU borrowing", "euro", (4, 50)),
    ("GAZA", "TANKS IN", "Israel crosses Gaza ceasefire 'yellow line'",
     "First such push since 2025 truce", "tank", (34, 31)),
    ("WALL STREET", "-561", "Dow falls 1.1% to 50,198 points",
     "S&P 500 down 5th day; Nvidia swings", "chart", (-74, 41)),
    ("VENEZUELA", "DEAL", "US and Venezuela restore military ties",
     "Hegseth signs pact in Caracas", "flags", (-67, 10)),
    ("COP31 · TURKIYE", "DEADLOCK", "UN climate talks stall in Antalya",
     "Countries launch 'climate reality check'", "globe", (31, 37)),
    ("US SENATE", "FLIPPED", "Democrat Peltola wins Alaska seat",
     "Unseats Republican Dan Sullivan", "ballot", (-150, 62)),
    ("TECH", "OUTAGE", "Apple Pay, iCloud and Gmail disrupted",
     "NSA internal network also down", "cloud", (-122, 37)),
    ("GOLD", "$3,742", "Gold hits lowest price in over a year",
     "Worry for African gold producers", "gold", (28, -26)),
    ("UK ECONOMY", "3.6%", "UK inflation rises as fuel prices climb",
     "Petrol and diesel costs up", "pound", (-1, 52)),
    ("IRAQ · TURKEY", "OIL FLOWS", "Iraq pumps oil to Turkey after 12 years",
     "Route avoids Hormuz disruption", "barrel", (44, 35)),
    ("HAITI", "AIRSTRIKE", "Bukele confirms strike on gang boss's home",
     "Haiti, El Salvador sign security pact", "strike", (-72, 19)),
]

BRIEFS = [
    ("EUROPE", ["Deutsche Bank 15M-file leak probed", "Rally against Slovak PM Fico",
                "146,000 protest across France", "Record rain in Portugal"]),
    ("N. AMERICA", ["Jeffries wins 251 votes in Speaker bid", "Alleged Russian spy arrested in Silicon Valley",
                    "Waymo pulls robotaxis off highways", "Trump ordered to testify in BBC case"]),
    ("LATIN AM.", ["Ecuador fishermen sue US over strike at sea", "Brazil police probe vote-meddling claim",
                   "Mexico asks Xi for a panda", "Hegseth heads on to Colombia"]),
    ("MIDEAST", ["Kahana elected Knesset speaker", "Iran army chief vows 'more crushing' reply",
                 "Bahraini activist Nabeel Rajab dies at 62", "UN warns of health crisis in Taiz, Yemen"]),
    ("AFRICA", ["Mercenary-law suspects in S. Africa court", "Medieval cathedral floor found in Sudan",
                "Amnesty seeks probe of RSF drone strikes", "Nigeria police rescue 15 kidnap victims"]),
    ("S. ASIA", ["Bangladesh police clash with garment workers", "62 students hit by toxic gas in Kerala",
                 "Militant commander killed in Kashmir", "Pakistan, Turkmenistan push TAPI pipeline"]),
    ("ASIA-PAC", ["AI cheating scandal hits Korea exams", "Takaichi invites Lee to Japan",
                  "M5.8 quake near Madang, PNG", "Albanese arrives in Shenzhen",
                  "Hanson: cut refugee intake 90%"]),
]

# rough continent outlines, (lon, lat)
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


# ---------- icons: each drawn inside box (x, y, s) ----------

def icon_summit(d, x, y, s):
    for i, col in enumerate([(200, 30, 30), (40, 70, 150), (230, 230, 230)]):
        fx = x + 6 + i * s * 0.3
        d.line([fx, y + 6, fx, y + s * 0.4], fill=INK, width=2)
        d.rectangle([fx, y + 6, fx + s * 0.22, y + 6 + s * 0.15], fill=col, outline=INK)
    for cx, col in [(x + s * 0.3, (200, 30, 30)), (x + s * 0.7, NAVY)]:
        d.ellipse([cx - 9, y + s * 0.42, cx + 9, y + s * 0.42 + 18], fill=(230, 190, 150), outline=INK)
        d.rectangle([cx - 11, y + s * 0.42 + 20, cx + 11, y + s - 4], fill=col, outline=INK)
    d.line([x + s * 0.3 + 10, y + s * 0.72, x + s * 0.7 - 10, y + s * 0.72], fill=INK, width=5)


def icon_euro(d, x, y, s):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.45
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 60, 150), outline=INK, width=3)
    for k in range(12):
        a = 2 * math.pi * k / 12
        sx, sy = cx + r * 0.78 * math.cos(a), cy + r * 0.78 * math.sin(a)
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(250, 210, 40))
    d.text((cx, cy), "€", font=font("arialbd.ttf", int(s * 0.45)), fill=(250, 210, 40), anchor="mm")


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
    pts = [(x + 8, y + s * 0.25), (x + s * 0.3, y + s * 0.38), (x + s * 0.45, y + s * 0.32),
           (x + s * 0.65, y + s * 0.6), (x + s * 0.8, y + s * 0.55), (x + s - 12, y + s * 0.82)]
    d.line(pts, fill=RED, width=5)
    ex, ey = pts[-1]
    d.polygon([(ex - 4, ey + 9), (ex + 9, ey - 5), (ex - 12, ey - 8)], fill=RED)


def icon_flags(d, x, y, s):
    d.rectangle([x + 2, y + 6, x + s * 0.5, y + s * 0.4], fill=WHITE, outline=INK)
    hh = (s * 0.4 - 6) / 7
    for k in range(0, 7, 2):
        d.rectangle([x + 2, y + 6 + k * hh, x + s * 0.5, y + 6 + (k + 1) * hh], fill=RED)
    d.rectangle([x + 2, y + 6, x + s * 0.24, y + 6 + 4 * hh], fill=NAVY)
    hy = (s * 0.34) / 3
    for k, col in enumerate([(250, 205, 0), (0, 50, 140), (205, 20, 40)]):
        d.rectangle([x + s * 0.5, y + s * 0.58 + k * hy, x + s - 2, y + s * 0.58 + (k + 1) * hy], fill=col)
    d.rectangle([x + s * 0.5, y + s * 0.58, x + s - 2, y + s * 0.58 + 3 * hy], outline=INK)
    d.line([x + s * 0.18, y + s * 0.82, x + s * 0.4, y + s * 0.55], fill=INK, width=3)


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
    d.ellipse([x + 2, y + s * 0.15, x + s * 0.78, y + s * 0.91], fill=(205, 205, 210), outline=INK, width=3)
    d.text((x + s * 0.4, y + s * 0.53), "£", font=font("arialbd.ttf", int(s * 0.5)), fill=INK, anchor="mm")
    d.line([x + s * 0.88, y + s * 0.85, x + s * 0.88, y + s * 0.12], fill=RED, width=5)
    d.polygon([(x + s * 0.88 - 9, y + s * 0.18), (x + s * 0.88 + 9, y + s * 0.18), (x + s * 0.88, y + 2)], fill=RED)


def icon_barrel(d, x, y, s):
    d.rounded_rectangle([x + 4, y + s * 0.12, x + s * 0.5, y + s * 0.9], radius=8, fill=(40, 40, 44), outline=INK)
    for f in (0.32, 0.7):
        d.line([x + 4, y + s * f, x + s * 0.5, y + s * f], fill=(120, 120, 130), width=3)
    d.rectangle([x + s * 0.5, y + s * 0.55, x + s - 2, y + s * 0.67], fill=GREY, outline=INK)
    d.polygon([(x + s * 0.8, y + s * 0.2), (x + s * 0.72, y + s * 0.38), (x + s * 0.8, y + s * 0.45),
               (x + s * 0.88, y + s * 0.38)], fill=INK)


def icon_strike(d, x, y, s):
    d.rectangle([x + s * 0.12, y + s * 0.6, x + s * 0.7, y + s - 2], fill=(200, 180, 150), outline=INK, width=2)
    d.polygon([(x + s * 0.06, y + s * 0.6), (x + s * 0.41, y + s * 0.38), (x + s * 0.76, y + s * 0.6)],
              fill=(150, 60, 40), outline=INK)
    pts = []
    for k in range(16):
        r = s * (0.24 if k % 2 == 0 else 0.11)
        a = math.pi * 2 * k / 16
        pts.append((x + s * 0.7 + r * math.cos(a), y + s * 0.32 + r * math.sin(a)))
    d.polygon(pts, fill=(245, 150, 30), outline=RED)
    d.line([x + 2, y + 4, x + s * 0.6, y + s * 0.25], fill=GREY, width=3)


ICONS = dict(summit=icon_summit, euro=icon_euro, tank=icon_tank, chart=icon_chart, flags=icon_flags,
             globe=icon_globe, ballot=icon_ballot, cloud=icon_cloud, gold=icon_gold, pound=icon_pound,
             barrel=icon_barrel, strike=icon_strike)


def draw_map(d, x0, y0, w, h):
    lon0, lon1, lat0, lat1 = -170, 180, -50, 80

    def p(lon, lat):
        return (x0 + (lon - lon0) / (lon1 - lon0) * w, y0 + (lat1 - lat) / (lat1 - lat0) * h)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA, outline=INK, width=2)
    for poly in CONTINENTS:
        d.polygon([p(a, b) for a, b in poly], fill=LAND, outline=(150, 135, 100))
    placed = []
    for i, c in enumerate(CARDS):
        px, py = p(*c[5])
        for _ in range(6):  # nudge a pin that would overlap an earlier one
            if all(math.hypot(px - qx, py - qy) >= 19 for qx, qy in placed):
                break
            py += -19 if py > y0 + 30 else 19
        placed.append((px, py))
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=2)
        d.text((px, py), str(i + 1), font=F_PIN, fill=WHITE, anchor="mm")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 58], fill=INK)
    d.text((W / 2, 30), "THE WORLD TODAY", font=F_MAST, fill=PAPER, anchor="mm")
    d.rectangle([0, 58, W, 84], fill=RED)
    d.text((W / 2, 71), "WEDNESDAY, 18 NOVEMBER 2026  ·  THE DAY'S WORLD NEWS ON ONE PAGE", font=F_DATE,
           fill=WHITE, anchor="mm")

    # 12 cards, 4 x 3
    top, gap, ch = 90, 6, 200
    cw = (W - 16 - 3 * gap) / 4
    for i, (tag, fact, head, sub, ic, _) in enumerate(CARDS):
        cx = 8 + (i % 4) * (cw + gap)
        cy = top + (i // 4) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD, outline=INK, width=2)
        d.rectangle([cx, cy, cx + cw, cy + 20], fill=NAVY)
        d.ellipse([cx + 4, cy + 2, cx + 20, cy + 18], fill=RED)
        d.text((cx + 12, cy + 10), str(i + 1), font=F_TAG, fill=WHITE, anchor="mm")
        d.text((cx + 26, cy + 10), tag, font=F_TAG, fill=WHITE, anchor="lm")
        ICONS[ic](d, cx + 6, cy + 26, 80)
        ff = fit(d, fact, "arialbd.ttf", 30, cw - 100)
        d.text((cx + 92 + (cw - 98) / 2, cy + 66), fact, font=ff, fill=RED, anchor="mm")
        lines = wrap(d, head, F_HEAD, cw - 12)
        if len(lines) > 3:
            WARN.append(f"WRAP: card {i + 1} headline {len(lines)} lines")
        ty = cy + 112
        for ln in lines:
            d.text((cx + 6, ty), ln, font=F_HEAD, fill=INK)
            ty += 22
        sl = wrap(d, sub, F_SUB, cw - 12)
        if len(sl) > 1:
            WARN.append(f"WRAP: card {i + 1} subline {len(sl)} lines")
        sy = cy + ch - 20
        if sy < ty:
            WARN.append(f"OVERLAP: card {i + 1}")
        d.text((cx + 6, sy), sl[0], font=F_SUB, fill=GREY)

    # bottom: map (left) and briefs (right)
    by = top + 3 * ch + 2 * gap + 6
    bh = H - 26 - by
    d.text((8, by), "WHERE THE LEAD STORIES HAPPENED", font=F_REG, fill=RED)
    draw_map(d, 8, by + 18, 380, bh - 20)

    bx = 398
    d.text((bx, by), "MORE NEWS FROM 18 NOVEMBER, BY REGION", font=F_REG, fill=RED)
    rh = (bh - 18) / len(BRIEFS)
    n = len(CARDS)
    for k, (reg, items) in enumerate(BRIEFS):
        ry = by + 18 + k * rh
        d.rectangle([bx, ry + 2, bx + 84, ry + rh - 3], fill=NAVY)
        d.text((bx + 42, ry + rh / 2), reg, font=F_REG, fill=WHITE, anchor="mm")
        lines = wrap(d, "  •  ".join(items), F_BRIEF, W - 8 - bx - 92)
        if len(lines) > 2:
            WARN.append(f"WRAP: briefs {reg} {len(lines)} lines")
        ly = ry + rh / 2 - 8 * len(lines)
        for ln in lines:
            d.text((bx + 92, ly), ln, font=F_BRIEF, fill=INK)
            ly += 16
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
