# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/tianzhaoming28-maker/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/tianzhaoming28-maker/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Sum up the world's news of Monday 23 November 2026 in one image.

The front page leads with Ukraine sinking the Russian corvette
Merkury off Libya — seven sea drones, 2,400 km from the front — and
carries seven more stories from the day: the Indonesian factory fire
confirmed at 24 dead, India's $1.62bn package for flood-hit Nepal,
US sanctions on Iran's "shadow banking" networks, the COP31
aftermath in Australia and the Pacific, Shuri Castle reopening in
Okinawa, a Thai court halving an opposition MP's jail term, and
China's 2030 eldercare and childcare plan. Every story is
double-sourced in [SOURCES.md](SOURCES.md).

## Run it

```sh
python3 draw.py        # renders entry.png (1024x1024, Pillow)
node pack.mjs          # embeds entry.png into main.ts as one base64 line
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

`main.ts` decodes the embedded image and writes it to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`), byte for
byte identical to `entry.png`.

---
