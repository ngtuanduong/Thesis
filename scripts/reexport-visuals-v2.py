"""
Re-export thesis visuals from HTML at 2x DPI, cropped to content only.
Uses Playwright to screenshot the #tight-container element (or body if no container).
"""
import asyncio
import importlib.util
import io
import os
import sys

from playwright.async_api import async_playwright
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML_DIR = "C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/visuals/html"
PNG_DIR = "C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/visuals/png"


async def export_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Use 2x device scale for high DPI
        context = await browser.new_context(
            viewport={"width": 1400, "height": 900},
            device_scale_factor=2,
        )
        page = await context.new_page()

        html_files = sorted(f for f in os.listdir(HTML_DIR) if f.endswith(".html"))
        results = []

        for fname in html_files:
            html_path = os.path.join(HTML_DIR, fname)
            png_name = fname.replace(".html", ".png")
            png_path = os.path.join(PNG_DIR, png_name)

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


print("=== Re-exporting all visuals (2x DPI, content-cropped) ===")
visuals = asyncio.run(export_all())
print(f"\nExported {len(visuals)} visuals")

# Report resolution improvement
for v in visuals:
    status = "OK" if v["w"] >= 1200 else "STILL_LOW"
    print(f"  {v['png']:50s} {v['w']:5d}x{v['h']:5d}px  {status}")
