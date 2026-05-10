# Visual Style Guide — Final Thesis

**Source of truth.** Every chart, figure, diagram, table, or screenshot in
`documents/fixed-final-thesis-paper/` follows the rules below. Apply this guide
when authoring new visuals, fixing existing ones, or reviewing pull requests
that touch images.

If a visual was authored before 2026-05-10 and uses saturated colors, it is
**out of date**. Run it through `scripts/visual-grayscale-convert.py` and
re-export.

---

## 1. Why grayscale

The user's instruction (2026-05-10) is to drop vibrant colors and use grayscale
(white / black / gray) across all charts and tables, **without losing meaning**.

Reasons this matters for an undergraduate thesis:

- **Print fidelity.** The defense committee may print the thesis. Colors that
  pop on screen muddy in greyscale print. Designing for gray means the printed
  copy is identical to the screen copy.
- **Calm professionalism.** A 70-page thesis with rainbow accents reads as a
  conference poster, not as an engineering report. Gray reads as engineering.
- **Forces meaningful distinctions.** When you cannot use color, you have to
  earn distinctions through layout, spacing, typography, and pattern. The
  result is usually clearer, not less clear.

This guide is consistent with the existing colorblind note in the
`documents/thesis-chapters/visuals/VISUAL-GUIDE.md` (line 362–364) which
already states: *"All visuals use both color and labeling so they remain
interpretable in grayscale."* This guide makes the grayscale path the only
path.

---

## 2. Palette (concrete hex codes)

Use only these values:

### 2.1 Light fills (backgrounds, container surfaces)

| Hex | Use |
|---|---|
| `#fff` | Page / canvas background |
| `#f5f5f5` | Default light-gray fill (e.g., contribution boxes, cells) |
| `#ebebeb` | Slightly emphasised fill (e.g., highlighted row in a table) |
| `#e0e0e0` | Strongest light fill (e.g., a "this thesis" callout box) |

### 2.2 Dark accents (borders, accent text, glyphs)

| Hex | Use |
|---|---|
| `#000` | Primary text, axis lines |
| `#222` | Strongest border / emphasis text (e.g., "This thesis" outline) |
| `#444` | Secondary text |
| `#555` | Default border / connector / glyph |
| `#888` | De-emphasised border / supporting label |
| `#bbb` | Gridlines, very faint dividers |

That is **10 grays**, plus white. No other colors.

### 2.3 Forbidden colors

The previous palette is now banned. The bulk grayscale converter searches for
these and rewrites them:

| Old hex | Old role |
|---|---|
| `#1565c0`, `#1a56db`, `#4285f4`, `#283593`, `#0d47a1` | Blue (BKT / Layer 1 / Ch1) |
| `#880e4f`, `#c2185b` | Pink (Elo / Layer 2 / Ch2) |
| `#e65100`, `#ea4335`, `#c5221f` | Orange / red (MAB / Layer 3 / Ch3) |
| `#6a1b9a`, `#7b1fa2` | Purple (FSRS / Layer 4 / Ch4) |
| `#2e7d32`, `#1b5e20` | Green (KG / highlights / Ch5) |
| `#00695c`, `#004d40` | Teal (data structures topic group) |
| `#e3f2fd`, `#fce4ec`, `#e8eaf6`, `#fff3e0`, `#f3e5f5`, `#e8f5e9`, `#e0f2f1` | Light tints of the above |

If you spot a new color creeping in (e.g., a rainbow chart palette from a
library default), add it to the converter map.

---

## 3. Distinguishability without color

When a visual must show multiple categories (e.g., five layers of the adaptive
engine, three contribution buckets), color is the easy way out and now banned.
Use these instead, in order of preference:

### 3.1 Stroke pattern (preferred for lines and borders)

