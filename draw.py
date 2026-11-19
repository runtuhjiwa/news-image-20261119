#!/usr/bin/env python3
"""Draw the v2 news-image entry: one 1024x1024 editorial infographic
summarising world news on Thursday, 19 November 2026.

Deterministic: no randomness, no timestamps, no network. Running this
script twice produces byte-identical output.

Usage: python3 draw.py   (writes entry.png next to this script)
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- canvas
W, H = 1024, 1024
BG = (253, 251, 245)          # warm paper white
INK = (17, 17, 17)            # near-black
RED = (178, 34, 34)           # editorial red for the date / kickers
GREY = (85, 85, 85)           # secondary text
LINE = (200, 196, 188)        # hairline separators
MARGIN = 48
CONTENT_W = W - 2 * MARGIN    # 928

# ---------------------------------------------------------------- fonts
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(bold, size):
    return ImageFont.truetype(F_BOLD if bold else F_REG, size)


# ---------------------------------------------------------------- helpers
def wrap(text, fnt, max_width, draw):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, line_height, fill, align="left",
               max_width=None):
    """Draw lines top-to-bottom; returns the y just below the last line."""
    for line in lines:
        if align == "center" and max_width is not None:
            lx = x + (max_width - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += line_height
    return y


def hline(draw, y, x0, x1, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def vline(draw, x, y0, y1, width=1, fill=LINE):
    draw.line([(x, y0), (x, y1)], fill=fill, width=width)


# ---------------------------------------------------------------- content
MASTHEAD = "WORLD NEWS"
DATE_LINE = "THURSDAY, 19 NOVEMBER 2026"
SUBTITLE = "Seven stories that defined the day"

HERO_HEAD = "TRUMP, XI & PUTIN MEET IN SHENZHEN"
HERO_SUB = ("First three-way summit of the US, China and Russia leaders, "
            "on APEC sidelines; nuclear arms control on the agenda.")

# (headline, sub) for stories 2-7, in reading order.
STORIES = [
    ("UKRAINE HITS CRIMEAN BRIDGE AGAIN",
     "Third strike on the crossing in a week; traffic halted as damage "
     "is assessed."),
    ("US\u2013IRAN FIRE SPREADS IN THE GULF",
     "US struck missile sites on Qeshm Island; Iran widened attacks on "
     "US bases in Kuwait and Bahrain."),
    ("JEFFRIES SET TO BE FIRST BLACK HOUSE SPEAKER",
     "Democrat Hakeem Jeffries nominated to lead the US House \u2014 a "
     "first for an African-American."),
    ("ANTHROPIC\u2019S $81.3BN IPO \u2014 BIGGEST EVER",
     "Claude-maker\u2019s stock market debut raises a record amount."),
    ("VOYAGER 1 REACHES ONE LIGHT-DAY",
     "NASA probe, ~50 years after launch, becomes the first human object "
     "a light-day from Earth."),
    ("EU APPROVES INDONESIA TRADE PACT",
     "EU Council greenlights deal to cut tariffs and counter US trade "
     "pressure."),
]

FOOTER = "WORLD NEWS  \u2022  THURSDAY, 19 NOVEMBER 2026"


# ---------------------------------------------------------------- draw
def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    y = 34
    f_mast = font(True, 74)
    y = draw_lines(d, [MASTHEAD], f_mast, MARGIN, y, 84, INK,
                   align="center", max_width=CONTENT_W)
    f_date = font(True, 34)
    y = draw_lines(d, [DATE_LINE], f_date, MARGIN, y + 2, 44, RED,
                   align="center", max_width=CONTENT_W)
    f_sub = font(False, 22)
    y = draw_lines(d, [SUBTITLE], f_sub, MARGIN, y + 6, 30, GREY,
                   align="center", max_width=CONTENT_W)

    # double rule under the masthead
    y = 214
    hline(d, y, MARGIN, W - MARGIN, width=3)
    hline(d, y + 7, MARGIN, W - MARGIN, width=1)

    # ---- hero ----------------------------------------------------------
    y = 240
    f_kick = font(True, 18)
    y = draw_lines(d, ["TOP STORY"], f_kick, MARGIN, y, 24, RED)
    f_hero = font(True, 46)
    hero_lines = wrap(HERO_HEAD, f_hero, CONTENT_W, d)
    y = draw_lines(d, hero_lines, f_hero, MARGIN, y + 6, 56, INK)
    f_hero_sub = font(False, 22)
    hero_sub_lines = wrap(HERO_SUB, f_hero_sub, CONTENT_W, d)
    y = draw_lines(d, hero_sub_lines, f_hero_sub, MARGIN, y + 8, 30, GREY)

    # rule under the hero
    hline(d, 446, MARGIN, W - MARGIN, width=2)

    # ---- grid: 2 rows x 3 columns --------------------------------------
    grid_top = 468
    row_h = 246
    gutter = 24
    col_w = (CONTENT_W - 2 * gutter) // 3  # 293
    f_head = font(True, 23)
    f_cell_sub = font(False, 16)

    for idx, (head, sub) in enumerate(STORIES):
        row, col = divmod(idx, 3)
        x = MARGIN + col * (col_w + gutter)
        top = grid_top + row * row_h

        head_lines = wrap(head, f_head, col_w, d)
        cy = draw_lines(d, head_lines, f_head, x, top, 29, INK)
        sub_lines = wrap(sub, f_cell_sub, col_w, d)
        draw_lines(d, sub_lines, f_cell_sub, x, cy + 8, 21, GREY)

    # vertical separators between columns
    for col in (1, 2):
        x = MARGIN + col * col_w + (col - 1) * gutter + gutter // 2
        vline(d, x, grid_top, grid_top + 2 * row_h - 12)
    # horizontal separator between the two rows
    hline(d, grid_top + row_h - 8, MARGIN, W - MARGIN, width=1, fill=LINE)

    # ---- footer ---------------------------------------------------------
    hline(d, 986, MARGIN, W - MARGIN, width=2)
    f_foot = font(True, 15)
    draw_lines(d, [FOOTER], f_foot, MARGIN, 996, 20, GREY,
               align="center", max_width=CONTENT_W)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
