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
- Preferred edit strategy: `documents.batchUpdate` with `replaceAllText` requests. Embedded `\n` in `replaceText` produces paragraph breaks that inherit the replaced paragraph's style.
- Verification pattern: after batchUpdate, re-fetch doc and substring-check for each new sentence.
