# Conference Paper — Outline & Budget

**Target doc:** `1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs`
**Rules:** HTKH GV-SV 2025 (Tiếng Việt + English bilingual front matter, English body)
**Target length:** ~8.5 pages (min 7), ~3,100 English body words

---

## 0. Page budget

| # | Block | Target page | Target word (EN) |
|---|---|---|---|
| F | Title VI + Title EN + Authors | 0.3 | 50 |
| F | Abstract VI (150–200 w) + Keywords VI | 0.25 | 180 VI |
| F | Abstract EN (150–200 w) + Keywords EN | 0.25 | 180 EN |
| 1 | Introduction | 1.25 | 550 |
| 2 | Related Work & Theoretical Background | 1.3 | 600 |
| 3 | Methodology | 2.25 | 900 |
| 4 | Results & Discussion | 2.0 | 800 |
| 5 | Conclusion | 0.5 | 250 |
| R | References (≤15, APA 7) | 0.75 | — |
| **Σ** | | **~8.9 pages** | **~3,280 EN words** |

---

## 1. Visual shortlist (4 keep + 1 optional)

| Label | Source (VISUAL-GUIDE.md) | Catbox | Appears in | Rationale |
|---|---|---|---|---|
| **Figure 1** | `ch3-system-architecture` | `1j18y7.png` | §3.1 | Central artifact — five-layer architecture. Must be in conference paper. |
| **Figure 2** | `ch4-adaptive-engine-sequence` | `vq16l2.png` | §4.1 (walk-through) | Shows closed-loop submission pipeline — proves implementation. |
| **Figure 3** | `ch5-experiment-timeline` | `xaopkb.png` | §3.8 (protocol) | Makes the pre-registered protocol concrete. |
| **Table 1** | `ch2-technique-complementarity` | `8ulh9q.png` | §2 (integration argument) | Justifies why BKT+Elo+MAB+FSRS together — core motivation. |
| **Figure 4 (OPT)** | `ch3-knowledge-graph` | `puhgbh.png` | §3.2 (if space) | Nice-to-have; drop if page count tight. |

*Decision:* start with 4 (Fig 1–3 + Table 1), add Fig 4 only if preflight shows we're under 8 pages.

---

## 2. Front matter (file `03-front-matter.md`)

### Title VI (draft)
*"Nền tảng học thích ứng cho môn lập trình bậc đại học: tích hợp truy vết tri thức Bayes, xếp hạng Elo, bandit đa cánh tay và lịch lặp lại cách quãng FSRS"*

### Title EN (draft)
*"An Adaptive Learning Platform for University Programming Courses: Integrating Bayesian Knowledge Tracing, Elo Rating, Multi-Armed Bandits, and FSRS"*

### Authors block
```
Nguyễn Tuấn Dương
Lớp 1C22, Khoa Công Nghệ Thông Tin
Email: ntduongvbhp@gmail.com

Giáo viên hướng dẫn: ThS. Bùi Quốc Khánh
```
*Arial 10pt italic bold (per thể lệ).*

