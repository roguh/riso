#!/usr/bin/env python3
# coding: utf-8
import colorsys
import random
import sys
from pathlib import Path

import PIL
from PIL import Image, ImageChops, ImageDraw, ImageOps, ImageFont
from PIL.ImageChops import multiply  # The key

try:
    from tqdm import tqdm
except:

    def tqdm(a):
        return a


DEFAULT_INK_COLORS = "cyan magenta yellow black".split()
CACHE = dict()  # ...

def shuffled_colors():
    c = "cyan magenta yellow".split()
    random.shuffle(c)
    return c + ["black"]


def offset_with_chop(i, limit, no_wrap=False):
    rand = lambda: random.randint(-limit, limit)
    x, y = rand(), rand()
    r = ImageChops.offset(i, x, y)
    if no_wrap:
        color = "black"
        if x > 0:
            r.paste(color, (0, 0, x, i.size[1]))
        elif x < 0:
            r.paste(color, (0, i.size[1] - y, x, i.size[1]))  # idk
        if y > 0:
            r.paste(color, (0, 0, i.size[0], y))
        elif y < 0:
            r.paste(color, (i.size[0] - x, 0, i.size[0], y))
    return r


def color_with_rand(color, rand_color_pct):
    P = rand_color_pct / 100
    r, g, b = [c / 255 for c in color]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    rand = lambda: 1 + ((1 - random.random() * 2) * P)
    r = colorsys.hsv_to_rgb(h * rand(), s * rand(), v * rand())
    return tuple((int(c * 255)) % 255 for c in r)

MAX_HEIGHT = 2500 # speed
def get_layers(path):
    if path not in CACHE:
        with Image.open(path) as im:
            w, h = im.size
            if h > MAX_HEIGHT:
                rim = im.resize((int(w * MAX_HEIGHT / h), MAX_HEIGHT))
            else:
                rim = im
            CACHE[path] = rim.convert("CMYK").split()
    return CACHE[path]

def draw(
    path,
    debug=False,
    colors=DEFAULT_INK_COLORS,
    color_pct=0,
    offset_pct=0,
    label=False,
):
    _colors = [PIL.ImageColor.getrgb(c) for c in colors]
    if color_pct:
        _colors = [color_with_rand(c, color_pct) for c in _colors]
    ink_for = dict(zip("CMYK", _colors))

    _layers = get_layers(path)
    size = _layers[0].size
    # Random shift, Riso imperfection
    lim = int(offset_pct / 100 * min(size))
    _layers = [offset_with_chop(L, lim) for L in _layers]
    layers = dict(zip("CMYK", _layers))

    # Colorize each layer.
    # What this does is everything that is black will become the color we have chosen, everything that is white, will remain white. A 50% grey will look like a 50-50 mix of the color and white. Exactly what we want.
    ink_layers = {
        color_name: ImageOps.colorize(
            (ImageOps.invert((layer))), black=ink_for[color_name], white="white"
        )
        for color_name, layer in layers.items()
    }

    # For example: ((Y * C) * M) * K
    def iterate(images, op):
        if len(images) == 1:
            return images[0]
        return op(iterate(images[:-1], op), images[-1])

    # TODO the order doesn't matter, how to simulate effect of different ink ordering?
    # for order in ['YCMK', 'YCM', 'MCY', 'CMY', 'KMYC']:
    # preview2 = iterate([imgs[o] for o in order], multiply)

    preview = iterate(list(ink_layers.values()), multiply)

    if debug:
        # [layer.show() for layer in layers.values()]
        [
            layer.show() if debug is True else debug(name, layer)
            for name, layer in ink_layers.items()
        ]
    if label:
        draw = ImageDraw.Draw(preview)
        # Draw label and rectangles relative to image size
        R = size[1] * 0.025
        RR = R / 10
        try:
            font = ImageFont.truetype("Inconsolata-Light.ttf", max(14, R))
        except OSError:
            font = PIL.ImageFont.load_default()
            print("DEFAULT FONT")
        colors_str = [f"# {r:02X} {g:02X} {b:02X}" for r, g, b in _colors]
        draw.text((10, 10), f"{offset_pct}  {' '.join(colors_str)}", fill="black", font=font)
        for i, c in enumerate(_colors):
            x0, y0 = RR, R + i * R
            x1, y1 = size[0] - RR * 2, R + (i + 1) * R - RR
            draw.rectangle((x0, y0, x1, y1), fill=c)
            draw.text((x0 + RR, y0 + RR), colors_str[i], fill="black", font=font)
    return preview


# https://graphicdesign.stackexchange.com/questions/55673/how-can-i-simulate-screen-printing-offset-colors-in-a-non-destructive-way


def main(fname, N=20):
    fname = Path(fname).expanduser()
    # Try different percentages of color and offset intensities (units are percent %)
    variations = [(2, 5), (1, 1), (2, 0), (0, 1)]
    print("Processing", fname, f"{N} possibilities")
    print("Color/offset randomization percentages:", "; ".join(map(str, variations)))
    # Save each ink layer
    draw(
        fname,
        debug=lambda name, img: img.save(name + ".jpg"),
    )

    # Try MANY variations
    for i in tqdm(range(N)):
        for j, (color_pct, offset_pct) in enumerate(variations):
            suffix = str(fname.with_suffix(f".__{j}_{i}.jpg").name)
            draw(
                fname,
                debug=False,
                colors=shuffled_colors(),
                label=True,
                color_pct=color_pct,
                offset_pct=offset_pct,
            ).save(suffix)

if __name__ == "__main__":
    # _fname = "./Blattermann_test.png"
    # main(_fname, N=1)

    # friend G, Axel, and other 2025s
    # Miss you, Axel <3
    # variations = [(2, 5), (1, 1), (2, 0), (0, 1)]
    # _fname = "~/sync/art/2026/riso/_FEL9990_plus_9994.png"
    # _fname = "~/sync/art/2026/riso/axel_2025-12-23_20.25.57.jpg"
    # _fname = "~/sync/art/2026/riso/_FEL4089.jpg"
    # _fname = "~/sync/art/2026/riso/_FEL8043_pcrop.png"
    # _fname = "~/sync/art/2026/riso/_FEL3175.jpg"
    _fname = "~/sync/art/2026/riso/FEL_0163.jpg"
    main(_fname, N=20)

    # Abstract realism in the Appalachian forest (Ohio 2025)
    # variations = [(2, 5), (1, 1), (2, 0), (0, 1)]
    # for _fname in "3731 3787 3825".split():
    #     main("~/sync/art/2026/riso/_FEL" + _fname + ".jpg", N=5)
