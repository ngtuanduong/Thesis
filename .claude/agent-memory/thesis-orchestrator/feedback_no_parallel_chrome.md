---
name: No parallel Chrome DevTools
description: Never run multiple Chrome DevTools agents in parallel -- causes wrong-page screenshots due to tab/page conflicts
type: feedback
---

Never run two Chrome DevTools agents simultaneously. When two agents open/navigate pages in parallel, `take_screenshot` can capture the wrong tab, resulting in incorrect visuals being saved and uploaded.

**Why:** All Ch1-Ch3 visuals were captured incorrectly in the initial run because two agents used Chrome DevTools concurrently. Every visual had to be redone.

**How to apply:** When capturing HTML-to-PNG screenshots, process files strictly one at a time: navigate, wait, screenshot, close page, then move to the next file. No parallelism at any stage of the capture pipeline.
