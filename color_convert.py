#!/usr/bin/env python3
"""Color space converter — RGB, HSL, HSV, HEX, CMYK, YUV.

Usage:
    python color_convert.py "#FF5733"
    python color_convert.py rgb 255 87 51
    python color_convert.py hsl 11 100 60
    python color_convert.py --test
"""
import sys, math

def hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c*2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b): return f"#{r:02X}{g:02X}{b:02X}"

def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    l = (mx+mn)/2
    if mx == mn: return 0, 0, round(l*100,1)
    d = mx - mn
    s = d/(2-mx-mn) if l > 0.5 else d/(mx+mn)
    if mx == r: h = ((g-b)/d + (6 if g < b else 0))/6
    elif mx == g: h = ((b-r)/d + 2)/6
    else: h = ((r-g)/d + 4)/6
    return round(h*360,1), round(s*100,1), round(l*100,1)

def hsl_to_rgb(h, s, l):
    h, s, l = h/360, s/100, l/100
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
    return tuple(round(hue2rgb(p, q, h+x)*255) for x in (1/3, 0, -1/3))

def rgb_to_hsv(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    v = mx
    d = mx - mn
    s = 0 if mx == 0 else d/mx
    if mx == mn: h = 0
    elif mx == r: h = ((g-b)/d + (6 if g < b else 0))/6
    elif mx == g: h = ((b-r)/d + 2)/6
    else: h = ((r-g)/d + 4)/6
    return round(h*360,1), round(s*100,1), round(v*100,1)

def rgb_to_cmyk(r, g, b):
    if r == g == b == 0: return 0, 0, 0, 100
    c, m, y = 1-r/255, 1-g/255, 1-b/255
    k = min(c, m, y)
    return tuple(round(v*100,1) for v in ((c-k)/(1-k), (m-k)/(1-k), (y-k)/(1-k), k))

def rgb_to_yuv(r, g, b):
    y = 0.299*r + 0.587*g + 0.114*b
    u = -0.14713*r - 0.28886*g + 0.436*b
    v = 0.615*r - 0.51499*g - 0.10001*b
    return round(y,2), round(u,2), round(v,2)

def color_name(r, g, b):
    names = {(255,0,0):'Red',(0,255,0):'Green',(0,0,255):'Blue',(255,255,0):'Yellow',
             (255,0,255):'Magenta',(0,255,255):'Cyan',(255,255,255):'White',(0,0,0):'Black',
             (255,165,0):'Orange',(128,0,128):'Purple',(255,192,203):'Pink'}
    best, best_d = 'Unknown', float('inf')
    for (nr,ng,nb), name in names.items():
        d = math.sqrt((r-nr)**2 + (g-ng)**2 + (b-nb)**2)
        if d < best_d: best, best_d = name, d
    return best

def show_all(r, g, b):
    print(f"  HEX:  {rgb_to_hex(r,g,b)}")
    print(f"  RGB:  ({r}, {g}, {b})")
    h,s,l = rgb_to_hsl(r,g,b); print(f"  HSL:  ({h}°, {s}%, {l}%)")
    h,s,v = rgb_to_hsv(r,g,b); print(f"  HSV:  ({h}°, {s}%, {v}%)")
    c,m,y,k = rgb_to_cmyk(r,g,b); print(f"  CMYK: ({c}%, {m}%, {y}%, {k}%)")
    yy,u,v = rgb_to_yuv(r,g,b); print(f"  YUV:  ({yy}, {u}, {v})")
    print(f"  Name: ~{color_name(r,g,b)}")

def test():
    print("=== Color Converter Tests ===\n")
    assert hex_to_rgb("#FF5733") == (255, 87, 51)
    assert rgb_to_hex(255, 87, 51) == "#FF5733"
    print("✓ HEX ↔ RGB")

    r,g,b = hsl_to_rgb(*rgb_to_hsl(255, 87, 51))
    assert abs(r-255) <= 1 and abs(g-87) <= 1 and abs(b-51) <= 1
    print("✓ RGB → HSL → RGB roundtrip")

    assert rgb_to_hsl(255, 0, 0) == (0, 100.0, 50.0)
    print("✓ Pure red HSL")

    assert rgb_to_hsv(255, 0, 0) == (0, 100.0, 100.0)
    print("✓ Pure red HSV")

    assert rgb_to_cmyk(0, 0, 0) == (0, 0, 0, 100)
    print("✓ Black CMYK")

    y,u,v = rgb_to_yuv(255, 255, 255)
    assert abs(y - 255) < 1
    print("✓ White YUV")

    assert hex_to_rgb("#abc") == (170, 187, 204)
    print("✓ Short hex")

    assert color_name(255, 0, 0) == 'Red'
    print("✓ Color name lookup")

    print("\nFull conversion of #FF5733:")
    show_all(255, 87, 51)
    print("\nAll tests passed! ✓")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--test": test()
    elif args[0].startswith('#'): show_all(*hex_to_rgb(args[0]))
    elif args[0] == 'rgb': show_all(int(args[1]), int(args[2]), int(args[3]))
    elif args[0] == 'hsl': show_all(*hsl_to_rgb(float(args[1]), float(args[2]), float(args[3])))
