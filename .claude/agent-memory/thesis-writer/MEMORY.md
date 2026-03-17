# Thesis Writer Memory

## Completed Sections
- **Chapter 1 (Introduction)**: Complete, ~3800 words, references [1]-[21]
- **Chapter 2 (Literature Review)**: Complete, ~8300 words, references [22]-[55]
  - Structure: 2.1 Theoretical Foundations, 2.2 Related Technologies, 2.3 Related Work, 2.4 Research Gap
  - 12 numbered equations (2.1-2.12)
  - 3 tables (Table 2.1: KT comparison, Table 2.2: system comparison, Table 2.3: technique gaps)
- **Chapter 3 (System Design)**: Revised (2026-03-18), ~9500 prose words (~11800 total with code/diagrams)
  - Structure: 3.1 Requirements (+ 3.1.4 Traceability Matrix), 3.2 System Overview and Design Rationale (3.2.1 Four-Component Architecture, 3.2.2 Design Principles and Key Decisions), 3.3 Five-Layer Architecture (+ 3.3.8 Hyperparameter Summary), 3.4 Data Flow (+ 3.4.3 Error Handling, 3.4.4 Cold Start), 3.5 DB Schema, 3.6 API Design, 3.7 Caching
  - 7 numbered equations (3.1-3.7)
  - 5 tables (Table 3.1: design principles/decisions, Table 3.2: traceability matrix, Table 3.3: hyperparameter summary, Table 3.4: new DB tables, Table 3.5: caching config)
  - 4 figures (Fig 3.1: architecture, Fig 3.2: KG, Fig 3.3: sequence diagram, Fig 3.4: ER diagram)
  - New references: [56] pyBKT, [57] Csikszentmihalyi Flow, [58] Agrawal & Goyal Thompson Sampling

## Architecture Framing (confirmed 2026-03-18)
- System is described as NEW, purpose-built — NOT as improvement of old system
- Four-component architecture: React frontend, NestJS gateway, FastAPI AI service, PostgreSQL+Redis+Docker
- No "weakness analysis" framing; instead use "design principles and rationale"
- Table 3.1 is design principles table (6 rows: separation of concerns, write ownership, async updates, caching/concurrency, progressive enhancement, security by isolation)
- Section 3.6.3 retitled "Endpoints with Adaptive Integration" (not "Modifications to Existing")

## Citation Numbering
- Chapter 1 uses [1]-[21] (defined in chapter1-introduction.md)
- Chapter 2 introduces [22]-[55] (new references listed at end of chapter2)
- Chapter 3 introduces [56]-[58] (pyBKT, Csikszentmihalyi, Agrawal & Goyal)
- Next chapter should continue from [59] onwards if new refs needed
- Several [CITE: ...] placeholders remain for papers needing author verification (refs 36, 37, 38, 40, 41, 47-54)

## Key Terminology & Parameters (confirmed in Ch.3)
- "mastery probability" (not "knowledge state probability")
- "prerequisite gating" for BKT threshold check; threshold theta_m = 0.85
- "Zone of Proximal Development" operationalized as Elo range; delta_min=50, delta_max=250
- Review threshold: theta_r = 0.7
- Layer naming: L1=Knowledge Tracer, L2=Difficulty Calibrator, L3=Problem Selector, L4=Review Scheduler, L5=LLM Feedback Engine
- "rating mapping" for FSRS submission-to-rating translation
- Cold start: 3 round-robin interactions, resolves after ~10 submissions
- Elo init: students=1200, problems EASY=1000/MEDIUM=1200/HARD=1400
- MAB reward weights: w1=0.5 (learning gain), w2=0.3 (correctness), w3=0.2 (efficiency)

## Schema Details (confirmed from Prisma)
- BKT defaults: p_l0=0.1, p_transit=0.2, p_guess=0.15, p_slip=0.1
- Elo default: rating=1200.0, k_value=25.0
- MAB default: alpha=1.0, beta=1.0
- FSRS default: difficulty=5.0, stability=1.0, retrievability=1.0, state="NEW"

## Style Notes
- IEEE numbered citation format [N]
- Formal academic English, third person/passive voice
- Chapter intros summarize what the chapter covers
- Chapters end with transition sentence to next chapter

## File Locations
- Thesis chapters: documents/thesis-chapters/
- Prisma schema: server/prisma/schema.prisma
- AI service code: ai-service/app/
- V2 design docs: documents/v2/
- References master list: documents/v2/09-REFERENCES.md
