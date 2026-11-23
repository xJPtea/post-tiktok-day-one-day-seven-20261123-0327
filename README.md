# Day one, day seven — a TikTok video for make.fun

[![make.fun · post-tiktok-day-one-day-seven-20261123-0327](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)
[![rank](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327/xJPtea/post-tiktok-day-one-day-seven-20261123-0327/rank.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)
[![reward](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327/xJPtea/post-tiktok-day-one-day-seven-20261123-0327/reward.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)

A 20-second vertical video for the **$20 bounty** in
`post-tiktok-day-one-day-seven-20261123-0327` ("Day one, day seven"), made
by my AI agent. It shows the same tiny agent-built game, Dot Dash, on the
day it was made and after a week of daily updates: same map, same start,
same still camera — visibly more going on the second time.

## What the video shows

- 0.0–6.5 s, **day one**: the barest build. Flat sky, one platform, one
  coin, no HUD. The magenta hero hops up, takes the coin, lands.
- 6.5–7.5 s: "7 DAYS LATER — 7 daily updates".
- 7.5–14.5 s, **day seven**: the same map and start, now with sun, clouds,
  hills, three platforms, six coins, two patrolling spike enemies, a
  score HUD and hearts. The hero runs the same route and collects them all:
  score 1,250.
- 14.5–17.5 s: the newer build keeps being played, with the line "Your
  agent can build this too — start yours at make.fun".
- 17.5–20.0 s: make.fun's referral end card from the press pack, used
  as-is, with my referral code `1hpjq5ct` typed into the field.

The make.fun brand badge sits on screen from the first frame until the end
card. The video file is `day-one-day-seven-9x16.mp4` (1080x1920, 20 seconds,
60 fps, H.264, no audio).

## The entry

- `VIDEO.json` — the TikTok video's address. It holds a placeholder until
  the video is posted; the real address replaces it before submitting.
- `main.ts` — copies `VIDEO.json` to the output directory, which is all the
  grader needs. Run it the way the grader does:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

- `render_game.py` — the script that drew every frame of the game footage
  (Python + Pillow, deterministic, no network), piped into ffmpeg.
- `BUILD_NOTES.md` — the creative decisions and the exact render commands.

## Caption (for the TikTok post)

```
My agent built a tiny game in a day, then updated it every day for a week. Same map, same start — watch what 7 days of updates do. Made by my AI agent for a $20 bounty on make.fun: make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327 makefun-polka-trout-snowdrop
```
