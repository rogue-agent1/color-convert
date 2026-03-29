from color_convert import hex_to_rgb, rgb_to_hex, rgb_to_hsl, hsl_to_rgb, rgb_to_cmyk, complementary
assert hex_to_rgb("#ff0000") == (255, 0, 0)
assert rgb_to_hex(255, 0, 0) == "#ff0000"
h, s, l = rgb_to_hsl(255, 0, 0)
assert h == 0 and s == 100 and l == 50
r, g, b = hsl_to_rgb(0, 100, 50)
assert (r, g, b) == (255, 0, 0)
assert complementary(255, 0, 0) == (0, 255, 255)
print("Color convert tests passed")