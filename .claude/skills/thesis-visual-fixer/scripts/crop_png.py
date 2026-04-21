#!/usr/bin/env python3
"""
Crop a PNG image by trimming white space with 4px padding.
Usage: python3 crop_png.py <input.png> [output.png]
If output is omitted, overwrites the input file.
"""
import sys
from PIL import Image, ImageChops

def crop_whitespace(input_path, output_path=None, padding=4):
    if output_path is None:
        output_path = input_path

    img = Image.open(input_path)
    old_w, old_h = img.size

    # Create white background matching image mode
    if img.mode == 'RGBA':
        bg_color = (255, 255, 255, 255)
    else:
        bg_color = (255, 255, 255)

    bg = Image.new(img.mode, img.size, bg_color)
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()

    if not bbox:
        print(f"WARNING: {input_path} appears to be entirely white — no content found")
        sys.exit(1)

    # Apply padding
    x1 = max(0, bbox[0] - padding)
    y1 = max(0, bbox[1] - padding)
    x2 = min(img.width, bbox[2] + padding)
    y2 = min(img.height, bbox[3] + padding)

    cropped = img.crop((x1, y1, x2, y2))
    cropped.save(output_path)

    new_w, new_h = cropped.size
    saved_pct = round((1 - (new_w * new_h) / (old_w * old_h)) * 100)
    print(f"CROPPED: {old_w}x{old_h} -> {new_w}x{new_h} ({saved_pct}% smaller)")
    print(f"OUTPUT: {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 crop_png.py <input.png> [output.png]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    crop_whitespace(input_file, output_file)
