#!/usr/bin/env python3
"""Render the frames of the 'Day one, day seven' TikTok video.

A tiny agent-built dodger game, 'Dot Dash': one square hero, one map,
one fixed camera. Day one is the barest build (one platform, one coin,
no HUD). Day seven is the same map and start, same camera, after seven
daily updates (more platforms, coins, enemies, clouds, particles, HUD).
The cut between the two identical moments is the whole story.

Writes raw RGB24 frames (1080x1920, 30 fps, 20 s = 600 frames) to stdout,
to be piped into ffmpeg. Everything here is deterministic: no random
module, no clock, no network, so a re-render is byte-identical.
"""

import math
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
TOTAL_SECONDS = 20.0
FRAMES = int(TOTAL_SECONDS * FPS)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
GROUND_Y = 1560
HERO = 96

MAGENTA = (196, 28, 131)
INK = (25, 20, 25)
GOLD = (245, 184, 30)
WHITE = (255, 255, 255)


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def lerp(a, b, u):
    return a + (b - a) * u


def clamp(u, lo=0.0, hi=1.0):
    return max(lo, min(hi, u))


def sky(draw, top, bottom):
    """Vertical gradient, drawn as 64 horizontal bands."""
    for i in range(64):
        u = i / 64
        c = tuple(int(lerp(top[k], bottom[k], u)) for k in range(3))
        y0 = int(i / 64 * GROUND_Y)
        y1 = int((i + 1) / 64 * GROUND_Y)
        draw.rectangle([0, y0, W, y1], fill=c)


def text_centred(draw, y, s, f, fill, stroke=INK, stroke_w=4):
    box = draw.textbbox((0, 0), s, font=f)
    w = box[2] - box[0]
    draw.text(((W - w) / 2 - box[0], y), s, font=f, fill=fill,
              stroke_width=stroke_w, stroke_fill=stroke)


def chip(draw, x, y, w, h, fill, outline=None):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill,
                           outline=outline, width=4)


def coin(draw, cx, cy, t):
    """A spinning coin: its width breathes with |cos|."""
    squash = abs(math.cos(t * 3.0))
    w = max(6.0, 34.0 * squash)
    draw.ellipse([cx - w, cy - 42, cx + w, cy + 42], fill=GOLD,
                 outline=(176, 124, 8), width=4)
    if w > 22:
        # The $ only fits while the coin faces us; it shrinks with the spin.
        size = int(52 * squash)
        f = font(size)
        box = draw.textbbox((0, 0), "$", font=f)
        tw, th = box[2] - box[0], box[3] - box[1]
        draw.text((cx - tw / 2 - box[0], cy - th / 2 - box[1]), "$", font=f,
                  fill=(176, 124, 8))


def spike(draw, cx, base_y, s=1.0):
    """One red spike enemy standing on the ground, eyes on its face."""
    w, h = int(70 * s), int(90 * s)
    draw.polygon([(cx - w, base_y), (cx + w, base_y), (cx, base_y - h)],
                 fill=(229, 72, 77), outline=(140, 20, 25))
    for ex in (-16, 14):
        draw.ellipse([cx + ex - 9, base_y - 62, cx + ex + 9, base_y - 44],
                     fill=WHITE)
        draw.ellipse([cx + ex - 4, base_y - 57, cx + ex + 4, base_y - 49],
                     fill=INK)


def hero(draw, x, feet_y, t, trail):
    """The magenta square hero. The trail is a few small fading dots."""
    for i, (tx, ty) in enumerate(trail):
        r = 14 * (i + 1) / max(1, len(trail))
        cx, cy = tx + HERO / 2, ty - HERO / 2
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(232, 90, 168))
    draw.rounded_rectangle([x, feet_y - HERO, x + HERO, feet_y], radius=18,
                           fill=MAGENTA, outline=WHITE, width=4)
    # eyes, looking right
    draw.ellipse([x + 52, feet_y - 68, x + 70, feet_y - 50], fill=WHITE)
    draw.ellipse([x + 74, feet_y - 68, x + 92, feet_y - 50], fill=WHITE)
    draw.ellipse([x + 59, feet_y - 62, x + 67, feet_y - 54], fill=INK)
    draw.ellipse([x + 81, feet_y - 62, x + 89, feet_y - 54], fill=INK)


