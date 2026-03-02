# Evaluation Plan — Experiment Design

**Thesis:** Adaptive Learning Platform for University Programming Courses

---

## 1. Research Questions

| ID | Research Question | Measurement | Type |
|----|------------------|-------------|------|
| RQ1 | How accurately can the multi-layer adaptive system model student knowledge and predict performance? | BKT prediction accuracy (AUC), Elo prediction accuracy (AUC), acceptance rate per difficulty band, Elo convergence speed | Primary |
| RQ2 | Does Hierarchical MAB problem selection improve learning outcomes compared to content-based filtering? | Normalized Learning Gain (NLG), problems-to-mastery ratio | Secondary |
| RQ3 | Does spaced repetition scheduling improve long-term retention of programming concepts? | Retention test score (Week 8), concept recall rate after 2-week gap | Secondary |
| RQ4 | How do students perceive the usability and usefulness of the adaptive platform? | SUS score, TAM scores, qualitative interview themes | Qualitative |

**Note:** Consolidated from 5 to 4 RQs. Original RQ1 (knowledge state modeling) and RQ2 (Elo difficulty calibration) merged into a single RQ1 because both measure the system's learner modeling accuracy via AUC-ROC. This ensures each RQ can be adequately answered within the available sample size and 4-week evaluation period. RQ numbering in subsequent sections reflects this consolidation.

---

## 2. Experiment Design

### 2.1 Design Type

**Between-subjects, pre-test / post-test with control group:**

```
                    Week 1          Weeks 2-5            Week 6
                    ┌──────┐       ┌────────────┐       ┌──────────┐
Experimental (E):   │Pre-  │──────▶│ Adaptive   │──────▶│Post-test │
                    │test  │       │ Platform   │       │+ Survey  │
                    └──────┘       └────────────┘       └──────────┘

                    ┌──────┐       ┌────────────┐       ┌──────────┐
Control (C):        │Pre-  │──────▶│ Non-adapt. │──────▶│Post-test │
                    │test  │       │ Platform   │       │+ Survey  │
                    └──────┘       └────────────┘       └──────────┘
```

**Experimental group (E):** Full adaptive platform — all 5 layers active (BKT + Elo + MAB + FSRS + LLM hints)

**Control group (C):** Same platform with adaptive layers disabled:
- Problems recommended by content-based filtering (current system)
- No knowledge tracing, no Elo calibration, no spaced repetition
- Same problems available, same code execution, same UI (minus adaptive indicators)

### 2.2 Participants

**Target:** 40–60 students from Hanoi University

**Inclusion criteria:**
- Enrolled in a programming course (introduction to programming, data structures, or algorithms)
- Ability to use a web-based platform
- Informed consent provided

**Exclusion criteria:**
- Students with prior competitive programming experience (Elo > 1600 equivalent)
- Students unable to commit to 4 weeks of platform use

**Sample size justification:**
- For a medium effect size (d = 0.5) with α = 0.05 and power = 0.80:
- Required n per group: ~26 (using G*Power for independent t-test)
- Target: 30 per group to account for dropout (~20% expected)
- Minimum viable: 20 per group

**Backup plan for smaller sample (20–30 total participants):**
If recruitment yields only 20–30 participants (10–15 per group):
- **Statistical power:** Can only detect large effects (d ≥ 0.8) with 80% power
- **Adjusted analysis:** Use non-parametric tests (Mann-Whitney U) which are more robust at small n
- **Supplementary evidence:** Compensate with stronger within-group analysis:
  - Detailed BKT/Elo convergence curves per student (rich individual trajectories)
  - Per-concept mastery progression showing adaptive system's behavior
  - System log analysis (recommendations accepted/rejected, session patterns)
- **Reframe contribution:** Shift emphasis from "statistically significant group difference" to "demonstration of integrated adaptive system with preliminary effectiveness evidence"
- **Qualitative strengthening:** Interview all participants (not just a sample) for richer thematic analysis

**Random assignment:**
- Stratified randomization by pre-test score (low/medium/high terciles)
- Ensures balanced baseline ability between groups

### 2.3 Ethical Considerations

