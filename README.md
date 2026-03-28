# color_convert

Convert between color formats (HEX, RGB, HSL, HSV, CMYK). Generate palettes and gradients.

## Usage

```bash
# Convert any color format
python3 color_convert.py convert "#ff6600"
python3 color_convert.py convert "rgb(255, 102, 0)"
python3 color_convert.py convert "hsl(24, 100%, 50%)"

# Generate color palette
python3 color_convert.py palette "#ff6600" --type complementary
python3 color_convert.py palette "#ff6600" --type triadic

# Blend between colors
python3 color_convert.py blend "#ff0000" "#0000ff" --steps 7
```

## Supported Formats
- HEX (`#ff6600`, `ff6600`, `#f60`)
- RGB (`rgb(255, 102, 0)`)
- HSL (`hsl(24, 100%, 50%)`)
- HSV (`hsv(24, 100%, 100%)`)
- CMYK (output only)

## Zero dependencies. Single file. Python 3.8+.
