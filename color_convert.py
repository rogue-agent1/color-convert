#!/usr/bin/env python3
"""Color space converter. Zero dependencies."""
import math, sys

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    l = (mx+mn)/2
    if mx == mn: return 0, 0, round(l*100, 1)
    d = mx - mn
    s = d/(2-mx-mn) if l > 0.5 else d/(mx+mn)
    if mx == r: h = (g-b)/d + (6 if g < b else 0)
    elif mx == g: h = (b-r)/d + 2
    else: h = (r-g)/d + 4
    return round(h*60, 1), round(s*100, 1), round(l*100, 1)

def hsl_to_rgb(h, s, l):
    s, l = s/100, l/100
    if s == 0: v = round(l*255); return v, v, v
    def hue2rgb(p, q, t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q-p)*6*t
        if t < 1/2: return q
        if t < 2/3: return p + (q-p)*(2/3-t)*6
        return p
    q = l*(1+s) if l < 0.5 else l+s-l*s
    p = 2*l - q
    h /= 360
    return tuple(round(hue2rgb(p, q, h+x)*255) for x in (1/3, 0, -1/3))

def rgb_to_hsv(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    v = mx; d = mx - mn; s = 0 if mx == 0 else d/mx
    if mx == mn: h = 0
    elif mx == r: h = (g-b)/d + (6 if g < b else 0)
    elif mx == g: h = (b-r)/d + 2
    else: h = (r-g)/d + 4
    return round(h*60, 1), round(s*100, 1), round(v*100, 1)

def rgb_to_cmyk(r, g, b):
    if r == g == b == 0: return 0, 0, 0, 100
    c, m, y = 1-r/255, 1-g/255, 1-b/255
    k = min(c, m, y)
    return tuple(round((v-k)/(1-k)*100, 1) for v in (c, m, y)) + (round(k*100, 1),)

def complementary(r, g, b):
    return 255-r, 255-g, 255-b

def blend(c1, c2, t=0.5):
    return tuple(round(a*(1-t) + b*t) for a, b in zip(c1, c2))

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Color converter")
    p.add_argument("color", help="Hex color like #ff0000")
    args = p.parse_args()
    r, g, b = hex_to_rgb(args.color)
    print(f"RGB:  ({r}, {g}, {b})")
    print(f"HSL:  {rgb_to_hsl(r,g,b)}")
    print(f"HSV:  {rgb_to_hsv(r,g,b)}")
    print(f"CMYK: {rgb_to_cmyk(r,g,b)}")
    print(f"Comp: {rgb_to_hex(*complementary(r,g,b))}")