```
solid               solid              <-- stroke-dasharray="0" (default)
dashed -- -- --     dashed             <-- stroke-dasharray="4 2"
dotted . . . .      dotted             <-- stroke-dasharray="1 2"
long-dashed --- --- long-dashed         <-- stroke-dasharray="6 3"
dash-dot -.-.-      dash-dot           <-- stroke-dasharray="4 2 1 2"
```

Pick the simplest that still distinguishes. For 2 categories: solid + dashed.
For 3: solid + dashed + dotted. For 4: add long-dashed. Avoid ≥ 5 patterns —
that's a sign the visual is doing too much.

### 3.2 Stroke weight

`1px` (gridline / supporting), `1.5px` (default), `2px` (emphasis), `3px`
(callout). Do not use weights > 3px; it looks shouty.

### 3.3 Fill pattern (for areas)

When you need to distinguish filled regions:
- Plain fill with `#f5f5f5`, `#ebebeb`, `#e0e0e0` (3 levels)
- Hatched fill (SVG `<pattern>` with diagonal lines) for the second category
- Cross-hatched for the third
- Avoid fill patterns for small shapes; they go noisy below ~20×20 px.

### 3.4 Typography weight

Bold headers, regular body, italic captions. Don't use bold for emphasis
within body text — use a bold lead word at most.

### 3.5 Shape

When categories are still hard to distinguish, change the shape itself:
rectangles for "components", rounded rectangles for "states", parallelograms
for "data flow", diamonds for "decisions". This is standard flowchart
practice.

---

## 4. Required SVG idioms

### 4.1 Text halo (readability over lines) — REVISED 2026-05-10

The earlier halo CSS turned **on by default** and exempted only bold text.
That broke text inside dark-fill blocks: a `fill="#f5f5f5"` body line on a
`#222` rectangle picked up the white halo, and the resulting glyph rendered
as "gray text with a white border" — exactly the artifact the 2026-05-10
review surfaced. The new rule inverts the polarity: halo is **opt-in via
class**, off by default.

```css
/* Default: no halo. Text on light background reads fine without one. */
svg text { paint-order: stroke fill; stroke-width: 0; }

/* Opt-in: white halo for text that overlaps lines on a light background. */
svg text.halo {
  stroke: #fff;
  stroke-width: 3px;
  stroke-linejoin: round;
}

/* Opt-in: dark halo for text that overlaps lines on a dark background. */
svg text.halo-dark {
  stroke: #222;
  stroke-width: 3px;
  stroke-linejoin: round;
}
```

**Forbidden combinations (do not regress):**

- `fill="#f5f5f5"` (or any near-white) text + `stroke="white"` halo on a
  `#222` block. Light-on-light halo over dark fill reads as gray.
- `class="halo"` on text that doesn't actually cross a line. The halo adds
  visual weight; use it only when needed.

**Backward-compatible variant (transitional, for files still using the old
"halo on by default" template):** keep the override clause, but expand it
to cover light fills as well:

```css
svg .state-label, svg rect + text, svg [font-weight="bold"],
svg text[fill="#fff"], svg text[fill="#FFF"], svg text[fill="white"],
svg text[fill="#f5f5f5"], svg text[fill="#F5F5F5"],
svg text[fill="#ebebeb"], svg text[fill="#e0e0e0"] {
  stroke-width: 0;
}
```

This is the patched form applied to legacy HTMLs in the 2026-05-10 fix
pass. New visuals should use the opt-in template above.

### 4.1.1 Decoration boundary rule (added 2026-05-10)

Lines, edges, and arrows — solid or dashed — **must not cross any content
block's bounding box** other than at their endpoints. The endpoint should
land **on the block boundary**, not several pixels inside it.

Allowed exceptions:

1. **Sequence-diagram lifelines.** A vertical dashed lifeline crossing the
   actor's box is the standard UML idiom. Keep it.
2. **Layer-grouping outline rectangles.** A dashed `<rect>` that *outlines*
   a region (e.g., the four-layer adaptive engine band) is valid; it
   doesn't *cross* internal blocks, it surrounds them.

