---
name: chapter1-published-to-gdoc
description: Chapter 1 was published to Google Doc 1Q1mihSftbOtxuPTitDmcdjE7Av-EHxyjgZAfqw3Gfok with humanized text and images
type: project
---

Chapter 1 (Introduction) was re-published on 2026-03-18 to Google Doc ID `1Q1mihSftbOtxuPTitDmcdjE7Av-EHxyjgZAfqw3Gfok` with full workflow including text humanization.

**Why:** User requested full publishing workflow with Phase 2 text humanization via QuillBot AI Humanizer.

**How to apply:** The publishing script at `scripts/publish_chapter1.py` now contains a `HUMANIZED_PARAGRAPHS` dictionary mapping original paragraph starts to humanized replacements. 21 out of 77 paragraphs were humanized. The script handles: markdown parsing, humanization lookup, visual insertion (5 images from catbox.moe), and Google Docs API formatting. QuillBot free tier limits to 125 words per request and blocks after ~3 uses without sign-up, so humanized text was pre-computed and embedded in the script.
