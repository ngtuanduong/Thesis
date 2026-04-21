---
name: Force UTF-8 stdout on Windows when printing doc text
description: gdoc read scripts crash on Windows cp1252 console without an explicit utf-8 wrapper
type: feedback
---

When a gdoc-read script prints paragraphs that contain Vietnamese diacritics or em-dashes, the default Windows console encoding (cp1252) throws `UnicodeEncodeError`.

**Why:** Python on Windows defaults stdout to cp1252; the thesis doc contains characters like `Ộ` (U+1ED8) and em-dashes that are not in that codepage.

**How to apply:** In any `scripts/gdoc-read-*.py` or `scripts/gdoc-write-*.py` that prints doc content, add at the top:

```python
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
```
