---
name: Crop visuals tightly for Google Docs
description: PNG exports must be tightly cropped — no white space margins — so text is readable when inserted at 468pt width
type: feedback
---

Always crop PNG exports tightly around the actual figure content — no surrounding white space/margins.

**Why:** When PNGs with large white margins are inserted into Google Docs at ~468pt width, the actual figure content gets shrunk down and text becomes unreadable. The white space wastes image area.

**How to apply:** When exporting HTML visuals to PNG:
1. Set body margin/padding to 0 in the HTML
2. Wrap content in a `display: inline-block` container with `width: fit-content`
3. Resize the browser viewport to match the container dimensions before screenshotting
4. Or use element-level screenshots targeting the content container
5. Result: PNG should contain only the figure content, no surrounding whitespace
