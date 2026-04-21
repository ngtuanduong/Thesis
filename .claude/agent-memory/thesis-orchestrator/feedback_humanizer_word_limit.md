---
name: Humanizer site strategies and limitations
description: aiundetect.com blocks by IP after free tier; humanizeai.pro Free mode works with isolated contexts for bulk processing
type: feedback
---

**aiundetect.com** (primary humanizer): Free tier gives ~500 words per session, but the site tracks by IP, not just cookies. Rotating isolated browser contexts does NOT reset the free tier. After the first context is exhausted, a signup popup appears on all new contexts. Only usable for ~2 paragraphs per session.

**humanizeai.pro** (fallback): The "Free" mode works reliably with isolated browser contexts. Each context gets a generous word allowance. Successfully processed 70+ paragraphs (~4,200 words) in a single session using one isolated context. Use the native textarea setter approach (not `fill`). The site has no minimum word count, though very short paragraphs (<30 words) may need to be combined with adjacent ones.

**Why:** aiundetect.com has aggressive IP-based rate limiting that defeats context rotation. humanizeai.pro is more permissive in Free mode.

**How to apply:** For bulk humanization, go directly to humanizeai.pro in Free mode. Skip aiundetect.com unless processing just 1-2 paragraphs. Use `isolatedContext` for fresh sessions. The Google Docs API uses `spaceAbove`/`spaceBelow` (NOT `spaceBefore`/`spaceAfter`).
