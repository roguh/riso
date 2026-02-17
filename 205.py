#!/usr/bin/env python3
# coding: utf-8
import colorsys
import random
import sys
from pathlib import Path

import PIL
from PIL import Image, ImageChops, ImageDraw, ImageOps
from PIL.ImageChops import multiply  # The key
from tqdm import tqdm


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
    r, g, b = [c / 255 for c in PIL.ImageColor.getrgb(color)]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    rand = lambda _max: 1 + ((1 - random.random() * 2) * P)
    r = colorsys.hsv_to_rgb(h * rand(1), s * rand(1), (v * rand(1)))
    return [(int(c * 255)) % 255 for c in r]


def draw(
    path,
    debug=False,
    colors="cyan magenta yellow black",
    color_pct=0,
    offset_pct=0,
    label=False,
):
    _colors = [color_with_rand(c, color_pct) for c in colors.split()]
    ink_for = dict(zip("CMYK", _colors))

    with Image.open(fname) as im:
        _layers = im.convert("CMYK").split()
        size = _layers[0].size
        # Random shift, Riso imperfection
        lim = int(offset_pct / 100 * min(size))
        _layers = [offset_with_chop(L, lim) for L in _layers]
        layers = dict(zip("CMYK", _layers))

    # Colorize each layer.
    # What this does is everything that is black will become the color we have chosen, everything that is white, will remain white. A 50% grey will look like a 50-50 mix of the color and white. Exactly what we want.
    ink_layers = {color_name:
        ImageOps.colorize(
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
        [layer.show() if debug is True else debug(name, layer) for name, layer in ink_layers.items()]
    if label:
        draw = ImageDraw.Draw(preview)
        try:
            ImageFont.truetype("Arial.ttf", 50)
        except:
            font = PIL.ImageFont.load_default()
        color_str = " ".join(f"#{r:02X}{g:02X}{b:02X}" for r, g, b in _colors)
        draw.text((10, 10), f"{offset_pct}  {color_str}", fill="black", font=font)
    return preview


# https://graphicdesign.stackexchange.com/questions/55673/how-can-i-simulate-screen-printing-offset-colors-in-a-non-destructive-way


if __name__ == "__main__":
    # "./Blattermann_test.png"
    N = 20
    fname = "~/sync/art/2026/_FEL9990_plus_9994.png"
    fname = Path(fname).expanduser()
    # Save each ink layer
    draw(
        fname,
        debug=lambda name, img: img.save(name + ".png"),
    )

    for i in tqdm(range(N)):
        suffix = str(fname.with_suffix(f"._{i}.png").name)
        draw(
            fname,
            debug=False,
            label=True,
            color_pct=20,
            offset_pct=5,
        ).save(suffix)
