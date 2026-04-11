# Algorithm Design — Deep Dive

**Thesis:** Adaptive Learning Platform for University Programming Courses
**Purpose:** Mathematical formulations, pseudocode, and design rationale for each adaptive layer

---

## 1. Layer 1: Bayesian Knowledge Tracing (BKT)

### 1.1 Mathematical Model

BKT models each (student, concept) pair as a Hidden Markov Model with two hidden states:
- **L** (Learned): student has mastered the concept
- **¬L** (Not Learned): student has not mastered the concept

**Four parameters (per concept):**

| Symbol | Parameter | Meaning | Range |
|--------|-----------|---------|-------|
| P(L₀) | Prior knowledge | Probability that student knew the concept before any practice | [0, 0.5] |
| P(T) | Learn rate | Probability of transitioning from ¬L to L after one practice | [0.01, 0.5] |
| P(G) | Guess rate | Probability of correct answer when concept is NOT known | [0, 0.3] |
| P(S) | Slip rate | Probability of incorrect answer when concept IS known | [0, 0.2] |

**State transition diagram:**

```
                P(T)
    ┌────────────────────────┐
    │                        ▼
 ┌──┴───┐    1-P(T)    ┌────────┐
 │  ¬L  │─────────────▶│   ¬L   │
 └───┬───┘              └────┬───┘
     │                       │
     │ P(G)          1-P(G)  │
     ▼                       ▼
  Correct              Incorrect

 ┌───────┐    1        ┌────────┐
 │   L   │────────────▶│   L    │   (no forgetting in basic BKT)
 └───┬───┘              └────┬───┘
     │                       │
     │ 1-P(S)          P(S)  │
     ▼                       ▼
  Correct              Incorrect
```

### 1.2 Update Equations

Given the current mastery probability P(L_t) and an observed response:

**Step 1: Posterior update (given observation)**

After a **correct** response:
```
P(L_t | correct) = P(L_t) × (1 - P(S)) / P(correct)

where:
P(correct) = P(L_t) × (1 - P(S)) + (1 - P(L_t)) × P(G)
```

After an **incorrect** response:
```
P(L_t | incorrect) = P(L_t) × P(S) / P(incorrect)

where:
P(incorrect) = P(L_t) × P(S) + (1 - P(L_t)) × (1 - P(G))
```

**Step 2: Learning transition**
```
P(L_{t+1}) = P(L_t | obs) + (1 - P(L_t | obs)) × P(T)
```

This accounts for the possibility that even if the student didn't know the concept before, practicing it may have caused learning.

### 1.3 Pseudocode

```python
def bkt_update(p_mastery: float, is_correct: bool, params: BKTParams) -> float:
    """
    Update mastery probability after a single observation.

    Args:
        p_mastery: Current P(L_t) before this observation
        is_correct: Whether the student answered correctly
        params: BKT parameters (p_l0, p_transit, p_guess, p_slip)

    Returns:
        Updated P(L_{t+1}) after this observation
    """
    p_l = p_mastery
    p_t = params.p_transit
    p_g = params.p_guess
    p_s = params.p_slip

    if is_correct:
        # Posterior: P(L | correct)
        p_correct = p_l * (1 - p_s) + (1 - p_l) * p_g
        p_l_given_obs = (p_l * (1 - p_s)) / p_correct
    else:
        # Posterior: P(L | incorrect)
        p_incorrect = p_l * p_s + (1 - p_l) * (1 - p_g)
        p_l_given_obs = (p_l * p_s) / p_incorrect

    # Apply learning transition
    p_l_new = p_l_given_obs + (1 - p_l_given_obs) * p_t

    return p_l_new


def predict_correctness(p_mastery: float, params: BKTParams) -> float:
    """
    Predict probability of correct response.
    Used for AUC evaluation.
    """
    return p_mastery * (1 - params.p_slip) + (1 - p_mastery) * params.p_guess
```

### 1.4 Parameter Initialization and Fitting

**Default parameters (before sufficient data):**

| Concept Type | P(L₀) | P(T) | P(G) | P(S) |
|-------------|--------|-------|-------|-------|
| Basic (variables, I/O) | 0.2 | 0.3 | 0.2 | 0.1 |
| Intermediate (loops, functions) | 0.1 | 0.2 | 0.15 | 0.1 |
| Advanced (DP, graphs) | 0.05 | 0.15 | 0.1 | 0.1 |

**Parameter fitting (when sufficient data accumulates):**

Use Expectation-Maximization (EM) via `pyBKT`:
```python
from pyBKT.models import Model

model = Model()
model.fit(data={
    'order_id': attempt_order,
    'skill_name': concept_names,
    'correct': correctness_labels,
    'user_id': student_ids
})

# Extract fitted parameters per concept
for concept in concepts:
    params = model.params()
    # params contains fitted P(L₀), P(T), P(G), P(S)
```

