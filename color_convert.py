#!/usr/bin/env python3
"""Color format converter (hex/rgb/hsl)."""
import sys, colorsys, re

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0,2,4))

def rgb_to_hex(r,g,b): return f'#{r:02x}{g:02x}{b:02x}'

def rgb_to_hsl(r,g,b):
    h,l,s = colorsys.rgb_to_hls(r/255,g/255,b/255)
    return round(h*360), round(s*100), round(l*100)

def hsl_to_rgb(h,s,l):
    r,g,b = colorsys.hls_to_rgb(h/360,l/100,s/100)
    return round(r*255), round(g*255), round(b*255)

def parse_and_convert(s):
    s = s.strip()
    if s.startswith('#') or re.match(r'^[0-9a-fA-F]{6}$', s):
        r,g,b = hex_to_rgb(s)
        h,sat,l = rgb_to_hsl(r,g,b)
        print(f"HEX: {rgb_to_hex(r,g,b)}")
        print(f"RGB: rgb({r}, {g}, {b})")
        print(f"HSL: hsl({h}, {sat}%, {l}%)")
    elif s.startswith('rgb'):
        nums = list(map(int, re.findall(r'\d+', s)))
        r,g,b = nums[:3]
        h,sat,l = rgb_to_hsl(r,g,b)
        print(f"HEX: {rgb_to_hex(r,g,b)}")
        print(f"RGB: rgb({r}, {g}, {b})")
        print(f"HSL: hsl({h}, {sat}%, {l}%)")
    elif s.startswith('hsl'):
        nums = list(map(int, re.findall(r'\d+', s)))
        h,sat,l = nums[:3]
        r,g,b = hsl_to_rgb(h,sat,l)
        print(f"HEX: {rgb_to_hex(r,g,b)}")
        print(f"RGB: rgb({r}, {g}, {b})")
        print(f"HSL: hsl({h}, {sat}%, {l}%)")

if __name__ == '__main__':
    if len(sys.argv) < 2: print("Usage: color_convert.py <color>"); sys.exit(1)
    parse_and_convert(' '.join(sys.argv[1:]))
