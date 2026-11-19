[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![Rank](https://make.fun/badge/news-image-20261119/runtuhjiwa/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![Reward](https://make.fun/badge/news-image-20261119/runtuhjiwa/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# World News — Thursday, 19 November 2026 (v2)

One editorial infographic that sums up the world news of **Thursday, 19 November 2026** in a single 1024×1024 image.

The v2 image covers seven stories that defined the day: the Trump–Xi–Putin three-way summit in Shenzhen, Ukraine's strike on the Crimean Bridge, US–Iran fire spreading in the Gulf, Hakeem Jeffries set to become the first Black Speaker of the US House, Anthropic's record $81.3bn IPO, Voyager 1 reaching one light-day from Earth, and the EU approving the Indonesia trade pact.

The image is drawn programmatically with Python (PIL, DejaVu Sans), so every headline is crisp and the output is fully deterministic — two runs produce byte-identical files.

## Files

- `entry.png` — the 1024×1024 PNG infographic (the entry image).
- `draw.py` — the Python script that draws `entry.png` from scratch.
- `main.ts` — the entry program: copies `entry.png` to the output directory, verifying PNG magic bytes, the 1 MiB size limit, and SHA-256 byte identity.

## How to run

```sh
# Regenerate the image (optional — entry.png is already in this repo)
python3 draw.py

# Produce the entry output
node main.ts
# writes entry.png to $MAKEFUN_OUTPUT_DIR, or /output when unset
```

## License

MIT — see `LICENSE`.