Refit parameters periodically (e.g., weekly) as more data accumulates.

### 1.5 Multi-Concept Extension

When a problem maps to multiple concepts, we update BKT for each concept with **weighted contribution:**

```python
def update_multi_concept(student_id, problem_id, is_correct, concept_mappings):
    """
    concept_mappings: [(concept_id, is_primary)] from problem_concept table
    """
    for concept_id, is_primary in concept_mappings:
        state = get_knowledge_state(student_id, concept_id)

        # Primary concept gets full update
        # Secondary concepts get attenuated update
        if is_primary:
            state.p_mastery = bkt_update(state.p_mastery, is_correct, state.params)
        else:
            # Attenuated: only update if correct (don't penalize for secondary)
            if is_correct:
                state.p_mastery = bkt_update(state.p_mastery, True, state.params)
            # If incorrect, don't update secondary concepts
            # (failure might be due to primary concept, not secondary)

        save_knowledge_state(state)
```

---

## 2. Layer 2: Dynamic K-Value Elo

### 2.1 Standard Elo Formulation

**Expected score (probability of student solving the problem):**

```
E(student, problem) = 1 / (1 + 10^((R_problem - R_student) / 400))
```

**Rating update:**

```
R'_student = R_student + K_student × (S - E)
R'_problem = R_problem + K_problem × (E - S)
```

Where S = 1 if correct, S = 0 if incorrect.

Note: Student and problem ratings move in **opposite directions** — if a student solves a problem, the student's rating goes up and the problem's rating goes down (it was easier than its rating suggested).

### 2.2 Dynamic K-Value Calculation

The K-factor controls update sensitivity. Dynamic K adapts based on learning trend:

```python
def compute_dynamic_k(history: list[dict], k_min=10, k_max=40,
                       lam=2.0, window=10) -> float:
    """
    Compute dynamic K-value based on recent performance trend.

    Args:
        history: Recent submissions [{is_correct, expected_score, timestamp}]
        k_min: Minimum K-factor (for stable students)
        k_max: Maximum K-factor (for students needing re-calibration)
        lam: Decay parameter for trend sensitivity
        window: Number of recent submissions to consider

    Returns:
        Adapted K-value
    """
    if len(history) < 3:
        return k_max  # New students get high K for fast initial calibration

    recent = history[-window:]

    # Compute weighted trend: sum of (actual - expected) with recency weighting
    trend = 0.0
    total_weight = 0.0
    for i, h in enumerate(recent):
        weight = 0.9 ** (len(recent) - 1 - i)  # exponential recency
        residual = (1.0 if h['is_correct'] else 0.0) - h['expected_score']
        trend += weight * residual
        total_weight += weight

    trend = trend / total_weight  # normalize to [-1, 1]

    if trend > 0:
        # Student is improving → lower K (stable, smaller updates)
        k = k_min + (k_max - k_min) * math.exp(-lam * trend)
    else:
        # Student is struggling → higher K (needs faster re-calibration)
        k = k_min + (k_max - k_min) * (1 - math.exp(lam * trend))

    return k
```

### 2.3 Complete Elo Update Pseudocode

```python
def elo_update(student_id: int, problem_id: int, is_correct: bool):
    """
    Full Elo update after a submission.
    Updates both student and problem ratings with dynamic K.
    """
    student_elo = get_elo(student_id, 'STUDENT')
    problem_elo = get_elo(problem_id, 'PROBLEM')

    # Expected score
    expected = 1.0 / (1.0 + 10 ** ((problem_elo.rating - student_elo.rating) / 400))
    actual = 1.0 if is_correct else 0.0

    # Dynamic K for student
    student_history = get_recent_submissions(student_id, limit=10)
    k_student = compute_dynamic_k(student_history)

    # Fixed K for problem (problem difficulty should be stable)
    k_problem = max(10, 40 / math.sqrt(max(1, problem_elo.n_attempts)))
    # ↑ Problem K decreases as more students attempt it (more data = more stable)

    # Update ratings
    student_elo.rating += k_student * (actual - expected)
    problem_elo.rating += k_problem * (expected - actual)

    # Clamp to valid range
    student_elo.rating = max(400, min(2800, student_elo.rating))
    problem_elo.rating = max(400, min(2800, problem_elo.rating))

    # Update trend for next K calculation
    student_elo.trend = compute_trend(student_history + [
        {'is_correct': is_correct, 'expected_score': expected}
    ])
    student_elo.n_attempts += 1
    problem_elo.n_attempts += 1

    # Store history point
    student_elo.rating_history.append({
        'timestamp': now(),
        'rating': student_elo.rating,
        'opponent_rating': problem_elo.rating,
        'outcome': actual,
        'expected': expected
    })

    save_elo(student_elo)
    save_elo(problem_elo)

    return {
        'student_elo_before': student_elo.rating - k_student * (actual - expected),
        'student_elo_after': student_elo.rating,
        'problem_elo_before': problem_elo.rating - k_problem * (expected - actual),
        'problem_elo_after': problem_elo.rating,
        'expected': expected
    }
```

