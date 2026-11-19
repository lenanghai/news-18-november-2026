"""Build entry.png: front page of world news for Wednesday 18 November 2026.

Run locally (needs Pillow and Windows system fonts): python build.py
Sources for every item are listed in SOURCES.md.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONTS = "C:/Windows/Fonts/"
INK = (24, 22, 20)
PAPER = (247, 242, 230)
RED = (178, 34, 34)
NAVY = (28, 52, 96)
GREY = (110, 104, 96)


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


F_MAST = font("georgiab.ttf", 58)
F_DATE = font("arialbd.ttf", 22)
F_HEAD = font("arialbd.ttf", 25)
F_SUB = font("arial.ttf", 16)
F_TAG = font("arialbd.ttf", 13)
F_REG = font("arialbd.ttf", 15)
F_BRIEF = font("arial.ttf", 13)
F_FOOT = font("arial.ttf", 13)

CARDS = [
    ("ASIA · APEC", "Xi hugs Trump on Shenzhen tarmac", "Xi meets Putin before 3-way summit", "summit"),
    ("EUROPE", "EU proposes €45bn loan for Ukraine", "Backed by joint EU debt", "euro"),
    ("MIDDLE EAST", "Israeli tanks cross Gaza ceasefire line", "First push past 'yellow line' since 2025", "tank"),
    ("MARKETS", "Dow falls 561 points, -1.1%", "S&P 500 down 5 days; Nvidia swings", "chart"),
    ("AMERICAS", "US and Venezuela sign military deal", "Hegseth visits Caracas", "flags"),
    ("CLIMATE", "COP31 talks deadlocked in Antalya", "UN launches 'climate reality check'", "globe"),
    ("US POLITICS", "Peltola flips Alaska Senate seat", "Democrat unseats Sen. Dan Sullivan", "ballot"),
    ("TECH", "Apple and Google services go down", "NSA internal network also out", "cloud"),
    ("COMMODITIES", "Gold sinks below $3,800 an ounce", "Lowest price in over a year", "gold"),
]

BRIEFS = [
    ("EUROPE", ["UK inflation rises to 3.6%", "Deutsche Bank 15M-file leak probed",
                "Slovakia rally against PM Fico", "146,000 protest across France",
                "Storms bring record rain to Portugal"]),
    ("N. AMERICA", ["Jeffries wins 251 votes for Speaker", "Alleged Russian spy held in Silicon Valley",
                    "Waymo pulls taxis off highways", "Trump must testify in BBC case",
                    "Warner and Paramount TV merge"]),
    ("LATIN AM.", ["Bukele strikes Haiti gang boss home", "Ecuador fishermen sue US over strike",
                   "Brazil probes vote meddling claim", "Mexico asks Xi for a panda",
                   "Hegseth heads on to Colombia"]),
    ("MIDEAST", ["Kahana elected Knesset speaker", "Iraq pumps oil to Turkey again",
                 "Iran army vows 'crushing' reply", "Activist Nabeel Rajab dies at 62",
                 "UN: health crisis in Taiz, Yemen"]),
    ("AFRICA", ["S. Africa mercenary suspects in court", "Medieval cathedral floor found, Sudan",
                "Amnesty: probe RSF drone strikes", "Nigeria police free 15 hostages",
                "Kenya issues antibiotic guidelines"]),
    ("S. ASIA", ["Bangladesh police clash with workers", "62 students hit by toxic gas, Kerala",
                 "Militant commander killed, Kashmir", "India signs ₹1,976cr IAI deal",
                 "Pakistan pushes TAPI gas pipeline"]),
    ("ASIA-PAC", ["AI cheating scandal hits Korea exams", "Takaichi invites Lee to Japan",
                  "Albanese lands in Shenzhen", "M5.8 quake near Madang, PNG",
                  "Hanson: cut refugee intake 90%"]),
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


# ---------- icons: each drawn inside box (x, y, s) ----------

def icon_summit(d, x, y, s):
    for i, col in enumerate([(200, 30, 30), (40, 70, 150), (230, 230, 230)]):
        fx = x + 8 + i * s * 0.3
        d.line([fx, y + 10, fx, y + s - 8], fill=INK, width=3)
        d.rectangle([fx, y + 10, fx + s * 0.22, y + 10 + s * 0.16], fill=col, outline=INK)
    # two figures shaking hands
    for cx, col in [(x + s * 0.3, (200, 30, 30)), (x + s * 0.7, NAVY)]:
        d.ellipse([cx - 10, y + s * 0.42, cx + 10, y + s * 0.42 + 20], fill=(230, 190, 150), outline=INK)
        d.rectangle([cx - 12, y + s * 0.42 + 22, cx + 12, y + s - 6], fill=col, outline=INK)
    d.line([x + s * 0.3 + 12, y + s * 0.7, x + s * 0.7 - 12, y + s * 0.7], fill=INK, width=5)


def icon_euro(d, x, y, s):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 60, 150), outline=INK, width=3)
    for k in range(12):
        a = 2 * math.pi * k / 12
        sx, sy = cx + r * 0.78 * math.cos(a), cy + r * 0.78 * math.sin(a)
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(250, 210, 40))
    d.text((cx, cy), "€", font=font("arialbd.ttf", int(s * 0.45)), fill=(250, 210, 40), anchor="mm")


def icon_tank(d, x, y, s):
    d.rectangle([x + 6, y + s * 0.55, x + s - 6, y + s * 0.78], fill=(95, 105, 70), outline=INK, width=2)
    d.rectangle([x + s * 0.28, y + s * 0.38, x + s * 0.66, y + s * 0.56], fill=(110, 120, 80), outline=INK, width=2)
    d.line([x + s * 0.62, y + s * 0.45, x + s - 2, y + s * 0.36], fill=INK, width=5)
    for k in range(5):
        wx = x + 14 + k * (s - 28) / 4
        d.ellipse([wx - 7, y + s * 0.78 - 4, wx + 7, y + s * 0.78 + 10], fill=GREY, outline=INK)
    d.line([x, y + s * 0.95, x + s, y + s * 0.95], fill=(230, 190, 40), width=4)


def icon_chart(d, x, y, s):
    d.rectangle([x + 4, y + 4, x + s - 4, y + s - 4], fill=(255, 255, 255), outline=INK, width=2)
    pts = [(x + 10, y + s * 0.3), (x + s * 0.3, y + s * 0.4), (x + s * 0.45, y + s * 0.35),
           (x + s * 0.65, y + s * 0.6), (x + s * 0.8, y + s * 0.55), (x + s - 12, y + s * 0.82)]
    d.line(pts, fill=RED, width=5)
    ex, ey = pts[-1]
    d.polygon([(ex - 4, ey + 8), (ex + 8, ey - 6), (ex - 12, ey - 8)], fill=RED)


def icon_flags(d, x, y, s):
    # US flag
    d.rectangle([x + 4, y + 10, x + s * 0.48, y + s * 0.42], fill=(255, 255, 255), outline=INK)
    for k in range(0, 7, 2):
        yy = y + 10 + k * (s * 0.32 - 10) / 7
        d.rectangle([x + 4, yy, x + s * 0.48, yy + (s * 0.32 - 10) / 7], fill=RED)
    d.rectangle([x + 4, y + 10, x + s * 0.22, y + s * 0.26], fill=NAVY)
    # Venezuela flag
    hy = (s * 0.32) / 3
    for k, col in enumerate([(250, 205, 0), (0, 50, 140), (205, 20, 40)]):
        d.rectangle([x + s * 0.52, y + s * 0.5 + k * hy, x + s - 4, y + s * 0.5 + (k + 1) * hy], fill=col)
    d.rectangle([x + s * 0.52, y + s * 0.5, x + s - 4, y + s * 0.5 + 3 * hy], outline=INK)
    d.line([x + s * 0.3, y + s * 0.72, x + s * 0.48, y + s * 0.6], fill=INK, width=3)
    d.line([x + s * 0.48, y + s * 0.6, x + s * 0.42, y + s * 0.6], fill=INK, width=3)


def icon_globe(d, x, y, s):
    cx, cy, r = x + s * 0.42, y + s / 2, s * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(80, 150, 210), outline=INK, width=2)
    d.polygon([(cx - r * 0.6, cy - r * 0.4), (cx - r * 0.1, cy - r * 0.6), (cx, cy), (cx - r * 0.5, cy + r * 0.3)],
              fill=(90, 160, 80))
    d.polygon([(cx + r * 0.2, cy + r * 0.1), (cx + r * 0.7, cy - r * 0.1), (cx + r * 0.5, cy + r * 0.6)],
              fill=(90, 160, 80))
    tx = x + s * 0.88
    d.rounded_rectangle([tx - 6, y + 8, tx + 6, y + s - 18], radius=6, fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([tx - 2, y + s * 0.4, tx + 2, y + s - 18], fill=RED)
    d.ellipse([tx - 10, y + s - 26, tx + 10, y + s - 6], fill=RED, outline=INK)


def icon_ballot(d, x, y, s):
    d.rectangle([x + 10, y + s * 0.45, x + s - 10, y + s - 6], fill=(240, 240, 240), outline=INK, width=3)
    d.rectangle([x + s * 0.3, y + s * 0.45, x + s * 0.7, y + s * 0.5], fill=INK)
    d.rectangle([x + s * 0.32, y + 8, x + s * 0.68, y + s * 0.47], fill=(255, 255, 255), outline=INK, width=2)
    d.line([x + s * 0.38, y + s * 0.26, x + s * 0.46, y + s * 0.36, x + s * 0.62, y + s * 0.16], fill=NAVY, width=4)
    d.text((x + s / 2, y + s * 0.75), "AK", font=font("arialbd.ttf", 20), fill=NAVY, anchor="mm")


def icon_cloud(d, x, y, s):
    c = (180, 190, 205)
    d.ellipse([x + 6, y + s * 0.35, x + s * 0.5, y + s * 0.75], fill=c, outline=INK, width=2)
    d.ellipse([x + s * 0.3, y + s * 0.2, x + s * 0.8, y + s * 0.7], fill=c, outline=INK, width=2)
    d.ellipse([x + s * 0.55, y + s * 0.38, x + s - 4, y + s * 0.76], fill=c, outline=INK, width=2)
    d.rectangle([x + s * 0.2, y + s * 0.5, x + s * 0.8, y + s * 0.75], fill=c)
    d.line([x + s * 0.36, y + s * 0.4, x + s * 0.64, y + s * 0.68], fill=RED, width=7)
    d.line([x + s * 0.64, y + s * 0.4, x + s * 0.36, y + s * 0.68], fill=RED, width=7)


def icon_gold(d, x, y, s):
    gold, dark = (225, 180, 40), (150, 110, 20)

    def bar(bx, by, w, h):
        d.polygon([(bx, by + h), (bx + w, by + h), (bx + w - 10, by), (bx + 10, by)], fill=gold, outline=dark)
    bar(x + 6, y + s * 0.62, s * 0.44, s * 0.24)
    bar(x + s * 0.5, y + s * 0.62, s * 0.44, s * 0.24)
    bar(x + s * 0.28, y + s * 0.38, s * 0.44, s * 0.24)
    d.line([x + s * 0.75, y + 6, x + s * 0.75, y + s * 0.3], fill=RED, width=5)
    d.polygon([(x + s * 0.75 - 9, y + s * 0.26), (x + s * 0.75 + 9, y + s * 0.26), (x + s * 0.75, y + s * 0.38)], fill=RED)


ICONS = dict(summit=icon_summit, euro=icon_euro, tank=icon_tank, chart=icon_chart, flags=icon_flags,
             globe=icon_globe, ballot=icon_ballot, cloud=icon_cloud, gold=icon_gold)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 96], fill=INK)
    d.text((W / 2, 36), "THE WORLD TODAY", font=F_MAST, fill=PAPER, anchor="mm")
    d.rectangle([0, 72, W, 96], fill=RED)
    d.text((W / 2, 84), "WEDNESDAY, 18 NOVEMBER 2026  ·  WORLD NEWS IN ONE PAGE", font=F_DATE, fill=(255, 255, 255), anchor="mm")

    # cards: 3 x 3
    top, gap, cw, ch = 106, 8, 330, 210
    left = (W - 3 * cw - 2 * gap) / 2
    for i, (tag, head, sub, ic) in enumerate(CARDS):
        cx = left + (i % 3) * (cw + gap)
        cy = top + (i // 3) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=(255, 253, 247), outline=INK, width=2)
        d.rectangle([cx, cy, cx + cw, cy + 22], fill=NAVY)
        d.text((cx + 8, cy + 11), f"{i + 1}  {tag}", font=F_TAG, fill=(255, 255, 255), anchor="lm")
        ICONS[ic](d, cx + 8, cy + 30, 100)
        lines = wrap(d, head, F_HEAD, cw - 124)
        if len(lines) > 4:
            WARN.append(f"WRAP: card {i + 1} headline {len(lines)} lines")
        ty = cy + 32
        for ln in lines:
            d.text((cx + 116, ty), ln, font=F_HEAD, fill=INK)
            ty += 29
        sl = wrap(d, sub, F_SUB, cw - 16)
        sy = cy + ch - 10 - 19 * len(sl)
        if sy < max(ty, cy + 134):
            WARN.append(f"OVERLAP: card {i + 1}")
        for ln in sl:
            d.text((cx + 8, sy), ln, font=F_SUB, fill=GREY)
            sy += 19

    # briefs: 7 regions in columns
    by = top + 3 * ch + 2 * gap + 10
    d.line([12, by - 4, W - 12, by - 4], fill=INK, width=3)
    d.text((W / 2, by + 9), "MORE FROM 18 NOVEMBER, BY REGION", font=F_REG, fill=RED, anchor="mm")
    colw = (W - 24) / 7
    n = len(CARDS)
    for k, (reg, items) in enumerate(BRIEFS):
        x0 = 12 + k * colw
        d.rectangle([x0 + 2, by + 22, x0 + colw - 2, by + 42], fill=NAVY)
        d.text((x0 + colw / 2, by + 32), reg, font=F_REG, fill=(255, 255, 255), anchor="mm")
        yy = by + 48
        for it in items:
            lines = wrap(d, it, F_BRIEF, colw - 10)
            if len(lines) > 2:
                WARN.append(f"WRAP: brief '{it}' {len(lines)} lines")
            d.ellipse([x0 + 3, yy + 5, x0 + 7, yy + 9], fill=RED)
            for ln in lines:
                d.text((x0 + 10, yy), ln, font=F_BRIEF, fill=INK)
                yy += 15
            yy += 3
            n += 1
        if yy > H - 30:
            WARN.append(f"OVERFLOW: column {reg} bottom {yy}")

    # footer
    d.rectangle([0, H - 24, W, H], fill=INK)
    d.text((W / 2, H - 12), f"DATE CHECK: Wed 18 Nov 2026 · {n} stories · Sources: AP, Guardian, Euronews, "
           "Democracy Now!, UN News, Africanews, The Hindu, ABC", font=F_FOOT, fill=PAPER, anchor="mm")

    assert n >= 40, n
    img.save("entry.png", optimize=True)
    print("stories:", n)
    for w in WARN:
        print(w)


if __name__ == "__main__":
    main()
