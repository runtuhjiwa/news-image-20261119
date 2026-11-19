#!/usr/bin/env python3
"""Draw entry.png — one image summing up the world news of Thursday 19 November 2026.

Editorial newspaper-style infographic, 1024x1024 PNG. All text is rendered by
this script (PIL), so every label stays sharp and readable. Run:
    python3 draw.py
which writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
BG = (250, 246, 236)          # warm paper cream
PANEL = (255, 255, 255)       # white panels
INK = (20, 33, 61)            # dark navy text
MUTED = (70, 80, 100)         # grey-blue body text
RULE = (180, 170, 150)        # hairline rule
RED = (180, 35, 24)           # masthead date red
BORDER = (215, 205, 185)      # panel border

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_icon_hero(d, cx, cy):
    """Three meeting circles: US (navy), China (red), Russia (dark teal)."""
    r = 34
    offs = [(-78, -18, (30, 60, 140), "US"),
            (0, -34, (180, 35, 24), "CN"),
            (78, -18, (20, 90, 90), "RU")]
    for dx, dy, col, lab in offs:
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                  fill=col, outline=(255, 255, 255), width=3)
        f = font(FONT_BOLD, 20)
        tw = d.textlength(lab, font=f)
        d.text((cx + dx - tw / 2, cy + dy - 11), lab, font=f, fill=(255, 255, 255))
    # table line under the three circles
    d.line([(cx - 118, cy + 52), (cx + 118, cy + 52)], fill=INK, width=5)
    d.line([(cx - 118, cy + 52), (cx - 118, cy + 66)], fill=INK, width=5)
    d.line([(cx + 118, cy + 52), (cx + 118, cy + 66)], fill=INK, width=5)


def draw_icon_burst(d, cx, cy, col):
    """Explosion burst: orange star + smoke dots (US-Iran strikes)."""
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = 46 if i % 2 == 0 else 20
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=col)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(255, 220, 120))


def draw_icon_probe(d, cx, cy):
    """Voyager probe: dish + body + signal arcs, on a star."""
    d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=(235, 225, 255))
    d.polygon([(cx - 30, cy + 8), (cx + 30, cy + 8), (cx, cy - 34)], fill=(90, 70, 160))
    d.rectangle([cx - 12, cy + 6, cx + 12, cy + 26], fill=(60, 50, 110))
    d.line([(cx - 34, cy - 40), (cx - 22, cy - 28)], fill=(90, 70, 160), width=3)
    d.line([(cx + 34, cy - 40), (cx + 22, cy - 28)], fill=(90, 70, 160), width=3)
    for r in (52, 62):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=300, end=360, fill=(90, 70, 160), width=3)


def draw_icon_chart(d, cx, cy, col):
    """Rising bars + dollar sign (IPO)."""
    bars = [22, 38, 56]
    x0 = cx - 48
    for i, bh in enumerate(bars):
        d.rectangle([x0 + i * 34, cy + 30 - bh, x0 + i * 34 + 24, cy + 30], fill=col)
    d.line([(cx - 54, cy + 40), (cx + 54, cy + 40)], fill=INK, width=4)
    f = font(FONT_BOLD, 34)
    d.text((cx + 8, cy - 62), "$", font=f, fill=(20, 120, 80))


def draw_icon_eu(d, cx, cy):
    """EU circle of stars + coin (Ukraine loan)."""
    import math
    d.ellipse([cx - 48, cy - 48, cx + 48, cy + 48], fill=(30, 60, 140))
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        sx = cx + 34 * math.cos(ang)
        sy = cy + 34 * math.sin(ang)
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 215, 0))
    f = font(FONT_BOLD, 26)
    d.text((cx - 9, cy - 14), "€", font=f, fill=(255, 255, 255))


def draw_icon_city(d, cx, cy):
    """Vice City skyline + sun (GTA VI)."""
    d.ellipse([cx + 22, cy - 44, cx + 54, cy - 12], fill=(255, 170, 60))
    heights = [44, 66, 38, 58, 48]
    x0 = cx - 56
    for i, bh in enumerate(heights):
        d.rectangle([x0 + i * 24, cy + 30 - bh, x0 + i * 24 + 18, cy + 30],
                    fill=(200, 60, 120) if i % 2 else (90, 40, 130))
    d.line([(cx - 58, cy + 30), (cx + 58, cy + 30)], fill=INK, width=4)


def panel(d, x, y, w, h, accent, tag, title, summary, icon, title_size=24,
          sum_size=18, icon_box=120):
    """One story panel: accent top bar, tag, bold title, summary, icon at right."""
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=BORDER, width=2)
    d.rectangle([x, y, x + w, y + 8], fill=accent)
    tx = x + 16
    ty = y + 20
    f_tag = font(FONT_BOLD, 15)
    d.text((tx, ty), tag, font=f_tag, fill=accent)
    ty += 24
    text_w = w - 32 - icon_box
    f_title = font(FONT_BOLD, title_size)
    for line in wrap(d, title, f_title, text_w):
        d.text((tx, ty), line, font=f_title, fill=INK)
        ty += title_size + 4
    ty += 4
    f_sum = font(FONT_REG, sum_size)
    for line in wrap(d, summary, f_sum, text_w):
        d.text((tx, ty), line, font=f_sum, fill=MUTED)
        ty += sum_size + 5
    icon(d, x + w - icon_box // 2 - 8, y + h // 2 + 6)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    f_mast = font(FONT_BOLD, 62)
    mast = "WORLD NEWS"
    tw = d.textlength(mast, font=f_mast)
    d.text(((W - tw) / 2, 22), mast, font=f_mast, fill=INK)
    f_date = font(FONT_BOLD, 34)
    date = "THURSDAY, 19 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 92), date, font=f_date, fill=RED)
    d.line([(24, 132), (W - 24, 132)], fill=RULE, width=3)
    f_sub = font(FONT_REG, 17)
    sub = "Six stories that defined the day — across every region and every field"
    tw = d.textlength(sub, font=f_sub)
    d.text(((W - tw) / 2, 138), sub, font=f_sub, fill=MUTED)

    # ---- Hero story (1): Trump, Xi & Putin ----
    hx, hy, hw, hh = 24, 164, W - 48, 196
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=PANEL, outline=BORDER, width=2)
    d.rectangle([hx, hy, hx + hw, hy + 8], fill=(20, 33, 61))
    f_tag = font(FONT_BOLD, 15)
    d.text((hx + 18, hy + 18), "GEOPOLITICS  •  HERO STORY", font=f_tag, fill=(20, 33, 61))
    f_t = font(FONT_BOLD, 30)
    ty = hy + 42
    for line in wrap(d, "TRUMP, XI & PUTIN MEET IN SHENZHEN", f_t, 600):
        d.text((hx + 18, ty), line, font=f_t, fill=INK)
        ty += 34
    f_s = font(FONT_REG, 19)
    ty += 4
    for line in wrap(d, "Leaders of the US, China and Russia hold a trilateral meeting "
                      "on the sidelines of the APEC summit in Shenzhen.", f_s, 600):
        d.text((hx + 18, ty), line, font=f_s, fill=MUTED)
        ty += 24
    draw_icon_hero(d, hx + hw - 150, hy + hh // 2 - 6)

    # ---- Grid of the other five stories ----
    gx, gy = 24, 374
    col_w = (W - 48 - 16) // 2
    row_h = 196
    gap = 14
    stories = [
        ((200, 60, 30), "MIDDLE EAST",
         "US–IRAN FIRE SPREADS IN THE GULF",
         "The US strikes Iranian missile sites on Qeshm Island; Iran widens "
         "attacks on US bases in Kuwait and Bahrain.",
         lambda dd, cx, cy: draw_icon_burst(dd, cx, cy, (230, 90, 30))),
        ((90, 70, 160), "SCIENCE",
         "VOYAGER 1 REACHES ONE LIGHT-DAY",
         "After ~50 years in space, NASA's Voyager 1 becomes the first "
         "human-made object one light-day from Earth.",
         draw_icon_probe),
        ((20, 120, 80), "TECHNOLOGY",
         "ANTHROPIC'S $81.3BN IPO — BIGGEST EVER",
         "The maker of Claude raises $81.3 billion in the largest IPO "
         "in history.",
         lambda dd, cx, cy: draw_icon_chart(dd, cx, cy, (20, 120, 80))),
        ((30, 60, 140), "EUROPE",
         "EU PROPOSES €45BN UKRAINE LOAN",
         "The European Union proposes a €45 billion loan for Ukraine, "
         "repaid after Russia pays reparations.",
         draw_icon_eu),
    ]
    for i, (accent, tag, title, summary, icon) in enumerate(stories):
        r, c = divmod(i, 2)
        x = gx + c * (col_w + 16)
        y = gy + r * (row_h + gap)
        panel(d, x, y, col_w, row_h, accent, tag, title, summary, icon)

    # ---- Story 6: full-width bottom row ----
    y6 = gy + 2 * (row_h + gap)
    panel(d, gx, y6, W - 48, row_h, (200, 60, 120), "CULTURE",
          "GTA VI ROLLS OUT WORLDWIDE",
          "Grand Theft Auto VI begins its global release as players return to "
          "Vice City after a 13-year wait.",
          draw_icon_city, title_size=26, sum_size=19, icon_box=150)

    # ---- Footer ----
    f_f = font(FONT_REG, 14)
    foot = "19 NOVEMBER 2026  •  Stories as reported on the day  •  One day's world news in one image"
    tw = d.textlength(foot, font=f_f)
    d.text(((W - tw) / 2, H - 26), foot, font=f_f, fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
