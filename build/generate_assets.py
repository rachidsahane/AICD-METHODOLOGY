#!/usr/bin/env python3
"""Generate the two raster assets the AICD document references.

By default this regenerates only assets/social-preview.png, the card link
previews show, from whatever cover is in src/.

src/cover_bg.jpg and src/portrait_circle.png are the AUTHOR'S OWN artwork and
photograph. They are committed source, not build output, and a normal run does
not touch them. The generated stand-ins are still here, behind --placeholders,
for a checkout where the artwork is missing; that flag overwrites both files.

The output is deterministic: every random draw is seeded, so re-running this
script reproduces the committed files byte for byte on the same Pillow and
NumPy versions.

Usage:
    python3 build/generate_assets.py [--out-dir src]

Requires Pillow and NumPy (see build/requirements.txt).

The cover background is an original generated work and is covered by the
repository's CC BY 4.0 license. The portrait file produced here is a monogram
placeholder, not a photograph; see build/fonts.md and PUBLISHING.md.
"""

import argparse
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Palette lifted from the document's own CSS custom properties.
INK = (27, 31, 36)
ACCENT = (15, 76, 92)
ACCENT2 = (227, 100, 20)
PALE = (206, 228, 234)
LIGHT = np.array([244.0, 247.0, 248.0])
DEEP = np.array([12.0, 62.0, 76.0])

# Font files are looked up by name across the usual platform locations.
FONT_DIRS = [
    os.path.expanduser("~/Library/Fonts"),
    "/Library/Fonts",
    "/System/Library/Fonts",
    "/usr/share/fonts/truetype/crosextra",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype",
    "/usr/share/fonts",
    "/usr/local/share/fonts",
]


def find_font(*names):
    """Return the first readable path for any of the given font file names."""
    for name in names:
        for root in FONT_DIRS:
            if not os.path.isdir(root):
                continue
            direct = os.path.join(root, name)
            if os.path.isfile(direct):
                return direct
            for dirpath, _dirnames, filenames in os.walk(root):
                if name in filenames:
                    return os.path.join(dirpath, name)
    raise SystemExit(
        "font not found: tried %s. Install the document fonts first; "
        "build/fonts.md lists the commands." % ", ".join(names)
    )


def smoothstep(v, a, b):
    s = np.clip((v - a) / (b - a), 0.0, 1.0)
    return s * s * (3.0 - 2.0 * s)


# --------------------------------------------------------------------- cover

