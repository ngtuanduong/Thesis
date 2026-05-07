# Conference Presentation — Verbatim Speaker Script (English)

**Talk:** *An Adaptive Learning Platform for University Programming Courses — Integrating BKT, Elo, MAB & FSRS*
**Duration:** ~11 min speaking + ~3–4 min Q&A in a 15-min slot
**Speaker:** Nguyễn Tuấn Dương (solo, non-native English)
**Pace assumption:** ~125–135 wpm — *slightly slower than native* for clarity

Legend used in this script:
- **Bold** = stress this word.
- *Italic* = optional aside; cut if running over time.
- `[ … ]` = stage direction or timing cue.
- `‹word›` = pronunciation note on the next line.

Pronunciation cheat-sheet (rehearse out loud once before the talk):
- **Bayesian** → BAY-zee-an
- **Vygotsky** → vih-GOT-skee
- **Pelánek** → PEL-ah-nek
- **retrievability** → ree-TREE-va-BIL-i-ty
- **posterior** → pos-TEER-ee-or
- **prerequisite-constrained** → PREE-rek-wi-zit con-STRAYND
- **asynchronous** → ay-SIN-kruh-nus
- **Socratic** → so-KRAT-ik

Anchor transitions (memorise three; you will need them when nervous):
1. *“This is where the integration matters.”*
2. *“Let me show one concrete submission.”*
3. *“To be explicit about what is built versus what is planned …”*

---

## Slide 1 — Title  `[0:15]`

> Good morning, everyone. My name is **Nguyễn Tuấn Dương**, from class 1C22, Faculty of Information Technology. My advisor is **Master Bùi Quốc Khánh**.
>
> Today I will present a **five-layer adaptive learning platform** that personalises programming practice on every code submission.
>
> One sentence up front: this is an **implementation paper** with a **pre-registered pilot evaluation protocol**. I will be very explicit about which parts are built and which parts are planned.

`[~70 words ≈ 30 s — but speak at ~50 wpm pace because this is your opening; pause after “Master Bùi Quốc Khánh” to let the audience read.]`

---

## Slide 2 — The 30–40% problem  `[1:00]`

> Introductory programming courses fail **between thirty and forty percent** of students worldwide. This is not a new problem. The systematic literature review by **Luxton-Reilly and colleagues, in 2018**, shows that this number has been stable for several decades.
>
> The interesting thing is **why**. It is **not** because students lack practice material. There are millions of programming problems online — on LeetCode, on HackerRank, on Codeforces.
>
> The gap is **structural**. Programming skill is acquired **individually**, through **practice**. But it is taught **uniformly**, at scale, in large lecture rooms.
>
> So the bottleneck is the mismatch — not the volume.

`[≈ 95 words ≈ 45 s. Pause for 2 seconds on the “30–40%”. Then keep moving.]`

---

## Slide 3 — The integration gap  `[0:50]`

> The literature already gives us **four mature techniques** for this kind of mismatch.
>
> **Bayesian Knowledge Tracing** — Corbett and Anderson, 1995 — estimates per-concept mastery.
>
> **Elo rating**, brought into education by **Pelánek** in 2016 — calibrates difficulty.
>
> **Multi-Armed Bandits**, with Thompson Sampling — balance exploration and exploitation.
>
> And **FSRS**, the Free Spaced Repetition Scheduler, 2022 — schedules reviews to fight forgetting.
>
> The problem is that these four have been studied **alone, or in pairs**. **No prior system** combines all four for **programming education**, under a single shared knowledge graph. *That gap is what this paper closes.*

`[≈ 105 words ≈ 50 s. Speak the four technique names slowly — they are the four pillars of the rest of the talk.]`

---

## Slide 4 — Five-layer architecture  `[0:45]`

> Here is the proposed architecture.
>
> The foundation is a **knowledge graph of 28 programming concepts**, with about **45 prerequisite edges**. Every layer above reads from, and writes to, this single graph.
>
> Above the graph: Layer 1 is **BKT** — per-concept mastery. Layer 2 is **dynamic Elo** — difficulty calibration. Layer 3 is the **hierarchical Multi-Armed Bandit** — picks the next concept and the next problem. Layer 4 is **FSRS** — review scheduling. Layer 5 is an **optional LLM** Socratic-hint module, off by default during evaluation.
>
> The next four slides walk through layers one to four.

`[≈ 90 words ≈ 45 s. Use the laser pointer. Walk the figure top-down so the audience’s eye follows yours.]`

---

## Slide 5 — Layer 1, BKT  `[0:40]`

> **Layer 1** is Bayesian Knowledge Tracing.
>
> It maintains, for **every learner**, for **every concept**, a posterior probability of mastery — the four classical parameters: prior, transition, guess, slip. A concept is mastered when the posterior crosses **theta-m equals zero point eight five**.
>
> One design choice deserves attention. We do **not** use a single textbook prior. We use **tiered priors** — five sets of parameters, one per difficulty tier. Foundational concepts start with a higher prior of mastery; advanced concepts start lower. This gives a calibrated cold-start across the curriculum.

