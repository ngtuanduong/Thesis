# Thesis Guide Memory

## Student Profile
- **Name:** Nguyen Tuan Duong (Student ID: 2201040036)
- **Degree:** Bachelor's thesis (Khoa luan tot nghiep)
- **Institution:** Hanoi University, Faculty of Information Technology
- **Advisor:** Bui Quoc Khanh
- **Language:** Vietnamese student, thesis written in academic English

## Thesis Details
- **Title:** Adaptive Learning Platform for University Programming Courses
- **Vietnamese:** He thong ho tro hoc tap thich ung cho mon lap trinh tai dai hoc
- **Citation style:** IEEE (used in 09-REFERENCES.md)
- **Target word count:** 29,000-42,000 total; Chapter 1: 3,000-4,000 words

## Research Questions (Consolidated to 4)
- RQ1 (Primary): Learner model accuracy (BKT AUC + Elo AUC)
- RQ2: H-MAB vs content-based filtering (NLG comparison)
- RQ3: FSRS spaced repetition for retention
- RQ4: Usability/usefulness (SUS, TAM, interviews)

## Key Contributions
1. Integrated multi-layer adaptive architecture (BKT+Elo+MAB+FSRS) - STRONG
2. Prerequisite-constrained Hierarchical MAB - MODERATE
3. FSRS for programming skill retention (novel domain) - STRONG
4. Open-source platform for Vietnamese context - MODERATE
- Note: Dynamic K-Value Elo is NOT a standalone contribution (fold into #1)

## System Architecture
- 5-layer adaptive engine: BKT -> Elo -> MAB -> FSRS -> LLM (optional)
- Foundation: Knowledge Graph (~30 concepts, ~36 prerequisite edges)
- Tech stack: React+TS, NestJS+Prisma, FastAPI (Python), PostgreSQL+pgvector, Docker sandbox, Redis
- Layer 5 (LLM) is optional/supplementary

## Chapter Status
- Chapter 1 (Introduction): DRAFTED - saved to documents/thesis-chapters/chapter1-introduction.md
- Chapters 2-6: Not yet written (extensive planning docs exist in documents/v2/)

## Project Structure
- Main thesis outline: documents/thesis.md
- V2 planning docs: documents/v2/ (00-09 files covering outline, lit review, architecture, algorithms, implementation, evaluation, contributions, references)
- Thesis chapters output: documents/thesis-chapters/

## Notes
- Vietnamese CS education references (Nguyen 2022, Tran 2023, Pham 2024) need verification before submission
- Several 2025-2026 references have incomplete citations (bracketed in 09-REFERENCES.md)
- Implementation is substantially complete (30 problems seeded, adaptive layers built)
- Evaluation timeline: ~10 weeks (March-May 2026)