def build_cover(path):
    """A4 cover background: a calm light field above a deep teal field.

    The upper two thirds stay near-flat because the cover sets 96pt type
    directly on them with no panel behind it. The lower field carries five
    strata lines, one per layer of the methodology's architecture, and a
    sparse constellation that fades out at the horizon.
    """
    width, height = 2480, 3508           # A4 at 300 dpi
    mm = width / 210.0                   # pixels per millimetre
    ss = 2                               # supersample factor for vector work
    horizon_a, horizon_b = 176.0, 268.0  # transition band, in millimetres

    xs = np.arange(width, dtype=np.float64)
    ys = np.arange(height, dtype=np.float64)
    grid_x, grid_y = np.meshgrid(xs, ys)
    x_mm, y_mm = grid_x / mm, grid_y / mm

    tilt = (x_mm / 210.0 - 0.5) * 7.0    # the horizon leans very slightly
    t = smoothstep(y_mm + tilt, horizon_a, horizon_b)

    base = LIGHT[None, None, :] * (1.0 - t[..., None]) + DEEP[None, None, :] * t[..., None]

    # A barely-there wash keeps the light field from reading as dead flat.
    wash = np.clip(
        1.0 - np.sqrt(((x_mm - 200.0) / 210.0) ** 2 + ((y_mm - 6.0) / 220.0) ** 2), 0.0, 1.0
    )
    base -= (wash ** 2 * (1.0 - t))[..., None] * np.array([7.0, 4.0, 3.0])[None, None, :]

    # Depth in the lower field only, masked well past the horizon.
    deep_mask = t ** 2
    glow_x, glow_y, glow_r = 0.30 * width, 1.02 * height, 0.72 * width
    dist = np.sqrt((grid_x - glow_x) ** 2 + (grid_y - glow_y) ** 2) / glow_r
    base += (np.clip(1.0 - dist, 0.0, 1.0) ** 2 * deep_mask)[..., None] * np.array(
        [16.0, 46.0, 54.0]
    )

    field = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")

    vec = Image.new("RGBA", (width * ss, height * ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(vec)

    def px(v):
        return v * mm * ss

    # Five strata, one per layer, clear of the cover's author panel.
    for idx, line_mm in enumerate([234.0, 247.0, 260.0, 273.0, 286.0]):
        alpha = int(30 + 8 * idx)
        draw.line(
            [px(0.0), px(line_mm), px(210.0), px(line_mm)],
            fill=PALE + (alpha,),
            width=max(1, int(0.30 * mm * ss)),
        )
        draw.line(
            [px(0.0), px(line_mm), px(10.0 + 2.5 * idx), px(line_mm)],
            fill=ACCENT2 + (int(alpha * 2.3),),
            width=max(1, int(0.50 * mm * ss)),
        )

    rng = random.Random(20260930)
    cell, jitter, link = 33.0, 11.0, 41.0
    nodes = []
    for row in range(-1, int(297 / cell) + 2):
        for col in range(-1, int(210 / cell) + 2):
            node_x = col * cell + rng.uniform(-jitter, jitter)
            node_y = row * cell + rng.uniform(-jitter, jitter)
            if -12 < node_x < 222 and 168.0 < node_y < 309:
                nodes.append((node_x, node_y))

    def fade(value_mm):
        return float(smoothstep(np.array(value_mm), 186.0, 236.0))

    edges = set()
    for i, (x1, y1) in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            x2, y2 = nodes[j]
            if math.hypot(x2 - x1, y2 - y1) <= link:
                edges.add((i, j))

    for i, j in sorted(edges):
        x1, y1 = nodes[i]
        x2, y2 = nodes[j]
        alpha = 19.0 * fade(0.5 * (y1 + y2))
        if alpha < 1.0:
            continue
        draw.line(
            [px(x1), px(y1), px(x2), px(y2)],
            fill=PALE + (int(alpha),),
            width=max(1, int(0.24 * mm * ss)),
        )

    for k, (node_x, node_y) in enumerate(nodes):
        alpha = 40.0 * fade(node_y)
        if alpha < 1.5:
            continue
        accent = (k % 17 == 9)
        radius = rng.uniform(0.9, 1.6) + (0.5 if accent else 0.0)
        colour = ACCENT2 if accent else PALE
        if accent:
            alpha = min(175.0, alpha * 3.6)
        draw.ellipse(
            [px(node_x - radius), px(node_y - radius), px(node_x + radius), px(node_y + radius)],
            fill=colour + (int(alpha),),
        )

    vec = vec.resize((width, height), Image.LANCZOS)
    out = Image.alpha_composite(field.convert("RGBA"), vec).convert("RGB")

    # A little noise dithers the gradient, which otherwise bands under JPEG.
    arr = np.asarray(out, dtype=np.float64)
    noise = np.random.default_rng(7).normal(0.0, 1.5, size=(height, width, 1))
    out = Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8), "RGB")

    out.save(path, "JPEG", quality=90, optimize=True, progressive=True, dpi=(300, 300))
    return out.size


# ------------------------------------------------------------------ portrait

