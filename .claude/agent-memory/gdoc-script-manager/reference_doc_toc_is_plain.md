---
name: Thesis doc Table of Contents is plain text, not a generated TOC
description: There is no structured TOC entry for Chapter 5 to update — TOC is a single 4-line text block
type: reference
---

Near the front of the doc (around startIndex 4415), the "Table of Contents" region is literally one paragraph:

```
Table of Contents
List of Figures
List of Tables
List of Abbreviations
```

There are no chapter entries with page numbers in the document body. If a revision plan asks to "update the TOC entry for Chapter X", there is nothing to update in the document text itself — the real TOC (if any) is generated in the PDF/print pipeline, not here. Report this as an anomaly when asked to edit TOC entries.