When a direct path between two blocks would cross a third block, route the
line via SVG path with corner waypoints:

```svg
<path d="M x1 y1 L x1 ymid L x2 ymid L x2 y2"
      fill="none" stroke="#555" stroke-width="1.2"/>
```

If a relationship diagram has more than three or four crossings even after
routing (e.g., an entity-relationship diagram with thirteen tables),
prefer **removing the lines entirely** and conveying the relationship via
column naming (`student_id` references `users.id`, etc.). This is the
approach taken in Figure 3.5 after the 2026-05-10 review.

### 4.1.1.5 No embedded "Figure N.M" / "Table N.M" caption inside the image (added 2026-05-10)

The PNG must contain ONLY the diagram or table itself — no embedded "Figure 4.2. ..." or "Table 3.1. ..." caption text. The formal caption is added in the chapter markdown directly below the image:

```markdown
![](images/figure-4-2-bkt-state-transition.png)

*Figure 4.2. BKT as a two-state Hidden Markov Model. ...*
```

**Why:** Embedding the formal caption inside the image creates two sources of truth. Renumbering a table or figure (e.g., closing a 2.1 gap) would otherwise require re-rendering every affected image. With the caption owned by the markdown, renaming is a one-line edit.

**Allowed inside the image:** content/diagram self-titles that describe the depicted system (e.g., "BKT Hidden Markov Model — State Transitions", "Knowledge Graph: Programming Concept Prerequisites"). These are part of the diagram, not the formal numbered caption.

**Forbidden inside the image:** any string starting with `Figure N.M.` or `Table N.M.`, or `<div class="table-title">`/`<div class="caption">` containing such labels. The 2026-05-10 sweep removed these from all 33 visual HTML sources.

### 4.1.2 Data-backed figure rule (added 2026-05-10)

Any figure that depicts system data — database schemas, knowledge graphs,
API flows, seed datasets — **must cite its source file in an HTML comment
at the top of the document**:

```html
<!-- Source: server/prisma/seed-adaptive.ts (verified 2026-05-10) -->
```

When the source data changes (a new concept is added, a column is
renamed), update the figure in the same pull request. Reviewers should
flag any data figure whose comment date is older than the latest change to
its source file.

Simplified figures that intentionally show a subset of the data **must
disclose the count**: e.g., "Showing 10 of 34 concepts; full graph (34
nodes, 52 prerequisite edges) in Appendix B." Never claim the figure is
complete when it is not.

### 4.2 Default font

Times New Roman across all SVG text. Matches the thesis body font.

```css
svg text { font-family: 'Times New Roman', Times, serif; }
```

### 4.3 Tight container

Wrap the SVG in `<div id="tight-container">` with explicit width and zero
margin. The export script (`scripts/reexport-visuals-v2.py`) crops to this
container, eliminating whitespace.

```html
<div id="tight-container" style="display:inline-block; width:680px; padding:5px;">
  <div class="figure-container"><svg ...>...</svg></div>
  <div class="caption"><strong>Figure X.Y.</strong> Caption text.</div>
</div>
```

---

## 5. Tables

Tables follow the same gray palette. Specifics:

- **Header row:** `#ebebeb` background, `#000` text, bold.
- **Body rows:** `#fff` background, `#000` text.
- **Highlighted row** (e.g., "this thesis"): `#e0e0e0` background, `#222`
  border (1.5px), no row padding change.
- **Borders:** `#bbb` for cell borders, 1px. Keep grid light.
- **No vertical color bars** marking categories. Use the leftmost column for
  category labels instead.

---

## 6. Don'ts

- **No saturated hues** (any color whose RGB channels differ by ≥ 80).
- **No rainbow gradients** for ordered data; use a single-hue gray ramp
  (`#f5f5f5` → `#222`).
- **No per-layer color coding.** Layers are distinguished by labels and
  position, not color.
