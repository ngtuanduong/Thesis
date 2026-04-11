---
name: thesis-visual-fixer
description: Fix thesis visual HTML files — QA with Chrome DevTools, fix overlaps/sizing, crop PNG, export, upload to catbox, update VISUAL-GUIDE.md. Use when user says "fix visual", "fix the diagram", "visual has overlap", "text is too small", "crop the visual", "re-export visual", or references fixing any HTML file in documents/thesis-chapters/visuals/html/.
---

# Thesis Visual Fixer

Fix, QA, crop, and re-export thesis visual HTML files following a strict 6-phase sequential workflow.

## When to Use

- "Fix the visual for thesis chapters in `documents/thesis-chapters`"
- "The knowledge graph diagram has overlapping text"
- "Re-export all chapter 2 visuals"
- "This table visual is too small to read"
- "Crop and re-upload the ERD"
- Any issue with HTML files in `documents/thesis-chapters/visuals/html/`

## Project Paths

```
BASE: /Users/avada/WebstormProjects/Thesis
HTML: documents/thesis-chapters/visuals/html/{name}.html
PNG:  documents/thesis-chapters/visuals/png/{name}.png     ← MANDATORY save location
GUIDE: documents/thesis-chapters/visuals/VISUAL-GUIDE.md
CROP SCRIPT: .claude/skills/thesis-visual-fixer/scripts/crop_png.py
```

## UNIVERSAL RULES (non-negotiable)

1. **ALL phases are STRICTLY SEQUENTIAL.** Phase N+1 CANNOT start until Phase N's gate passes.
2. **NO `/tmp` storage.** All files saved to `documents/thesis-chapters/visuals/png/`.
3. **NO in-memory shortcuts.** Read files from disk. Verify files exist with `ls -la`.
4. **NO parallel Chrome DevTools.** ONE page open at a time. Close before opening next.
5. **SHOW YOUR WORK.** Report every phase gate with file path, size, and status.
6. **VERIFY BEFORE PROCEEDING.** If a file doesn't exist after writing, the phase FAILED.

---

## The 6-Phase Workflow

### Phase 1: Read & Understand the HTML

1. Read the HTML file from `documents/thesis-chapters/visuals/html/{name}.html`
2. Understand the visual's purpose (table, diagram, flowchart, timeline, etc.)
3. Identify the user's reported issue (overlap, sizing, white space, wrong content, etc.)
4. Verify with `ls -la` that the file exists

**GATE:** "✅ Phase 1 complete. HTML file: {path}, size: {bytes}. Issue: {description}."
**HARD BLOCK: Do NOT start Phase 2 until this gate passes.**

### Phase 2: Open & Inspect in Browser

5. Use `mcp__chrome-devtools__navigate_page` to open `file:///Users/avada/WebstormProjects/Thesis/documents/thesis-chapters/visuals/html/{name}.html`
6. Use `mcp__chrome-devtools__resize_page` to set the viewport:
   - Tables: 700-900px wide
   - Diagrams/flowcharts: 900-1000px wide
   - Architecture diagrams: 1100-1240px wide
   - Default: 900px wide, 900px tall
7. Use `mcp__chrome-devtools__take_screenshot` to capture the current render
8. **Visually inspect** the screenshot using the Read tool — check every item on the Overlap Detection Checklist

**GATE:** "✅ Phase 2 complete. Screenshot captured and inspected. Issues found: {list} OR No issues found."
**HARD BLOCK: Do NOT start Phase 3 until this gate passes.**

### Phase 3: Fix Issues (iterative loop)

9. If ANY issue is found:
   a. Edit the HTML file to fix the issue (increase spacing, font size, container width, etc.)
   b. Reload the page with `mcp__chrome-devtools__navigate_page` (same URL)
   c. Take a new screenshot with `mcp__chrome-devtools__take_screenshot`
   d. Re-inspect — go back to step 9 if issues remain
10. **Do NOT stop until:** zero overlaps, all text readable, layout professional
11. Maximum 5 iterations — if unfixable in 5 rounds, simplify the layout

**GATE:** "✅ Phase 3 complete. QA passed after {N} iterations. All issues resolved."
**HARD BLOCK: Do NOT start Phase 4 until this gate passes.**

### Phase 4: Screenshot, Crop, & Save PNG

12. Take the final full-page screenshot
13. Save raw screenshot to `documents/thesis-chapters/visuals/png/{name}-raw.png`
14. **MANDATORY: Crop with the bundled script:**
    ```bash
    python3 /Users/avada/WebstormProjects/Thesis/.claude/skills/thesis-visual-fixer/scripts/crop_png.py \
      /Users/avada/WebstormProjects/Thesis/documents/thesis-chapters/visuals/png/{name}-raw.png \
      /Users/avada/WebstormProjects/Thesis/documents/thesis-chapters/visuals/png/{name}.png
    ```
