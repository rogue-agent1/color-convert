#!/usr/bin/env python3
"""color_convert - Convert between color spaces."""
import argparse, math, sys

def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    l = (mx+mn)/2
    if mx == mn: return 0, 0, l
    d = mx - mn
    s = d/(2-mx-mn) if l > 0.5 else d/(mx+mn)
    if mx == r: h = (g-b)/d + (6 if g < b else 0)
    elif mx == g: h = (b-r)/d + 2
    else: h = (r-g)/d + 4
    return h*60, s, l

def hsl_to_rgb(h, s, l):
    if s == 0: v = int(l*255); return v, v, v
    def hue2rgb(p, q, t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q-p)*6*t
        if t < 1/2: return q
        if t < 2/3: return p + (q-p)*(2/3-t)*6
        return p
    q = l*(1+s) if l < 0.5 else l+s-l*s
    p = 2*l - q
    return tuple(int(hue2rgb(p, q, h/360+x)*255) for x in [1/3, 0, -1/3])

def rgb_to_hex(r, g, b): return f"#{r:02x}{g:02x}{b:02x}"
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_cmyk(r, g, b):
    if r == g == b == 0: return 0, 0, 0, 1.0
    c, m, y = 1-r/255, 1-g/255, 1-b/255
    k = min(c, m, y)
    return (c-k)/(1-k), (m-k)/(1-k), (y-k)/(1-k), k

def main():
    p = argparse.ArgumentParser(description="Color space converter")
    p.add_argument("input", help="Color value (e.g., #ff0000, rgb(255,0,0), hsl(0,100,50))")
    a = p.parse_args()
    inp = a.input.strip()
    if inp.startswith("#"):
        r, g, b = hex_to_rgb(inp)
    elif inp.startswith("rgb"):
        parts = inp.replace("rgb(","").replace(")","").split(",")
        r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
    elif inp.startswith("hsl"):
        parts = inp.replace("hsl(","").replace(")","").split(",")
        r, g, b = hsl_to_rgb(float(parts[0]), float(parts[1])/100, float(parts[2])/100)
    else:
        parts = inp.split(",")
        r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
    h, s, l = rgb_to_hsl(r, g, b)
    c, m, y, k = rgb_to_cmyk(r, g, b)
    print(f"HEX:  {rgb_to_hex(r,g,b)}")
    print(f"RGB:  rgb({r},{g},{b})")
    print(f"HSL:  hsl({h:.0f},{s*100:.0f}%,{l*100:.0f}%)")
    print(f"CMYK: cmyk({c:.0f}%,{m:.0f}%,{y:.0f}%,{k*100:.0f}%)")

if __name__ == "__main__": main()
