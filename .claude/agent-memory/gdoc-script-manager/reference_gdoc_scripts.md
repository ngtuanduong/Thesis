---
name: gdoc-* script layout in this repo
description: Where maintained gdoc scripts live and naming convention used
type: reference
---

- Location: `scripts/` (Python, not TypeScript — the repo already has many publish/verify Python scripts using googleapiclient)
- Naming: `gdoc-<verb>-<target>.py` where verb is `read` / `find` / `write` / `util`
- Current scripts:
  - `scripts/gdoc-util-auth.py` - shared auth + doc iteration helpers
  - `scripts/gdoc-read-full.py` - dump whole doc as JSONL (one paragraph per line with startIndex, endIndex, style, text)
  - `scripts/gdoc-write-ch5-batch1.py` - one-shot Batch 1 Ch.5 revision (T1/T2/T4/T5). Idempotent via replaceAllText.
  - `scripts/gdoc-write-ch1-batch3.py` - Batch 3: rewrite §1.3/§1.4/§1.7 bodies (delete+insert+style).
  - `scripts/gdoc-write-ch1-batch4.py` - Batch 4: global marketing-phrase replacements + Ch.1/Ch.2 redundancy deletion. Skips References range (doc-index >= 209787 at time of writing); counts body hits before sending replaceAllText to avoid bibliography mutation.
  - `scripts/gdoc-write-conference-paper.py` - publishes `documents/conference-paper/paper-final.md` (tagged markdown: `<!-- TITLE_VI_BEGIN -->` etc.) to doc ID `1b21l8G9SX...` with HTKH GV-SV 2025 styling (Tahoma title, Times New Roman 13pt body, etc.) and catbox/Drive image replacement.
  - `scripts/gdoc-write-conference-paper-plain.py` - overwrites the same conference-paper doc (ID `1b21l8G9SX...`) from a plain `.txt` mirror with NO styling side-effects: clear body, insert one paragraph per non-empty line, verify first 200 chars and presence of `[1]` IEEE citation. Use when the source is plain text (e.g. `Bài báo tham dự hội thảo khoa học.txt`) rather than the tagged markdown assembly file.
  - `scripts/gdoc-apa-to-ieee.py` - in-place APA -> IEEE numeric for the conference-paper doc (`1b21l8G9SX...`). 17 ordered `replaceAllText` rules (combos before individual refs, narrative-style before parenthetical), NFD-fallback retry for 'Pelánek', then deleteContentRange+insertText to swap the alphabetical References list for an IEEE-ordered [1]..[14] block. Preserves the 'References' HEADING_2 anchor; applies `updateParagraphStyle NORMAL_TEXT` + `deleteParagraphBullets` across the inserted range to kill inherited list numbering. Range math: delete from `ref_heading.endIndex` to `body_end - 1` (never touch the sentinel newline at body_end).
  - `scripts/gdoc-apa-to-ieee-fixup.py` - regex-scan follow-up to `gdoc-apa-to-ieee.py`. Catches citations nested inside outer parentheticals (e.g. `(19 parameters, defaults from Ye et al., 2022)`) that the paren-anchored rules in the main script cannot match. Scans body pre-References with three regexes (et_al / and-or-amp / single-name), dedups overlapping spans, maps leading surname via `AUTHOR_TO_IEEE`, applies bare-form `replaceAllText` batch, and re-scans to prove 0 residuals. Unknown surnames are flagged for manual review rather than auto-rewritten.
- Preferred edit strategy: `documents.batchUpdate` with `replaceAllText` requests. Embedded `\n` in `replaceText` produces paragraph breaks that inherit the replaced paragraph's style.
- Verification pattern: after batchUpdate, re-fetch doc and substring-check for each new sentence.
