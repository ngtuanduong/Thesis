# Conference Paper — Session Summary

## Deliverable

**Google Doc:** https://docs.google.com/document/d/1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs/edit

**PDF snapshot (local, for reference):** `c:/tmp/conf-paper-check.pdf`

## Compliance against thể lệ HTKH GV-SV 2025

| Rule | Required | Actual | Status |
|---|---|---|---|
| Minimum length | ≥ 7 pages A4 | 14 pages | PASS |
| Page size | A4 (210 × 297 mm) | 595.28 × 841.89 pt ✓ | PASS |
| Margins | top 2.5cm, bottom 2.5cm, left 3cm, right 3cm | 70.87/70.87/85.04/85.04 pt ✓ | PASS |
| Title | Tahoma 15pt bold center | Tahoma 15pt bold CENTER ✓ | PASS |
| Author | Arial 10pt italic bold | Arial 10pt bold italic CENTER ✓ | PASS |
| Abstract | Arial 10pt italic, 150-200 words VI | VI 198 words, Arial 10pt italic ✓ | PASS |
| Abstract EN (bilingual) | 150-200 words | 191 words ✓ | PASS |
| Keywords | 3-5 alphabetical, both langs | 5 VI + 5 EN ✓ | PASS |
| Body font | Times New Roman 13pt | TNR 13pt ✓ | PASS |
| First-line indent | 0.85 cm | 0.85cm ✓ | PASS |
| Spacing before | 6 pt | 6pt ✓ | PASS |
| Line spacing | Exactly 17pt | 131% × 13pt ≈ 17.03pt (approximated) | MANUAL FIX (10s) |
| Structure | 5 required sections + refs | 1 Intro, 2 Related, 3 Method, 4 Results+Disc, 5 Conclusion, Refs ✓ | PASS |
| References | ≤15, APA 7 | 14 entries ✓ | PASS |
| No "figure above/table below" | — | 0 hits ✓ | PASS |
| Figures/Tables labelled | Figure N / Table N explicit | 3 figures + 1 table, explicit numbering ✓ | PASS |

## Advisor comments applied (13 CRITICAL → integrated)

| Comment | Where applied |
|---|---|
| #2 Control group logic fix | §3.8 Methodology |
| #4 Preserve Ch5 eval framing | §4.1 Results (evaluation protocol status paragraph) |
| #5 Highlight implementation evidence | §4.1 Deployment block |
| #6 Heuristic weighting sentence | §3.5 Layer 3 MAB |
| #7 K=25 rationale | §3.4 Layer 2 Elo |
| #8 θ_m=0.85 rationale | §3.3 Layer 1 BKT |
| #9 Emphasize tech chapters | §3 given ~900 words (largest section) |
| #10/11/12 Cut lit review + "Relevance to this work" endings | §2.1–2.5 each ends with "Relevance to this work" line |
| #14 Artifact-vs-plan distinction | Abstract VI+EN, §1 close, §4.1 + §4.2 close, §5 re-statement |
| #16 Tense consistency | §4.1 uses present/past for deployed system throughout |
| #17 RQ1 = predictive validity only | §3.8 Protocol paragraph |
| #18 Implementation paper framing | §1 close + §5 re-statement |
| #19 Duolingo = language not programming | §1 ("Duolingo demonstrates the scalability of adaptive techniques in language learning, which suggests potential transfer to programming education") |

3 CONF-NICE items: #1 closing takeaway, #3 key Q&A quote, #15 emphasize at conference — all naturally absorbed.
3 THESIS-ONLY items (#13 Fig 1.4, #20 Fig 1.1, #21 §3.1.3) — not applicable to conference paper.

## Remaining manual actions for you

1. **Line spacing "Exactly 17pt" fix** (10 seconds, optional but recommended before submission):
   - Open the doc → Ctrl+A (select all) → Format → Line & paragraph spacing → Custom spacing → Exactly 17pt → Apply.
   - Or leave as 131% approximation (≈17.03pt) — reviewers almost certainly won't notice.

2. **Advisor review**: share the doc link with Thầy Khánh, fetch new comments with:
   ```bash
   python scripts/gdoc-read-comments.py --doc-id 1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs
   python scripts/gdoc-map-comments-to-chapters.py
   ```
   If new comments arrive, re-open the relevant section file in `documents/conference-paper/03-section*.md`, edit, then re-run:
   ```bash
   python scripts/conf-paper-preflight.py documents/conference-paper/paper-final.md
   python scripts/gdoc-write-conference-paper.py
   ```

3. **Submission package**: the doc is ready. When it's time to submit, export via File → Download → Microsoft Word (.docx) or PDF.

## File inventory (artefacts produced this session)

```
documents/conference-paper/
├── 01-comments-triage.md           (advisor comments triaged with labels)
├── 02-outline.md                   (section-by-section skeleton + budget)
├── 03-front-matter.md              (titles, authors, 2 abstracts, 2 keyword blocks)
├── 03-section1-introduction.md     (582 words)
├── 03-section2-literature.md       (603 words, Table 1)
├── 03-section3-methodology.md      (863 words, Figures 1 & 2)
├── 03-section4-results.md          (745 words, Figure 3)
├── 03-section5-conclusion.md       (271 words)
├── 03-references.md                (14 APA 7 entries)
├── paper-final.md                  (assembled, preflight ALL PASS)
└── SESSION-SUMMARY.md              (this file)

scripts/
├── conf-paper-preflight.py         (new — validates paper-final.md)
└── gdoc-write-conference-paper.py  (new — publishes to GDoc with HTKH format)
```

## Statistics

- Total English body: 3,064 words (target 2,500–3,800 ✓)
- Abstract VI: 198 words (target 150–200 ✓)
- Abstract EN: 191 words (target 150–200 ✓)
- References: 14 (target ≤ 15 ✓)
- Figures: 3 + Tables: 1
- Unique inline citations: 14
- Orphan citations / unused references: 0
