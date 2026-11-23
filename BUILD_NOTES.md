# BUILD_NOTES — post-tiktok-day-one-day-seven-20261123-0327

Built in this session, after the bounty opened (2026-11-23T03:27:00Z).
Video: `day-one-day-seven-9x16.mp4`, 1080x1920, 20.0 s, 60 fps, H.264,
~1.6 MB. No audio track.

## Creative decisions (my own words)

The brief wants the same tiny agent-built game on day one and after a week
of daily updates, cut between identical moments with a still camera. The
game is Dot Dash, a one-button dodger I invented for this video: a magenta
square hero runs a fixed side-view map, jumping on platforms and collecting
coins. Animation, not real gameplay footage — the rules allow generated
scenes, and animation keeps the two moments pixel-identical where the brief
wants them identical: same ground line, same first platform in the same
place, same starting spot, same camera.

- 0.0–6.5 s, day one: the barest build. Pale flat sky, one platform, one
  coin, no HUD, no enemies, no decoration. The hero stands at the start,
  runs a little, hops onto the platform, takes the one coin. Slow and empty
  on purpose — the emptiness is the point.
- 6.5–7.5 s: a plain ink card, "7 DAYS LATER / 7 daily updates". A hard cut
  to black between the two eras, so the viewer feels the jump.
- 7.5–14.5 s, day seven: the same map and start, now alive. Sun, drifting
  clouds, hills, two more platforms, six coins, two spike enemies
  patrolling, sparkles on every pickup, a trail behind the hero, and a HUD
  (DAY 7, SCORE counting to 1,250, three hearts). The hero runs the same
  opening route — same first jump onto the same first platform — and the
  difference is everything around it.
- 14.5–17.5 s: the day-seven build keeps being played under the call to
  action, "YOUR AGENT CAN BUILD THIS TOO / Start yours at make.fun". The
  camera never moves in the whole video.
- 17.5–20.0 s: the press pack's transparent referral end card over the
  blurred clip, with my referral code `1hpjq5ct` typed into the field in
  JetBrains Mono Bold, ink #191419, per the manifest.

The brand badge (`makefun-badge-9x16.png`, full-frame overlay, used as-is)
sits at its manifest position (x 120–450, y 272–400) from the very first
frame until the end card comes in at 17.5 s. All on-screen text stays below
y 450 so it never collides with the badge, and above y 1500 so it stays
clear of TikTok's caption and buttons.

## Press files fetched in this session

From https://make.fun/press/manifest.json (edition 2026-11-21) and
https://make.fun/press/llms.txt, kept in `press/` outside the repo:

- `makefun-card-9x16-transparent.webm` — 768,936 bytes, sha256
  286b76c671fa3bf3b1580a7c71675d7b7e502f4fb374b56d30f1104044808cd1,
  matches the manifest exactly.
- `makefun-badge-9x16.png` — 22,841 bytes, used as-is.
- `JetBrainsMono-Bold.ttf` — downloaded fresh from the JetBrains Mono
  repository (raw.githubusercontent.com), 274,096 bytes, for the code in
  the referral field.

## Render commands (run in this session)

Base clip — `render_game.py` writes raw RGB24 frames to stdout:

```sh
python3 render_game.py | ffmpeg -v error -y -f rawvideo -pix_fmt rgb24 \
  -s 1080x1920 -r 30 -i - -c:v libx264 -pix_fmt yuv420p -crf 18 -r 30 \
  -movflags +faststart clip.mp4
```

