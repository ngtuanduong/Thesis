---
name: Math parser single-line $$ bug
description: Markdown parser for thesis chapters has a critical bug with single-line $$ math equations that must be checked for in all future chapter publishing
type: feedback
---

The markdown parser used in publish_chapter4.py and republish_chapter4_humanized.py has a critical bug in $$ math block handling: single-line equations like `$$R'_{problem} = ... $$` (where $$ appears at both start AND end of the same line) trigger multi-line math mode. The parser strips the leading $$, then looks for the NEXT line ending with $$, consuming everything in between (headings, code blocks, paragraphs) into one giant "math" block.

**Why:** This caused sections 4.4.2 through 4.6.1 (6 headings + all their content) to be swallowed into one block, producing a 10,664-character blob in the Google Doc instead of properly formatted sections.

**How to apply:** When publishing ANY chapter, the parser MUST check if a line both starts and ends with $$ before entering multi-line math mode. The fix is:
```python
if stripped.endswith('$$') and len(stripped) > 4:
    # Single-line math: extract content between $$ markers
    math_content = stripped[2:-2].strip()
    blocks.append(('math', math_content))
else:
    # Multi-line math: consume until closing $$
```

The corrected parser is in `scripts/fix_chapter4.py`. The original scripts (`publish_chapter4.py`, `republish_chapter4_humanized.py`) still have the bug and should NOT be reused without this fix.