### 2.4 ZPD Filtering

```python
def get_zpd_problems(student_id: int, concept_id: int,
                      zpd_min=100, zpd_max=300) -> list[int]:
    """
    Get problems within the student's Zone of Proximal Development.

    ZPD is defined as problems where:
        student_elo + zpd_min <= problem_elo <= student_elo + zpd_max

    ZPD range justification:
    - The [+100, +300] range is treated as a HYPERPARAMETER, not a fixed constant.
    - Initial values based on:
      * Elo scale: 400 points ≈ 10× expected score difference
      * +100 offset: P(correct) ≈ 0.64 → challenging but achievable
      * +300 offset: P(correct) ≈ 0.36 → difficult stretch zone
      * This maps to ~36%–64% expected success rate, aligning with
        flow theory (Csikszentmihalyi) and desirable difficulty (Bjork)
    - Tuning strategy:
      * If completion rate > 85%: shift range up (e.g., [+150, +350])
      * If completion rate < 40%: shift range down (e.g., [+50, +250])
      * Per-student ZPD adaptation is a future enhancement
    - Alternative ranges to evaluate:
      * [+50, +200]: conservative, higher success rate (~45%–76%)
      * [+150, +400]: aggressive, more challenge (~25%–53%)
    """
    student_elo = get_elo(student_id, 'STUDENT').rating

    target_min = student_elo + zpd_min
    target_max = student_elo + zpd_max

    # SQL: SELECT problem_id FROM elo_rating
    #      WHERE entity_type = 'PROBLEM' AND concept_id = ?
    #      AND rating BETWEEN ? AND ?
    problems = query_problems_in_elo_range(concept_id, target_min, target_max)

    # If no problems in ZPD, expand range
    if not problems:
        # Try broader range: +0 to +400
        problems = query_problems_in_elo_range(concept_id,
                                                 student_elo,
                                                 student_elo + 400)

    # If still no problems, return easiest unsolved
    if not problems:
        problems = get_easiest_unsolved(student_id, concept_id, limit=5)

    return problems
```

### 2.5 Multidimensional Elo

For finer-grained matching, maintain **per-concept Elo ratings** for students:

```python
# Instead of one global student Elo:
student_elo_global = 1350

# Per-concept Elo:
student_elo = {
    'arrays': 1500,      # strong in arrays
    'recursion': 1100,   # weak in recursion
    'sorting': 1350,     # average in sorting
    'dp': 900,           # beginner in DP
}

# Use concept-specific Elo for ZPD matching
# Use global Elo (average across concepts) for dashboard display
```

---

## 3. Layer 3: Hierarchical Multi-Armed Bandit

### 3.1 Thompson Sampling with Beta Priors

Each arm (concept or problem) maintains a Beta distribution representing our belief about its reward probability:

```
θ_arm ~ Beta(α, β)

where:
  α = number of "successes" + 1 (prior)
  β = number of "failures" + 1 (prior)

Expected reward: E[θ] = α / (α + β)
Variance: Var[θ] = αβ / ((α + β)²(α + β + 1))
```

**Selection rule:**
```python
def thompson_select(arms: list[dict]) -> dict:
    """
    Select arm with highest sampled value.

    Each arm: {'id': ..., 'alpha': ..., 'beta': ...}
    """
    best_arm = None
    best_sample = -1

    for arm in arms:
        # Sample from Beta distribution
        sample = np.random.beta(arm['alpha'], arm['beta'])
        if sample > best_sample:
            best_sample = sample
            best_arm = arm

    return best_arm
```

### 3.2 Reward Function

The reward for recommending a problem should reflect **learning gain**, not just correctness:

```python
def compute_reward(student_id: int, concept_id: int,
                    p_mastery_before: float, p_mastery_after: float,
                    is_correct: bool, attempt_number: int,
                    time_spent: float) -> float:
    """
    Compute MAB reward for a (concept, problem) recommendation.

    Reward = weighted combination of learning signals.
    Higher reward = the recommendation was good (student learned something).
    """
    # Component 1: Learning gain (most important)
    # Positive if mastery increased
    learning_gain = p_mastery_after - p_mastery_before

    # Component 2: Appropriate difficulty
    # Reward is highest when problem was challenging but solvable
    if is_correct and attempt_number <= 3:
        difficulty_reward = 1.0  # solved within reasonable attempts
    elif is_correct and attempt_number > 3:
        difficulty_reward = 0.5  # solved but struggled a lot
    elif not is_correct and attempt_number >= 3:
        difficulty_reward = 0.0  # too hard, student gave up
    else:
        difficulty_reward = 0.3  # failed but still practicing

    # Component 3: Efficiency
    # Bonus for solving in reasonable time
    efficiency = min(1.0, 300.0 / max(time_spent, 30.0))  # normalized to [0, 1]

    # Weighted combination
    reward = (
        0.5 * max(0, learning_gain * 10)  # scale up small gains
        + 0.3 * difficulty_reward
        + 0.2 * efficiency
    )

    return min(1.0, max(0.0, reward))  # clamp to [0, 1]
```

