# Visual Guide: Thesis Chapter Visuals

This document catalogs all generated visuals for the thesis "Adaptive Learning Platform for University Programming Courses." Each entry lists the chapter/section, visual type, file name, rationale for the format chosen, and integration guidance.

---

## Cover Page & Abstract

No visuals required. The cover page is text-only per university formatting standards. The abstract is a summary paragraph with no data to visualize.

---

## Chapter 1: Introduction

### Visual 1.1 — Platform Comparison Table (Table 1.1)
- **File:** `html/ch1-platform-comparison-table.html`
- **PNG Export:** `png/ch1-platform-comparison-table.png`
- **Catbox URL:** https://files.catbox.moe/5j02nc.png
- **Type:** Formatted HTML table (APA style)
- **Section:** 1.2.3 The Gap in Existing Platforms
- **Why table:** This compares 10 platforms across 6 binary/categorical attributes. Exact values and cross-referencing are essential. A table is the only format that allows readers to look up specific cells (e.g., "Does Duolingo have knowledge tracing?").
- **Integration:** Reference as Table 1.1 in the thesis. This is the most important visual in Chapter 1 — it establishes the research gap at a glance. The "This Thesis" row is highlighted to show full coverage.

### Visual 1.2 — Research Gap Diagram (Figure 1.1)
- **File:** `html/ch1-research-gap-diagram.html`
- **PNG Export:** `png/ch1-research-gap-diagram.png`
- **Catbox URL:** https://files.catbox.moe/iiyquw.png
- **Type:** SVG Venn diagram
- **Section:** 1.2.3 The Gap in Existing Platforms
- **Why diagram:** The research gap is best understood as an intersection between two categories (programming platforms and adaptive platforms). A Venn diagram communicates this positioning instantly and memorably.
- **Integration:** Place after Table 1.1 to provide a visual summary of the gap. Reference as Figure 1.1.

### Visual 1.3 — Closed-Loop Adaptive Workflow (Figure 1.2)
- **File:** `html/ch1-closed-loop-workflow.html`
- **PNG Export:** `png/ch1-closed-loop-workflow.png`
- **Catbox URL:** https://files.catbox.moe/eygpcs.png
- **Type:** SVG flowchart with feedback loop
- **Section:** 1.5.2 Closed-Loop Workflow
- **Why flowchart:** The four-step cycle (request -> engine -> submit -> update -> repeat) is fundamentally a process with feedback. A cyclic flowchart makes the "closed loop" concept tangible.
- **Integration:** Reference as Figure 1.2. Place immediately after the textual description of the workflow in Section 1.5.2.

### Visual 1.4 — Five-Layer Architecture Overview (Figure 1.3)
- **File:** `html/ch1-five-layer-architecture-overview.html`
- **PNG Export:** `png/ch1-five-layer-architecture-overview.png`
- **Catbox URL:** https://files.catbox.moe/uq1e9d.png
- **Type:** SVG stacked layer diagram
- **Section:** 1.5.1 Architecture Overview
- **Why layered diagram:** The five layers have a logical dependency ordering (bottom to top). A stacked diagram communicates hierarchy, dependency direction, and the role of each layer simultaneously.
- **Integration:** Reference as Figure 1.3. This is the conceptual overview; Chapter 3 provides the detailed architecture diagram (Figure 3.1).

### Visual 1.5 — Thesis Structure Roadmap (Figure 1.4)
- **File:** `html/ch1-thesis-structure-roadmap.html`
- **PNG Export:** `png/ch1-thesis-structure-roadmap.png`
- **Catbox URL:** https://files.catbox.moe/ve758p.png
- **Type:** SVG roadmap with chapter flow, contributions, and research questions
- **Section:** 1.8 Thesis Structure
- **Why roadmap:** Readers benefit from seeing how chapters connect, where contributions land, and which RQs map to which sections. A linear flow with cross-references communicates structure better than a bullet list.
- **Integration:** Reference as Figure 1.4. Place at the end of Chapter 1 to orient the reader for subsequent chapters.

---

## Chapter 2: Literature Review

