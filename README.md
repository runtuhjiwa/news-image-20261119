# World News — Thursday, 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/runtuhjiwa/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/runtuhjiwa/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up the world's news of Thursday, 19 November 2026.
An editorial infographic: a masthead naming the day, one hero story, and
five more stories across regions and fields — geopolitics, the Middle East,
science, technology, Europe, and culture.

## The six stories

1. **Trump, Xi & Putin meet in Shenzhen** — leaders of the US, China and
   Russia hold a trilateral meeting on the sidelines of the APEC summit.
2. **US–Iran fire spreads in the Gulf** — the US strikes Iranian missile
   sites on Qeshm Island; Iran widens attacks on US bases in Kuwait and
   Bahrain.
3. **Voyager 1 reaches one light-day** — after ~50 years in space, NASA's
   Voyager 1 becomes the first human-made object one light-day from Earth.
4. **Anthropic's $81.3bn IPO, biggest ever** — the maker of Claude raises
   $81.3 billion in the largest IPO in history.
5. **EU proposes a €45bn Ukraine loan** — the European Union proposes a
   €45 billion loan for Ukraine, repaid after Russia pays reparations.
6. **GTA VI rolls out worldwide** — Grand Theft Auto VI begins its global
   release as players return to Vice City after a 13-year wait.

## How it is built

- `draw.py` draws `entry.png` (1024×1024, PNG) with Python and Pillow:
  every label is rendered by code, so the text stays sharp and legible.
- `main.ts` (Node, standard library only) copies `entry.png` next to it
  to `/output/entry.png`, verifying the PNG magic bytes, the 1 MiB limit,
  and that the copy is byte-identical to the source.

## Run it

```sh
python3 draw.py            # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # write out/entry.png
```

Entry for the make.fun competition
[news-image-20261119](https://make.fun/bounty/news-image-20261119) —
"Sum up 19 November's world news in one image".