- **Informed consent:** Written consent explaining purpose, data collection, right to withdraw
- **No academic penalty:** Participation is voluntary, non-participation does not affect course grades
- **Data anonymization:** Student IDs replaced with random identifiers in analysis
- **Equal access:** After experiment, control group gets access to adaptive features
- **Data retention:** Raw data stored for 2 years, then deleted
- **IRB/Ethics approval:** Submit to university ethics committee before recruitment

---

## 3. Protocol

### 3.1 Week 1: Baseline & Setup

| Day | Activity | Duration |
|-----|----------|----------|
| 1 | Information session + informed consent | 30 min |
| 2 | Pre-test administration | 60 min |
| 3 | System onboarding: account creation, tutorial | 30 min |
| 3 | Random assignment (stratified by pre-test score) | — |
| 4-5 | Practice period: students explore platform freely | — |

**Pre-test design:**
- 20 multiple-choice + short-answer questions
- Covers 5 difficulty levels (4 questions each)
- Topics: variables, control flow, functions, data structures, algorithms
- Time limit: 60 minutes
- Auto-graded (objective scoring)

### 3.2 Weeks 2–5: Intervention

| Aspect | Experimental Group | Control Group |
|--------|-------------------|---------------|
| Problem selection | Adaptive (MAB + Elo ZPD) | Content-based filtering |
| Difficulty matching | Dynamic Elo | Static labels (EASY/MEDIUM/HARD) |
| Review scheduling | FSRS-based spaced repetition | No scheduled reviews |
| Knowledge tracking | BKT per concept | None (skill embedding only) |
| Hints | LLM Socratic hints | No hints |
| Dashboard | Mastery visualization + Elo | Basic stats only |
| Available problems | Same set | Same set |
| Code execution | Identical sandbox | Identical sandbox |

**Minimum engagement requirement:** Students must attempt at least 3 problems per week to be included in analysis. Students below this threshold are flagged but not excluded (intent-to-treat analysis).

**Data collected during intervention:**
- All submission events (timestamp, code, result, time spent)
- All recommendation events (what was recommended, what was clicked)
- All page views and session durations
- BKT state snapshots (daily, for experimental group)
- Elo rating history (for experimental group)
- FSRS review events (for experimental group)
- Hint requests and responses (for experimental group)

### 3.3 Week 6: Post-Assessment

| Day | Activity | Duration |
|-----|----------|----------|
| 1 | Post-test administration | 60 min |
| 2 | SUS questionnaire | 10 min |
| 2 | TAM questionnaire | 10 min |
| 3 | Semi-structured interviews (10 students from each group) | 20 min each |
| 5 | Data export and anonymization | — |

**Post-test design:**
- Parallel form to pre-test: same topics, same difficulty distribution, different questions
- Ensures pre/post comparison is valid (no test-retest effect from identical questions)

### 3.4 Week 8 Retention Test (Committed)

This test is **committed, not optional**. FSRS evaluation (RQ3) requires retention data — without it, we can only claim short-term learning improvement, not long-term retention.

- Administered **2 weeks** after the intervention ends (Week 8)
- 10-question retention test (subset of post-test topics)
- Tests whether FSRS spaced repetition leads to better long-term retention
- Only concepts that were "mastered" during intervention are tested
- **Critical for RQ3:** 4-week intervention is already short for spaced repetition evaluation. FSRS stability values typically need several weeks to diverge between conditions. The Week 8 retention test provides the minimum viable window to detect FSRS effects.
- **Logistics:** Communicate to participants during onboarding that a brief follow-up assessment is part of the study. Schedule reminders 3 days and 1 day before the retention test.

---

## 4. Evaluation Metrics

### 4.1 Learning Effectiveness Metrics

#### Normalized Learning Gain (NLG) — Primary Metric

```
NLG = (post_score - pre_score) / (max_score - pre_score)
```

**Interpretation:**
- NLG > 0: Student improved
- NLG = 0: No change
- NLG < 0: Student regressed (rare)
- NLG > 0.3: Medium gain (Hake, 1998)
- NLG > 0.7: High gain

**Why NLG:** Normalizes for different starting points — a student who scores 90% on the pre-test has less room to improve than one who scores 30%.

#### Problems-to-Mastery Ratio

```
PTM = number_of_problems_attempted / number_of_concepts_mastered
```

