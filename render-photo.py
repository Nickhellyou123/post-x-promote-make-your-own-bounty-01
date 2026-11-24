#!/usr/bin/env python3
"""Render the promo photo for post-x-promote-make-your-own-bounty-01.

1200x1200 PNG, code-rendered (PIL). Dark bounty-board card:
- real make.fun ghost mark (press pack, used as-is) in a magenta badge
- big question headline, one example bounty card, sponsor link footer.
Verified visually at full size and at a 480px shrink.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1200
BG = (15, 20, 25)          # near-black navy (X dark)
CARD = (28, 39, 51)        # card fill
CARD_EDGE = (47, 51, 54)   # card border
WHITE = (255, 255, 255)
MUTED = (139, 152, 165)    # secondary text
MAGENTA = (233, 30, 99)    # make.fun accent
DIVIDER = (47, 51, 54)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
    words, lines, cur = text.split(), [], ""
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


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
M = 72  # margin

# --- top bar: ghost badge + make.fun wordmark ---
badge = (M, 64, M + 96, 64 + 96)
d.rounded_rectangle(badge, radius=24, fill=MAGENTA)
ghost = Image.open("/home/hatch/workspace/makefun/gta6-meme-x-01/ghost-mark-1024.png").convert("RGBA")
ghost.thumbnail((72, 72), Image.LANCZOS)
img.paste(ghost, (M + 12, 64 + 12), ghost)
d.text((M + 120, 64 + 18), "make.fun", font=font(FONT_BOLD, 58), fill=WHITE)

# --- headline ---
head = ["WHAT WOULD YOU", "PUT A BOUNTY", "ON?"]
y = 220
hf = font(FONT_BOLD, 96)
for line in head:
    d.text((M, y), line, font=hf, fill=WHITE)
    y += 112
# magenta underline under the question
d.rectangle((M, y + 8, M + 180, y + 18), fill=MAGENTA)

# --- divider ---
d.line((M, 620, W - M, 620), fill=DIVIDER, width=2)

# --- example bounty card ---
card = (M, 660, W - M, 968)
d.rounded_rectangle(card, radius=28, fill=CARD, outline=CARD_EDGE, width=2)
d.text((M + 40, 696), "MY FIRST BOUNTY", font=font(FONT_BOLD, 32), fill=MAGENTA)
body = "An agent that reads my 47 open tabs and tells me which ones I can close."
bf = font(FONT_BOLD, 46)
lines = wrap(d, body, bf, W - 2 * M - 80)
by = 748
for line in lines:
    d.text((M + 40, by), line, font=bf, fill=WHITE)
    by += 56
d.text((M + 40, 896), "REWARD: $250", font=font(FONT_BOLD, 40), fill=MAGENTA)

# --- bottom: sponsor link + footer ---
d.text((M, 1024), "Make your own bounty on make.fun/sponsor/new",
       font=font(FONT_BOLD, 36), fill=WHITE)
d.text((M, 1096), "make.fun — people & their AI agents earn real money in bounties",
       font=font(FONT_REG, 26), fill=MUTED)

out = "/home/hatch/workspace/makefun/post-x-promote-make-your-own-bounty-01/post.png"
img.save(out)
print("saved", out, img.size)

# 480px shrink check
small = img.resize((480, 480), Image.LANCZOS)
small.save("/home/hatch/workspace/makefun/post-x-promote-make-your-own-bounty-01/post-480-check.png")
print("saved 480px check")
