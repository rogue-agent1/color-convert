#!/usr/bin/env python3
"""color_convert - Convert between color spaces."""
import sys, argparse, json, colorsys

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def main():
    p = argparse.ArgumentParser(description="Color converter")
    p.add_argument("color", help="Color value (hex, rgb, hsl)")
    p.add_argument("--from-space", choices=["hex","rgb","hsl","hsv"], default="hex")
    args = p.parse_args()
    if args.from_space == "hex":
        r, g, b = hex_to_rgb(args.color)
    elif args.from_space == "rgb":
        r, g, b = map(int, args.color.split(","))
    elif args.from_space == "hsl":
        h, s, l = map(float, args.color.split(","))
        r, g, b = [int(x*255) for x in colorsys.hls_to_rgb(h/360, l/100, s/100)]
    elif args.from_space == "hsv":
        h, s, v = map(float, args.color.split(","))
        r, g, b = [int(x*255) for x in colorsys.hsv_to_rgb(h/360, s/100, v/100)]
    h_hls, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    h_hsv, s_hsv, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    print(json.dumps({"hex": rgb_to_hex(r,g,b), "rgb": [r,g,b], "hsl": [round(h_hls*360,1), round(s*100,1), round(l*100,1)], "hsv": [round(h_hsv*360,1), round(s_hsv*100,1), round(v*100,1)]}))

if __name__ == "__main__": main()