def sparkles(draw, cx, cy, age):
    """Eight sparks flying out from a collected coin."""
    if age < 0 or age > 0.6:
        return
    for k in range(8):
        ang = k * math.pi / 4
        r = 30 + age * 260
        px = cx + math.cos(ang) * r
        py = cy + math.sin(ang) * r - age * 60
        s = 10 * (1 - age / 0.6)
        draw.ellipse([px - s, py - s, px + s, py + s], fill=GOLD)


# (time, x, feet_y, jump_height) keyframes; jumps arc between neighbours.
DAY1_KEYS = [
    (0.0, 150, GROUND_Y, 0),
    (1.5, 150, GROUND_Y, 0),
    (2.5, 380, GROUND_Y, 0),
    (3.3, 570, 1240, 380),
    (4.2, 570, 1240, 0),
    (5.0, 700, GROUND_Y, 220),
    (6.5, 700, GROUND_Y, 0),
]

DAY7_KEYS = [
    # The first jump waits until the DAY SEVEN title is gone (t 2.0),
    # so the hero never crosses its own title.
    (0.0, 150, GROUND_Y, 0),
    (2.0, 480, GROUND_Y, 0),
    (2.8, 570, 1240, 420),
    (3.4, 570, 1240, 0),
    (4.2, 890, 1080, 340),
    (4.8, 890, 1080, 0),
    (5.6, 700, GROUND_Y, 260),
    (6.4, 950, GROUND_Y, 0),
    (7.0, 950, GROUND_Y, 0),
    # One high hop back across the spike's patrol zone, never touching it.
    (7.8, 380, GROUND_Y, 260),
    (8.6, 570, 1240, 380),
    (9.2, 570, 1240, 0),
    (10.0, 700, GROUND_Y, 220),
    (10.5, 700, GROUND_Y, 0),
]

# (x, y, collect_time_in_day7_segment) for the six day-seven coins.
DAY7_COINS = [
    (570, 1150, 2.8), (830, 990, 4.1), (920, 990, 4.3),
    (480, 1470, 1.95), (760, 1470, 5.8), (930, 1470, 6.3),
]


def hero_pos(keys, t):
    """Interpolate the hero along the keyframes; jumps are parabolas."""
    for i in range(len(keys) - 1):
        t0, x0, y0, _ = keys[i]
        t1, x1, y1, h = keys[i + 1]
        if t0 <= t <= t1:
            u = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
            x = lerp(x0, x1, u)
            y = lerp(y0, y1, u) - 4 * h * u * (1 - u)
            return x, y
    return keys[-1][1], keys[-1][2]


def platform(draw, x0, x1, top, grass):
    draw.rectangle([x0, top, x1, top + 36], fill=grass)
    draw.rectangle([x0, top + 36, x1, top + 78], fill=(74, 111, 165))
    draw.rectangle([x0, top + 36, x1, top + 44], fill=(52, 82, 130))


def draw_day1(img, t):
    draw = ImageDraw.Draw(img)
    sky(draw, (232, 237, 243), (207, 217, 228))
    draw.rectangle([0, GROUND_Y, W, H], fill=(138, 165, 120))
    draw.rectangle([0, GROUND_Y, W, GROUND_Y + 14], fill=(110, 138, 96))
    platform(draw, 420, 720, 1240, (107, 124, 147))
    hx, hy = hero_pos(DAY1_KEYS, t)
    if t < 3.6:
        coin(draw, 570, 1150, t)
    else:
        sparkles(draw, 570, 1150, t - 3.6)
    trail = []
    hero(draw, hx, hy, t, trail)
    if t < 2.2:
        text_centred(draw, 520, "DAY ONE", font(130), WHITE, stroke_w=6)
        text_centred(draw, 700, "built today", font(48), (240, 244, 248),
                     stroke_w=3)
    elif t < 3.4:
        text_centred(draw, 520, "one platform. one coin.", font(52),
                     WHITE, stroke_w=3)