### 3.2.1 Reward Function — Sensitivity Analysis

**The ΔP(mastery) noise problem:**

A single BKT update typically produces small mastery changes (0.01–0.05 per interaction). This means the `learning_gain` component of the reward is inherently noisy:
- A correct response on a nearly-mastered concept (P(mastery)=0.9) yields ΔP ≈ 0.02
- A correct response on a new concept (P(mastery)=0.1) yields ΔP ≈ 0.12
- An incorrect response may yield ΔP < 0 (small negative)

**Consequences if unaddressed:**
- MAB converges slowly: needs ~50–100 pulls per arm before Beta distributions narrow meaningfully
- Noisy rewards lead to suboptimal arm selection in early interactions

**Mitigations implemented in the reward function:**
1. **Scaling factor:** `learning_gain * 10` amplifies the small BKT deltas to a range where Beta updates are meaningful
2. **Multi-component reward:** The `difficulty_reward` (0.3 weight) and `efficiency` (0.2 weight) components provide less noisy signals that help the MAB learn even when BKT changes are tiny
3. **Minimum exploration guarantee:** Beta(1,1) prior ensures every arm gets explored at least a few times before exploitation dominates

**Hyperparameter sensitivity:**

| Parameter | Default | Low Alternative | High Alternative | Effect |
|-----------|---------|----------------|-----------------|--------|
| Learning gain weight | 0.5 | 0.3 | 0.7 | Lower → MAB relies more on difficulty/efficiency; Higher → MAB tracks mastery more closely |
| Gain scaling factor | 10 | 5 | 20 | Lower → slower MAB convergence; Higher → oversensitive to small mastery changes |
| Difficulty weight | 0.3 | 0.1 | 0.5 | Lower → ignores difficulty matching; Higher → over-optimizes for "easy wins" |

**Recommendation:** Start with defaults. After 2 weeks of data collection, analyze reward distributions across arms. If variance is too high (coefficient of variation > 1.0), increase the difficulty/efficiency weights to stabilize.

### 3.3 Hierarchical Selection Algorithm