### Visual 2.1 — Literature Landscape Map (Figure 2.1)
- **File:** `html/ch2-literature-landscape-map.html`
- **Type:** SVG convergence diagram (6 research streams flowing to thesis)
- **Section:** Chapter 2 overview / 2.4 Research Gap
- **Why convergence diagram:** The literature review covers six distinct research streams that all converge on this thesis. A convergence diagram shows readers the breadth of the literature landscape and how each stream contributes to the thesis, providing a mental model for the entire chapter.
- **Integration:** Reference as Figure 2.1. Place at the beginning of Chapter 2 as an advance organizer, or at Section 2.4 as a synthesis visual.

### Visual 2.2 — Detailed Comparison Table (Table 2.2)
- **File:** `html/ch2-detailed-comparison-table.html`
- **Type:** Formatted HTML table (extended APA style)
- **Section:** 2.4.1 Synthesis of Adaptive Capabilities
- **Why table:** Extends Table 1.1 with additional systems (academic prototypes) and a domain column. The 15-row x 8-column matrix requires tabular format for precise cross-referencing. Color-coded domain column aids scanning.
- **Integration:** Reference as Table 2.2. This is the comprehensive version; Table 1.1 is the accessible summary.

### Visual 2.3 — Technique Complementarity Table (Table 2.3)
- **File:** `html/ch2-technique-complementarity-table.html`
- **Type:** Formatted HTML table (APA style, 3 columns)
- **Section:** 2.4.2 Identified Gaps — Gap 1
- **Why table:** The "addresses vs. does not address" structure for 6 techniques is inherently tabular. Color coding (green for addresses, red for blind spots) provides quick visual scanning.
- **Integration:** Reference as Table 2.3. This table directly motivates why integration is necessary.

### Visual 2.4 — Knowledge Tracing Evolution Timeline (Figure 2.2)
- **File:** `html/ch2-kt-evolution-timeline.html`
- **Type:** SVG horizontal timeline
- **Section:** 2.2.1--2.2.2 (BKT and DKT sections)
- **Why timeline:** Knowledge tracing has evolved through distinct phases (BKT 1994 -> DKT 2015 -> DKT2 2025). A timeline shows this evolution, positioning the thesis's choice of BKT in historical context and showing the upgrade path to DKT2.
- **Integration:** Reference as Figure 2.2. Place at the end of Section 2.2.2 or beginning of 2.2.3.

### Visual 2.5 — Spaced Repetition Evolution (Figure 2.3)
- **File:** `html/ch2-spaced-repetition-evolution.html`
- **Type:** SVG timeline with innovation callout
- **Section:** 2.2.5 Spaced Repetition
- **Why timeline + callout:** The evolution from Ebbinghaus to FSRS is a historical progression. The callout box highlights the key innovation (rating mapping for programming), which is the thesis's novel contribution in this area.
- **Integration:** Reference as Figure 2.3. Place at the end of Section 2.2.5.

---

## Chapter 3: System Requirements and Architecture

### Visual 3.1 — Functional & Non-Functional Requirements Tables (Tables 3.1, 3.2)
- **File:** `html/ch3-functional-requirements-table.html`
- **Type:** Two formatted HTML tables (APA style)
- **Section:** 3.1.1 Functional Requirements, 3.1.2 Non-Functional Requirements
- **Why tables:** Requirements are structured data (ID, description, priority, source). Tables are the standard format for requirements specification in software engineering theses.
- **Integration:** Reference as Table 3.1 and Table 3.2. Place in Section 3.1.

### Visual 3.2 — System Architecture Diagram (Figure 3.1)
- **File:** `html/ch3-system-architecture-diagram.html`
- **Type:** SVG architecture diagram showing four components and five layers
- **Section:** 3.2 System Architecture / 3.3 Five-Layer Adaptive Architecture
- **Why architecture diagram:** This is the central technical figure of the thesis. It shows how the four platform components (React, NestJS, FastAPI, Docker) interact and where the five adaptive layers sit within the AI Service. No other format can communicate system topology this effectively.
- **Integration:** Reference as Figure 3.1. This is the most important figure in Chapter 3.