`[≈ 90 words ≈ 40 s. If asked why BKT and not DKT — the answer is on the slide and in the Q&A bank.]`

---

## Slide 6 — Layer 2, Elo + ZPD  `[0:55]`

> **Layer 2** is Elo. We use **dual ratings** — every learner has a rating, and **every problem has a rating**. They evolve together.
>
> The K-factor — how aggressively we update the rating — is **dynamic**, between ten and forty. New or struggling learners get a larger K, so the system calibrates them quickly. Stable learners get a smaller K, so we don’t introduce noise.
>
> Then we apply a **Zone of Proximal Development filter**. We keep only problems whose Elo is between fifty and two hundred and fifty rating points **above** the learner. That corresponds to roughly **thirty-six to sixty-four percent** predicted success — *hard, but not too hard*. This is **Bjork’s desirable difficulty**, formalised.
>
> The output of this filter is the **candidate pool** that Layer 3 picks from.

`[≈ 135 words ≈ 60 s. Stress “dual” and “dynamic”. The ZPD numbers are an audience favourite — slow down on “thirty-six to sixty-four percent”.]`

---

## Slide 7 — Layer 3, Hierarchical MAB  `[1:00]`

> **Layer 3** is the bandit — a key technical innovation embedded inside the integrated platform.
>
> It is a **two-level Thompson Sampling** bandit. The **outer arm** chooses the next **concept**; the **inner arm** chooses the next **problem** inside that concept. Each arm carries a Beta posterior.
>
> Here is the key part. Arms are **gated**. A concept becomes an arm **only if every prerequisite has BKT mastery above theta-m**. So a learner cannot be recommended *recursion* until its prerequisites are mastered. The inner level is then filtered by Layer 2’s **ZPD band**.
>
> The **reward** is a scalar in zero to one — a weighted combination of BKT learning gain, correctness, and solve-time efficiency. The weights are **heuristic**; re-estimation from pilot traces is named future work.

`[≈ 130 words ≈ 60 s. The densest slide of the talk — practise the rhythm. Hand-mime the two-level structure if it helps.]`

---

## Slide 8 — Layer 4, FSRS  `[1:30]`

> **Layer 4** is — to my knowledge — the most original single idea inside the platform: the **first application of FSRS to programming retention**.
>
> FSRS was designed for **flashcards**. A flashcard gives one signal — recall, on a four-level scale: Again, Hard, Good, Easy. A code submission gives a much richer signal — **correctness, number of attempts, time spent**.
>
> The mapping you see on the right is how we bridge the two worlds.
>
> If the submission is **wrong**, the rating is **Again**.
> If it is correct on the **first attempt**, in under two minutes — **Easy**.
> Two to five minutes — **Good**. Over five minutes — **Hard**. More than one attempt — also **Hard**.
>
> Eighteen lines of Python. But this is what lets a scheduler designed for flashcard recall drive **review of a procedural skill** like programming. And the system reschedules the next review when retrievability drops below **zero point nine**.

`[≈ 175 words ≈ 80 s. The most quotable slide; deliver it slowly. Point at the code as you read each branch.]`

---

## Slide 9 — The closed loop  `[1:20]`

> **This is the most important slide of the talk.**
>
> *Let me show one concrete submission.*
>
> A learner submits a Python solution to a problem tagged with the concept *recursion*. The code runs in an **isolated Docker sandbox** — capped on memory, CPU time, with no network access.
>
> The sandbox emits a verdict — a triple of correctness, attempts, and time.
>
> This is where the integration matters. A single Python call — `asyncio dot gather` — fans out **four updates in parallel**.
>
> Layer 1 updates the BKT posterior for *recursion*.
> Layer 2 updates the learner’s Elo and the problem’s Elo.
> Layer 4 maps the verdict to an FSRS rating and rewrites the next review date.
> Layer 3 takes the new state and re-ranks the candidate pool.
>
> The cache is invalidated. The next request gets fresh state. **The learner model is never stale.**
>
> All of this completes well under five hundred milliseconds, at our target of one hundred concurrent users.

`[≈ 175 words ≈ 80 s. The technical heart. Walk the sequence diagram from left to right with the laser pointer.]`

---

## Slide 10 — The artifact today  `[0:50]`

> So let me show what is **actually built**.
>
> Four components — React on the frontend, NestJS as the API gateway, FastAPI for the adaptive engine, PostgreSQL with Redis as the data layer.
>
> About **fifteen thousand lines of code**, **twenty-eight concepts** in the knowledge graph, **one hundred and seventy curated problems**, **sub-five-hundred-millisecond** recommendation latency at the target load.
>
> End-to-end tests cover the full submit-to-recommend round-trip. Deployment is **one Docker Compose command**. The whole thing is open-source.

`[≈ 105 words ≈ 50 s. Read the numbers crisply — slow on the digits.]`

---

