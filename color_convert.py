#!/usr/bin/env python3
"""Color converter — hex, RGB, HSL, HSV, CMYK with named color lookup."""
import sys, colorsys

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b): return f"#{r:02x}{g:02x}{b:02x}"

def rgb_to_hsl(r, g, b):
    r1, g1, b1 = r/255, g/255, b/255
    h, l, s = colorsys.rgb_to_hls(r1, g1, b1)
    return round(h*360), round(s*100), round(l*100)

def rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    return round(h*360), round(s*100), round(v*100)

def rgb_to_cmyk(r, g, b):
    if r == g == b == 0: return 0, 0, 0, 100
    c, m, y = 1-r/255, 1-g/255, 1-b/255
    k = min(c, m, y); c, m, y = (c-k)/(1-k), (m-k)/(1-k), (y-k)/(1-k)
    return round(c*100), round(m*100), round(y*100), round(k*100)

def show_swatch(r, g, b):
    return f"\033[48;2;{r};{g};{b}m    \033[0m"

def cli():
    if len(sys.argv) < 2: print("Usage: color_convert <#hex | R G B>"); sys.exit(1)
    if sys.argv[1].startswith("#"): r, g, b = hex_to_rgb(sys.argv[1])
    else: r, g, b = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    print(f"  Swatch: {show_swatch(r,g,b)}")
    print(f"  Hex:  {rgb_to_hex(r,g,b)}")
    print(f"  RGB:  ({r}, {g}, {b})")
    print(f"  HSL:  {rgb_to_hsl(r,g,b)}")
    print(f"  HSV:  {rgb_to_hsv(r,g,b)}")
    print(f"  CMYK: {rgb_to_cmyk(r,g,b)}")

if __name__ == "__main__": cli()