def build_portrait(path):
    """Monogram placeholder for the author photograph.

    This is not a likeness and is not a photograph. It exists so the document
    builds and renders correctly before a real portrait is supplied. Replace
    src/portrait_circle.png with a square photograph to use the real one; no
    markup change is needed. The CSS clips the file to a circle and draws the
    teal border, so the design here stays inside the inscribed circle.
    """
    size = 1000
    ss = 4
    big = size * ss

    xs = np.arange(size, dtype=np.float64)
    grid_x, grid_y = np.meshgrid(xs, xs)
    radius = np.sqrt((grid_x - size / 2.0) ** 2 + (grid_y - size / 2.0) ** 2) / (size / 2.0)

    centre = np.array([24.0, 98.0, 117.0])
    edge = np.array([9.0, 50.0, 62.0])
    blend = np.clip(radius, 0.0, 1.2) / 1.2
    blend = blend ** 1.35
    base = centre[None, None, :] * (1.0 - blend[..., None]) + edge[None, None, :] * blend[..., None]

    # Light falls from the upper left, the way it does in the cover's field.
    lift = np.clip(
        1.0 - np.sqrt(((grid_x - 0.30 * size) / (0.85 * size)) ** 2
                      + ((grid_y - 0.24 * size) / (0.85 * size)) ** 2),
        0.0,
        1.0,
    )
    base += (lift ** 2)[..., None] * np.array([14.0, 30.0, 34.0])[None, None, :]

    field = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

    vec = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(vec)

    # A quiet ring, and one orange arc as the accent the document uses.
    ring_r = 0.405 * big
    box = [big / 2 - ring_r, big / 2 - ring_r, big / 2 + ring_r, big / 2 + ring_r]
    draw.ellipse(box, outline=PALE + (46,), width=max(1, int(0.004 * big)))
    draw.arc(box, start=118, end=188, fill=ACCENT2 + (205,), width=max(1, int(0.011 * big)))

    # Sparse constellation, the same motif as the cover, kept very faint.
    rng = random.Random(4071)
    points = []
    while len(points) < 26:
        px_, py_ = rng.uniform(0.08, 0.92), rng.uniform(0.08, 0.92)
        if math.hypot(px_ - 0.5, py_ - 0.5) < 0.46:
            points.append((px_ * big, py_ * big))
    for i, (x1, y1) in enumerate(points):
        for x2, y2 in points[i + 1:]:
            if math.hypot(x2 - x1, y2 - y1) <= 0.22 * big:
                draw.line([x1, y1, x2, y2], fill=PALE + (16,), width=max(1, int(0.0018 * big)))
    for x1, y1 in points:
        r = 0.0035 * big
        draw.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=PALE + (40,))

    # Monogram. Caladea is the face the document actually renders the author
    # name in, because the GFS Baskerville listed before it carries no Latin
    # glyphs at all; build/fonts.md records the measurement.
    font_path = find_font("Caladea-Regular.ttf", "Caladea-Bold.ttf", "DejaVuSerif.ttf")
    font = ImageFont.truetype(font_path, int(0.355 * big))

    letters = ["A", "S"]
    tracking = int(0.045 * big)
    widths = []
    for ch in letters:
        left, _top, right, _bottom = font.getbbox(ch)
        widths.append(right - left)
    total = sum(widths) + tracking * (len(letters) - 1)

    probe = font.getbbox("AS")
    glyph_top, glyph_bottom = probe[1], probe[3]
    cursor = (big - total) / 2.0
    baseline_y = big / 2.0 - (glyph_top + glyph_bottom) / 2.0
    for ch, w in zip(letters, widths):
        left = font.getbbox(ch)[0]
        draw.text((cursor - left, baseline_y), ch, font=font, fill=(234, 241, 243, 240))
        cursor += w + tracking

    vec = vec.resize((size, size), Image.LANCZOS)
    out = Image.alpha_composite(field, vec).convert("RGB")

    # No dithering here, unlike the cover. PNG is lossless, so the gradient
    # carries no compression banding, and grain would more than triple the
    # file size for no visible gain at the 58mm the page prints it at.
    out.save(path, "PNG", optimize=True)
    return out.size


# -------------------------------------------------------------- social preview

