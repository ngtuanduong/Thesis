# Visual Re-capture Plan

## Problem
Visuals in the Google Doc (1cJlWFX9QCEsqYo7mp6cpCWAba3Xc433-IRu8nlR63o0) were captured incorrectly because two Chrome DevTools agents ran in parallel, causing wrong-page screenshots.

## Root Cause
Parallel Chrome DevTools usage -- when two agents open/navigate pages simultaneously, `take_screenshot` can capture the wrong tab/page.

## Solution: Sequential Single-Agent Capture Pipeline

All 20 HTML visuals must be re-captured ONE AT A TIME using a single Chrome DevTools session. No parallelism at any point in the capture phase.

---

## Capture Method Per File

Each HTML file follows this exact sequence:

1. **Navigate** to `file:///Users/avada/WebstormProjects/Thesis/documents/thesis-chapters/visuals/html/{filename}.html`
2. **Wait** for full render (wait_for selector on the main content element)
3. **Resize** the page to match the content width:
   - Ch1 files (with `#tight-container`): width 700px (680px container + margins)
   - Ch2/Ch3 files: match their `max-width` CSS (900px or 1200px) + padding
4. **Evaluate script** to get the exact bounding box of the content (document.body scrollHeight)
5. **Take screenshot** -- full page capture
6. **Crop** using ImageMagick `convert` to trim whitespace: `convert input.png -trim +repage -border 2x2 -bordercolor white output.png`
7. **Verify dimensions** -- check resulting PNG is not taller than 5000px (Google Docs limit). If it is, flag for splitting or native table conversion.
8. **Upload to catbox** via curl: `curl -F "reqtype=fileupload" -F "fileToUpload=@output.png" https://catbox.moe/user/api.php`
9. **Record** the catbox URL and dimensions
10. **Close the page** before proceeding to the next file

---

## Chapter 1 Visuals (5 files)

All Ch1 files use `#tight-container` (680px width, inline-block). Resize page to 700px width.

| # | File | Figure/Table ID | Expected Content |
|---|------|----------------|------------------|
| 1 | ch1-platform-comparison-table.html | Table 1.1 | Comparison of Adaptive Capabilities Across Platforms |
| 2 | ch1-thesis-structure-roadmap.html | Figure 1.1 | Thesis Structure Roadmap |
| 3 | ch1-closed-loop-workflow.html | Figure 1.2 | Closed-Loop Adaptive Workflow |
| 4 | ch1-research-gap-diagram.html | Figure 1.3 | Research Gap Diagram |
| 5 | ch1-five-layer-architecture-overview.html | Figure 1.4 | Five-Layer Architecture Overview |

**Sequence**: 1 -> 2 -> 3 -> 4 -> 5 (strictly sequential)

---

## Chapter 2 Visuals (5 files)

Ch2 files use `max-width: 900px` with body margin/padding. Resize page to 940px width.

| # | File | Figure/Table ID | Expected Content |
|---|------|----------------|------------------|
| 6 | ch2-kt-evolution-timeline.html | Figure 2.2 | Evolution of Knowledge Tracing Methods |
| 7 | ch2-technique-complementarity-table.html | Table 2.1 | Technique Complementarity |
| 8 | ch2-detailed-comparison-table.html | Table 2.2 | Detailed Comparison |
| 9 | ch2-spaced-repetition-evolution.html | Figure 2.x | Spaced Repetition Evolution |
| 10 | ch2-literature-landscape-map.html | Figure 2.x | Literature Landscape Map |

**Sequence**: 6 -> 7 -> 8 -> 9 -> 10 (strictly sequential)

---

## Chapter 3 Visuals (10 files)

Ch3 files use varying `max-width` (900px-1200px). Check each file's CSS before setting page width.

