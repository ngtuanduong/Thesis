# Presentation Cheat Sheet — Key Talking Points

**Talk:** *An Adaptive Learning Platform for University Programming Courses — Integrating BKT, Elo, MAB & FSRS*
**Slot:** 15 min · Speaking ≈ 11 min · Q&A ≈ 3–4 min · 13 slides
**Style:** Glance only when nervous. Each slide = 3–5 anchors, one stress point, one transition.

---

## Slide 1 — Title  `[0:30]`

- Greet: name → **Nguyễn Tuấn Dương**, class **1C22**, Faculty of IT.
- Advisor: **M.Sc. Bùi Quốc Khánh**.
- One-line pitch: *"a five-layer adaptive platform that personalises programming practice on every code submission."*
- Frame upfront: **implementation paper + pre-registered pilot protocol**.

> Pause 2s after advisor's name. Don't rush.

---

## Slide 2 — The 30–40% problem  `[0:45]`

- **30–40%** failure in CS1. *Stable for decades* (Luxton-Reilly 2018).
- **Not** lack of practice — millions of problems online (LeetCode, HackerRank, Codeforces).
- Root cause is **structural**: skill is acquired *individually*, taught *uniformly*.
- → bottleneck is the **mismatch**, not the volume.

> Stress "30–40%". Pause 2s.

---

## Slide 3 — The integration gap  `[0:50]`

Four mature techniques:
- **BKT** (Corbett & Anderson 1995) — per-concept mastery.
- **Elo** (Pelánek 2016) — difficulty calibration.
- **MAB / Thompson Sampling** — explore vs. exploit.
- **FSRS** (Ye et al. 2022) — spaced reviews.

- Each studied **alone or in pairs**. **Nobody** has composed all four for **programming education** under a shared knowledge graph.
- *That gap is what this paper closes.*

> Slow on the four names — they're the four pillars of the rest of the talk.

---

## Slide 4 — Five-layer architecture  `[0:45]`

- Foundation: **knowledge graph** of **28 concepts**, **~45 prerequisite edges**.
- L1 BKT — mastery posterior.
- L2 dynamic Elo — difficulty calibration.
- L3 hierarchical MAB — picks next concept and next problem.
- L4 FSRS — review scheduling.
- L5 LLM Socratic hints — **off by default during evaluation**.

> Use laser pointer top-down. Mention L5 quickly, then move on.

---

## Slide 5 — Layer 1, BKT  `[0:40]`

- Per-learner, per-concept posterior — 4 classical params (prior, transition, guess, slip).
- Mastered when posterior crosses **θₘ = 0.85**.
- **Tiered priors** — 5 sets, one per difficulty tier → calibrated cold-start across the curriculum.

> Anticipate "Why BKT not DKT?" — answer is on the slide; defer to Q&A if asked.

---

## Slide 6 — Layer 2, Elo + ZPD  `[1:00]`