### Abstract VI (target 180 từ, khoảng 150-200)
Structure 4 khối tương ứng abstract EN:
1. Problem (Tỉ lệ rớt môn lập trình cao, khoảng trống tích hợp adaptive techniques cho lập trình)
2. Solution (Đề xuất nền tảng adaptive 5 lớp tích hợp BKT, Elo, H-MAB, FSRS, tuỳ chọn LLM)
3. Method (Kiến trúc closed-loop trên đồ thị tri thức 28 khái niệm; giao thức đánh giá pre-registered n=40-60, 4 tuần)
4. Contribution (4 đóng góp: kiến trúc tích hợp, H-MAB có ràng buộc prerequisite, ánh xạ submission→FSRS rating đầu tiên cho lập trình, nền tảng open-source; **nêu rõ** Contribution 1 đã triển khai kỹ thuật, Contribution 2 đã thiết kế nhưng chưa chạy thực nghiệm — per comment #14)

### Keywords VI (alphabet VN)
*Bandit đa cánh tay; Giáo dục lập trình; Học lặp lại cách quãng; Học thích ứng; Truy vết tri thức Bayes*

### Abstract EN (target 180 words, range 150-200)
Structure:
1. Problem (failure rate 30-40%, integration gap — none combine BKT+Elo+MAB+FSRS for programming)
2. Proposal (5-layer adaptive platform)
3. Method (KG 28 concepts, closed-loop; pre-registered pilot n=40-60)
4. Contribution + explicit artifact-vs-plan distinction [comment #14, #18]

### Keywords EN (alphabet)
*Adaptive learning; Bayesian knowledge tracing; Multi-armed bandit; Programming education; Spaced repetition*

---

## 3. Section 1 — Introduction (~550 words, file `03-section1-introduction.md`)

**Sub-beats:**
1. **Problem statement (~120 w).** 30-40% failure rate in intro programming (cite Luxton-Reilly 2018); root cause = mismatch between individualized practice-intensive skill acquisition and uniform large-class instruction.
2. **Gap in existing platforms (~120 w).** LeetCode/HackerRank/Codeforces offer volume, not personalization. Static difficulty; no closed-loop adaptation. Duolingo shows adaptive scale in *language learning* — not programming — suggesting transfer potential [apply comment #19 fix].
3. **Proposed approach (~130 w).** Five-layer adaptive engine unified by a knowledge graph: Layer 1 BKT (mastery estimation), Layer 2 Dynamic Elo (difficulty calibration), Layer 3 Hierarchical MAB (problem selection), Layer 4 FSRS (review scheduling, **first application to programming**), Layer 5 LLM Socratic hints (optional).
4. **Contributions + artifact-vs-plan statement (~140 w).** Four contributions listed. Explicit disclaimer: *"This paper should be read as an implementation paper with a pre-registered pilot evaluation protocol, not as a completed classroom study. Contribution 1 (the integrated platform) is implemented and demonstrated technically; Contribution 2 (the evaluation protocol) is specified but not yet empirically executed."* [comments #14, #18]
5. **Paper roadmap (~40 w).** One sentence pointing to sections 2–5.

---

## 4. Section 2 — Related Work & Theoretical Background (~600 words, file `03-section2-literature.md`)

**Directive from comment #10/#11/#12:** each subsection ≤120 words, ends with "Relevance to this work" in 1-2 sentences.

- **2.1 Knowledge tracing (120 w).** BKT (Corbett & Anderson 1995) — four-parameter HMM, interpretable. DKT (Piech 2015) — better accuracy, opaque. **Relevance:** we choose BKT for interpretability + lower data requirement; DKT deferred as future work.
- **2.2 Difficulty calibration & ZPD (100 w).** Elo (Pelánek 2016) for adaptive education; Vygotsky (1978) ZPD and Bjork's desirable difficulties. **Relevance:** we use dual Elo (student + problem) with ZPD-gated candidate filtering.
- **2.3 Multi-Armed Bandits in education (100 w).** Thompson Sampling (Chapelle & Li 2011) for exploration-exploitation; Rollinson & Brunskill (2015) for instructional policy. **Relevance:** Thompson Sampling + prerequisite-gated hierarchical arms is our core selection mechanism.
- **2.4 Spaced Repetition — FSRS (120 w).** Ebbinghaus forgetting curve; Cepeda et al. (2006) spacing effect. FSRS (Ye 2022) achieves 20-30% review reduction vs SM-2; Settles & Meeder (2016) adaptive scheduling for language. **Relevance:** applying FSRS to programming (a procedural skill) is novel; we map code submission outcomes to FSRS ratings.
- **2.5 Integration gap (90 w).** Prior work treats BKT, Elo, MAB, FSRS in isolation or pairs; no system combines all four for programming. Our position: integration > sum of parts. **Relevance:** this is the paper's central contribution. See Table 1 for complementarity.

---

## 5. Section 3 — Methodology (~900 words, file `03-section3-methodology.md`)

**Largest section** per comment #9 (tech = paper's strength).

- **3.1 System overview & closed-loop architecture (~150 w + Figure 1).** Four-component platform (React + NestJS + FastAPI + PostgreSQL + Docker sandbox) with a five-layer adaptive engine. Each submission triggers async update across all layers.
- **3.2 Knowledge graph foundation (~100 w).** 28 concepts, ~45 prerequisite edges spanning 5 difficulty tiers and 7 topic groups. Layers share KG as the common substrate. (Skip Figure 4 KG to save space; describe in text.)
- **3.3 Layer 1 — BKT (~120 w).** Standard four-param HMM (P(L₀), P(T), P(G), P(S)) per concept. Mastery threshold θ_m = 0.85. *Rationale sentence [comment #8]:* "θ_m = 0.85 is a design choice informed by the ITS literature (Corbett & Anderson, 1995), not empirically optimized on this dataset."
- **3.4 Layer 2 — Dynamic Elo (~130 w).** Dual ratings: student (init 1200) + problem (1000/1200/1400 for Easy/Medium/Hard). Dynamic K ∈ [10, 40], base K=25. *Rationale sentence [comment #7]:* "K=25 is a heuristic midpoint chosen for moderate volatility in educational settings, not a tuned optimum." ZPD filter: δ ∈ [50, 250] rating points.
- **3.5 Layer 3 — Hierarchical MAB with Thompson Sampling (~160 w).** Two-level: concept → problem within concept. Prerequisite gate — arm is eligible only when all prerequisites reach θ_m. Reward function combines learning gain (w₁=0.5), correctness (w₂=0.3), efficiency (w₃=0.2). *Rationale sentence [comment #6]:* "These weights are a heuristic weighting combining learning gain, difficulty match, and efficiency; they are not learned from empirical data."
- **3.6 Layer 4 — FSRS + submission-to-rating mapping (~150 w).** FSRS-5 with 19 trainable parameters. **Novel contribution:** mapping code submission outcomes → 4 FSRS rating levels (Again/Hard/Good/Easy) via correctness × attempt-count × time-spent. Enables spaced review of programming concepts.
- **3.7 Layer 5 — LLM feedback (optional, ~40 w).** Socratic-style hints via RAG grounded in student knowledge state. Turned off by default for evaluation.
- **3.8 Pre-registered evaluation protocol (~100 w + Figure 3).** Between-subjects design, n=40-60 Hanoi University undergraduates, 4-week intervention + 8-week retention. **RQ1 (primary):** predictive validity of BKT/Elo (AUC-ROC). **RQ2 (supporting):** recommendation acceptance and convergence speed. **RQ3 (outcome):** normalized learning gain. *[RQ1 refocused per comment #17.]*

---

## 6. Section 4 — Results & Discussion (~800 words, file `03-section4-results.md`)

### 4.1 Results — Implemented artifact (~450 w)

**Reframe per plan:** system = result. Three blocks.

- **Deployment & code metrics (~200 w + implicit summary table).** ~2,500 LOC Python (adaptive engine), ~4,000 LOC TypeScript (NestJS backend), ~3,000 LOC TypeScript/React (frontend additions). Stack: React 18, NestJS 10, FastAPI (Python 3.11), PostgreSQL 16, Redis 7, Docker-based code sandbox (256MB memory, 5s CPU timeout, unprivileged). System is deployed and operational; recommendation latency <500ms at 100 concurrent users. *[Tense: present/past consistent per comment #16.]* *[Highlight implementation evidence per comment #5.]*
- **Closed-loop walk-through (~150 w + Figure 2).** One concrete scenario: student submits code for Problem P on Concept C → outcome scored → BKT posterior updated → Elo adjusted → MAB re-ranked → FSRS queue rescheduled. Figure 2 shows the sequence.
- **Evaluation protocol status (~100 w).** *"The evaluation is designed as a pre-registered pilot, not yet executed. The study design is fully specified (Section 3.8); the protocol has been IRB-reviewed. Results will be reported in a follow-up publication."* [per comments #4, #18]

### 4.2 Discussion (~350 w)

- **Layer-by-layer benchmark comparison (~150 w).** Expected BKT AUC ≥ 0.70 (standard ITS threshold, Corbett & Anderson 1995). Expected FSRS 20-30% review reduction vs SM-2 (Ye 2022 validation). Elo expected convergence ~20 attempts per learner (Pelánek 2016). Each of these is a *design target derived from literature*, not an empirical result of this system.
- **Why integration > sum of parts (~130 w).** BKT mastery gates MAB arm eligibility; Elo narrows candidate set to ZPD; FSRS urgency interrupts exploration. Each handoff is informed by one layer and consumed by the next — emergent adaptive behavior that no single technique achieves alone.
- **Limitations (~70 w).** No empirical learning-gain data yet. Single-site sample. Bundled treatment (cannot attribute effect to individual layers in between-subjects design). **Explicit framing:** artifact is validated; evaluation is planned [per comments #14, #18].

---

## 7. Section 5 — Conclusion (~250 words, file `03-section5-conclusion.md`)

- **Recap (~100 w).** Presented first integrated 5-layer adaptive platform for programming. Four contributions: integration, prerequisite-constrained H-MAB, FSRS submission-rating mapping, deployable open-source system.
- **Artifact-vs-plan re-statement (~60 w).** *"Contribution 1 is implemented and demonstrated technically. Contribution 2 — the evaluation protocol — is specified, IRB-reviewed, and pre-registered, but the classroom pilot has not yet been conducted."*
- **Future work (~50 w).** Execute pre-registered pilot (n=40-60); multi-site expansion; full LLM Layer 5 evaluation.
- **Closing takeaway (~40 w).** Single-sentence message suitable for conference closing slide [per comment #1]. Draft: *"By integrating four adaptive techniques that have, until now, been studied in isolation, this work demonstrates a working architecture for the long-standing ambition of individualized programming education at scale."*

---

## 8. References — 15-entry shortlist (APA 7, alphabetical)

1. Anderson, J. R., Corbett, A. T., Koedinger, K. R., & Pelletier, R. (1995). Cognitive tutors: Lessons learned. *The Journal of the Learning Sciences*, 4(2), 167–207.
2. Bjork, R. A., & Bjork, E. L. (2011). Making things hard on yourself, but in a good way: Creating desirable difficulties to enhance learning. In *Psychology and the real world* (pp. 56–64). Worth Publishers.
3. Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin*, 132(3), 354–380.
4. Chapelle, O., & Li, L. (2011). An empirical evaluation of Thompson sampling. In *Advances in Neural Information Processing Systems* (Vol. 24, pp. 2249–2257).
5. Corbett, A. T., & Anderson, J. R. (1995). Knowledge tracing: Modeling the acquisition of procedural knowledge. *User Modeling and User-Adapted Interaction*, 4(4), 253–278.
6. Luxton-Reilly, A., Simon, Albluwi, I., Becker, B. A., Giannakos, M., Kumar, A. N., Ott, L., Paterson, J., Scott, M. J., Sheard, J., & Szabo, C. (2018). Introductory programming: A systematic literature review. In *Proceedings of ITiCSE-WGR '18* (pp. 55–106). ACM.
7. Ma, W., Adesope, O. O., Nesbit, J. C., & Liu, Q. (2014). Intelligent tutoring systems and learning outcomes: A meta-analysis. *Journal of Educational Psychology*, 106(4), 901–918.
8. Pelánek, R. (2016). Applications of the Elo rating system in adaptive educational systems. *Computers & Education*, 98, 169–179.
9. Piech, C., Bassen, J., Huang, J., Ganguli, S., Sahami, M., Guibas, L., & Sohl-Dickstein, J. (2015). Deep knowledge tracing. In *Advances in Neural Information Processing Systems* (Vol. 28, pp. 505–513).
10. Rollinson, J., & Brunskill, E. (2015). From predictive models to instructional policies. In *Proceedings of EDM 2015* (pp. 179–186).
11. Segal, A., Gal, Y., Kamar, E., Horvitz, E., & Miller, G. (2018). Optimizing interventions via offline policy evaluation: Studies in citizen science. In *Proceedings of AAAI 2018* (pp. 3893–3900).
12. Settles, B., & Meeder, B. (2016). A trainable spaced repetition model for language learning. In *Proceedings of ACL 2016* (pp. 1848–1858).
13. Vygotsky, L. S. (1978). *Mind in society: The development of higher psychological processes*. Harvard University Press.
14. Ye, J., Su, J., & Cao, Y. (2022). A stochastic shortest path algorithm for optimizing spaced repetition scheduling. In *Proceedings of KDD '22* (pp. 4381–4390). ACM.
15. Wang, R. E., Wirawarn, Q., Goodman, N., & Demszky, D. (2023). SocraticLM: Exploring Socratic questioning strategies in language models. In *Proceedings of EMNLP 2023 Findings*.

---

## 9. Cross-cutting compliance checklist (applies to every section)

Per comment triage synthesis:
- [ ] Artifact vs plan distinction stated in: abstract (VI + EN), §1 close, §4 close, §5. **4 occurrences.**
- [ ] Every hyperparameter / threshold mentioned has a rationale clause (§3.3 θ_m, §3.4 K, §3.5 reward weights).
- [ ] Each §2 subsection ends with a "Relevance to this work" line (1-2 sentences).
- [ ] RQ1 framed as predictive validity only. Acceptance/convergence = supporting.
- [ ] Duolingo reference fixed (language, not programming) in §1.
- [ ] Tense: deployed system in present/past; evaluation in future.
- [ ] All citations APA 7; list ≤ 15 entries; alphabetical.
- [ ] No "figure above" / "table below" / "hình trên" / "bảng dưới".
- [ ] Figures/tables labelled Figure 1.., Table 1..
- [ ] Caption format: "Figure X. Caption text." then new line "Source: author's own work." (or thesis citation).

---

## 10. Stage gate status

- [x] Stage 1 — Intake (comments fetched + triaged + author metadata received)
- [ ] **Stage 2 — This outline (awaiting user approval)**
- [ ] Stage 3 — Write front matter + 5 sections + references
- [ ] Stage 4 — Assemble + preflight
- [ ] Stage 5 — Publish to GDoc
- [ ] Stage 6 — Final QA
