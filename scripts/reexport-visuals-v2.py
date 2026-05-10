"""
Re-export thesis visuals from HTML at 2x DPI, cropped to content only.
Uses Playwright to screenshot the #tight-container element (or body if no container).

Usage:
    python scripts/reexport-visuals-v2.py
    python scripts/reexport-visuals-v2.py --output-dir documents/fixed-final-thesis-paper/images
    python scripts/reexport-visuals-v2.py --only ch1-thesis-structure-roadmap.html
"""
import argparse
import asyncio
import importlib.util
import io
import os
import sys

from playwright.async_api import async_playwright
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML_DIR = "C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/visuals/html"
DEFAULT_PNG_DIR = "C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/visuals/png"


async def export_all(output_dir, only_filename=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Use 2x device scale for high DPI
        context = await browser.new_context(
            viewport={"width": 1400, "height": 900},
            device_scale_factor=2,
        )
        page = await context.new_page()

        os.makedirs(output_dir, exist_ok=True)
        all_html_files = sorted(f for f in os.listdir(HTML_DIR) if f.endswith(".html"))
        if only_filename:
            html_files = [f for f in all_html_files if f == only_filename]
            if not html_files:
                print(f"ERROR: --only file '{only_filename}' not found in {HTML_DIR}", file=sys.stderr)
                await browser.close()
                return []
        else:
            html_files = all_html_files
        results = []

        for fname in html_files:
            html_path = os.path.join(HTML_DIR, fname)
            png_name = fname.replace(".html", ".png")
            png_path = os.path.join(output_dir, png_name)

            url = f"file:///{html_path.replace(os.sep, '/')}"
            try:
                await page.goto(url, wait_until="networkidle", timeout=10000)
                await page.wait_for_timeout(300)

                # Try to find #tight-container, fall back to body > first child, then body
                element = None
                for selector in ["#tight-container", ".figure-container", "body > div", "body > table", "body"]:
                    el = page.locator(selector).first
                    if await el.count() > 0:
                        element = el
                        break

                if element:
                    # Get bounding box to verify it has actual content
                    box = await element.bounding_box()
                    if box and box["width"] > 50 and box["height"] > 50:
                        await element.screenshot(path=png_path, type="png")
                    else:
                        # Fallback: full page
                        await page.screenshot(path=png_path, full_page=True, type="png")
                else:
                    await page.screenshot(path=png_path, full_page=True, type="png")

                # Auto-crop whitespace from the PNG
                img = Image.open(png_path)
                # Convert to RGB if needed
                if img.mode == "RGBA":
                    # Create white background
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[3])
                    img = bg
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                # Find content bounding box (non-white pixels)
                bbox = img.getbbox()
                if bbox:
                    # Add small padding (10px)
                    x1, y1, x2, y2 = bbox
                    pad = 10
                    x1 = max(0, x1 - pad)
                    y1 = max(0, y1 - pad)
                    x2 = min(img.width, x2 + pad)
                    y2 = min(img.height, y2 + pad)
                    cropped = img.crop((x1, y1, x2, y2))
                    cropped.save(png_path)
                    w, h = cropped.size
                else:
                    w, h = img.size

                print(f"  {fname:55s} -> {w}x{h}px")
                results.append({"html": fname, "png": png_name, "png_path": png_path, "w": w, "h": h})

            except Exception as e:
                print(f"  {fname:55s} -> ERROR: {e}")

        await browser.close()
        return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_PNG_DIR,
        help=f"Where to save exported PNGs (default: {DEFAULT_PNG_DIR})",
    )
    parser.add_argument(
        "--only",
        default=None,
        metavar="FILENAME",
        help="Export only this single HTML (e.g., ch1-thesis-structure-roadmap.html)",
    )
    args = parser.parse_args()

    target = "single file" if args.only else "all visuals"
    print(f"=== Re-exporting {target} (2x DPI, content-cropped) -> {args.output_dir} ===")
    visuals = asyncio.run(export_all(args.output_dir, args.only))
    print(f"\nExported {len(visuals)} visual(s)")

    for v in visuals:
        status = "OK" if v["w"] >= 1200 else "STILL_LOW"
        print(f"  {v['png']:55s} {v['w']:5d}x{v['h']:5d}px  {status}")


if __name__ == "__main__":
    main()