def draw_day7(img, t, cta=False):
    draw = ImageDraw.Draw(img)
    sky(draw, (111, 195, 242), (216, 241, 255))
    # sun, top right
    draw.ellipse([830, 120, 990, 280], fill=(255, 217, 77))
    draw.ellipse([855, 145, 965, 255], fill=(255, 232, 130))
    # drifting clouds: overlapping circles so each reads as one cloud
    for base, speed, cy, s in [(100, 26, 300, 1.0), (620, 18, 430, 0.7),
                               (300, 32, 190, 0.55)]:
        cx = ((base + t * speed) % 1500) - 210
        for ox, oy, r in [(0, 0, 58), (48, -16, 50), (96, 2, 54)]:
            draw.ellipse([cx + ox - r * s, cy + oy - r * s,
                          cx + ox + r * s, cy + oy + r * s],
                         fill=(255, 255, 255))
    # distant hills, same ground line as day one
    draw.ellipse([-260, 1330, 420, 1620], fill=(156, 203, 142))
    draw.ellipse([700, 1380, 1340, 1640], fill=(127, 184, 116))
    # ground
    draw.rectangle([0, GROUND_Y, W, H], fill=(95, 168, 92))
    draw.rectangle([0, GROUND_Y, W, GROUND_Y + 14], fill=(121, 201, 111))
    # platforms: P1 is exactly where day one had it
    platform(draw, 420, 720, 1240, (121, 201, 111))
    platform(draw, 760, 1020, 1080, (121, 201, 111))
    platform(draw, 60, 320, 1000, (121, 201, 111))
    # coins, spinning until collected
    collected = 0
    for cx, cy, ct in DAY7_COINS:
        if t < ct:
            coin(draw, cx, cy, t)
        else:
            collected += 1
            sparkles(draw, cx, cy, t - ct)
    # spike enemies patrolling the ground: S1 far right, past the hero's
    # furthest step; S2 mid-map, where the hero only ever crosses in the air
    s1 = 1025 + 35 * math.sin(t * 0.9)
    s2 = 560 + 40 * math.sin(t * 1.3 + 2.0)
    spike(draw, s1, GROUND_Y)
    spike(draw, s2, GROUND_Y)
    # hero with a short trail
    hx, hy = hero_pos(DAY7_KEYS, t)
    trail = []
    for back in (0.12, 0.08, 0.04):
        px, py = hero_pos(DAY7_KEYS, max(0.0, t - back))
        trail.append((px, py))
    hero(draw, hx, hy, t, trail)
    # HUD: day chip, score, hearts - kept below the badge (badge ends y 400)
    chip(draw, 60, 470, 250, 84, (25, 20, 25))
    draw.text((100, 488), "DAY 7", font=font(52), fill=WHITE)
    score = 50 + 200 * collected
    score_text = "SCORE %d" % score
    score_w = draw.textbbox((0, 0), score_text, font=font(52))[2] + 56
    chip(draw, 360, 470, score_w, 84, (25, 20, 25))
    draw.text((388, 488), score_text, font=font(52), fill=GOLD)
    for k in range(3):
        cx = 360 + score_w + 32 + k * 78
        draw.text((cx, 478), "♥", font=font(56), fill=(229, 72, 77))
    if t < 2.0:
        text_centred(draw, 640, "DAY SEVEN", font(130), WHITE, stroke_w=6)
        text_centred(draw, 820, "same map. same start.", font(48),
                     (240, 244, 248), stroke_w=3)
    if cta:
        text_centred(draw, 640, "YOUR AGENT CAN", font(96), WHITE,
                     stroke_w=5)
        text_centred(draw, 760, "BUILD THIS TOO", font(96), WHITE,
                     stroke_w=5)
        cta_text = "Start yours at make.fun"
        cta_w = draw.textbbox((0, 0), cta_text, font=font(50))[2] + 72
        chip(draw, (W - cta_w) // 2, 920, cta_w, 96, MAGENTA)
        draw.text(((W - draw.textbbox((0, 0), cta_text, font=font(50))[2]) // 2,
                   942), cta_text, font=font(50), fill=WHITE)


def draw_transition(img):
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, H], fill=INK)
    draw.rectangle([390, 880, 690, 896], fill=MAGENTA)
    text_centred(draw, 760, "7 DAYS LATER", font(120), WHITE, stroke=INK,
                 stroke_w=0)
    text_centred(draw, 940, "7 daily updates", font(56), (232, 90, 168),
                 stroke=INK, stroke_w=0)


def main():
    out = sys.stdout.buffer
    for frame in range(FRAMES):
        t = frame / FPS
        img = Image.new("RGB", (W, H))
        if t < 6.5:
            draw_day1(img, t)
        elif t < 7.5:
            draw_transition(img)
        elif t < 14.5:
            draw_day7(img, t - 7.5)
        else:
            draw_day7(img, t - 7.5, cta=(t >= 14.5))
        out.write(img.tobytes())
        out.flush()


if __name__ == "__main__":
    main()
