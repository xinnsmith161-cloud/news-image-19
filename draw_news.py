#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: a newspaper front page for
Thursday 19 November 2026. PIL only, no network. 1024x1024 PNG."""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (139, 26, 26)
GREY = (110, 108, 100)
RULE = (60, 58, 52)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

M = 36                      # side margin
CW = W - 2 * M              # content width = 952


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped paragraph; returns y after last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_us_flag(d, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.4, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(5):
        for cidx in range(6):
            dx = x + cw * (0.08 + 0.16 * cidx)
            dy = y + ch * (0.12 + 0.19 * r)
            d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def draw_cn_flag(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon(star_points(x + w * 0.16, y + h * 0.30, 13, 5), fill=(255, 222, 0))
    for sx, sy in [(0.34, 0.14), (0.42, 0.24), (0.42, 0.40), (0.34, 0.50)]:
        d.polygon(star_points(x + w * sx, y + h * sy, 5, 2), fill=(255, 222, 0))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def draw_ru_flag(d, x, y, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def draw_scales(d, cx, y, w):
    """Small scales-of-justice icon, top beam at y, width w."""
    top = y
    d.line([(cx - w / 2, top), (cx + w / 2, top)], fill=INK, width=3)
    d.line([(cx, top), (cx, top + 34)], fill=INK, width=3)
    d.polygon([(cx - 4, top - 8), (cx + 4, top - 8), (cx, top - 14)], fill=RED)
    for sx in (cx - w / 2 + 6, cx + w / 2 - 6):
        d.line([(sx, top), (sx, top + 22)], fill=INK, width=2)
        d.arc([sx - 16, top + 14, sx + 16, top + 38], start=0, end=180,
              fill=INK, width=2)
        d.line([(sx - 16, top + 26), (sx + 16, top + 26)], fill=INK, width=2)


def draw_chart(d, x, y, w, h):
    """Bar chart with a rising arrow."""
    bars = [0.35, 0.55, 0.45, 0.75]
    bw = w / 5
    for i, f in enumerate(bars):
        bx = x + i * (bw + 6)
        bh = h * f
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(150, 160, 175))
    pts = [(x + 4, y + h - 14), (x + w * 0.35, y + h - 26),
           (x + w * 0.55, y + h - 20), (x + w * 0.8, y + h - 44)]
    d.line(pts, fill=RED, width=4)
    ax, ay = pts[-1]
    d.polygon([(ax, ay - 12), (ax + 14, ay + 2), (ax - 2, ay + 6)], fill=RED)
    d.line([(x, y + h), (x + w, y + h)], fill=INK, width=2)


def draw_flame(d, cx, y, s):
    """Simple flame: outer teardrop + inner flame, red/orange."""
    pts = []
    for t in range(0, 181, 6):
        a = math.radians(t)
        px = cx + s * 0.55 * math.sin(a) * (1 - 0.25 * math.cos(a))
        py = y + s * 0.9 - s * 0.95 * (1 - math.cos(a)) / 2
        pts.append((px, py))
    # teardrop approximated with an ellipse body + pointed tip
    d.ellipse([cx - s * 0.5, y + s * 0.25, cx + s * 0.5, y + s], fill=(214, 90, 20))
    d.polygon([(cx - s * 0.5, y + s * 0.55), (cx, y - s * 0.15),
               (cx + s * 0.5, y + s * 0.55)], fill=(214, 90, 20))
    d.ellipse([cx - s * 0.26, y + s * 0.5, cx + s * 0.26, y + s * 0.95],
              fill=(255, 200, 40))
    d.polygon([(cx - s * 0.26, y + s * 0.7), (cx, y + s * 0.28),
               (cx + s * 0.26, y + s * 0.7)], fill=(255, 200, 40))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    mast = font(SERIF_B, 96)
    d.text((W / 2, 18), "THE WORLD", font=mast, fill=INK, anchor="ma")
    date_f = font(SERIF_I, 30)
    d.text((W / 2, 128), "Thursday, 19 November 2026", font=date_f,
           fill=INK, anchor="ma")
    d.line([(M, 172), (W - M, 172)], fill=RED, width=4)
    d.line([(M, 180), (W - M, 180)], fill=INK, width=1)

    # ---------- lead story ----------
    y = 196
    kick = font(SANS_B, 17)
    d.text((M, y), "WORLD  •  SUMMIT", font=kick, fill=RED)
    y += 30
    # auto-fit the lead headline to the content width
    hl_size = 45
    hl = font(SERIF_B, hl_size)
    lead_headline = "TRUMP, XI AND PUTIN MEET IN SHENZHEN"
    while d.textlength(lead_headline, font=hl) > CW and hl_size > 30:
        hl_size -= 1
        hl = font(SERIF_B, hl_size)
    d.text((M, y), lead_headline, font=hl, fill=INK)
    y += hl_size + 16
    sf = font(SERIF_I, 24)
    y = para(d, M, y,
             "First-ever three-way summit ends with a four-point "
             "\u2018Declaration toward Peace\u2019 \u2014 but no mention "
             "of the Ukraine or Iran wars.",
             sf, CW, 30)
    y += 10

    # three flag panels
    fw, fh = 300, 84
    gap = (CW - 3 * fw) / 2
    for i, (draw_fn, label) in enumerate([
            (draw_us_flag, "UNITED STATES"),
            (draw_cn_flag, "CHINA"),
            (draw_ru_flag, "RUSSIA")]):
        fx = M + i * (fw + gap)
        draw_fn(d, fx, y, fw, fh)
        lf = font(SANS, 15)
        d.text((fx + fw / 2, y + fh + 8), label, font=lf, fill=GREY,
               anchor="ma")
    y += fh + 32
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 14

    # ---------- three-column row ----------
    col_w = 300
    col_gap = (CW - 3 * col_w) / 2
    cols = [
        ("THE HAGUE", "COURT: MYANMAR COMMITTED GENOCIDE",
         "scales",
         "The UN\u2019s top court rules Myanmar committed genocide "
         "against the Rohingya, 9\u20136, in the case brought by Gambia."),
        ("MARKETS", "ANTHROPIC PRICES RECORD IPO",
         "chart",
         "Shares priced at $83, valuing the AI company at about "
         "$1.5 trillion; Nasdaq trading expected Thursday."),
        ("SOUTH ASIA", "BANGLADESH IN TURMOIL",
         "flame",
         "Violence in 28 districts; Muhammad Yunus\u2019s ancestral "
         "home set on fire amid protests by Sheikh Hasina\u2019s party."),
    ]
    col_top = y
    col_bottom = col_top
    for i, (kicker, headline, icon, caption) in enumerate(cols):
        cx = M + i * (col_w + col_gap)
        cy = col_top
        kf = font(SANS_B, 16)
        d.text((cx, cy), kicker, font=kf, fill=RED)
        cy += 26
        hf = font(SERIF_B, 27)
        for line in wrap(d, headline, hf, col_w):
            d.text((cx, cy), line, font=hf, fill=INK)
            cy += 32
        cy += 6
        if icon == "scales":
            draw_scales(d, cx + col_w / 2, cy + 6, 120)
        elif icon == "chart":
            draw_chart(d, cx + 30, cy + 4, col_w - 60, 42)
        else:
            draw_flame(d, cx + col_w / 2, cy + 2, 40)
        cy += 56
        cf = font(SERIF, 19)
        cy = para(d, cx, cy, caption, cf, col_w, 25)
        col_bottom = max(col_bottom, cy)
        if i < 2:
            d.line([(cx + col_w + col_gap / 2, col_top),
                    (cx + col_w + col_gap / 2, col_bottom + 6)],
                   fill=(200, 196, 186), width=1)

    y = col_bottom + 12
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 14

    # ---------- also today strip ----------
    d.text((M, y), "ALSO TODAY", font=font(SANS_B, 17), fill=RED)
    y += 28
    items = [
        "Hormuz tanker attacks mount as US\u2013Iran strikes escalate",
        "Van Gogh sells for $190.4 million, a record for the artist",
        "US and Venezuela sign military cooperation deal",
        "US Senate rejects Iran war-powers resolution, 51\u201348",
    ]
    it_f = font(SERIF, 20)
    for item in items:
        d.rectangle([M, y + 6, M + 10, y + 16], fill=RED)
        d.text((M + 20, y), item, font=it_f, fill=INK)
        y += 28

    y += 6
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 10
    d.text((W / 2, y), "THE WORLD  \u2022  THURSDAY, 19 NOVEMBER 2026",
           font=font(SANS_B, 15), fill=GREY, anchor="ma")

    out = "/home/hatch/workspace/makefun/news-image-20261119/news-image/entry.png"
    img.save(out, "PNG")
    print("saved", out)


if __name__ == "__main__":
    main()