| # | File | Figure/Table ID | Expected Content |
|---|------|----------------|------------------|
| 11 | ch3-system-architecture-diagram.html | Figure 3.1 | System Architecture (max-width: 1200px -> resize to 1240px) |
| 12 | ch3-layer-interaction-matrix.html | Table 3.1 | Layer Interaction Matrix |
| 13 | ch3-functional-requirements-table.html | Table 3.2 | Functional Requirements |
| 14 | ch3-hyperparameter-summary-table.html | Table 3.3 | Hyperparameter Summary (WARNING: likely very tall, may need split) |
| 15 | ch3-knowledge-graph-diagram.html | Figure 3.2 | Knowledge Graph Structure |
| 16 | ch3-cold-start-flowchart.html | Figure 3.3 | Cold Start Handling Flowchart |
| 17 | ch3-submission-processing-flow.html | Figure 3.4 | Submission Processing Flow |
| 18 | ch3-database-schema-erd.html | Figure 3.5 | Database Schema ERD |
| 19 | ch3-recommendation-sequence-diagram.html | Figure 3.7 | Recommendation Sequence Diagram |
| 20 | ch3-caching-strategy-table.html | Table 3.5 | Caching Strategy |

**Sequence**: 11 -> 12 -> 13 -> 14 -> 15 -> 16 -> 17 -> 18 -> 19 -> 20 (strictly sequential)

---

## Cropping Protocol

For every captured PNG:

```bash
# Step 1: Trim all surrounding whitespace
convert input.png -trim +repage output.png

# Step 2: Verify dimensions
identify output.png
# If height > 5000px, flag the file -- do NOT attempt Google Docs insertion
```

The `-trim` flag removes all uniform-color borders. The `+repage` resets the virtual canvas. No additional border is added (tight crop per user preference).

---

## Upload Protocol

Each cropped PNG is uploaded to catbox immediately after cropping:

```bash
curl -F "reqtype=fileupload" -F "fileToUpload=@/path/to/cropped.png" https://catbox.moe/user/api.php
```

The returned URL is recorded in a tracking table below.

---

## Google Doc Update Protocol

After ALL 20 visuals are captured, cropped, and uploaded, update the Google Doc using the `thesis-gdoc-publisher` agent:

1. For each visual, identify its current (incorrect) position in the Google Doc
2. Delete the old inline image at that position
3. Insert the new (correct) image from the catbox URL at the same position
4. Verify the image displays correctly

This must also be done sequentially -- one image replacement at a time to avoid index shifting issues in the Google Docs API.

---

## Tracking Table

Fill in as captures complete:

| # | File | Cropped Dims | Catbox URL | GDoc Updated | Status |
|---|------|-------------|------------|--------------|--------|
| 1 | ch1-platform-comparison-table | | | | PENDING |
| 2 | ch1-thesis-structure-roadmap | | | | PENDING |
| 3 | ch1-closed-loop-workflow | | | | PENDING |
| 4 | ch1-research-gap-diagram | | | | PENDING |
| 5 | ch1-five-layer-architecture-overview | | | | PENDING |
| 6 | ch2-kt-evolution-timeline | | | | PENDING |
| 7 | ch2-technique-complementarity-table | | | | PENDING |
| 8 | ch2-detailed-comparison-table | | | | PENDING |
| 9 | ch2-spaced-repetition-evolution | | | | PENDING |
| 10 | ch2-literature-landscape-map | | | | PENDING |
| 11 | ch3-system-architecture-diagram | | | | PENDING |
| 12 | ch3-layer-interaction-matrix | | | | PENDING |
| 13 | ch3-functional-requirements-table | | | | PENDING |
| 14 | ch3-hyperparameter-summary-table | | | | PENDING |
| 15 | ch3-knowledge-graph-diagram | | | | PENDING |
| 16 | ch3-cold-start-flowchart | | | | PENDING |
| 17 | ch3-submission-processing-flow | | | | PENDING |
| 18 | ch3-database-schema-erd | | | | PENDING |
| 19 | ch3-recommendation-sequence-diagram | | | | PENDING |
| 20 | ch3-caching-strategy-table | | | | PENDING |

---

## Special Handling: Oversized Images

The following files are at risk of exceeding the 5000px height limit:
- **ch3-hyperparameter-summary-table.html** -- Previously measured at 13535px tall. Options:
  1. Split into 2-3 separate PNGs and insert sequentially
  2. Convert to native Google Docs table (preferred if feasible)
  3. Re-export at reduced font size / condensed layout

Decision to be made after capture and measurement.

---

## Safety Rules

1. **ONE Chrome DevTools page open at a time** -- navigate, capture, close, then move to next
2. **NO parallel agent invocations** during the capture phase
3. **Verify each screenshot** by reading the PNG file to confirm it shows the correct content before uploading
4. **Record everything** in the tracking table above
5. **If a capture looks wrong**, re-do it immediately before moving on
