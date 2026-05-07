---
name: APA -> IEEE conversion gotcha: nested citations
description: Paren-anchored replaceAllText rules miss citations nested inside outer parentheticals; always follow up with a regex scanner that matches bare forms.
type: reference
---

When converting APA in-text citations to IEEE numeric on a Google Doc via
`replaceAllText`, rules of the form `(Author, YEAR)` / `(Author et al., YEAR)`
only match when the citation's opening `(` is the author-paren itself.

**Failure mode**: if the source has an outer parenthetical like
`(19 parameters, defaults from Ye et al., 2022)`, the `(` belongs to the prose
paren, so the inner citation appears in the doc as the **bare form**
`Ye et al., 2022` (no paren immediately before `Ye`). Paren-anchored rules
skip it silently.

**Remediation pattern** (implemented by `scripts/gdoc-apa-to-ieee-fixup.py`):
  1. Run the paren-anchored pass first (`gdoc-apa-to-ieee.py`).
  2. Re-scan the body (pre-References, to avoid bibliography false positives)
     with three regexes:
     - `[A-Z][a-zà-ỹA-Z\-]+ et al\., \d{4}`
     - `[A-Z][a-zà-ỹA-Z\-]+ (?:and|&) [A-Z][a-zà-ỹA-Z\-]+, \d{4}`
     - `[A-Z][a-zà-ỹA-Z\-]+, \d{4}`
     Order-of-specificity matters: record et-al/and matches first, drop
     single-name matches that overlap.
  3. For each match, look up the leading surname in an `AUTHOR_TO_IEEE` map.
     Unknown surname -> manual review (likely a date like "September, 2024",
     not a citation).
  4. Build bare-form `replaceAllText` rules (no surrounding parens) and apply
     a second batch. Re-scan; expect 0 remaining citation-looking matches.

Empirically confirmed on doc `1b21l8G9SX...` (conference paper): first pass
left exactly one residual, `Ye et al., 2022` in the §3.6 Layer 4 paragraph.
Fixup caught and rewrote it to `Ye et al. [6]` with `occurrencesChanged=1`.
