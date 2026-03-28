#!/usr/bin/env python3
"""color_convert — Convert between color formats (HEX, RGB, HSL, HSV, CMYK).

Usage:
    color_convert.py "#ff6600"
    color_convert.py "rgb(255, 102, 0)"
    color_convert.py "hsl(24, 100%, 50%)"
    color_convert.py --from hex --to rgb ff6600
    color_convert.py palette "#ff6600" --type complementary
    color_convert.py blend "#ff0000" "#0000ff" --steps 5
"""

import re
import sys
import json
import argparse
import colorsys


def hex_to_rgb(h: str) -> tuple:
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b) -> str:
    return f'#{r:02x}{g:02x}{b:02x}'


def rgb_to_hsl(r, g, b) -> tuple:
    r1, g1, b1 = r / 255, g / 255, b / 255
    h, l, s = colorsys.rgb_to_hls(r1, g1, b1)
    return round(h * 360, 1), round(s * 100, 1), round(l * 100, 1)


def hsl_to_rgb(h, s, l) -> tuple:
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return round(r * 255), round(g * 255), round(b * 255)


def rgb_to_hsv(r, g, b) -> tuple:
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return round(h * 360, 1), round(s * 100, 1), round(v * 100, 1)


def hsv_to_rgb(h, s, v) -> tuple:
    r, g, b = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
    return round(r * 255), round(g * 255), round(b * 255)


def rgb_to_cmyk(r, g, b) -> tuple:
    if r == 0 and g == 0 and b == 0:
        return 0, 0, 0, 100
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255
    k = min(c, m, y)
    c = round((c - k) / (1 - k) * 100, 1)
    m = round((m - k) / (1 - k) * 100, 1)
    y = round((y - k) / (1 - k) * 100, 1)
    return c, m, y, round(k * 100, 1)


def cmyk_to_rgb(c, m, y, k) -> tuple:
    c, m, y, k = c / 100, m / 100, y / 100, k / 100
    r = round(255 * (1 - c) * (1 - k))
    g = round(255 * (1 - m) * (1 - k))
    b = round(255 * (1 - y) * (1 - k))
    return r, g, b


def parse_color(s: str) -> tuple:
    """Parse any color format to RGB tuple."""
    s = s.strip()
    # Hex
    if re.match(r'^#?[0-9a-fA-F]{3,6}$', s):
        return hex_to_rgb(s)
    # rgb(r, g, b)
    m = re.match(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', s)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    # hsl(h, s%, l%)
    m = re.match(r'hsl\(\s*([\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?\s*\)', s)
    if m:
        return hsl_to_rgb(float(m.group(1)), float(m.group(2)), float(m.group(3)))
    # hsv(h, s%, v%)
    m = re.match(r'hsv\(\s*([\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?\s*\)', s)
    if m:
        return hsv_to_rgb(float(m.group(1)), float(m.group(2)), float(m.group(3)))
    raise ValueError(f'Cannot parse color: {s!r}')


def color_block(r, g, b) -> str:
    """ANSI true color block."""
    return f'\033[48;2;{r};{g};{b}m    \033[0m'


def show_all_formats(r, g, b, with_preview=True):
    h_hsl, s_hsl, l_hsl = rgb_to_hsl(r, g, b)
    h_hsv, s_hsv, v_hsv = rgb_to_hsv(r, g, b)
    c, m, y, k = rgb_to_cmyk(r, g, b)
    
    if with_preview:
        print(f'Preview: {color_block(r, g, b)}')
    print(f'HEX:  {rgb_to_hex(r, g, b)}')
    print(f'RGB:  rgb({r}, {g}, {b})')
    print(f'HSL:  hsl({h_hsl}, {s_hsl}%, {l_hsl}%)')
    print(f'HSV:  hsv({h_hsv}, {s_hsv}%, {v_hsv}%)')
    print(f'CMYK: cmyk({c}%, {m}%, {y}%, {k}%)')


def cmd_convert(args):
    color = ' '.join(args.color) if args.color else args.input
    r, g, b = parse_color(color)
    if args.json:
        h_hsl, s_hsl, l_hsl = rgb_to_hsl(r, g, b)
        h_hsv, s_hsv, v_hsv = rgb_to_hsv(r, g, b)
        c, m, y, k = rgb_to_cmyk(r, g, b)
        print(json.dumps({
            'hex': rgb_to_hex(r, g, b),
            'rgb': [r, g, b],
            'hsl': [h_hsl, s_hsl, l_hsl],
            'hsv': [h_hsv, s_hsv, v_hsv],
            'cmyk': [c, m, y, k],
        }, indent=2))
    else:
        show_all_formats(r, g, b)


def cmd_palette(args):
    r, g, b = parse_color(args.color)
    h, s, l = rgb_to_hsl(r, g, b)
    
    palettes = {
        'complementary': [(h + 180) % 360],
        'analogous': [(h - 30) % 360, (h + 30) % 360],
        'triadic': [(h + 120) % 360, (h + 240) % 360],
        'split': [(h + 150) % 360, (h + 210) % 360],
        'tetradic': [(h + 90) % 360, (h + 180) % 360, (h + 270) % 360],
    }
    
    hues = palettes.get(args.type, palettes['complementary'])
    
    print(f'Base: {rgb_to_hex(r, g, b)} {color_block(r, g, b)}')
    print(f'Type: {args.type}\n')
    for hue in hues:
        pr, pg, pb = hsl_to_rgb(hue, s, l)
        print(f'  {rgb_to_hex(pr, pg, pb)} {color_block(pr, pg, pb)} hsl({hue:.0f}, {s}%, {l}%)')


def cmd_blend(args):
    r1, g1, b1 = parse_color(args.color1)
    r2, g2, b2 = parse_color(args.color2)
    
    steps = args.steps
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0
        r = round(r1 + (r2 - r1) * t)
        g = round(g1 + (g2 - g1) * t)
        b = round(b1 + (b2 - b1) * t)
        print(f'{rgb_to_hex(r, g, b)} {color_block(r, g, b)}')


def main():
    p = argparse.ArgumentParser(description='Color format converter')
    p.add_argument('--json', action='store_true')
    sub = p.add_subparsers(dest='cmd')

    # Default: convert
    sc = sub.add_parser('convert', help='Convert color between formats')
    sc.add_argument('color', nargs='+')
    sc.set_defaults(func=cmd_convert)

    sp = sub.add_parser('palette', help='Generate color palette')
    sp.add_argument('color')
    sp.add_argument('--type', choices=['complementary', 'analogous', 'triadic', 'split', 'tetradic'], default='complementary')
    sp.set_defaults(func=cmd_palette)

    sb = sub.add_parser('blend', help='Blend between two colors')
    sb.add_argument('color1')
    sb.add_argument('color2')
    sb.add_argument('--steps', type=int, default=5)
    sb.set_defaults(func=cmd_blend)

    args = p.parse_args()
    if args.cmd is None:
        # Try to parse first arg as color
        if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
            args.color = sys.argv[1:]
            args.json = False
            args.func = cmd_convert
        else:
            p.print_help()
            return
    args.func(args)


if __name__ == '__main__':
    main()