## Slide 11 — The pre-registered pilot  `[0:50]`

> *To be explicit about what is built versus what is planned* — here is the pilot.
>
> A **between-subjects** design, with a control group on a non-adaptive version of the same UI. Forty to sixty Hanoi University undergraduates. Four weeks of intervention, plus a Week-Eight retention follow-up. IRB review **completed**. The protocol is **pre-registered**.
>
> The **primary research question** — RQ1 — is **predictive validity**: do BKT and Elo predict post-intervention item correctness with **AUC at least zero point seven oh**? Acceptance rate, convergence speed, and learning gain are supporting indicators.
>
> Empirical results will be reported in a **follow-up publication**.

`[≈ 115 words ≈ 50 s. The most important risk-defusal moment. Slow, calm, no apology.]`

---

## Slide 12 — Contributions, recapped  `[0:40]`

> Two contributions.
>
> **C1** — the design and implementation of an **integrated five-layer adaptive platform** that unifies BKT, Elo, hierarchical MAB, and FSRS under a shared knowledge graph. The prerequisite-constrained bandit and the code-submission-to-FSRS-rating mapping are the **internal technical innovations** that make this integration work — not separate claims.
>
> **C2** — a **pre-registered pilot evaluation protocol** that specifies the classroom study in which the platform's learning effect will be measured.
>
> One last reminder. **C1** is **implemented and demonstrated**. **C2** is **specified, IRB-reviewed, and pre-registered, but not yet executed**.

`[≈ 95 words ≈ 40 s. Hold up two fingers when saying "Two contributions" — the audience anchor.]`

---

## Slide 13 — Closing + Q&A  `[0:30]`

> So — closing thought.
>
> *By integrating four adaptive techniques that have, until now, been studied in isolation, this work offers a working architectural step toward individualised programming education at scale.*
>
> Thank you.
>
> I would be happy to take questions.

`[≈ 50 words ≈ 25 s. Smile. Pause for 2 seconds before “Thank you”. Then look at the chair.]`

---

## Total words & time check

| Slide | Words | Cumul. seconds |
|---|---:|---:|
| 1 — Title | 70 | 30 |
| 2 — 30–40% | 95 | 75 |
| 3 — Integration gap | 105 | 125 |
| 4 — Five-layer | 90 | 170 |
| 5 — BKT | 90 | 210 |
| 6 — Elo + ZPD | 135 | 270 |
| 7 — MAB | 130 | 330 |
| 8 — FSRS | 175 | 410 |
| 9 — Closed loop | 175 | 490 |
| 10 — Artifact today | 105 | 540 |
| 11 — Pilot protocol | 115 | 590 |
| 12 — Contributions | 95 | 630 |
| 13 — Closing | 50 | 655 |
| **Total** | **~1,430** | **~11 min** |

→ ≈ 4 min of slack for transitions, slow English delivery, and Q&A in a 15-min slot.

**Cuts vs. previous version (~14:30 actual delivery):**
- Dropped Slide 9 (Layer 5 LLM hints) — already off during evaluation; mention stays on architecture slide.
- Trimmed asides on Slides 3, 4, 5, 7, 9 (closed loop), 10 (artifact).
- Re-numbered Slides 10–14 → 9–13.

---

## Q&A bank — quick recall (full versions in `04-presentation-plan.md` §5)

1. **Why BKT, not DKT?** — Cold-start, interpretable, calibrated posterior the bandit can consume.
2. **Reward weights chosen how?** — Heuristic; pilot traces will be used to re-estimate.
3. **Why hand-authored KG?** — Scope; auto-construction is future work.
4. **What if pilot misses AUC ≥ 0.70?** — That *is* the research finding. Pre-registered, null-result-safe.
5. **Single-language sandbox?** — Python today; adding JS/C++ is a Dockerfile change, not a redesign.
6. **vs LeetCode / Codeforces?** — Structural, not empirical: those have static tags, **no closed loop**.
7. **Cold start?** — Tiered BKT + dynamic Elo K up to 40 + ZPD seeded by tier.
8. **Why FSRS for programming is non-trivial?** — Flashcards are one-shot recall; programming is procedural — the mapping is the original work.
9. **IRB / ethics?** — IRB-cleared at Hanoi University; voluntary; control gets identical UI with non-adaptive recommendations.
10. **LLM in the evaluation?** — No, off by default; full evaluation is medium-term future work.

---

## Pre-talk checklist

- [ ] Run `python scripts/build-presentation.py` to regenerate the `.pptx` if anything in the script changed.
- [ ] Open `documents/conference-paper/05-presentation.pptx` and skim every slide once.
- [ ] Rehearse twice with a timer. Target ≤ 13:00.
- [ ] Q&A drill: ask a friend to throw any 3 questions from the bank, cold.
- [ ] Final lap (morning of): re-read paper-final.md §3.6 (FSRS mapping) and §4.2 (limitations).
- [ ] Bring slides on a USB stick **and** in a Google Drive backup.