- **No "color = positive / red = negative" semantics**; use plain text labels
  ("up 12%" vs "down 8%") with optional ▲ / ▼ glyphs.
- **No drop shadows or soft glows.** Flat geometry only.
- **No emoji / icon fonts** in the visuals. Plain shapes.

---

## 7. Print contrast

Every text element over a fill must have ≥ 4.5:1 contrast for body text and ≥
3:1 for large text (≥ 14pt bold). Quick check:

| Text | Fill | Contrast | Pass? |
|---|---|---:|---|
| `#000` | `#fff` | 21.0 | ✓ |
| `#000` | `#f5f5f5` | 19.6 | ✓ |
| `#222` | `#ebebeb` | 12.7 | ✓ |
| `#444` | `#e0e0e0` | 7.7 | ✓ |
| `#555` | `#fff` | 7.5 | ✓ |
| `#888` | `#fff` | 3.5 | ✗ for body, ✓ for large bold |
| `#888` | `#f5f5f5` | 3.3 | ✗ |

Don't pair `#888` text with any non-white fill.

---

## 8. Examples (before / after)

### 8.1 Chapter / contribution box (from Figure 1.3)

**Before:**
```svg
<rect x="18" y="62" width="100" height="82" rx="6"
      fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
<text font-size="14" font-weight="bold" fill="#1565c0" ...>Chapter 1</text>
```

**After:**
```svg
<rect x="18" y="62" width="100" height="82" rx="6"
      fill="#f5f5f5" stroke="#222" stroke-width="2"/>
<text font-size="14" font-weight="bold" fill="#000" ...>Chapter 1</text>
```

### 8.2 Multi-category line chart (e.g., FSRS retrievability curves)

**Before:** 3 lines colored blue, orange, green — same weight, same dash.
**After:** 3 lines all `#222`, but:
- Curve A: solid, 2px
- Curve B: dashed (`stroke-dasharray="4 2"`), 1.5px
- Curve C: dotted (`stroke-dasharray="1 2"`), 1.5px
- Direct labels at the right end of each curve (no separate legend if avoidable)

### 8.3 Knowledge-graph topic groups (from ch3-knowledge-graph-diagram)

**Before:** 6 topic groups with 6 saturated hues.
**After:** 6 groups all `#f5f5f5` fill / `#555` border, but:
- Spatial grouping (cluster on the canvas) does the visual work.
- Each cluster has a single bold heading (`#000`, 14pt) above it.
- Optional: a thin labelled boundary curve around each cluster (`#bbb`, 1px,
  dashed) — only if clusters overlap visually.

---

## 9. How to apply this guide

### 9.1 To existing HTMLs

Run the bulk converter:

```bash
python scripts/visual-grayscale-convert.py --dry-run     # preview
python scripts/visual-grayscale-convert.py               # write
python scripts/visual-grayscale-convert.py --only ch1-thesis-structure-roadmap.html  # one file
```

Originals are backed up to `documents/thesis-chapters/visuals/html.backup-pre-grayscale/`.

### 9.2 To new HTMLs

Start from the template in §4.3. Use only palette values from §2.1 and §2.2.
Use distinguishability tools from §3 when you have multiple categories. Run
the export:

```bash
python scripts/reexport-visuals-v2.py \
    --output-dir documents/fixed-final-thesis-paper/images/
```

### 9.3 To existing PNGs (when HTML source is missing)

Re-render in the `thesis-visual-fixer` skill, applying this guide. If a PNG
has no HTML source (e.g., a screenshot), keep as-is but check that the
palette doesn't fight the gray standard (e.g., a UI screenshot with one
brand color is fine; a chart screenshot is not).

---

## 10. Maintenance

This guide is updated whenever the palette or rules change. The grayscale
converter (`scripts/visual-grayscale-convert.py`) reads its color map from
this file's §2.3 — keep the table format stable.

Last updated: 2026-05-10 (initial version + halo/boundary/data-source revisions).
