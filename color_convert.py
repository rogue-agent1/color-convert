#!/usr/bin/env python3
"""Color converter — hex, RGB, HSL, HSV, CMYK."""
import sys, colorsys
def hex_to_rgb(h): h=h.lstrip("#"); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def rgb_to_hex(r,g,b): return f"#{r:02x}{g:02x}{b:02x}"
def cli():
    if len(sys.argv) < 2: print("Usage: color_convert <#hex | R G B>"); sys.exit(1)
    if sys.argv[1].startswith("#"): r,g,b = hex_to_rgb(sys.argv[1])
    else: r,g,b = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
    h,l,s = colorsys.rgb_to_hls(r/255,g/255,b/255)
    hv,sv,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    print(f"  Hex: {rgb_to_hex(r,g,b)}  RGB: ({r},{g},{b})")
    print(f"  HSL: ({h*360:.0f},{s*100:.0f}%,{l*100:.0f}%)  HSV: ({hv*360:.0f},{sv*100:.0f}%,{v*100:.0f}%)")
if __name__ == "__main__": cli()