```python
def hierarchical_mab_recommend(student_id: int, n_recommendations: int = 5) -> list:
    """
    Full hierarchical MAB recommendation pipeline.

    Level 1: Select concept (which topic to study)
    Level 2: Select problem within concept (which specific problem)
    """
    recommendations = []

    # Step 0: Check FSRS review queue
    due_reviews = get_due_reviews(student_id)  # concepts with R < 0.9

    # Step 1: Get eligible concepts from Knowledge Graph
    all_concepts = get_all_concepts()
    knowledge_states = get_knowledge_states(student_id)

    eligible_concepts = []
    for concept in all_concepts:
        prerequisites = get_prerequisites(concept.id)
        all_prereqs_met = all(
            knowledge_states.get(p.id, {}).get('p_mastery', 0) >= 0.85
            for p in prerequisites
        )

        # Skip fully mastered concepts (unless they're due for review)
        is_mastered = knowledge_states.get(concept.id, {}).get('p_mastery', 0) >= 0.95
        is_due_review = concept.id in [r.concept_id for r in due_reviews]

        if all_prereqs_met and (not is_mastered or is_due_review):
            eligible_concepts.append(concept)

    # Step 2: Allocate recommendations between review and new concepts
    # FSRS-MAB Conflict Resolution: Threshold Mechanism
    #
    # Problem: If FSRS flags 10 concepts for review, MAB exploration is
    # completely suppressed. This prevents the student from learning new
    # material even when reviews are only slightly overdue.
    #
    # Solution: Cap review allocation based on urgency thresholds:
    #   - Critical reviews (R < 0.7): always included, up to n_recommendations
    #   - Standard reviews (0.7 ≤ R < 0.9): limited to max 50% of recommendations
    #   - If zero critical reviews: allocate max 40% of slots to standard reviews
    #
    # This ensures MAB always gets at least some exploration slots.
    critical_reviews = [r for r in due_reviews if r.retrievability < 0.7]
    standard_reviews = [r for r in due_reviews if 0.7 <= r.retrievability < 0.9]

    # Critical reviews take absolute priority
    n_critical = min(len(critical_reviews), n_recommendations)
    # Standard reviews get up to 50% of remaining slots
    remaining_after_critical = n_recommendations - n_critical
    n_standard = min(len(standard_reviews), remaining_after_critical // 2)
    n_review = n_critical + n_standard
    n_new = n_recommendations - n_review
    # Guarantee: MAB always gets at least 1 slot (unless all slots are critical reviews)
    if n_new == 0 and n_critical < n_recommendations:
        n_review -= 1
        n_new = 1

    # Step 3: Select review concepts (prioritize by urgency)
    # Critical reviews first (lowest retrievability), then standard reviews
    all_reviews_sorted = sorted(critical_reviews + standard_reviews,
                                 key=lambda r: r.retrievability)
    review_concepts = all_reviews_sorted[:n_review]

    for review in review_concepts:
        problem = select_problem_for_concept(
            student_id, review.concept_id, eligible_concepts
        )
        if problem:
            recommendations.append({
                'problem_id': problem.id,
                'concept_id': review.concept_id,
                'reason': 'REVIEW',
                'retrievability': review.retrievability
            })

    # Step 4: Level 1 MAB — Select new concepts
    concept_arms = get_mab_arms(student_id, 'CONCEPT', eligible_concepts)

    selected_concepts = []
    for _ in range(n_new):
        # Thompson Sampling at concept level
        available = [a for a in concept_arms if a['id'] not in selected_concepts]
        if not available:
            break
        arm = thompson_select(available)
        selected_concepts.append(arm['id'])

        # Step 5: Level 2 MAB — Select problem within concept
        problem = select_problem_for_concept(student_id, arm['id'], eligible_concepts)
        if problem:
            recommendations.append({
                'problem_id': problem.id,
                'concept_id': arm['id'],
                'reason': 'NEW_CONCEPT' if knowledge_states.get(arm['id'], {}).get('p_mastery', 0) < 0.5 else 'PRACTICE'
            })

    return recommendations


def select_problem_for_concept(student_id: int, concept_id: int,
                                 eligible_concepts: list) -> Problem:
    """
    Level 2: Select specific problem within a concept.
    Combines MAB with ZPD filtering.
    """
    # Get problems for this concept
    problems = get_problems_for_concept(concept_id)

    # Filter by ZPD
    zpd_problems = get_zpd_problems(student_id, concept_id)
    eligible_problems = [p for p in problems if p.id in zpd_problems]

    # Filter out recently attempted (last 24h)
    eligible_problems = [p for p in eligible_problems
                          if not recently_attempted(student_id, p.id, hours=24)]

    if not eligible_problems:
        # Fall back to any unsolved problem in concept
        eligible_problems = [p for p in problems
                              if not is_solved(student_id, p.id)]

    if not eligible_problems:
        return None

    # Thompson Sampling at problem level
    problem_arms = get_mab_arms(student_id, 'PROBLEM', eligible_problems)
    selected = thompson_select(problem_arms)

    return get_problem(selected['id'])
```

### 3.4 MAB State Update

```python
def update_mab(student_id: int, concept_id: int, problem_id: int,
                reward: float):
    """
    Update MAB state after observing a reward.

    Uses a continuous reward [0, 1] with Beta distribution:
    - alpha += reward (proportional success)
    - beta += (1 - reward) (proportional failure)
    """
    # Update concept-level arm
    concept_arm = get_mab_state(student_id, concept_id, 'CONCEPT')
    concept_arm.alpha += reward
    concept_arm.beta += (1.0 - reward)
    concept_arm.n_pulls += 1
    concept_arm.total_reward += reward
    save_mab_state(concept_arm)

    # Update problem-level arm
    problem_arm = get_mab_state(student_id, problem_id, 'PROBLEM')
    problem_arm.alpha += reward
    problem_arm.beta += (1.0 - reward)
    problem_arm.n_pulls += 1
    problem_arm.total_reward += reward
    save_mab_state(problem_arm)
```

---

## 4. Layer 4: FSRS (Free Spaced Repetition Scheduler)

### 4.1 Core FSRS Model

FSRS tracks three memory states per (student, concept) card:

| State | Symbol | Meaning | Range |
|-------|--------|---------|-------|
| Difficulty | D | Inherent difficulty of this concept for this student | [1, 10] |
| Stability | S | Days until retrievability decays to 90% (memory half-life) | (0, ∞) |
| Retrievability | R | Current probability of successful recall | [0, 1] |

### 4.2 Retrievability Decay

```
R(t, S) = (1 + t / (9 × S))^(-1)

where:
  t = elapsed time since last review (in days)
  S = current stability
```

**Properties:**
- R(0, S) = 1 (just reviewed → perfect recall)
- R(S, S) = 0.9 (at t = S days → 90% recall, by definition of stability)
- R → 0 as t → ∞ (forgotten without review)

### 4.3 FSRS State Transitions