def build_social(path, cover_path):
    """The 1280x640 card that link previews show on LinkedIn, X and Slack.

    Built from whatever cover is in src/, so it stays in step with the
    document rather than drifting from it. The crop is a fixed 2:1 band
    centred at 42 percent of the cover height, which is where both the
    author's artwork and the generated stand-in carry their detail. The
    type colours and the scrim are then chosen from the luminance of that
    band, so the card is legible whether the cover is light or dark. That
    matters: these cards are read at a third of their size in a feed.
    """
    width, height = 1280, 640

    cover = Image.open(cover_path).convert("RGB")
    crop_h = min(cover.height, cover.width // 2)
    crop_w = crop_h * 2
    x0 = (cover.width - crop_w) // 2
    y_centre = int(cover.height * 0.42)
    y0 = max(0, min(cover.height - crop_h, y_centre - crop_h // 2))
    card = cover.crop((x0, y0, x0 + crop_w, y0 + crop_h))
    card = card.resize((width, height), Image.LANCZOS).convert("RGBA")

    band = np.asarray(card.convert("L"), dtype=np.float64)
    light_ground = band.mean() > 140.0

    ss = 3
    layer = Image.new("RGBA", (width * ss, height * ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    left = 74 * ss
    if light_ground:
        # Mirror what the cover itself does: set the type over a panel rather
        # than straight onto the artwork it would otherwise compete with.
        draw.rectangle([0, 52 * ss, 900 * ss, 534 * ss], fill=(255, 255, 255, 214))
        acronym_fill = ACCENT + (255,)
        longform_fill = ACCENT2 + (255,)
        tagline_fill = INK + (255,)
    else:
        arr = np.asarray(card.convert("RGB"), dtype=np.float64) * 0.88
        card = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
        acronym_fill = (243, 248, 249, 255)
        longform_fill = (240, 150, 84, 255)
        tagline_fill = (214, 231, 236, 255)

    serif = find_font("Caladea-Regular.ttf", "DejaVuSerif.ttf")
    sans = find_font("Carlito-Regular.ttf", "DejaVuSans.ttf")
    italic = find_font("Caladea-Italic.ttf", "Caladea-Regular.ttf", "DejaVuSerif-Italic.ttf")

    draw.text((left, 86 * ss), "AICD", font=ImageFont.truetype(serif, 176 * ss), fill=acronym_fill)

    rule_y = 300 * ss
    draw.rectangle([left, rule_y, left + 128 * ss, rule_y + 7 * ss], fill=ACCENT2 + (255,))

    draw.text((left, 338 * ss), "Artificial Intelligence Centered Development",
              font=ImageFont.truetype(italic, 40 * ss), fill=longform_fill)

    tagline = ImageFont.truetype(sans, 33 * ss)
    for i, line in enumerate((
        "A software development methodology for teams",
        "whose code is written by AI agents.",
    )):
        draw.text((left, (426 + i * 46) * ss), line, font=tagline, fill=tagline_fill)

    layer = layer.resize((width, height), Image.LANCZOS)
    out = Image.alpha_composite(card, layer).convert("RGB")
    out.save(path, "PNG", optimize=True)
    return out.size


def main():
    parser = argparse.ArgumentParser(description="Generate the AICD document assets.")
    parser.add_argument(
        "--out-dir",
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"),
        help="directory holding the document's images (default: src/)",
    )
    parser.add_argument(
        "--placeholders",
        action="store_true",
        help=(
            "also regenerate cover_bg.jpg and portrait_circle.png. These are the "
            "author's own artwork and photograph, so this OVERWRITES them with "
            "generated stand-ins. Only for a checkout where they are missing."
        ),
    )
    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    cover = os.path.join(args.out_dir, "cover_bg.jpg")
    portrait = os.path.join(args.out_dir, "portrait_circle.png")

    if args.placeholders:
        print("cover_bg.jpg        %dx%d  (generated stand-in, overwrote the artwork)" % build_cover(cover))
        print("portrait_circle.png %dx%d  (monogram, NOT a photograph)" % build_portrait(portrait))

    if not os.path.isfile(cover):
        raise SystemExit(
            "generate_assets: %s is missing. It is the author's cover artwork and is "
            "committed to the repository. Restore it, or pass --placeholders to "
            "generate a stand-in." % cover
        )

    social_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    os.makedirs(social_dir, exist_ok=True)
    social = os.path.join(social_dir, "social-preview.png")
    print("social-preview.png  %dx%d  (from %s)" % (build_social(social, cover) + (os.path.basename(cover),)))
    print("written to %s" % social_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
