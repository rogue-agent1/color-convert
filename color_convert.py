#!/usr/bin/env python3
"""color_convert - Color space conversion tool."""
import argparse

def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    l = (mx+mn)/2
    if mx == mn: h = s = 0
    else:
        d = mx - mn
        s = d/(2-mx-mn) if l > 0.5 else d/(mx+mn)
        if mx == r: h = (g-b)/d + (6 if g<b else 0)
        elif mx == g: h = (b-r)/d + 2
        else: h = (r-g)/d + 4
        h /= 6
    return round(h*360), round(s*100), round(l*100)

def hsl_to_rgb(h, s, l):
    h, s, l = h/360, s/100, l/100
    if s == 0: r = g = b = l
    else:
        def hue2rgb(p, q, t):
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1/6: return p + (q-p)*6*t
            if t < 1/2: return q
            if t < 2/3: return p + (q-p)*(2/3-t)*6
            return p
        q = l*(1+s) if l < 0.5 else l+s-l*s
        p = 2*l - q
        r, g, b = hue2rgb(p,q,h+1/3), hue2rgb(p,q,h), hue2rgb(p,q,h-1/3)
    return round(r*255), round(g*255), round(b*255)

def rgb_to_cmyk(r, g, b):
    if r==g==b==0: return 0, 0, 0, 100
    c, m, y = 1-r/255, 1-g/255, 1-b/255
    k = min(c,m,y)
    return round((c-k)/(1-k)*100), round((m-k)/(1-k)*100), round((y-k)/(1-k)*100), round(k*100)

def rgb_to_hex(r, g, b): return f"#{r:02x}{g:02x}{b:02x}"
def hex_to_rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0,2,4))

def main():
    p = argparse.ArgumentParser(description="Color converter")
    p.add_argument("color", help="Color value (e.g., '#ff0000', '255,0,0', 'hsl:360,100,50')")
    args = p.parse_args()
    c = args.color
    if c.startswith('#'):
        r, g, b = hex_to_rgb(c)
    elif c.startswith('hsl:'):
        h, s, l = map(int, c[4:].split(','))
        r, g, b = hsl_to_rgb(h, s, l)
    else:
        r, g, b = map(int, c.split(','))
    h, s, l = rgb_to_hsl(r, g, b)
    c, m, y, k = rgb_to_cmyk(r, g, b)
    print(f"RGB:  ({r}, {g}, {b})")
    print(f"Hex:  {rgb_to_hex(r, g, b)}")
    print(f"HSL:  ({h}, {s}%, {l}%)")
    print(f"CMYK: ({c}%, {m}%, {y}%, {k}%)")

if __name__ == "__main__":
    main()