```python
# FSRS-5 parameters (19 optimizable weights)
W = [
    0.4072,  # w0: initial stability for rating 1
    1.1829,  # w1: initial stability for rating 2
    3.1262,  # w2: initial stability for rating 3
    15.4722, # w3: initial stability for rating 4
    7.2102,  # w4: initial difficulty for rating (scale)
    0.5316,  # w5: initial difficulty for rating (offset)
    1.0651,  # w6: difficulty update from rating
    0.0046,  # w7: difficulty mean reversion weight
    1.5401,  # w8: stability after successful recall (base)
    0.1700,  # w9: stability after successful recall (difficulty effect)
    1.0100,  # w10: stability after successful recall (stability effect)
    2.0700,  # w11: stability after successful recall (retrievability effect)
    0.0500,  # w12: stability after failure (base)
    0.3600,  # w13: stability after failure (difficulty effect)
    0.1500,  # w14: stability after failure (stability effect)
    0.2100,  # w15: stability after failure (retrievability effect)
    0.0500,  # w16: stability after failure (minimum factor)
    2.5000,  # w17: hard penalty
    0.2700,  # w18: easy bonus
]
```

### 4.4 FSRS Algorithm Pseudocode

```python
class FSRSCard:
    difficulty: float  # D: [1, 10]
    stability: float   # S: days
    state: str         # NEW | LEARNING | REVIEW | RELEARNING
    reps: int
    lapses: int
    last_review: datetime
    due_date: datetime


def fsrs_initial_stability(rating: int) -> float:
    """Initial stability based on first rating."""
    return W[rating - 1]  # w0..w3


def fsrs_initial_difficulty(rating: int) -> float:
    """Initial difficulty based on first rating."""
    return W[4] - math.exp(W[5] * (rating - 1)) + 1
    # Clamp to [1, 10]


def fsrs_update_difficulty(d: float, rating: int) -> float:
    """Update difficulty after a review."""
    d_new = d - W[6] * (rating - 3)  # rating 3 = neutral, 1-2 = harder, 4 = easier
    d_new = W[7] * fsrs_initial_difficulty(3) + (1 - W[7]) * d_new  # mean reversion
    return max(1.0, min(10.0, d_new))


def fsrs_update_stability_success(d: float, s: float, r: float,
                                    rating: int) -> float:
    """Update stability after successful recall (rating >= 2)."""
    hard_penalty = W[17] if rating == 2 else 1.0
    easy_bonus = W[18] if rating == 4 else 1.0

    s_new = s * (
        1 + math.exp(W[8])
        * (11 - d) ** W[9]
        * s ** (-W[10])
        * (math.exp((1 - r) * W[11]) - 1)
        * hard_penalty
        * easy_bonus
    )

    return max(0.1, s_new)


def fsrs_update_stability_fail(d: float, s: float, r: float) -> float:
    """Update stability after failed recall (rating = 1)."""
    s_new = (
        W[12]
        * d ** (-W[13])
        * ((s + 1) ** W[14] - 1)
        * math.exp((1 - r) * W[15])
    )

    return max(0.1, min(s, s_new))  # stability can't increase after failure


def fsrs_review(card: FSRSCard, rating: int) -> FSRSCard:
    """
    Process a review event.

    Rating: 1=Again, 2=Hard, 3=Good, 4=Easy
    """
    now = datetime.now()

    if card.state == 'NEW':
        # First review
        card.difficulty = fsrs_initial_difficulty(rating)
        card.stability = fsrs_initial_stability(rating)
        card.state = 'LEARNING' if rating < 3 else 'REVIEW'
    else:
        # Calculate current retrievability
        elapsed_days = (now - card.last_review).total_seconds() / 86400
        r = (1 + elapsed_days / (9 * card.stability)) ** (-1)

        # Update difficulty
        card.difficulty = fsrs_update_difficulty(card.difficulty, rating)

        if rating == 1:
            # Failed recall
            card.stability = fsrs_update_stability_fail(
                card.difficulty, card.stability, r
            )
            card.lapses += 1
            card.state = 'RELEARNING'
        else:
            # Successful recall
            card.stability = fsrs_update_stability_success(
                card.difficulty, card.stability, r, rating
            )
            card.state = 'REVIEW'

    card.reps += 1
    card.last_review = now

    # Schedule next review: when R will drop to 0.9
    # R(t) = (1 + t/(9S))^(-1) = 0.9
    # Solving: t = 9S × (0.9^(-1) - 1) = 9S × (1/0.9 - 1) = 9S × (1/9) = S
    # So next review is in S days (when R = 0.9)
    card.due_date = now + timedelta(days=card.stability)

    return card
```

### 4.5 Rating Mapping for Programming

```python
def submission_to_fsrs_rating(is_correct: bool, attempt_number: int,
                                time_spent_seconds: float) -> int:
    """
    Map a programming submission outcome to an FSRS rating (1-4).

    This is a key design decision unique to our thesis —
    translating code submission outcomes to memory ratings.
    """
    if not is_correct:
        return 1  # Again — concept needs re-learning

    # Correct submission
    if attempt_number == 1:
        if time_spent_seconds < 120:  # < 2 minutes
            return 4  # Easy — strong recall
        elif time_spent_seconds < 300:  # < 5 minutes
            return 3  # Good — moderate effort
        else:
            return 2  # Hard — correct but took a long time
    elif attempt_number <= 3:
        return 2  # Hard — needed multiple attempts
    else:
        return 2  # Hard — many attempts before success
```

