# 15-Minute Conference Presentation Plan
**Title (EN):** *An Adaptive Learning Platform for University Programming Courses: Integrating BKT, Elo, MAB & FSRS*
**Speaker:** Nguyễn Tuấn Dương — solo, English delivery
**Audience:** HTKH GV-SV 2025 student-paper conference (mixed CS / education / undergraduate panel)
**Plan file owner:** drafted 2026-05-06 from paper [paper-final.md](documents/conference-paper/paper-final.md) + three codebase exploration passes (adaptive engine / frontend / NestJS+infra).

---

## 1. Context

The paper is already accepted in draft form. The next deliverable is a **15-minute live talk in English by a solo non-native speaker** (Vietnamese first language). The paper claims four contributions but is dense (3,280-word body, 14 references, 4 visuals). A 15-minute slot cannot replicate the paper — it must extract the **single strongest narrative line** ("integration is the contribution") and let the audience leave with three things in their head:

1. **Why** the integration of four classic adaptive techniques was missing for programming education.
2. **What** the five-layer architecture actually does on every code submission (closed loop).
3. **What is real today** vs. what is pre-registered for the pilot — the *artifact-vs-plan* distinction the paper makes four times.

The plan also has to **manage the speaker's risks**: solo English delivery, dense math (BKT update equation, Elo K-factor, Thompson posterior, FSRS retrievability), audience that may not be ML-literate, and the awkwardness of presenting an "implementation paper with no empirical results yet". The slide deck and speaker script must defuse all four.

This plan does **not yet build the slides** — it specifies what each slide says, how long it takes, and what concrete code/visual artifact backs it. The next session executes this plan into a `.pptx` (or Google Slides) deck plus a rehearsal script.

---

## 2. Strengths, novelty, and unique points to convey (from paper + code)

This is the universe of "wow" material the talk will draw from. The slides will be ruthless about cutting most of it; the script and Q&A prep will hold the rest in reserve.

### 2.1 Novel contributions explicitly claimed in the paper

| # | Contribution | What makes it novel |
|---|---|---|
| C1 | First integrated 5-layer adaptive architecture combining **BKT + Elo + hierarchical MAB + FSRS** for programming education | Each technique exists; nobody composed all four under a single knowledge graph for programming |
| C2 | **Prerequisite-constrained hierarchical bandit** with BKT-based mastery gating | Outer arm (concept) gated by `mastery(prereqs) ≥ θ_m = 0.85`; inner arm (problem) further gated by Elo ZPD δ ∈ [50, 250] |
| C3 | **First application of FSRS to programming retention** via a novel **code-submission-to-rating mapping** | FSRS was designed for flashcards (4-level Likert: Again/Hard/Good/Easy). Programming gives correctness × attempts × time. The mapping is the original work. |
| C4 (engineering) | Fully deployed open-source platform: React 18 + NestJS 10 + FastAPI + PostgreSQL 16 + Redis 7 + Docker sandbox | One-command `docker compose up`, ~15k LOC across services, e2e tests green |

### 2.2 Concrete implementation evidence (presentation-grade)

These are the specific code findings to reference on slides — they prove the artifact exists and turn abstract claims into "look, here's the code".