Final assembly — badge from frame 0, transparent end card over the last
2.5 s, referral code typed in (the press pack's own recipe, HOLD=0):

```sh
CLIP=clip.mp4 CODE=1hpjq5ct FONT=press/JetBrainsMono-Bold.ttf \
CARD=press/makefun-card-9x16-transparent.webm BADGE=press/makefun-badge-9x16.png \
W=1080 H=1920 LEN=2.5 REST=1.433 CX=210 CY=1232 CW=5 CH=78 MID=1271 SIZE=62 HOLD=0
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$CLIP")
T=$(awk "BEGIN{print $D+$HOLD-$LEN}")
ffmpeg -v error -y -i "$CLIP" -c:v libvpx-vp9 -i "$CARD" -i "$BADGE" -filter_complex "\
[0:v]scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,setsar=1,fps=60,\
tpad=stop_mode=clone:stop_duration=$HOLD[base];\
[base][2:v]overlay=enable='lt(t,$T)',format=yuva420p,split[clip][soft];\
[soft]gblur=sigma=28,eq=saturation=0.35,fade=t=in:st=$T:d=0.8:alpha=1[soft];\
[clip][soft]overlay[bg];\
[1:v]format=yuva420p,setpts=PTS-STARTPTS+$T/TB[card];\
[bg][card]overlay=eof_action=pass,\
drawbox=x=$CX-2:y=$CY-2:w=$CW+4:h=$CH+4:color=white:t=fill:enable='gte(t,$T+$REST)',\
drawtext=fontfile=$FONT:text=$CODE:fontsize=$SIZE:fontcolor=0x191419:\
x=$CX:y=$MID-(ascent-descent)/2:enable='gte(t,$T+$REST)'[v]" \
  -map '[v]' -map '0:a?' -c:v libx264 -pix_fmt yuv420p -crf 18 \
  -movflags +faststart day-one-day-seven-9x16.mp4
```

## Frame checks (all looked at in this session)

- t=1 s: badge top-left at its manifest box; "DAY ONE / built today";
  hero at the start; one coin over one platform. Pass.
- t=9 s: "DAY SEVEN / same map. same start."; HUD DAY 7, SCORE, three
  hearts; hero mid-jump, spikes clear of the hero's path. Pass.
- t=12 s: hero standing on platform 2 with coin sparkles, SCORE 850.
  Pass.
- t=16 s: "YOUR AGENT CAN BUILD THIS TOO" and the "Start yours at
  make.fun" chip, both fully inside their chips; SCORE 1250 fits. Pass.
- t=18.8 s: end card building, referral field empty with the caret
  blinking (the code types in only once the field rests, per the recipe).
  Pass.
- Last frame: full magenta card, mark + wordmark, "Use my referral code",
  field reads `1hpjq5ct` in JetBrains Mono Bold ink, copy button visible,
  no caret beside the code. Pass.

## Fixes made during the build

1. The sky gradient first rendered as black stripes: the band loop mixed
   two different step sizes (`i/63` for the top edge, `(i+1)/64` for the
   bottom), leaving unpainted gaps. Fixed to one step size.
2. The hero first ran straight into a spike enemy mid-run. Moved the
   spikes' patrol zones to places the hero only crosses in the air, and
   made the run back a single high hop over the mid-map spike.
3. The score and the call-to-action chips were fixed-width and the text
   overflowed them ("SCORE 1250", "Start yours at make.fun"). Both chips
   are now sized from the measured text width.
4. The coin's "$" overflowed the ellipse while the coin spun edge-on; it
   is now drawn only while the coin faces the viewer, shrinking with it.
5. The spike's eye floated above its tip; the eyes sit on the face now.
   The hearts were pin shapes; they are a real ♥ glyph now.

## Codes

- Play code (code 0 of 4): `makefun-polka-trout-snowdrop`
- Referral code: `1hpjq5ct` (verified via GET /api/me/referrals)
- TikTok caption: see README.md. It carries the required line verbatim
  plus the play code.

## Status

Video rendered and frame-checked. Repo created and pushed; VIDEO.json
still holds a placeholder — the video must be posted publicly on TikTok
by JP first (cloud cannot sign in to TikTok), then VIDEO.json takes the
real `https://www.tiktok.com/@xjptea/video/<id>` address and the entry is
submitted. NOT submitted yet, on purpose.
