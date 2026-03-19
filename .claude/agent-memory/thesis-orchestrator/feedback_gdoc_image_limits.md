---
name: Google Docs image size limits
description: Google Docs API rejects images that are extremely tall (e.g., 1920x13535 px) even if file size is small (2.7MB). Must keep images within reasonable pixel dimensions.
type: feedback
---

Google Docs API insertInlineImage rejects PNGs that are extremely tall in pixel dimensions, even when the file size is under 3MB. The hyperparameter summary table (Table 3.3) at 1920x13535 pixels was rejected. The objectSize parameter controls display size, not the source image dimensions -- the API still downloads and processes the full-resolution source image.

**Why:** Google Docs has an undocumented pixel dimension limit for inline images. Very tall images (aspect ratio > ~8:1) seem to trigger this.

**How to apply:** Before inserting images, verify source PNG dimensions. If height exceeds ~5000 pixels, split into multiple images or re-export at lower resolution. Tables rendered as very tall PNGs should be converted to native Google Docs tables instead.
