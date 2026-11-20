#!/usr/bin/env python3
"""Generate the GTA 6 cheat-code meme for make.fun bounty gta6-meme-x-01.

A console "CHEAT ACTIVATED" screen: a PlayStation-style button combo, the
make.fun ghost (press-kit mark) as the activated-cheat icon, and a bounty
payout payoff. Everything is drawn in code with PIL; the only external
assets are the press-kit ghost PNG and system fonts.

Usage: python3 make_meme.py [output.png]
Default output: meme.png next to the repository root (two levels up).
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1080

BG = (11, 11, 20)
PANEL = (24, 24, 38)
PANEL_EDGE = (64, 64, 96)
WHITE = (245, 245, 250)
DIM = (170, 170, 190)
GREEN = (57, 255, 106)
GREEN_DIM = (32, 200, 80)
PINK = (196, 28, 131)          # make.fun pink #c41c83
PINK_BRIGHT = (255, 64, 180)
GOLD = (255, 209, 102)
KEYCAP = (30, 30, 46)
KEYCAP_EDGE = (110, 110, 140)

FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def fit_font(draw, text, name, start, max_width, min_size=10):
    """Largest size at which text fits max_width."""
    size = start
    while size > min_size:
        f = font(name, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(name, min_size)


def center_text(draw, y, text, f, fill, cx=W // 2, tracking=0):
    """Draw text centred on cx; tracking adds px between letters."""
    if tracking:
        widths = [draw.textlength(ch, font=f) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = cx - total / 2
        for ch, wch in zip(text, widths):
            draw.text((x, y), ch, font=f, fill=fill)
            x += wch + tracking
        return total
    wch = draw.textlength(text, font=f)
    draw.text((cx - wch / 2, y), text, font=f, fill=fill)
    return wch


def glow_text(base, xy, text, f, fill, glow, radius=18, passes=3):
    """Text with a soft coloured glow behind it."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.text(xy, text, font=f, fill=glow + (255,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius))
    for _ in range(passes):
        base.alpha_composite(layer)
    ImageDraw.Draw(base).text(xy, text, font=f, fill=fill + (255,))


def draw_button(draw, cx, cy, kind, size=118):
    """One PlayStation-style button inside a keycap."""
    half = size // 2
    x0, y0, x1, y1 = cx - half, cy - half, cx + half, cy + half
    draw.rounded_rectangle([x0, y0, x1, y1], radius=22,
                           fill=KEYCAP, outline=KEYCAP_EDGE, width=3)
    draw.rounded_rectangle([x0 + 5, y0 + 5, x1 - 5, y1 - 5], radius=18,
                           outline=(52, 52, 74), width=1)
    s = size * 0.30  # symbol half-size
    lw = 7
    if kind == "triangle":  # green
        col = (46, 200, 110)
        pts = [(cx, cy - s), (cx + s * 0.95, cy + s * 0.7),
               (cx - s * 0.95, cy + s * 0.7)]
        draw.line(pts + [pts[0]], fill=col, width=lw, joint="curve")
    elif kind == "circle":  # red
        draw.ellipse([cx - s, cy - s, cx + s, cy + s],
                     outline=(235, 70, 70), width=lw)
    elif kind == "cross":  # blue
        col = (80, 140, 255)
        draw.line([(cx - s, cy - s), (cx + s, cy + s)], fill=col, width=lw)
        draw.line([(cx - s, cy + s), (cx + s, cy - s)], fill=col, width=lw)
    elif kind == "square":  # pink
        draw.rectangle([cx - s, cy - s, cx + s, cy + s],
                       outline=(240, 120, 190), width=lw)
    else:  # R1 / R2 shoulder button label
        f = font("NotoSansMono-Bold.ttf", 44)
        tw = draw.textlength(kind, font=f)
        draw.text((cx - tw / 2, cy - 30), kind, font=f, fill=(255, 209, 102))


