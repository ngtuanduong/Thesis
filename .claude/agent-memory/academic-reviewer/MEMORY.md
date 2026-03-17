# Academic Reviewer Memory

## Project Context
- This is a bachelor's thesis at Hanoi University, Faculty of IT
- Title: "Adaptive Learning Platform for University Programming Courses"
- Tech stack: React frontend, NestJS API, FastAPI adaptive engine, PostgreSQL
- Branch: v2
- Thesis chapters located at: documents/thesis-chapters/
- Vietnamese thesis structure guide at: documents/sample/thesis-structure-in-vietname.md

## Review History
- Chapter 1 reviewed (2026-03-06, round 1): Major Revision recommended
  - Critical: unverifiable citation [Dynamic K-Value Elo, 2025], overclaimed novelty, Vietnamese citations need DOIs
  - Major: too much implementation detail in intro, RQs need hypothesis form, Table 1.1 biased comparison
- Chapter 1 reviewed (2026-03-07, round 2): PASS WITH MINOR REVISIONS
  - Fixed: Dynamic K-Value Elo citation removed, novelty claims hedged with "to the best of our knowledge", Table 1.1 footnote added, hypotheses added to RQ2/RQ3
  - Remaining: Vietnamese citations still lack DOIs, Table 1.1 needs category clarification, Section 1.2.1 slightly long, Klinkenberg et al. cited in refs but not in text, DKT2 undefined
  - Writing quality consistently strong for bachelor's level

## Patterns to Watch
- Author tends to make absolute novelty claims -- now mostly hedged, but verify in future chapters
- Vietnamese citations [Nguyen et al., 2022] and [Tran & Nguyen, 2023] repeatedly flagged for missing DOIs
- Section 1.2.1 historical content overlaps with what should be in Chapter 2 (Literature Review)
- Author handles scoping well -- optional Layer 5, honest effect size limitations
- Table comparisons mix different platform categories without explicit acknowledgment
- Unused references appear in the bibliography (Klinkenberg et al., 2011)
- "Mathematical equivalence" between Elo and IRT is slightly overclaimed -- should be "relationship"

## Vietnamese Thesis Standards (Key Points)
- Introduction should be 5-10 pages
- Practical contribution (working system) is highly valued
- Bilingual abstract required; system screenshots expected as evidence
- Implementation chapter should show actual code
- 50-80 pages total excluding appendices; min 20-30 references
- Defense before committee of 3-5 faculty members
