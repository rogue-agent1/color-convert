#!/usr/bin/env python3
"""Color space converter (RGB, HSL, HEX, HSV)."""
import sys
def hex_to_rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0,2,4))
def rgb_to_hex(r, g, b): return f"#{r:02x}{g:02x}{b:02x}"
def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255; mx, mn = max(r,g,b), min(r,g,b)
    l = (mx+mn)/2
    if mx == mn: h = s = 0
    else:
        d = mx - mn; s = d/(2-mx-mn) if l > 0.5 else d/(mx+mn)
        if mx == r: h = ((g-b)/d + (6 if g<b else 0))/6
        elif mx == g: h = ((b-r)/d + 2)/6
        else: h = ((r-g)/d + 4)/6
    return round(h*360), round(s*100), round(l*100)
def hsl_to_rgb(h, s, l):
    h, s, l = h/360, s/100, l/100
    if s == 0: r = g = b = l
    else:
        def hue(p, q, t):
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1/6: return p + (q-p)*6*t
            if t < 1/2: return q
            if t < 2/3: return p + (q-p)*(2/3-t)*6
            return p
        q = l*(1+s) if l < 0.5 else l+s-l*s; p = 2*l-q
        r, g, b = hue(p,q,h+1/3), hue(p,q,h), hue(p,q,h-1/3)
    return round(r*255), round(g*255), round(b*255)
if __name__ == "__main__":
    colors = ["#ff6347", "#4169e1", "#32cd32", "#ffd700"]
    for c in colors:
        r,g,b = hex_to_rgb(c); h,s,l = rgb_to_hsl(r,g,b)
        print(f"  {c} -> RGB({r},{g},{b}) -> HSL({h},{s}%,{l}%) -> {rgb_to_hex(*hsl_to_rgb(h,s,l))}")