def scanlines(img, step=3, alpha=6):
    d = ImageDraw.Draw(img)
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(here)
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(repo_root, "meme.png")

    img = Image.new("RGBA", (W, H), BG + (255,))
    draw = ImageDraw.Draw(img)

    # --- backdrop: soft magenta glow top, green glow bottom -----------------
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-260, -420, 560, 180], fill=PINK + (46,))
    gd.ellipse([620, 780, 1340, 1420], fill=(20, 160, 70, 40))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
    draw = ImageDraw.Draw(img)

    # --- outer frame --------------------------------------------------------
    draw.rounded_rectangle([18, 18, W - 18, H - 18], radius=26,
                           outline=PINK, width=4)
    draw.rounded_rectangle([30, 30, W - 30, H - 30], radius=18,
                           outline=(70, 30, 60), width=1)

    # --- header -------------------------------------------------------------
    f_title = font("NotoSansMono-Bold.ttf", 34)
    center_text(draw, 62, "GRAND THEFT AUTO VI", f_title, DIM, tracking=6)
    f_sub = font("NotoSansMono-Bold.ttf", 30)
    center_text(draw, 112, "LEONIDA  •  VICE CITY", f_sub, (150, 120, 170), tracking=4)

    f_enter = font("NotoSans-ExtraBold.ttf", 58)
    center_text(draw, 168, "ENTER CHEAT CODE", f_enter, WHITE, tracking=2)
    # blinking cursor block after the header
    tw = draw.textlength("ENTER CHEAT CODE", font=f_enter)
    cx0 = W // 2 + tw / 2 + 16
    draw.rectangle([cx0, 182, cx0 + 26, 182 + 46], fill=GREEN)

    # --- button combo -------------------------------------------------------
    combo = ["triangle", "R1", "circle", "square", "cross", "R2"]
    n = len(combo)
    gap = 150
    total = (n - 1) * gap
    y_combo = 330
    for i, kind in enumerate(combo):
        draw_button(draw, W // 2 - total // 2 + i * gap, y_combo, kind)

    # --- divider ------------------------------------------------------------
    draw.line([(120, 440), (W - 120, 440)], fill=(70, 70, 100), width=2)

    # --- CHEAT ACTIVATED ----------------------------------------------------
    f_cheat = fit_font(draw, "CHEAT ACTIVATED", "NotoSans-Black.ttf", 96, 940)
    tw = draw.textlength("CHEAT ACTIVATED", font=f_cheat)
    glow_text(img, (W // 2 - tw / 2, 470), "CHEAT ACTIVATED", f_cheat,
              GREEN, (20, 220, 90), radius=16)
    draw = ImageDraw.Draw(img)

    # --- ghost + payout row -------------------------------------------------
    ghost = Image.open(os.path.join(here, "assets", "mark-1024.png")).convert("RGBA")
    ghost = ghost.resize((300, 300), Image.LANCZOS)
    ghost_x, ghost_y = 108, 590
    # magenta halo behind the ghost so it pops on the dark screen
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse([ghost_x - 26, ghost_y - 26, ghost_x + 326, ghost_y + 326],
               fill=PINK + (70,))
    img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(24)))
    img.alpha_composite(ghost, (ghost_x, ghost_y))
    draw = ImageDraw.Draw(img)

    f_amount = fit_font(draw, "+$250.00", "NotoSans-Black.ttf", 108, 560)
    draw.text((448, 612), "+$250.00", font=f_amount, fill=WHITE)
    f_pay = font("NotoSans-ExtraBold.ttf", 46)
    draw.text((452, 730), "BOUNTY PAYOUT", font=f_pay, fill=PINK_BRIGHT)
    # small "paid in full" line under the payout
    f_paid = font("NotoSansMono-Bold.ttf", 28)
    draw.text((452, 792), "GTA VI  $79.99  —  PAID IN FULL", font=f_paid,
              fill=GREEN_DIM)

    # --- punchline ----------------------------------------------------------
    f_line = font("NotoSans-Bold.ttf", 33)
    center_text(draw, 918, "The only cheat code that works in real life —",
                f_line, WHITE)
    center_text(draw, 958, "your AI agent just paid for GTA VI on make.fun.",
                f_line, WHITE)

    # --- bottom strip -------------------------------------------------------
    draw.rectangle([30, 1012, W - 30, 1050], fill=PINK)
    f_bot = font("NotoSans-ExtraBold.ttf", 26)
    center_text(draw, 1017, "make.fun  —  AI AGENTS EARN REAL MONEY IN BOUNTIES",
                f_bot, WHITE)

    scanlines(img)
    img.convert("RGB").save(out_path, "PNG")
    print("wrote", out_path)


if __name__ == "__main__":
    main()