### Visual 3.3 — Knowledge Graph Diagram (Figure 3.2)
- **File:** `html/ch3-knowledge-graph-diagram.html`
- **Type:** SVG directed acyclic graph
- **Section:** 3.3.7 Knowledge Graph Foundation
- **Why graph diagram:** The knowledge graph is literally a graph; a DAG visualization with color-coded topic groups and prerequisite edges is the natural representation. Readers can trace prerequisite chains visually.
- **Integration:** Reference as Figure 3.2. Simplified view; reference Appendix B for the complete 28-concept graph.

### Visual 3.4 — Recommendation Flow Sequence Diagram (Figure 3.3)
- **File:** `html/ch3-recommendation-sequence-diagram.html`
- **Type:** SVG UML-style sequence diagram
- **Section:** 3.4.1 Recommendation Flow
- **Why sequence diagram:** The recommendation flow involves five actors (Student, React, NestJS, Redis, AI Service) exchanging messages in a specific order. A sequence diagram is the standard UML format for this and shows timing, parallelism, and cache interactions clearly.
- **Integration:** Reference as Figure 3.3. Place in Section 3.4.1.

### Visual 3.5 — Submission Processing Flow (Figure 3.4)
- **File:** `html/ch3-submission-processing-flow.html`
- **Type:** SVG dual-phase flowchart (synchronous + asynchronous)
- **Section:** 3.4.2 Submission Processing Flow
- **Why dual-phase flowchart:** The key insight is the separation of synchronous execution (student-facing) from asynchronous adaptive updates (background). A side-by-side layout makes this architectural decision immediately visible.
- **Integration:** Reference as Figure 3.4. Place in Section 3.4.2.

### Visual 3.6 — Hyperparameter Summary Table (Table 3.3)
- **File:** `html/ch3-hyperparameter-summary-table.html`
- **Type:** Formatted HTML table with layer color badges
- **Section:** 3.3.8 Hyperparameter Summary
- **Why table:** 20 hyperparameters with 6 attributes each (name, symbol, default, range, justification, layer). This is reference data that readers need to look up precisely. Color-coded layer badges enable quick scanning by layer.
- **Integration:** Reference as Table 3.3. This is a critical reference table for Chapter 4 (implementation) and Chapter 5 (evaluation sensitivity analysis).

### Visual 3.7 — Database Schema ERD (Figure 3.5)
- **File:** `html/ch3-database-schema-erd.html`
- **Type:** SVG entity-relationship diagram
- **Section:** 3.5 Database Schema Design
- **Why ERD:** The database schema has 9 tables with foreign key relationships. An ERD is the standard representation, showing table structures, column types, and relationships at a glance.
- **Integration:** Reference as Figure 3.5. Place in Section 3.5.

### Visual 3.8 — Layer Interaction Matrix (Figure 3.6)
- **File:** `html/ch3-layer-interaction-matrix.html`
- **Type:** SVG heatmap-style matrix
- **Section:** 3.3 (cross-layer discussion)
- **Why matrix:** The data dependencies between 5 layers + KG Foundation form a producer-consumer matrix. A grid visualization shows at a glance which layers talk to which, with the key insight (Layer 3 as integration hub) highlighted.
- **Integration:** Reference as Figure 3.6. Place after all layers are described, as a summary visualization.

### Visual 3.9 — Cold Start Handling Flowchart (Figure 3.7)
- **File:** `html/ch3-cold-start-flowchart.html`
- **Type:** SVG decision flowchart with timeline
- **Section:** 3.4.4 Cold Start Handling
- **Why flowchart:** The cold start strategy is a three-phase decision process based on submission count. A flowchart with a decision diamond and timeline bar shows both the logic and the temporal progression.
- **Integration:** Reference as Figure 3.7. Place in Section 3.4.4.

### Visual 3.10 — Caching Strategy Table (Table 3.5)
- **File:** `html/ch3-caching-strategy-table.html`
- **Type:** Formatted HTML table (APA style)
- **Section:** 3.7 Caching Strategy
- **Why table:** 7 cache entries with 4 attributes (key pattern, data, TTL, invalidation trigger). This is lookup-oriented reference data best served by a table.
- **Integration:** Reference as Table 3.5. Place in Section 3.7.