- **Dual ratings** — every learner rated, every problem rated.
- **Dynamic K ∈ [10, 40]** — bigger K when struggling, smaller when steady.
- **ZPD filter δ ∈ [50, 250]** rating points → ≈ **36–64% predicted success** ("hard, but not too hard" — Bjork's desirable difficulty).
- Output: candidate pool that L3 picks from.

> Stress "dual" and "dynamic". Slow on the **36–64%** number.

---

## Slide 7 — Layer 3, Hierarchical MAB  `[1:00]`

- **Two-level Thompson Sampling** — outer arm = concept, inner arm = problem.
- Each arm: **Beta(α, β)** posterior.
- **Prerequisite gate** — concept becomes an arm *only if every prerequisite has BKT mastery ≥ θₘ*. Inner level filtered by ZPD.
- Reward ∈ [0, 1] = weighted combo of BKT learning gain + correctness + solve-time efficiency. Weights are **heuristic** — re-estimation from pilot traces is named future work.

> Densest slide. Hand-mime the two-level structure if helpful.

---

## Slide 8 — Layer 4, FSRS  `[1:20]`

- **Most original single idea** — first application of **FSRS to programming retention**.
- FSRS designed for flashcards (single signal, 4-level recall: Again/Hard/Good/Easy).
- Code submission has **richer signal** — correctness + attempts + time.
- Mapping (right side):
  - wrong → **Again**
  - correct, 1st attempt, < 2 min → **Easy**
  - 2–5 min → **Good**; > 5 min → **Hard**; > 1 attempt → **Hard**
- Review fires when **retrievability R(t) < 0.9**.

> Quotable slide. Deliver slowly. Point at code as you read each branch.

---

## Slide 9 — The closed loop  `[1:20]`

- **Most important slide of the talk.**
- One concrete submission — Python solution, problem tagged *recursion*.
- Sandboxed run → verdict triple **(correctness, attempts, time)**.
- Single `asyncio.gather(...)` → **4 parallel updates**:
  - L1 updates BKT posterior for *recursion*
  - L2 updates learner's & problem's Elo
  - L4 maps verdict → FSRS rating, rewrites due date
  - L3 takes new state, re-ranks candidate pool
- Cache invalidated → next request gets fresh state. **Learner model never stale.**
- All under **500 ms** at **100 concurrent users**.

> Walk the sequence diagram left → right with laser pointer.

---

## Slide 10 — The artifact today  `[0:50]`

What's actually built:
- 4 components: **React** + **NestJS** + **FastAPI** + **PostgreSQL/Redis**.
- ~**15k LOC**, **28 concepts**, **170 problems**, **< 500 ms** p95 recommendation latency.
- E2E tests cover full submit-to-recommend round-trip.
- **One Docker Compose command** to deploy. Open-source.

> Read the numbers crisply. Slow on the digits.

---

## Slide 11 — The pre-registered pilot  `[0:50]`

- **Between-subjects**, control = same UI on non-adaptive recs.
- **n = 40–60** Hanoi University undergrads.
- **4-week intervention** + **Week-8 retention** follow-up.
- IRB **completed**. Protocol **pre-registered**.
- **Primary RQ1** = predictive validity → **AUC ≥ 0.70** for BKT/Elo on post-intervention items.
- Acceptance rate, convergence speed, learning gain = supporting indicators.
- Empirical results → **follow-up publication**.

> Most important risk-defusal moment. Slow, calm, no apology.

---

## Slide 12 — Contributions, recapped  `[0:40]`

**Two contributions:**

- **C1** — **Integrated five-layer adaptive platform** (BKT + Elo + MAB + FSRS unified by KG of 28 concepts). The **prerequisite-bandit** and **submission-to-FSRS-rating mapping** are *internal technical innovations*, not separate claims.
- **C2** — **Pre-registered pilot evaluation protocol**.

Closing reminder:
- **C1** = **implemented and demonstrated**.
- **C2** = **specified, IRB-reviewed, pre-registered, but not yet executed**.

> Hold up two fingers when saying "Two contributions" — audience anchor.

---

## Slide 13 — Closing + Q&A  `[0:30]`

- *"By integrating four adaptive techniques that have, until now, been studied in isolation, this work offers a working architectural step toward individualised programming education at scale."*
- Thank you.
- Look at the chair, take questions.

> Smile. Pause 2s before "Thank you".

---

## Q&A — quick recall (10 expected)

| # | Question | Anchor answer |
|---|---|---|
| 1 | Why BKT, not DKT? | Cold-start, interpretable, calibrated posterior the bandit can consume. |
| 2 | Reward weights chosen how? | Heuristic; pilot traces will re-estimate. |
| 3 | Why hand-authored KG? | Scope; auto-construction = future work. |
| 4 | What if pilot misses AUC ≥ 0.70? | That *is* the research finding. Pre-registered, null-result-safe. |
| 5 | Single-language sandbox? | Python today; JS/C++ = Dockerfile change, not redesign. |
| 6 | vs LeetCode / Codeforces? | Structural, not empirical: those have static tags, **no closed loop**. |
| 7 | Cold start? | Tiered BKT + dynamic Elo K up to 40 + ZPD seeded by tier. |
| 8 | Why FSRS for programming is non-trivial? | Flashcards = one-shot recall; programming = procedural — the mapping is the original work. |
| 9 | IRB / ethics? | IRB-cleared at Hanoi University; voluntary; control gets identical UI with non-adaptive recs. |
| 10 | LLM in the evaluation? | No, off by default; full LLM evaluation = medium-term future work. |

---

## Pronunciation cheat-sheet (quick glance)

- **Bayesian** → BAY-zee-an
- **Vygotsky** → vih-GOT-skee
- **Pelánek** → PEL-ah-nek
- **retrievability** → ree-TREE-va-BIL-i-ty
- **posterior** → pos-TEER-ee-or
- **Socratic** → so-KRAT-ik
- **asynchronous** → ay-SIN-kruh-nus

---

## Anchor transitions (memorise these)

1. *"This is where the integration matters."* → Slide 9 transition.
2. *"Let me show one concrete submission."* → Slide 9 opening.
3. *"To be explicit about what is built versus what is planned …"* → Slide 11 transition.

---

## Pre-talk checklist

- [ ] Re-read this file once + Slide 9/Slide 11 in detail.
- [ ] Open `05-presentation.pptx`, skim every slide.
- [ ] Time a full run-through. Target ≤ 11:30.
- [ ] Q&A drill: friend throws 3 cold questions.
- [ ] Slides on USB **and** Google Drive backup.