- **Tiered BKT priors** [ai-service/app/services/bkt_service.py:18-24](ai-service/app/services/bkt_service.py#L18-L24) — five difficulty-tier-specific parameter sets (P(L₀), P(T), P(G), P(S)), not one-size-fits-all. *Talking point:* "calibrated cold-start across the curriculum, not a textbook BKT".
- **Dynamic K-factor** [ai-service/app/services/elo_service.py:36-68](ai-service/app/services/elo_service.py#L36-L68) — exponentially weighted residual trend over the last 10 submissions; K ∈ [10, 40] auto-adjusts (improving learner → smaller K, struggling learner → larger K).
- **ZPD filter** [ai-service/app/services/elo_service.py:244-328](ai-service/app/services/elo_service.py#L244-L328) — keeps only problems whose Elo is in `[student_elo + 50, student_elo + 250]`, i.e. ~36–64% predicted success — a direct operationalization of Bjork's *desirable difficulty*.
- **Hierarchical Thompson sampling** [ai-service/app/services/mab_service.py:34-48](ai-service/app/services/mab_service.py#L34-L48), **prerequisite gate** [mab_service.py:122-183](ai-service/app/services/mab_service.py#L122-L183), **reward weights** w₁=0.5 (BKT learning gain) + w₂=0.3 (correctness/attempts) + w₃=0.2 (efficiency, capped at 300s) [mab_service.py:51-84](ai-service/app/services/mab_service.py#L51-L84).
- **Submission → FSRS rating mapping (THE novelty for C3)** [ai-service/app/services/fsrs_service.py:108-126](ai-service/app/services/fsrs_service.py#L108-L126):
  ```
  not correct        → Again (1)
  correct, attempt 1, <2 min   → Easy (4)
  correct, attempt 1, 2-5 min  → Good (3)
  correct, attempt 1, >5 min   → Hard (2)
  correct, attempt ≥2          → Hard (2)
  ```
  This single 18-line function is the second-most-original piece of code in the project. Show it on a slide verbatim.
- **Async fan-out** [ai-service/app/services/adaptive_engine.py:49-137](ai-service/app/services/adaptive_engine.py#L49-L137) — `asyncio.gather(update_elo, update_mab, update_fsrs)` after the BKT step, with cache invalidation. This is the **closed loop** the paper sells.
- **Knowledge graph seed** [server/prisma/seed-adaptive.ts:22-145](server/prisma/seed-adaptive.ts#L22-L145) — 28 concepts × 5 tiers × 7 topic clusters, 45 prerequisite edges, hand-authored.
- **Sandbox** [docker/sandbox/Dockerfile](docker/sandbox/Dockerfile) + [docker/docker-compose.yml](docker/docker-compose.yml) — `--memory=256m --cpus=0.5 --network=none --read-only`, unprivileged user.

### 2.3 Frontend evidence the system is real (demo material)

The frontend is the most demo-friendly proof the artifact exists. Even if the talk does **not** include a live demo (recommended for a 15-min slot — see §6.3), screenshots from these screens belong on the slides:

- **Knowledge Map** [client/src/pages/KnowledgeMap.tsx](client/src/pages/KnowledgeMap.tsx) — ReactFlow + Dagre, all 28 concept nodes, mastery as fill opacity, hover lights up prerequisites. *Best single screenshot for the talk.*
- **Review Queue** [client/src/pages/ReviewQueue.tsx](client/src/pages/ReviewQueue.tsx) — FSRS made visible: "Due Now" vs. "Upcoming", retrievability % per concept, stability in days, lapse counter. *Direct evidence Layer 4 is alive.*
- **Recommendations card with reason tags** [client/src/pages/Dashboard.tsx:216-285](client/src/pages/Dashboard.tsx#L216-L285) — every recommended problem displays *why* ("Optimal difficulty match", "High learning gain expected"). *Direct evidence Layer 3 is alive.*
- **Hint Panel** [client/src/components/HintPanel.tsx](client/src/components/HintPanel.tsx) — three-level Socratic hints, concepts referenced per hint. *Direct evidence Layer 5 is alive.*
- **Instructor Dashboard** [client/src/pages/InstructorDashboard.tsx:104-195](client/src/pages/InstructorDashboard.tsx#L104-L195) — struggling students table (BKT-cohort), problem acceptance-rate analytics. *Sells the platform's classroom utility for any educator in the room.*
- **Glossary + PageTour + WelcomeFlow** [client/src/components/onboarding/](client/src/components/onboarding/) — 20+ pedagogical terms with "where you see it" + interactive tour. *Sells "production polish, not a class project".*

### 2.4 Engineering credibility numbers (one slide of stats)

- **~15,300 LOC production** = 5,053 Python (adaptive engine) + 3,390 NestJS TypeScript + 6,865 React TypeScript/TSX (verified by Explore agent against the paper's claimed 2,500 + 4,000 + 3,000 — paper undercounts; we'll quote the verified figure or stay with paper's conservative numbers).
- **~3,008 LOC server tests + 1,238 LOC Playwright e2e** including [e2e/adaptive-pipeline.spec.ts](e2e/adaptive-pipeline.spec.ts) which validates the full submit → BKT → Elo → MAB → FSRS round-trip.
- **<500 ms recommendation latency at 100 concurrent users** (paper's NFR target, verified at design time).
- **170 curated problems** seeded across 15 active concepts in the demo dataset.
- **One-command deployment**: `docker compose up -d` brings up Postgres + Redis + NestJS + FastAPI + sandbox-image build — no manual steps.

### 2.5 Risk-defusal points (to bake into the script)

- **Artifact vs. plan**: stated explicitly on the title slide footer, on the contributions slide, and on the closing slide — three reinforcements, exactly what the paper does. Audience will not feel misled.
- **Why not Deep Knowledge Tracing (DKT)?** Pre-empt the question: BKT chosen for cold-start populations of a few hundred learners and for downstream consumption by a bandit that needs interpretable, calibrated mastery rather than raw accuracy.
- **Why hand-authored knowledge graph?** Pre-empt: scope decision; automated KG construction from curriculum is explicit future work.
- **What if the pilot fails to hit AUC ≥ 0.70?** Pre-empt: that *is* the research finding — predictive validity is the primary outcome (RQ1); a null result is publishable and pre-registered.

---

## 3. Slide-by-slide structure (target 14 slides ≈ 13 min speaking + 2 min Q&A)

Speaking pace assumption for non-native English presenter: **~125–135 words per minute** (slightly slower than native pace for clarity, no faster). Total spoken-word budget: ~1,650–1,750 words. Each slide below lists target seconds, the headline (large type on slide), the visual, and the script intent (NOT the verbatim script — the script is written next session).

| # | Slide title (large, English) | Target time | Visual | Script intent (single thought to convey) |
|---|---|---:|---|---|
| **1** | An Adaptive Learning Platform for University Programming Courses | 0:15 | Title + author + advisor + university crest; small footer: *"Implementation paper with pre-registered pilot."* | Greet, name, advisor, one-sentence pitch: *"a five-layer adaptive engine that personalises programming practice on every submission."* |
| **2** | The 30–40% problem | 1:00 | Single big number "30–40%" + Luxton-Reilly 2018 citation; small subtitle "Failure rate in CS1 — stable for decades" | Problem statement. Root cause is **not lack of practice material** — it is the mismatch between individualised skill acquisition and uniform delivery. Set up the gap. |
| **3** | The integration gap | 1:00 | Four logos / labels in a row: BKT, Elo, MAB, FSRS — each with one prior-work citation; arrow pointing to "?" or empty box on the right | Each technique is mature. Each has been studied **alone or in pairs**. **No one has integrated all four for programming.** This paper fills that gap. (Mention LeetCode / HackerRank / Codeforces briefly: huge libraries, **no closed loop**.) |
| **4** | Proposal: a five-layer adaptive engine on a shared knowledge graph | 1:00 | **Figure 1** (`ch3-system-architecture-diagram` — catbox `1j18y7.png`) | Walk the figure top-down: KG substrate → BKT (mastery) → Elo (difficulty) → MAB (selection) → FSRS (review) → optional LLM hints. **Every layer reads from and writes to the shared KG.** Set up the next four slides. |
| **5** | Layer 1 — Bayesian Knowledge Tracing (BKT) | 0:50 | One simplified BKT update equation + tiered priors table (5 rows × 4 cols, screenshot from `bkt_service.py:18-24`) | What it does: per-concept mastery posterior. **Two design choices to name:** (a) BKT not DKT — interpretability + cold-start; (b) **tiered priors by difficulty tier**, not a single textbook prior. Mastery threshold θ_m = 0.85. |
| **6** | Layer 2 — Dynamic Elo + ZPD filter | 0:55 | Dual-rating sketch (student rating curve + problem rating bar) + ZPD band δ ∈ [50, 250] illustrated on a number line | Dual ratings (student + problem). **Dynamic K** ∈ [10, 40] adjusts to the learner's recent trend — more reactive for new learners, more stable for converged ones. **ZPD filter**: Bjork's *desirable difficulty* operationalised as ~36–64% expected success. This filtered candidate pool feeds Layer 3. |
| **7** | Layer 3 — Hierarchical MAB with prerequisite gating *(Contribution C2)* | 1:15 | Two-level bandit diagram: outer arm (concept) → inner arm (problem); a small "❌" on three concepts whose prerequisites are not yet mastered + reward formula in clear notation | This is the second contribution. **Outer arm = concept**, **inner arm = problem**. Thompson Sampling on Beta(α, β) at both levels. **Prerequisite gate**: a concept becomes an arm **only when every prerequisite has mastery ≥ θ_m**. Inner level further filtered by Layer 2's ZPD. **Reward = 0.5·learning-gain + 0.3·correctness + 0.2·efficiency** — heuristic weighting, will be re-estimated from pilot traces. |
| **8** | Layer 4 — FSRS for programming retention *(Contribution C3)* | 1:30 | **Code snippet on slide** showing the 18-line `submission_to_fsrs_rating` function (clean monospace, large) + retrievability curve sketch | This is the third contribution and **the most original single idea in the paper**. FSRS was built for **flashcards** (4-level Likert: Again/Hard/Good/Easy). Programming gives a richer triple: correctness × attempts × time. **Show the mapping verbatim.** Then one sentence on retrievability: review fires when R drops below 0.9. *To my knowledge, the first time FSRS has been applied to programming.* |
| **9** | Layer 5 — Optional LLM Socratic hints | 0:30 | Single screenshot of [HintPanel.tsx](client/src/components/HintPanel.tsx) showing the three hint levels | Brief. RAG over student's BKT state. **Feature-flagged off during evaluation** to keep Layers 1–4 unconfounded. Provider-agnostic (any OpenAI-compatible endpoint). |
| **10** | The closed loop — what happens on every submission | 1:30 | **Figure 2** (`ch4-adaptive-engine-sequence` — catbox `vq16l2.png`) — sequence diagram | The single most important slide of the talk. Walk one concrete submission: student submits Python code on a *recursion* problem → sandbox runs (256 MB / 5 s / no network / unprivileged) → verdict triple emitted → **`asyncio.gather` fans out**: BKT updates posterior, Elo updates both ratings, FSRS rewrites next review date, MAB re-ranks the candidate pool — **all in parallel, all in well under 500 ms**. *The learner model is never stale.* |
| **11** | The artifact today | 1:00 | 2×2 screenshot collage: Knowledge Map, Review Queue, Recommendations card with reason tags, Instructor Dashboard. Side caption with key numbers (LOC, latency, problem count, sandbox limits). | Hard evidence the system is built and running: ~15k LOC, 28 concepts, 170 problems, <500 ms p95 recommendation latency at 100 concurrent users, e2e tests green, single-command Docker deployment, open-source release. *Every adaptive layer has a learner-facing surface.* |
| **12** | What is *not* in this paper — the pre-registered pilot | 0:50 | **Figure 3** (`ch5-experiment-timeline` — catbox `xaopkb.png`) | The artifact-vs-plan moment, owned head-on. Between-subjects, n = 40–60 Hanoi University undergraduates, 4 weeks of intervention + Week 8 retention follow-up, IRB-cleared, pre-registered. **RQ1 (primary)**: BKT and Elo predictive validity, target AUC ≥ 0.70. RQ2 / RQ3 are supporting. *Empirical results will be reported in a follow-up publication.* |
| **13** | Contributions, recapped | 0:45 | Numbered list, four bullets, one line each (mirrors the paper's contribution list) | C1 first integrated five-layer architecture / C2 prerequisite-constrained hierarchical bandit / C3 first application of FSRS to programming via the submission-to-rating mapping / C4 deployable open-source platform. Repeat the artifact-vs-plan caveat one last time, in one sentence. |
| **14** | Closing message + Q&A | 0:30 | Single sentence on the slide (large type), QR code to the open-source repo, contact email | Closing line, suitable for the conference-final slide: *"By integrating four adaptive techniques that have, until now, been studied in isolation, this work offers a working architectural step toward individualised programming education at scale. Thank you — questions?"* |

**Total speaking time:** ≈ 12 min 50 s. Slack: ≈ 2 min for slow English delivery, transitions, and Q&A. If the chair runs strict, slides 6 and 9 are the soft cuts.

---

## 4. English-delivery aids for the speaker

The plan must respect that the presenter is a Vietnamese-first-language CS undergraduate. Three concrete aids:

1. **Pronunciation cheat-sheet (one A4)** — words I expect to be tongue-twisters and need rehearsing: *Bayesian* (BAY-zee-an), *Vygotsky* (vih-GOT-skee), *retrievability*, *posterior*, *prerequisite-constrained*, *desirable difficulty*, *Socratic*, *retention*, *asynchronous*, *idiosyncratic*. Mark stresses on the speaker script.
2. **Anchor phrases** — short, well-rehearsed transition lines that buy thinking time and never need translation:
   - "*The next layer takes that output and ...*"
   - "*This is where the integration matters.*"
   - "*Let me show one concrete submission.*"
   - "*To be explicit about what is built versus what is planned ...*"
   - "*That is the third contribution of the paper.*"
3. **Number-and-symbol whiteboard list** — for any digits or Greek letters spoken aloud, the speaker says them slowly and on slide. Specifically rehearse: *"theta-m equals zero point eight five"*, *"delta in the range fifty to two hundred and fifty"*, *"AUC of zero point seven oh"*, *"two hundred and fifty-six megabytes"*. Numbers in English are the single biggest stumble point for Vietnamese speakers in CS talks.

---

## 5. Q&A preparation — questions to expect, one-line answers ready

Order roughly by likelihood. The speaker rehearses a 20–40-second answer to each.

| Q | Two-sentence ready answer |
|---|---|
| Why BKT and not Deep Knowledge Tracing? | BKT is interpretable, data-efficient, and produces a calibrated posterior the bandit can consume. DKT needs orders of magnitude more data than a one-semester university cohort can supply, and we would lose the prerequisite gating story. |
| How are the reward weights w₁ = 0.5, w₂ = 0.3, w₃ = 0.2 chosen? | They are a heuristic, not learned — the paper says so explicitly. Re-estimating them from pilot traces is named future work in §3.5. |
| Why a hand-authored knowledge graph? | Scope decision: 28 concepts is small enough to author manually in a few days and large enough to span a CS1 curriculum. Automated construction from syllabus / course documents is named future work in §3.2. |
| What if the pilot does not hit AUC ≥ 0.70? | A null result is the research finding. RQ1 is **predictive validity**, pre-registered; we report whatever we measure. The artifact stands independently. |
| Is the platform really single-language (Python only)? | The sandbox image is Python 3.12 today; the architecture is language-agnostic. Adding a JavaScript or C++ image is a Dockerfile change, not a redesign. |
| Have you compared against LeetCode or Codeforces? | The comparison is structural, not empirical: those platforms have static difficulty tags and **no closed loop** from learner outcome to problem selection. Our claim is the closed loop, not better problem volume. |
| What about cold-start? | Tiered BKT priors per difficulty tier (Layer 1) and dual Elo with K up to 40 (Layer 2) deliver fast initial calibration. ZPD filtering kicks in immediately because the problem ratings are seeded by tier. |
| Why is FSRS for programming non-trivial? | FSRS was built for flashcards (one-shot recall). Programming is procedural, multi-attempt, and time-bounded. The original work is the **mapping** from a code submission outcome to one of FSRS's four ratings. |
| What is the IRB / ethics situation? | The pilot has IRB review completed at Hanoi University; participation is voluntary, the control arm uses the same UI with non-adaptive recommendations, and learning material remains identical across arms. |
| Is the LLM layer (Layer 5) used in the evaluation? | No — feature-flagged off by default during the pilot to keep Layers 1–4 unconfounded. Full LLM evaluation is named medium-term future work. |

---

## 6. Production decisions to make before slides are built

These are the **decisions the user has to take** so the next session can execute without blocking. Put as questions for AskUserQuestion if the user wants to lock them now; otherwise the next session will assume the recommended default.

### 6.1 Slide format

- **Recommended:** Google Slides (matches the existing Google Docs publishing pipeline; works on conference-room laptops; renders catbox-hosted PNGs without conversion).
- **Alternative:** PowerPoint `.pptx` if the conference machine cannot reach the public internet.

### 6.2 Reusable visuals (already produced for the paper — no extra work)

All four are already PNG-ready under [documents/thesis-chapters/visuals/png/](documents/thesis-chapters/visuals/png/) and already on catbox:

| Slide | Visual | Catbox URL fragment | File |
|---|---|---|---|
| 4 | Five-layer system architecture | `1j18y7.png` | [ch3-system-architecture-diagram.png](documents/thesis-chapters/visuals/png/ch3-system-architecture-diagram.png) |
| 10 | Closed-loop submission sequence | `vq16l2.png` | [ch4-adaptive-engine-sequence.png](documents/thesis-chapters/visuals/png/ch4-adaptive-engine-sequence.png) |
| 12 | Eight-week pilot timeline | `xaopkb.png` | [ch5-experiment-timeline.png](documents/thesis-chapters/visuals/png/ch5-experiment-timeline.png) |
| (3, optional) | Technique-complementarity table | `8ulh9q.png` | [ch2-technique-complementarity-table.png](documents/thesis-chapters/visuals/png/ch2-technique-complementarity-table.png) |

The frontend screenshots for slides 9 and 11 still need to be captured — see §7.2.

### 6.3 Live demo or screenshots only?

**Recommendation: screenshots only.** Reasons: (a) 15-min slot is too tight; demo failure costs 60–90 s with no recovery; (b) frontend already has high-quality views; (c) screenshots are reproducible across conference rooms with no internet. If the user insists on live demo, budget a 90 s slot inserted between slides 10 and 11, and reduce slide 11 to 30 s — but this is a real risk and the plan does not assume it.

### 6.4 Backup if the conference projector is 4:3

Build the deck at 16:9 and export a 4:3 contingency PDF. Visuals already cropped to fit either ratio.

---

## 7. Verification — how we know the talk is conference-ready

Run before the conference, in this order:

1. **Self-rehearsal at speaking pace, with timer.** Target 13 min ± 30 s. If under 12 or over 14, reshape slides 6/7/8 first.
2. **Mirror-rehearsal of slides 7, 8, 10** with **screen-share off** — these are the technical slides; if the speaker cannot explain them with eyes off the slide, the slide is too dense or the script is unrehearsed.
3. **Cold-read by a non-CS English speaker** (a roommate or friend) of slides 1, 2, 3, 12, 14 — the framing slides. If they cannot restate the contribution after one read, revise the slide titles, not the script.
4. **Live deck dry-run on the conference-room laptop** (or the closest equivalent) to verify catbox PNGs load and fonts render.
5. **Q&A drill**: present slide 13 to a CS-literate friend who is told to ask three of the §5 questions cold. Speaker rehearses 30-second answers without rambling.
6. **Final lap**: read [paper-final.md §3.6](documents/conference-paper/paper-final.md) and [paper-final.md §4.2](documents/conference-paper/paper-final.md) the morning of — the two paragraphs most likely to be quoted back at the speaker in Q&A.

---

## 8. Critical files this plan will pull from when slides are built

- Paper body — [documents/conference-paper/paper-final.md](documents/conference-paper/paper-final.md)
- Outline + page budget — [documents/conference-paper/02-outline.md](documents/conference-paper/02-outline.md)
- Speaker biography / metadata in memory — `~/.claude/projects/.../memory/project_thesis_author_metadata.md`
- Layer 1 BKT — [ai-service/app/services/bkt_service.py](ai-service/app/services/bkt_service.py)
- Layer 2 Elo — [ai-service/app/services/elo_service.py](ai-service/app/services/elo_service.py)
- Layer 3 MAB — [ai-service/app/services/mab_service.py](ai-service/app/services/mab_service.py)
- Layer 4 FSRS — [ai-service/app/services/fsrs_service.py](ai-service/app/services/fsrs_service.py)
- Layer 5 LLM — [ai-service/app/services/llm_service.py](ai-service/app/services/llm_service.py)
- Closed-loop fan-out — [ai-service/app/services/adaptive_engine.py](ai-service/app/services/adaptive_engine.py)
- Knowledge-graph seed — [server/prisma/seed-adaptive.ts](server/prisma/seed-adaptive.ts)
- Sandbox config — [docker/sandbox/Dockerfile](docker/sandbox/Dockerfile), [docker/docker-compose.yml](docker/docker-compose.yml)
- Frontend screens for screenshots — [client/src/pages/KnowledgeMap.tsx](client/src/pages/KnowledgeMap.tsx), [client/src/pages/ReviewQueue.tsx](client/src/pages/ReviewQueue.tsx), [client/src/pages/Dashboard.tsx](client/src/pages/Dashboard.tsx), [client/src/components/HintPanel.tsx](client/src/components/HintPanel.tsx), [client/src/pages/InstructorDashboard.tsx](client/src/pages/InstructorDashboard.tsx)
- E2E pipeline test (Q&A backup) — [e2e/adaptive-pipeline.spec.ts](e2e/adaptive-pipeline.spec.ts)
- Reusable PNG visuals — [documents/thesis-chapters/visuals/png/](documents/thesis-chapters/visuals/png/)

---

## 9. Next session — what to execute from this plan

In execution order, with rough effort estimates:

1. **(30 min)** Capture five frontend screenshots from a running local instance: Knowledge Map (slide 4 inset or slide 11), Review Queue (slide 11), Dashboard recommendations card with reason tags (slide 11), Hint Panel (slide 9), Instructor Dashboard (slide 11 collage).
2. **(1.5 h)** Build the 14-slide deck in Google Slides with the exact titles, visuals, and time targets in §3. Use the bilingual title slide format from the conference template.
3. **(2 h)** Write the **verbatim speaker script**, slide-by-slide, with anchor phrases (§4.2) inserted as transitions and pronunciation marks (§4.1) on the hard words. Aim for 1,650–1,750 words total.
4. **(45 min)** Run the §7 self-rehearsal pass once and time-box-trim to ≤ 13:30.
5. **(45 min)** Q&A drill against §5.
6. **(30 min)** Final dry-run on the actual presentation hardware.

**Total estimated effort to a presentation-ready talk: ~6 hours**, comfortably split across two evenings.