### 4.6 Review Queue Management

```python
def get_review_queue(student_id: int) -> list[dict]:
    """
    Get concepts due for review, ordered by urgency.
    """
    cards = get_all_fsrs_cards(student_id)
    now = datetime.now()

    due_cards = []
    upcoming_cards = []

    for card in cards:
        if card.state == 'NEW':
            continue

        elapsed_days = (now - card.last_review).total_seconds() / 86400
        current_r = (1 + elapsed_days / (9 * card.stability)) ** (-1)
        card.retrievability = current_r

        if current_r < 0.9:  # Due for review
            due_cards.append({
                'concept_id': card.concept_id,
                'retrievability': current_r,
                'days_overdue': (now - card.due_date).days,
                'urgency': 1.0 - current_r  # higher urgency = lower retrievability
            })
        elif card.due_date <= now + timedelta(days=3):  # Due within 3 days
            upcoming_cards.append({
                'concept_id': card.concept_id,
                'due_date': card.due_date,
                'retrievability': current_r
            })

    # Sort by urgency (most forgotten first)
    due_cards.sort(key=lambda x: x['retrievability'])
    upcoming_cards.sort(key=lambda x: x['due_date'])

    return {'due_now': due_cards, 'upcoming': upcoming_cards}
```

---

## 5. Layer 5: LLM Feedback Engine (Optional)

### 5.1 RAG Pipeline

```python
def generate_hint(student_id: int, problem_id: int,
                   student_code: str, error_message: str) -> str:
    """
    Generate a Socratic hint using RAG + LLM.

    1. Retrieve relevant context from Knowledge Graph
    2. Build prompt with student's knowledge state
    3. Call LLM for hint generation
    """
    # Step 1: Get problem's concepts and prerequisites
    problem_concepts = get_problem_concepts(problem_id)
    primary_concept = next(c for c in problem_concepts if c.is_primary)
    prerequisites = get_prerequisites(primary_concept.id)

    # Step 2: Get student's knowledge state for these concepts
    knowledge = get_knowledge_states(student_id)
    weakest_prereq = min(prerequisites,
                          key=lambda p: knowledge.get(p.id, {}).get('p_mastery', 0))

    # Step 3: Retrieve common mistakes for this concept (from KG)
    common_mistakes = get_common_mistakes(primary_concept.id)

    # Step 4: Build RAG context
    context = f"""
    Problem concept: {primary_concept.display_name}
    Prerequisites: {', '.join(p.display_name for p in prerequisites)}
    Student's weakest prerequisite: {weakest_prereq.display_name}
        (mastery: {knowledge.get(weakest_prereq.id, {}).get('p_mastery', 0):.0%})
    Common mistakes for this concept:
    {chr(10).join(f'- {m}' for m in common_mistakes)}
    """

    # Step 5: Generate hint
    prompt = f"""You are a programming tutor helping a university student.

{context}

The student's code:
```python
{student_code}
```

Error: {error_message}

Generate a single Socratic question that:
1. Does NOT give the answer directly
2. Guides the student to identify the issue themselves
3. Focuses on the weakest prerequisite concept if relevant
4. Is encouraging and constructive

Respond with ONLY the hint question, nothing else."""

    hint = call_llm(prompt, max_tokens=200)
    return hint
```

### 5.2 Cost Management

```python
# Rate limiting per student
MAX_HINTS_PER_PROBLEM = 3    # max hints per problem attempt
MAX_HINTS_PER_DAY = 10       # max hints per day per student
HINT_COOLDOWN_SECONDS = 60   # minimum time between hint requests

# Cost estimation (GPT-4 pricing)
# ~500 tokens input + ~100 tokens output per hint
# $0.03/1K input + $0.06/1K output = ~$0.02 per hint
# Budget: $50/month → ~2,500 hints/month → ~83 hints/day
# For 50 active students: ~1.7 hints/student/day (within budget)
```

---

## 6. Foundation: Knowledge Graph

### 6.1 Concept Taxonomy for Python Programming

```
Level 1 (Basic):
  variables, data_types, operators, io, strings

Level 2 (Control Flow):
  conditionals, loops, nested_loops

Level 3 (Functions):
  functions, parameters, return_values, scope, recursion

Level 4 (Data Structures):
  lists, tuples, dictionaries, sets, stacks, queues

Level 5 (OOP):
  classes, objects, inheritance, polymorphism, encapsulation

Level 6 (Algorithms):
  searching, sorting, two_pointers, sliding_window,
  greedy, divide_and_conquer

Level 7 (Advanced):
  dynamic_programming, graphs, trees, backtracking, bit_manipulation
```