Lower PTM = more efficient learning (fewer problems needed to master each concept). This metric directly evaluates the quality of problem selection.

#### Concept Mastery Progression

For the experimental group, plot BKT P(mastery) over time for each concept. This shows:
- How quickly concepts are mastered
- Whether mastery is sustained (or regresses)
- Which concepts are hardest to master

#### Time to First Mastery

```
TFM(concept) = time from first attempt to P(mastery) ≥ 0.85
```

Shorter TFM = more efficient adaptive system.

### 4.2 Recommendation Quality Metrics

#### Acceptance Rate

```
Acceptance Rate = recommended_problems_attempted / total_recommendations_shown
```

High acceptance rate indicates recommendations are perceived as relevant and appropriately difficult.

#### Completion Rate

```
Completion Rate = recommended_problems_solved / recommended_problems_attempted
```

Target: 60–80%. Too high (>90%) suggests problems are too easy; too low (<40%) suggests too hard.

#### BKT Prediction Accuracy

```
AUC-ROC of P(correct) predictions vs actual outcomes
```

Target: AUC > 0.65 (moderate predictive power). This validates Layer 1.

#### Elo Prediction Accuracy

```
AUC-ROC of Elo-based expected score vs actual outcomes
```

Target: AUC > 0.65. This validates Layer 2.

#### Elo Convergence Speed

```
Number of submissions until rating standard deviation < threshold
```

Measures how quickly Elo ratings stabilize for both students and problems.

### 4.3 Engagement Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| Session frequency | Sessions per week per student | ≥ 3 sessions/week |
| Session duration | Average time per session (minutes) | 20–40 min |
| Problems per session | Average problems attempted per session | ≥ 3 problems |
| Voluntary return rate | % of students who use platform without being reminded | > 60% |
| Dropout rate | % of students who stop using platform before Week 5 | < 20% |
| Abandonment rate | % of started problems that are abandoned (no submission after viewing) | < 30% |

### 4.4 Usability Metrics

#### System Usability Scale (SUS)

Standard 10-item questionnaire (Brooke, 1996). Score range: 0–100.

| Score | Adjective Rating | Acceptability |
|-------|-----------------|---------------|
| < 50 | Not acceptable | Needs major redesign |
| 50–70 | Marginal | Usable but needs improvement |
| 70–85 | Good | Acceptable |
| > 85 | Excellent | Best-in-class |

**Target: SUS ≥ 70**

#### Technology Acceptance Model (TAM)

Measures two constructs (Davis, 1989):

**Perceived Usefulness (PU):** 6 items, 7-point Likert scale
- "The adaptive recommendations helped me learn programming more effectively"
- "The system's difficulty matching was appropriate for my skill level"
- "The review reminders helped me retain what I learned"
- "The progress visualization motivated me to keep learning"
- "The system saved me time compared to finding problems manually"
- "Overall, the adaptive features improved my learning experience"

**Perceived Ease of Use (PEOU):** 6 items, 7-point Likert scale
- "I found the recommendation system easy to understand"
- "The difficulty indicators were clear and helpful"
- "The review queue was easy to navigate"
- "The knowledge visualization was easy to interpret"
- "The hint system was easy to use"
- "Overall, the system was easy to use"

**Target: Mean PU ≥ 5.0, Mean PEOU ≥ 5.0 (on 7-point scale)**

---

## 5. Statistical Analysis Plan

### 5.1 Primary Analysis: Learning Gain

**Hypothesis:** H₁: NLG_experimental > NLG_control

**Test:** Independent samples t-test (if normality holds) or Mann-Whitney U test (if not)

```
1. Check normality: Shapiro-Wilk test on NLG for each group
2. Check homogeneity of variance: Levene's test
3. If both met: Independent t-test
   If normality violated: Mann-Whitney U
   If variance unequal: Welch's t-test
4. Report: test statistic, p-value, 95% CI, Cohen's d
```