15. Delete the raw file: `rm .../png/{name}-raw.png`
16. Verify cropped PNG exists: `ls -la .../png/{name}.png`
17. Read the cropped PNG to visually confirm: correct content AND tightly cropped (no white borders)

**GATE:** "✅ Phase 4 complete. PNG saved (cropped): {path}, dimensions: {W}x{H}, size: {bytes}"
**HARD BLOCK: Do NOT start Phase 5 until this gate passes. If PNG missing or has white space → FAILED.**

### Phase 5: Upload to catbox.moe

18. Upload the cropped PNG from the project directory:
    ```bash
    curl -F "reqtype=fileupload" -F "fileToUpload=@/Users/avada/WebstormProjects/Thesis/documents/thesis-chapters/visuals/png/{name}.png" https://catbox.moe/user/api.php
    ```
19. Verify the returned URL starts with `https://files.catbox.moe/`

**GATE:** "✅ Phase 5 complete. Uploaded: {local_path} → {catbox_url}"
**HARD BLOCK: Do NOT start Phase 6 until this gate passes.**

### Phase 6: Update VISUAL-GUIDE.md

20. Read `documents/thesis-chapters/visuals/VISUAL-GUIDE.md`
21. Find the entry for this visual and update:
    - `**PNG Export:**` → `png/{name}.png`
    - `**Catbox URL:**` → the new catbox URL
22. Verify by reading VISUAL-GUIDE.md and confirming the new URL appears

**GATE:** "✅ Phase 6 complete. VISUAL-GUIDE.md updated for {name}."

### Final Summary

```
📋 VISUAL FIXED: {name}
   HTML:   documents/thesis-chapters/visuals/html/{name}.html
   PNG:    documents/thesis-chapters/visuals/png/{name}.png
   URL:    https://files.catbox.moe/{id}.png
   Size:   {W}x{H}px, {bytes} bytes
   QA:     Passed (iteration {N})
   Fix:    {what was fixed}
```

---

## Overlap Detection Checklist (Phase 2 & 3)

When inspecting screenshots, check ALL of these:
- [ ] **SVG text elements**: Do any `<text>` elements sit on top of each other?
- [ ] **Table cells**: Are any cells too narrow, causing text to wrap and overlap?
- [ ] **Diagram boxes**: Do any boxes/rectangles overlap or touch without spacing?
- [ ] **Labels & arrows**: Do labels overlap arrows or nearby elements?
- [ ] **Legend/caption**: Does legend or caption overlap the main figure?
- [ ] **Viewport fit**: Does the visual fit within viewport (max ~1240px wide)?
- [ ] **Font readability**: Can all text be read without zooming?

## Font Size Guidelines

| Element | Minimum | Recommended |
|---------|---------|-------------|
| Main title | 18px | 20-24px |
| Section headers | 16px | 18px |
| Body/cell content | 14px | 15-16px |
| Labels (axis, legend) | 12px | 13-14px |
| Notes/footnotes | 11px | 12px |
| SVG text in diagrams | 13px | 14-16px |

## Design Conventions

- **Colors:** Blue (#1565c0) BKT/L1, Pink (#880e4f) Elo/L2, Orange (#e65100) MAB/L3, Purple (#6a1b9a) FSRS/L4, Green (#2e7d32) KG/LLM
- **Typography:** Times New Roman for body, Courier New for code
- **Tables:** APA 7th edition (horizontal rules only, title above, notes below)
- **Figures:** Captions below (Figure N. Description.)
- **Accessibility:** Use both color AND labels — must be readable in grayscale

## Common Fixes Reference

| Issue | Fix |
|-------|-----|
| Text overlap in SVG | Increase `y` spacing between elements by 20-30px |
| Table cells too narrow | Increase container width or reduce font size |
| Content cut off | Increase SVG viewBox width/height |
| Text too small | Increase font-size to meet minimums above |
| White space in PNG | Re-run crop script — check HTML for excessive margins |
| Boxes overlapping | Add margin/padding between container elements |
| Arrow labels overlap | Offset label position or reduce label text |

## Batch Mode

When fixing multiple visuals, process them ONE AT A TIME:
1. Complete all 6 phases for visual A
2. Close the Chrome page
3. Then start Phase 1 for visual B
4. NEVER have two Chrome pages open simultaneously