### 6.2 Prerequisite Graph (Core Edges)

```
variables → data_types
variables → operators
variables → io
data_types → strings
operators → conditionals
loops → nested_loops
conditionals → loops
variables → lists
io → functions
loops → functions
functions → parameters
functions → return_values
functions → scope
functions → recursion
lists → tuples
lists → dictionaries
lists → sets
lists → stacks
lists → queues
functions → classes
classes → objects
classes → inheritance
inheritance → polymorphism
classes → encapsulation
loops → searching
lists → sorting
sorting → two_pointers
loops → sliding_window
conditionals → greedy
recursion → divide_and_conquer
recursion → dynamic_programming
recursion → backtracking
lists → graphs
recursion → trees
operators → bit_manipulation
```

### 6.3 Concept Mastery States

```
NOT_STARTED:    P(mastery) = P(L₀) (initial prior, typically ~0.1)
IN_PROGRESS:    0.1 < P(mastery) < 0.85
MASTERED:       P(mastery) ≥ 0.85
LOCKED:         At least one prerequisite has P(mastery) < 0.85
```

---

## 7. Complete Recommendation Pipeline — End-to-End

```python
def get_adaptive_recommendations(student_id: int, limit: int = 5) -> dict:
    """
    Complete end-to-end recommendation pipeline.
    Orchestrates all 5 layers.
    """
    # Layer 1: Get knowledge state
    knowledge_states = get_all_knowledge_states(student_id)

    # Layer 2: Get student Elo
    student_elo = get_elo(student_id, 'STUDENT')

    # Layer 4: Check review queue
    review_queue = get_review_queue(student_id)

    # Foundation: Load Knowledge Graph
    kg = load_knowledge_graph()

    # Layer 3: Run Hierarchical MAB
    recommendations = hierarchical_mab_recommend(
        student_id=student_id,
        n_recommendations=limit,
        knowledge_states=knowledge_states,
        student_elo=student_elo,
        review_queue=review_queue,
        knowledge_graph=kg
    )

    # Enrich with metadata
    for rec in recommendations:
        problem = get_problem(rec['problem_id'])
        problem_elo = get_elo(rec['problem_id'], 'PROBLEM')
        concept_state = knowledge_states.get(rec['concept_id'], {})

        rec['problem_title'] = problem.title
        rec['difficulty_match'] = 1.0 - abs(
            student_elo.rating - problem_elo.rating - 200
        ) / 400  # normalized match score
        rec['expected_success'] = 1.0 / (
            1.0 + 10 ** ((problem_elo.rating - student_elo.rating) / 400)
        )
        rec['mastery_before'] = concept_state.get('p_mastery', 0.1)

    return {
        'recommendations': recommendations,
        'knowledge_summary': {
            'mastered_concepts': sum(
                1 for s in knowledge_states.values() if s.get('p_mastery', 0) >= 0.85
            ),
            'in_progress_concepts': sum(
                1 for s in knowledge_states.values()
                if 0.1 < s.get('p_mastery', 0) < 0.85
            ),
            'locked_concepts': count_locked_concepts(knowledge_states, kg),
            'student_elo': student_elo.rating,
            'due_reviews': len(review_queue['due_now'])
        }
    }


def process_submission_result(student_id: int, problem_id: int,
                                is_correct: bool, attempt_number: int,
                                time_spent: float, error_type: str = None):
    """
    Update all layers after a submission is evaluated.
    Called asynchronously after code execution completes.
    """
    # Get problem's primary concept
    concept_id = get_primary_concept(problem_id)

    # Layer 1: Update BKT
    state_before = get_knowledge_state(student_id, concept_id)
    p_mastery_before = state_before.p_mastery
    state_after = bkt_update(state_before.p_mastery, is_correct, state_before)
    save_knowledge_state(student_id, concept_id, state_after)

    # Layer 2: Update Elo
    elo_result = elo_update(student_id, problem_id, is_correct)

    # Layer 3: Update MAB
    reward = compute_reward(
        student_id, concept_id,
        p_mastery_before, state_after,
        is_correct, attempt_number, time_spent
    )
    update_mab(student_id, concept_id, problem_id, reward)

    # Layer 4: Update FSRS
    rating = submission_to_fsrs_rating(is_correct, attempt_number, time_spent)
    card = get_or_create_fsrs_card(student_id, concept_id)
    card = fsrs_review(card, rating)
    save_fsrs_card(card)

    # Invalidate caches
    invalidate_cache(f'knowledge_state:{student_id}')
    invalidate_cache(f'recommendations:{student_id}')

    return {
        'bkt_update': {'before': p_mastery_before, 'after': state_after},
        'elo_update': elo_result,
        'mab_reward': reward,
        'fsrs_update': {'rating': rating, 'next_review': card.due_date}
    }
```