**Effect size interpretation (Cohen's d):**
| d | Interpretation |
|---|---------------|
| 0.2 | Small |
| 0.5 | Medium |
| 0.8 | Large |

### 5.2 Secondary Analyses

#### Per-Concept Learning Gain
- Repeated measures: NLG per concept (comparing E vs C)
- Mixed ANOVA: group (between) × concept (within) × time (within)

#### Engagement Comparison
- Mann-Whitney U tests for session frequency, duration, problems per session
- Chi-square test for dropout rate comparison

#### Prediction Accuracy
- AUC-ROC computed from within-group predictions (experimental only)
- Bootstrapped 95% CI for AUC

#### Survey Analysis
- SUS: compute composite score per participant, report mean ± SD
- TAM: compute PU and PEOU subscale means, Cronbach's α for internal consistency
- Compare E vs C on SUS using t-test

### 5.3 Effect Size Reporting

All comparisons report effect sizes:
- **Continuous outcomes:** Cohen's d (or Hedge's g for small samples)
- **Binary outcomes:** Odds ratio
- **Correlation:** Pearson's r or Spearman's ρ

### 5.4 Multiple Comparisons

With 5 research questions and multiple metrics, apply:
- **Bonferroni correction** for the 4 primary comparisons (α' = 0.05/4 = 0.0125)
- Secondary/exploratory analyses reported without correction but flagged as exploratory

### 5.5 Missing Data

- **Intent-to-treat (ITT):** Primary analysis includes all randomized participants
- **Per-protocol (PP):** Sensitivity analysis includes only participants meeting minimum engagement (≥3 problems/week)
- Missing post-test scores: multiple imputation (if < 20% missing) or listwise deletion

---

## 6. Qualitative Analysis

### 6.1 Semi-Structured Interviews

**Sample:** 10 students from each group (20 total), stratified by NLG (high/medium/low gainers)

**Interview guide:**

1. "Describe your experience using the platform over the past 4 weeks."
2. "How did you typically decide which problem to work on next?"
   - (For E): "How did the recommendations influence your choices?"
   - (For C): "Would it have been helpful to get personalized recommendations?"
3. "Were there times when you felt the problems were too easy or too hard?"
4. "Did you feel you were making progress? How could you tell?"
5. (For E): "What did you think of the concept mastery visualization?"
6. (For E): "Did the review reminders change how you studied?"
7. "What would you change about the system?"
8. "Would you continue using this platform if it were available?"

**Analysis:** Thematic analysis (Braun & Clarke, 2006):
1. Familiarization with transcripts
2. Initial coding
3. Generating themes
4. Reviewing and refining themes
5. Reporting

---

## 7. Data Collection Infrastructure

### 7.1 Logging Requirements

All events logged with timestamp, student_id (anonymized), and session_id:

```json
// Submission event
{
  "event": "submission",
  "timestamp": "2026-04-15T14:32:00Z",
  "student_id": "S042",
  "problem_id": 15,
  "concept_id": 7,
  "is_correct": true,
  "attempt_number": 2,
  "time_spent_seconds": 185,
  "code_length": 342,
  "group": "experimental"
}

// Recommendation event
{
  "event": "recommendation_shown",
  "timestamp": "2026-04-15T14:30:00Z",
  "student_id": "S042",
  "recommendations": [42, 15, 23, 8, 31],
  "reasons": ["REVIEW", "PRACTICE", "NEW", "NEW", "PRACTICE"]
}

// Recommendation click event
{
  "event": "recommendation_clicked",
  "timestamp": "2026-04-15T14:31:00Z",
  "student_id": "S042",
  "problem_id": 15,
  "position": 1  // 0-indexed position in list
}

// Page view event
{
  "event": "page_view",
  "timestamp": "2026-04-15T14:29:00Z",
  "student_id": "S042",
  "page": "dashboard",
  "session_duration_seconds": 1200
}
```

### 7.2 Data Export

After experiment completion:
1. Export all event logs as JSON/CSV
2. Export BKT states (daily snapshots)
3. Export Elo rating histories
4. Export FSRS card states
5. Export pre-test and post-test scores
6. Export survey responses
7. Anonymize all exports (replace student_id with random codes)

---

## 8. Expected Outcomes

Based on literature benchmarks:

| Metric | Expected Experimental | Expected Control | Source |
|--------|----------------------|-----------------|--------|
| NLG | 0.35–0.50 | 0.15–0.25 | Ritter et al., 2007 (Cognitive Tutor: +0.2 NLG advantage) |
| SUS | ≥ 70 | ≥ 60 | Industry average ~68 |
| Acceptance rate | 70–85% | 40–60% | Adaptive systems show ~20% higher engagement |
| Completion rate | 60–75% | 50–65% | ZPD matching improves completion |
| BKT AUC | ≥ 0.65 | N/A | Corbett & Anderson, 1994: AUC ~0.7 |
| Elo AUC | ≥ 0.65 | N/A | Pelánek, 2016: AUC ~0.7 |

### 8.1 What Constitutes a "Successful" Thesis

**Minimum for thesis acceptance:**
- Working system with at least Layers 1–3 (BKT + Elo + MAB)
- Measurable NLG advantage of experimental over control (any positive difference with p < 0.05)
- SUS ≥ 60

**Target for strong thesis:**
- All 5 layers working
- NLG advantage with medium effect size (d ≥ 0.5)
- SUS ≥ 70
- BKT/Elo AUC ≥ 0.65
- Positive qualitative feedback themes

**Target for excellent thesis (publication potential):**
- Above + novel contribution clearly demonstrated
- NLG advantage with large effect size (d ≥ 0.8)
- Ablation study showing contribution of each layer
- Submitted to EDM, LAK, or AIED conference

---

## 9. Ablation Study Design — Within-System Approach

**Important clarification:** The ablation study uses **within-system programmatic layer disabling**, NOT separate participant groups. This is feasible with any sample size because it analyzes the same system's behavior under different configurations, using logged data rather than requiring additional participants.

### 9.1 Approach: Feature Flag Ablation

Using the feature flags defined in the implementation (see 05-IMPLEMENTATION-PLAN.md):

```python
ENABLE_BKT = os.getenv('ENABLE_BKT', 'true') == 'true'
ENABLE_ELO = os.getenv('ENABLE_ELO', 'true') == 'true'
ENABLE_MAB = os.getenv('ENABLE_MAB', 'true') == 'true'
ENABLE_FSRS = os.getenv('ENABLE_FSRS', 'true') == 'true'
```

**Method:** After the main experiment completes, **replay** the experimental group's interaction logs through the adaptive engine with different layer configurations disabled. Compare the *recommendations that would have been generated* under each ablation condition.

### 9.2 Ablation Conditions

| Condition | BKT | Elo | MAB | FSRS | What Changes |
|-----------|:---:|:---:|:---:|:----:|-------------|
| Full adaptive | ✓ | ✓ | ✓ | ✓ | Baseline (actual system) |
| No FSRS | ✓ | ✓ | ✓ | ✗ | No review scheduling — MAB explores freely |
| No MAB (random select) | ✓ | ✓ | ✗ | ✓ | Random problem selection within ZPD |
| No Elo (static difficulty) | ✓ | ✗ | ✓ | ✓ | No ZPD filtering — MAB selects from all problems |
| No BKT (no mastery tracking) | ✗ | ✓ | ✓ | ✓ | No prerequisite gating — all concepts eligible |

### 9.3 Metrics for Ablation

Since we can't measure actual learning gain under counterfactual conditions, we evaluate:
- **Recommendation divergence:** How different are recommendations under ablation vs full system?
- **Predicted correctness calibration:** Using the logged actual outcomes, compute AUC of predictions under each configuration
- **Prerequisite violation rate:** How often does the ablated system recommend problems with unmet prerequisites?
- **Difficulty mismatch rate:** How often are recommended problems outside the optimal difficulty range?

This approach is **not a substitute** for a true between-subjects ablation, but it provides compelling evidence for each layer's contribution without additional participants.

---

## 10. Timeline

| Week | Activity |
|------|----------|
| Week 1 | Ethics submission, instrument preparation, pre-test design |
| Week 2 | Participant recruitment, system deployment |
| Week 3 | Information session, pre-test, system onboarding |
| Weeks 4–7 | Intervention period (4 weeks) |
| Week 8 | Post-test, surveys, interviews |
| Week 9 | Data export, cleaning, anonymization |
| Week 10 | **Retention test** (2 weeks after intervention — committed, not optional) |
| Weeks 10–12 | Statistical analysis + writing |
