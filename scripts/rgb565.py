#!/usr/bin/env python3
import sys
from PIL import Image
import io

def rgb888_to_rgb565(r, g, b):
    """Convert 8-bit RGB to 16-bit RGB565."""
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

def main():
    # Read binary image data from stdin
    data = sys.stdin.buffer.read()

    # Load image into Pillow
    img = Image.open(io.BytesIO(data)).convert("RGB")
    width, height = img.size

    # Convert pixels
    out = bytearray()
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            rgb565 = rgb888_to_rgb565(r, g, b)
            # write little-endian (LVGL expects this for raw565)
            out.append(rgb565 & 0xFF)
            out.append((rgb565 >> 8) & 0xFF)

    # Output raw RGB565 bytes to stdout
    sys.stdout.buffer.write(out)

if __name__ == "__main__":
    main()