### Visual 3.11 — Database Tables Overview (Table 3.4)
- **Guide only:** The database tables table (Table 3.4) is already present in the chapter text as a markdown table. The ERD (Figure 3.5) provides the visual complement. No separate HTML file needed beyond the ERD.

---

## Summary Statistics

| Chapter | Tables Generated | Figures Generated | Total |
|---------|:---:|:---:|:---:|
| Chapter 1 | 1 | 4 | 5 |
| Chapter 2 | 2 | 3 | 5 |
| Chapter 3 | 4 | 5 | 9 |
| **Total** | **7** | **12** | **19** |
---

## File Listing

| # | File Name | Type | Chapter |
|---|-----------|------|---------|
| 1 | `html/ch1-platform-comparison-table.html` | Table | Ch.1 |
| 2 | `html/ch1-research-gap-diagram.html` | Figure (Venn) | Ch.1 |
| 3 | `html/ch1-closed-loop-workflow.html` | Figure (Flowchart) | Ch.1 |
| 4 | `html/ch1-five-layer-architecture-overview.html` | Figure (Layers) | Ch.1 |
| 5 | `html/ch1-thesis-structure-roadmap.html` | Figure (Roadmap) | Ch.1 |
| 6 | `html/ch2-literature-landscape-map.html` | Figure (Convergence) | Ch.2 |
| 7 | `html/ch2-detailed-comparison-table.html` | Table | Ch.2 |
| 8 | `html/ch2-technique-complementarity-table.html` | Table | Ch.2 |
| 9 | `html/ch2-kt-evolution-timeline.html` | Figure (Timeline) | Ch.2 |
| 10 | `html/ch2-spaced-repetition-evolution.html` | Figure (Timeline) | Ch.2 |
| 11 | `html/ch3-functional-requirements-table.html` | Table (x2) | Ch.3 |
| 12 | `html/ch3-system-architecture-diagram.html` | Figure (Architecture) | Ch.3 |
| 13 | `html/ch3-knowledge-graph-diagram.html` | Figure (DAG) | Ch.3 |
| 14 | `html/ch3-recommendation-sequence-diagram.html` | Figure (Sequence) | Ch.3 |
| 15 | `html/ch3-submission-processing-flow.html` | Figure (Flowchart) | Ch.3 |
| 16 | `html/ch3-hyperparameter-summary-table.html` | Table | Ch.3 |
| 17 | `html/ch3-database-schema-erd.html` | Figure (ERD) | Ch.3 |
| 18 | `html/ch3-layer-interaction-matrix.html` | Figure (Matrix) | Ch.3 |
| 19 | `html/ch3-cold-start-flowchart.html` | Figure (Flowchart) | Ch.3 |
| 20 | `html/ch3-caching-strategy-table.html` | Table | Ch.3 |

---

## Design Conventions Used

- **Color palette:** Consistent across all visuals. Blue (#1565c0) for BKT/L1, pink (#880e4f) for Elo/L2, orange (#e65100) for MAB/L3, purple (#6a1b9a) for FSRS/L4, green (#2e7d32) for KG/LLM/thesis highlights.
- **Typography:** Times New Roman for body text (academic standard), Courier New for code/schema elements.
- **Table formatting:** APA 7th edition conventions (horizontal rules only, title above, notes below).
- **Figure captions:** Below figures per APA convention (Figure N. Description.).
- **Colorblind considerations:** All visuals use both color and labeling so they remain interpretable in grayscale. Shapes and patterns supplement color coding.

## How to Use These Visuals

1. **Open any HTML file in a browser** to preview the visual at full quality.
2. **To export for the thesis document:**
   - Open the HTML file in a browser
   - Use the browser's Print function or a screenshot tool to capture at 300 DPI
   - Alternatively, use a tool like `wkhtmltoimage` or Puppeteer for programmatic export
3. **To edit:** Each file is self-contained HTML with inline SVG. Modify text, colors, or dimensions directly in the HTML.
4. **Numbering:** The figure/table numbers in these files follow the chapter text. Verify final numbering against the thesis document before submission.
