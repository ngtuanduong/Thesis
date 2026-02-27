# Literature Review — Comprehensive Thematic Survey

**Thesis:** Adaptive Learning Platform for University Programming Courses
**Purpose:** Foundation for Chapter 2 of thesis — organized by theme with academic citations

---

## 1. Adaptive Learning Systems

### 1.1 Definitions and Foundations

Adaptive learning refers to educational approaches that adjust instructional content, pace, and methodology based on individual learner characteristics and performance (Brusilovsky, 2001). The core premise is that learning is optimized when instruction matches the learner's current knowledge state, cognitive ability, and learning preferences.

Paramythis and Loidl-Reisinger (2004) classify adaptive systems along four dimensions:
1. **Adaptive interaction** — modifying the interface and navigation
2. **Adaptive content** — selecting and sequencing learning materials
3. **Adaptive assessment** — adjusting difficulty and format of evaluation
4. **Adaptive collaboration** — forming groups based on learner profiles

For this thesis, we focus primarily on **adaptive content** (selecting the right problem) and **adaptive assessment** (calibrating problem difficulty to the learner's ability).

### 1.2 Historical Evolution

**First Generation: Intelligent Tutoring Systems (1970s–1990s)**

The earliest adaptive systems were rule-based Intelligent Tutoring Systems (ITS). Anderson et al. (1985) developed the LISP Tutor and later the Cognitive Tutor series, based on ACT-R theory. These systems maintained an explicit model of student knowledge (a "student model") and used production rules to select instructional actions. The Cognitive Tutor for mathematics demonstrated a 50–100% improvement in problem-solving skills compared to traditional instruction in controlled studies (Ritter et al., 2007).

**Second Generation: Web-Based Adaptive Systems (2000s)**

The web enabled Adaptive Educational Hypermedia (AEH) systems like AHA! (De Bra et al., 2003) and KnowledgeTree (Brusilovsky, 2004). These systems adapted hyperlink visibility and content presentation based on user models. The shift from desktop to web dramatically increased accessibility but the underlying adaptation mechanisms remained largely rule-based.

**Third Generation: Data-Driven Platforms (2010s–present)**

Modern platforms leverage machine learning for adaptation:
- **ALEKS** (Assessment and LEarning in Knowledge Spaces) uses Knowledge Space Theory to map student states and select optimal learning paths (Doignon & Falmagne, 1999).
- **Khan Academy** employs a mastery-based learning model where students must demonstrate proficiency before advancing (Murphy et al., 2014).
- **Duolingo** uses spaced repetition and half-life regression for language learning (Settles & Meeder, 2016).

### 1.3 Adaptive Learning for Programming Education

Programming education presents unique challenges (Robins et al., 2003):
- Programming requires **procedural knowledge** (knowing how) not just **declarative knowledge** (knowing that)
- Student code submissions are rich artifacts containing far more signal than a multiple-choice answer
- Programming skills are hierarchical: understanding arrays requires understanding variables and loops
- There are multiple correct solutions to most programming problems

Luxton-Reilly et al. (2018) conducted a comprehensive survey of introductory programming research, finding that failure rates average 30–40% globally. They identified the need for individualized practice as a key research gap.

Existing adaptive programming platforms include:
- **CodeWorkout** (Edwards et al., 2020): exercise repository with adaptive selection based on concept mastery
- **Problets** (Kumar, 2005): problem generation with adaptive difficulty
- **PCRS** (Zingaro et al., 2018): peer code review system with adaptive pairing

However, **none of these platforms integrate all five components** (knowledge tracing + difficulty calibration + intelligent selection + spaced repetition + LLM feedback) into a unified adaptive pipeline. This is the gap our thesis addresses.

### 1.4 Summary Table: Commercial Platforms

| Platform | KT | Elo/IRT | MAB | Spaced Rep. | LLM | KG |
|----------|:---:|:-------:|:---:|:-----------:|:---:|:---:|
| LeetCode | ✗ | ✗ | ✗ | ✗ | Partial | ✗ |
| HackerRank | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Codeforces | ✗ | Elo (rating) | ✗ | ✗ | ✗ | ✗ |
| CodeSignal | ✗ | EloIRT | ✗ | ✗ | ✗ | ✗ |
| Duolingo | ✗ | ✗ | ✗ | FSRS | ✗ | ✗ |
| Khan Academy | Mastery | ✗ | ✗ | ✗ | Khanmigo | ✗ |
| **This Thesis** | **BKT** | **Dynamic Elo** | **H-MAB** | **FSRS** | **RAG+LLM** | **Yes** |

---

## 2. Knowledge Tracing

Knowledge Tracing (KT) is the task of modeling a student's knowledge state over time based on their interaction history with learning materials. The goal is to estimate the probability that a student has mastered a particular skill or concept.

### 2.1 Bayesian Knowledge Tracing (BKT)

**Original formulation:** Corbett and Anderson (1994) introduced BKT as a Hidden Markov Model (HMM) with two hidden states (Learned, Unlearned) and four parameters:

| Parameter | Symbol | Description | Typical Range |
|-----------|--------|-------------|---------------|
| Prior knowledge | P(L₀) | Probability student already knows the skill | 0.0–0.5 |
| Learn rate | P(T) | Probability of transitioning from Unlearned to Learned after practice | 0.01–0.4 |
| Guess rate | P(G) | Probability of correct answer despite not knowing | 0.0–0.3 |
| Slip rate | P(S) | Probability of incorrect answer despite knowing | 0.0–0.2 |

**Update equations:**

Given an observation (correct/incorrect), BKT updates the posterior probability of mastery:

```
After a CORRECT response:
P(L_t | correct) = P(L_{t-1}) * (1 - P(S)) / P(correct)
where P(correct) = P(L_{t-1}) * (1 - P(S)) + (1 - P(L_{t-1})) * P(G)

After an INCORRECT response:
P(L_t | incorrect) = P(L_{t-1}) * P(S) / P(incorrect)
where P(incorrect) = P(L_{t-1}) * P(S) + (1 - P(L_{t-1})) * (1 - P(G))

Then apply the learn transition:
P(L_t) = P(L_t | obs) + (1 - P(L_t | obs)) * P(T)
```

**Strengths:** Interpretable parameters, well-studied over 30 years, fast computation (O(1) per update), works well with sparse data.

**Limitations:** Binary skill state (known/unknown), assumes skill independence, no forgetting mechanism, assumes all problems for a skill are equivalent.

**Tooling:** `pyBKT` (Badrinath et al., 2021) provides an open-source Python implementation with EM parameter fitting, cross-validation, and integration with standard educational data formats.

### 2.2 Deep Knowledge Tracing (DKT)

Piech et al. (2015) revolutionized KT by applying recurrent neural networks (LSTMs) to model student knowledge states. Instead of hand-crafted parameters, DKT learns latent representations from interaction sequences.

**Architecture:**
- Input: one-hot encoding of (skill_id, correctness) at each timestep
- Hidden: LSTM processes the sequence, maintaining a hidden state
- Output: predicted probability of correctness for each skill at the next timestep

**Advantages over BKT:**
- Captures complex skill dependencies without explicit prerequisite modeling
- Handles long-range temporal patterns
- No assumption of skill independence
- No manual feature engineering

**Limitations:**
- Black-box: cannot interpret what the model "thinks" the student knows
- Requires large training datasets (thousands of students)
- Reconstruction inconsistency (predicting different mastery for the same skill at the same time)

**DKT+ (Yeung & Yeung, 2018):** Added regularization terms to address reconstruction inconsistency and waviness in predictions.

**DKVMN (Zhang et al., 2017):** Dynamic Key-Value Memory Networks: separates skill representation (key) from student state (value) using memory-augmented neural networks.

### 2.3 State-of-the-Art Knowledge Tracing (2024–2026)

#### DKT2 (Doan & Sahebi, ECML-PKDD 2025)

DKT2 combines **xLSTM** (Extended Long Short-Term Memory) with **IRT** (Item Response Theory) integration. Key innovations:
- xLSTM provides better long-range memory than standard LSTM, crucial for modeling learning over weeks
- IRT layer decomposes predictions into student ability and item difficulty, improving interpretability
- Achieves state-of-the-art on 5 benchmarks (ASSISTments, EdNet, Junyi, Statics, NIPS34)
- **Open source:** Available on GitHub with pre-trained models

**Relevance to thesis:** DKT2 represents a potential upgrade path from BKT. Start with BKT for simplicity and interpretability; upgrade to DKT2 if sufficient training data accumulates.

#### srcML-DKT (EDM 2025)

**Code-specific knowledge tracing** that uses features extracted from actual submitted source code:
- Parses source code into Abstract Syntax Trees (AST)
- Extracts code complexity features: lines of code, cyclomatic complexity, AST depth
- Feeds code features alongside correctness into a modified DKT architecture
- Significantly outperforms standard DKT for programming exercise datasets

**Relevance to thesis:** Highly relevant because our platform has access to submitted code. Could extract code features as additional BKT features in future versions.

#### UKT — Uncertainty-Aware Knowledge Tracing (AAAI 2025)

Instead of point estimates of mastery, UKT models **probability distributions** over student knowledge states:
- Outputs a distribution (mean + variance) rather than a single probability
- Higher variance = more uncertainty = need more observations
- Enables confidence-aware recommendations: avoid recommending problems where we're uncertain about mastery

**Relevance to thesis:** The uncertainty quantification is valuable for the MAB layer — uncertainty maps directly to exploration bonuses.

#### Other Notable Recent Work

- **LefoKT** (2025): Separates forgetting-related factors from learning-relevance factors, improving prediction when there are long gaps between practice sessions.
- **HCGKT** (2025): Hierarchical graph-based KT that models concept prerequisites as a graph and propagates knowledge estimates along prerequisite edges.

### 2.4 Knowledge Tracing for Programming — Special Considerations

Programming KT differs from traditional KT (e.g., mathematics) in several ways:

1. **Rich submission signals:** Beyond binary correctness, code submissions contain:
   - Number of attempts before success
   - Time between first attempt and success
   - Types of errors encountered (syntax, runtime, logic)
   - Code similarity to optimal solution
   - Cyclomatic complexity and code quality metrics

2. **Concept mapping complexity:** A single programming problem may involve multiple concepts (e.g., "two sum" requires arrays, hash maps, and iteration). BKT's single-skill-per-interaction assumption needs adaptation.

3. **Solution paths:** Students may solve the same problem using different algorithms (brute force vs optimal), revealing different knowledge states.

**Our approach:** Start with BKT using the **primary concept** of each problem. Extend to multi-concept BKT where a submission updates mastery for all tagged concepts with weighted contributions.

---

## 3. Spaced Repetition

### 3.1 The Forgetting Curve

Ebbinghaus (1885) established that memory decays exponentially over time without reinforcement. The "forgetting curve" describes this decay:

```
R(t) = e^(-t/S)
```

where R is retrievability (probability of recall), t is time since last review, and S is stability (memory strength). The **spacing effect** (Cepeda et al., 2006) shows that distributing practice over time produces stronger long-term retention than massing practice in a single session.

Bjork and Bjork (2011) formalized "desirable difficulties" — making retrieval effortful (e.g., by spacing reviews) strengthens the memory trace. This is the theoretical foundation for spaced repetition systems.

### 3.2 SM-2 Algorithm

Wozniak (1990) developed the SM-2 algorithm for SuperMemo, the first widely-used spaced repetition system:

```
New interval:
  I(1) = 1 day
  I(2) = 6 days
  I(n) = I(n-1) × EF

Easiness Factor update:
  EF' = EF + (0.1 - (5 - q) × (0.08 + (5 - q) × 0.02))
  where q is quality of response (0–5), EF ≥ 1.3
```

**Limitations of SM-2:**
- Fixed formulas, not optimized from data
- Same parameters for all users
- Quality rating is subjective and hard to calibrate
- No theoretical grounding in memory science

### 3.3 FSRS — Free Spaced Repetition Scheduler

FSRS (Ye, 2023) represents a major advancement over SM-2, now integrated into Anki 23.10+. It is grounded in the **DSR model** (Difficulty, Stability, Retrievability):

**Three memory states:**
- **Difficulty (D):** How inherently hard this material is for this learner (1–10 scale)
- **Stability (S):** The time (in days) for retrievability to decay to 90% — the "half-life" of the memory
- **Retrievability (R):** Current probability of successful recall

**Core formula:**

```
R(t, S) = (1 + t/(9·S))^(-1)
```

This is a power-law forgetting curve where:
- At t = 0: R = 1 (just reviewed, perfect recall)
- At t = S: R = 0.9 (by definition, stability is the 90% retention point)
- As t → ∞: R → 0

**Stability update after review:**

```
S' = S · (e^(w₁₇) · (D + 1)^(-w₁₈) · ((e^(w₁₉ · (1 - R)) - 1) · w₂₀) + 1)
```

where w₁₇–w₂₀ are optimizable parameters.

**Difficulty update after review:**

```
D' = w₇ · D₀(rating) + (1 - w₇) · (D - w₆ · (rating - 3))
```

**Key advantages over SM-2:**
1. **Data-driven:** Parameters optimized from actual review history using gradient descent
2. **Personalized:** Adapts to individual learner's memory characteristics
3. **Theoretically grounded:** Based on memory research (power-law forgetting)
4. **Empirically validated:** 20–30% fewer reviews than SM-2 for the same retention target

**FSRS ratings:**
| Rating | Meaning | Effect on Stability |
|--------|---------|-------------------|
| 1 (Again) | Complete failure | S resets to short interval |
| 2 (Hard) | Recalled with significant difficulty | S increases minimally |
| 3 (Good) | Recalled with moderate effort | S increases normally |
| 4 (Easy) | Recalled effortlessly | S increases maximally |

### 3.4 LECTOR (August 2025)

LECTOR integrates LLMs with spaced repetition scheduling:
- Uses LLM to dynamically generate review materials at appropriate difficulty
- Achieved 90.2% retention success rate in controlled study
- Combines FSRS-style scheduling with LLM content generation

**Relevance to thesis:** LECTOR validates the combination of spaced repetition with AI content generation. Our Layer 4 (FSRS) + Layer 5 (LLM) mirrors this architecture for programming.

### 3.5 Spaced Repetition for Programming — Novel Application

Applying spaced repetition to programming skills is a novel contribution of this thesis. Key design decisions:

**What is a "card" in programming?**
- Each (student, concept) pair is an FSRS card
- "Reviewing" a concept means solving a problem tagged with that concept
- The concept-level (not problem-level) approach prevents the student from memorizing specific problem solutions

**Rating mapping from submission outcomes:**

| Submission Outcome | FSRS Rating | Rationale |
|--------------------|-------------|-----------|
| ACCEPTED on first attempt, fast | 4 (Easy) | Strong recall of concept |
| ACCEPTED on first attempt, slow | 3 (Good) | Solid but needed thinking |
| ACCEPTED after 2–3 attempts | 2 (Hard) | Significant difficulty |
| Not solved / gave up | 1 (Again) | Concept needs re-learning |

**Integration with other layers:**
- FSRS communicates with MAB: "Concept X is due for review (R < 0.9)"
- MAB decides whether to schedule a review or explore a new concept
- Elo selects the specific review problem at the right difficulty level

---

## 4. Multi-Armed Bandits in Education

### 4.1 Problem Formulation

The Multi-Armed Bandit (MAB) problem (Robbins, 1952) is a classic formulation of the **exploration-exploitation tradeoff**:
- **Exploitation:** Recommend what we know works well (high expected reward)
- **Exploration:** Try uncertain options to discover potentially better ones

In educational recommendation:
- Each **arm** represents a learning activity (concept, problem, difficulty level)
- **Reward** represents learning gain from the activity
- The goal is to maximize cumulative learning over time

### 4.2 Thompson Sampling

Thompson Sampling (Thompson, 1933) is a Bayesian approach to MAB:

```
For each arm i:
  1. Maintain a Beta(αᵢ, βᵢ) distribution over reward probability
  2. Sample θᵢ ~ Beta(αᵢ, βᵢ)
  3. Select arm with highest sampled θᵢ
  4. Observe reward r ∈ {0, 1}
  5. Update: if r = 1, αᵢ += 1; if r = 0, βᵢ += 1
```

**Advantages for education:**
- Naturally balances exploration and exploitation
- Arms with high uncertainty get explored more (wide distributions → higher chance of sampling a high value)
- As evidence accumulates, exploitation dominates (narrow distributions → consistent sampling)
- No tuning parameter (unlike UCB's confidence parameter)

### 4.3 Hierarchical MAB for Problem Selection

Standard MAB treats each problem as a separate arm — impractical when there are hundreds of problems. The **hierarchical approach** introduces two levels:

**Level 1: Concept Selection**
```
For each concept c in unlocked_concepts:
  Sample θ_c ~ Beta(α_c, β_c)
Select concept c* = argmax θ_c
```

**Level 2: Problem Selection within Concept**
```
For each problem p in concept c* where Elo(p) in ZPD(student):
  Sample θ_p ~ Beta(α_p, β_p)
Select problem p* = argmax θ_p
```

**Reward function design:**

Learning gain is the reward signal. We define it as:

```
reward = Δ P(mastery_concept) after attempting the problem
```

If the student's mastery of the concept increased after attempting the problem, the reward is positive. If mastery didn't change (e.g., they already knew it), the reward is near zero — the MAB learns to stop recommending mastered concepts.

**Prerequisite constraint:** At Level 1, only concepts whose prerequisites have P(mastery) > 0.8 are eligible for selection. This prevents the MAB from recommending advanced concepts before foundations are solid.

### 4.4 MAB with Abandonment (NeurIPS 2024)

Shen et al. (2024) addressed a critical issue in educational MAB: **student abandonment**. When a problem is too hard or too boring, students disengage rather than attempting it. Standard MAB ignores this signal.

The modified model:
- Includes a third outcome: success, failure, **abandonment**
- Abandonment provides negative reward (penalizes arms that cause disengagement)
- Models student patience as a function of consecutive failures

**Relevance to thesis:** Programming exercises have high abandonment rates when difficulty is mismatched. Our Elo-based ZPD filtering partially addresses this, but the MAB should also learn from abandonment signals (recommend different concepts if student consistently skips).

### 4.5 Contextual Bandits

Contextual MAB extends the basic model by incorporating features (context) about both the student and the problem:
- Student context: current mastery vector, Elo rating, recent performance trend
- Problem context: concept, difficulty, prerequisites, estimated time
- The policy learns to map (student_context, problem_context) → expected reward

**LinUCB** (Li et al., 2010) and **Neural Contextual Bandits** (Riquelme et al., 2018) are relevant approaches. These are more sophisticated than Thompson Sampling but require more data to train.

**Our approach:** Start with hierarchical Thompson Sampling (simple, interpretable). If sufficient data accumulates, upgrade to contextual bandits with student/problem features.

---

## 5. Elo Rating and Item Response Theory

### 5.1 Classical Elo Rating System

The Elo rating system (Elo, 1978) was developed for chess but applies broadly to any domain with pairwise competition. In education, the "competition" is between a student and a problem.

**Expected score:**

```
E(student, problem) = 1 / (1 + 10^((R_problem - R_student) / 400))
```

Where R_student and R_problem are their respective ratings.

**Rating update after an attempt:**

```
R'_student = R_student + K_student × (S - E)
R'_problem = R_problem + K_problem × (E - S)
```

Where:
- S = actual score (1 for correct, 0 for incorrect)
- E = expected score
- K = update step size (K-factor)

**Interpretation:** If a student solves a problem they were expected to solve (E ≈ 1, S = 1), their rating barely changes. If they solve a problem they weren't expected to solve (E ≈ 0, S = 1), their rating jumps significantly. This naturally calibrates both student ability and problem difficulty.

### 5.2 Connection to Item Response Theory (IRT)

IRT is the standard psychometric framework for educational assessment. The simplest model (Rasch/1PL) has the same mathematical form as Elo:

```
P(correct | θ, β) = σ(θ - β) = 1 / (1 + e^(-(θ - β)))
```

Where θ is student ability and β is item difficulty. The Elo expected score formula is equivalent with a scaling factor:

```
E = σ((R_student - R_problem) / 400 × ln(10))
```

**Key equivalence:** Elo ratings converge to IRT ability/difficulty estimates under the Rasch model (Pelánek, 2016). The advantage of Elo for our system is that it updates incrementally (online) after each submission, whereas IRT traditionally requires batch re-estimation.

### 5.3 Dynamic K-Value Elo (Springer, 2025)

Standard Elo uses a fixed K-factor, which creates a tradeoff:
- Large K: fast adaptation but volatile ratings
- Small K: stable ratings but slow adaptation to genuine learning or difficulty changes

The **Dynamic K-Value** approach (Springer, 2025) adapts K based on the student's **learning trend**:

```
trend_t = Σᵢ₌₁ⁿ wᵢ × (Sᵢ - Eᵢ)    (weighted sum of recent residuals)

If trend_t > 0:  (student is improving)
  K = K_min + (K_max - K_min) × e^(-λ × trend_t)
  → K decreases, student is stable and improving, small updates

If trend_t < 0:  (student is struggling)
  K = K_min + (K_max - K_min) × (1 - e^(λ × trend_t))
  → K increases, student needs faster re-calibration
```

Where:
- K_min = 10, K_max = 40 (typical range)
- λ = decay parameter controlling sensitivity
- n = window size for trend calculation (e.g., last 10 submissions)
- wᵢ = exponential decay weights (more recent submissions weigh more)

**Advantages:**
- Struggling students get faster rating adjustments (they're not stuck at a wrong rating)
- Stable students get smaller fluctuations (prevents bouncing)
- No manual tuning of K — it adapts automatically

### 5.4 Elo for Programming Exercises — Empirical Evidence

Pelánek (2016) provides theoretical foundations for using Elo in education. More directly relevant, a study published in ACM Transactions on Computing Education demonstrated:

- Applied Elo ratings to 76 programming tasks across 299 students (50,055 attempts)
- Elo accurately predicted student success probability (AUC > 0.7)
- Elo ratings converged within ~20 attempts per student and ~30 attempts per problem
- The system successfully identified problems that were miscategorized in difficulty

### 5.5 Zone of Proximal Development (ZPD)

Vygotsky (1978) introduced the ZPD as the range of tasks a learner can accomplish with assistance but not independently. In our Elo framework:

```
ZPD(student) = [R_student + ZPD_min, R_student + ZPD_max]
```

Where ZPD_min = 100 and ZPD_max = 300 (calibrated from the Elo scale).

- Problems below ZPD: too easy, no learning gain (boredom)
- Problems within ZPD: optimal difficulty, maximal learning (flow state)
- Problems above ZPD: too hard, frustration and abandonment

The ZPD serves as a **hard constraint** in Layer 3 (MAB): problems outside the student's ZPD are never recommended, regardless of MAB scores.

### 5.6 Multidimensional Elo (EDM 2025)

Recent work extends Elo to multiple dimensions — a student has separate Elo ratings for each concept/skill. This aligns naturally with our concept-based knowledge graph:

```
R_student = {R_arrays, R_sorting, R_recursion, R_dp, ...}
```

Each problem's Elo is associated with its primary concept. When a student attempts a problem tagged with "sorting," only their sorting Elo and the problem's sorting Elo are updated.

**Our approach:** Use multidimensional Elo (one rating per concept) to complement BKT. BKT gives P(mastery) for prerequisite checking; Elo gives difficulty-calibrated matching for problem selection.

---

## 6. Knowledge Graphs and Graph Neural Networks

### 6.1 Knowledge Graphs for Programming Concepts

A **Knowledge Graph (KG)** represents concepts as nodes and relationships (especially prerequisites) as directed edges. For a Python programming course:

```
variables → data_types → operators → control_flow → loops
                                                       ↓
                               functions → recursion → sorting → searching
                                    ↓                              ↓
                                   OOP → inheritance → polymorphism
                                    ↓
                         data_structures → linked_lists → trees → graphs
                                    ↓
                              algorithms → dynamic_programming → greedy
```

**Construction approaches:**
1. **Manual curation** by domain experts (most reliable but labor-intensive)
2. **Automated extraction** using NLP on textbooks/curricula (ACE methodology)
3. **Hybrid:** manual skeleton + automated refinement from student performance data

### 6.2 ACE — Automatic Concept Extraction

The ACE methodology (Chen et al., 2023) automates KG construction:
1. Parse course materials (textbook, slides, problem descriptions)
2. Extract key concepts using NLP (named entity recognition, keyword extraction)
3. Identify prerequisite relationships from section ordering, reference patterns
4. Validate using student performance data: if students who master concept A first perform better on concept B, then A → B is a valid prerequisite

### 6.3 GNN-Based Educational Recommendation

**Tripartite Graph Approach:**
Li et al. (2024) model the educational domain as a tripartite graph with three node types:
- Students, Resources (problems), Knowledge Points (concepts)
- Edges represent: student-attempts-problem, problem-covers-concept, student-masters-concept
- GNN propagates information along these edges to generate recommendations
- Results: NDCG@10 = 0.93, significantly outperforming collaborative filtering baselines

**Graph Attention + Deep RL for Learning Paths:**
Wang et al. (2024) combine Graph Attention Networks with Deep Reinforcement Learning:
- GAT learns concept representations from the KG
- Deep RL agent selects the optimal next concept to study
- Achieves 5.8–12.8 point improvement in test scores compared to fixed curricula

### 6.4 Prerequisite-Enhanced GNN (2024)

Pan et al. (2024) specifically model prerequisites in GNN:
- Prerequisite edges carry "readiness" weights based on student mastery
- A concept is "unlocked" only when all prerequisite concepts have readiness > threshold
- This prevents skipping foundational concepts and creates personalized learning paths

### 6.5 Application in This Thesis

Our knowledge graph serves three roles:
1. **BKT structure:** Defines the set of concepts tracked by knowledge tracing
2. **MAB constraint:** Only unlocked concepts (prerequisites mastered) are eligible for recommendation
3. **LLM context:** KG provides structured context for generating relevant hints

We use a **manually curated KG** for the Python programming curriculum, validated against the university's course outline. Automated construction (ACE) is left for future work.

---

## 7. Large Language Models in Education

### 7.1 LLMs as Tutoring Agents

Large Language Models (GPT-4, Claude, Gemini) have demonstrated strong capabilities in educational settings:

**PyTutor (2024):** A ChatGPT-based Intelligent Tutoring System for Python:
- Uses Socratic questioning: guides students toward the answer rather than giving it directly
- Maintains a dialogue state to track what the student understands
- Prompts are engineered to match pedagogical strategies (scaffolding, analogies, worked examples)
- Student satisfaction: 4.2/5.0 in usability studies

**Risks and challenges:**
- **Hallucination:** LLMs may generate incorrect code or explanations
- **Answer giving:** Without careful prompt engineering, LLMs tend to give direct answers rather than guiding discovery
- **Inconsistency:** Same question may get different quality responses on different attempts
- **Cost:** API calls for every hint interaction can be expensive at scale

### 7.2 RAG-Enhanced Educational Systems

**KG + RAG + LLM Hybrid (ScienceDirect, 2025):**

Chen et al. (2025) demonstrate a three-component architecture:
1. **Knowledge Graph** stores structured domain knowledge (concepts, prerequisites, common misconceptions)
2. **RAG** retrieves relevant KG subgraph based on student's current problem and knowledge state
3. **LLM** generates personalized feedback grounded in retrieved knowledge

Key finding: The hybrid approach outperforms both:
- Adaptive-only systems (better engagement due to natural language feedback)
- GenAI-only systems (better accuracy due to structured knowledge grounding)

**Multimodal KG + RAG ITS (Frontiers, 2026):**

Wang et al. (2026) extend the approach to multimodal:
- KG includes code examples, diagrams, and video explanations as node attributes
- RAG retrieves the most relevant modality based on student's learning style and current difficulty
- Results: 15% improvement in concept mastery compared to text-only tutoring

### 7.3 LLM Integration in This Thesis (Layer 5)

Our proposed LLM layer operates as follows:

**Trigger:** Student has ≥3 failed attempts on a problem

**Process:**
1. Retrieve student's knowledge state from BKT (what they know/don't know)
2. Retrieve the problem's concept prerequisites from KG
3. Identify likely gap: which prerequisite has lowest mastery?
4. Construct RAG context: concept description + common mistakes + student's submitted code
5. Prompt LLM for a Socratic hint (not the answer)

**Prompt template:**
```
The student is working on a {concept} problem. Their code:
{student_code}

Their error: {error_message}

Their mastery of prerequisites:
- {prereq_1}: {mastery_1}%
- {prereq_2}: {mastery_2}%

Generate a single Socratic question that guides them toward
identifying the issue. Do NOT give the answer directly.
Focus on the prerequisite with lowest mastery.
```

**This is an optional layer** — the thesis's core contribution is Layers 1–4. The LLM layer is implemented if time permits and is clearly marked as supplementary.

---

## 8. Summary and Research Gap Analysis

### 8.1 Synthesis of Reviewed Techniques

| Technique | Addresses | Limitation |
|-----------|-----------|------------|
| BKT/DKT | Models what student knows | Doesn't decide what to teach next |
| Elo/IRT | Calibrates difficulty | Doesn't model knowledge growth |
| MAB | Optimizes selection | Doesn't model knowledge or difficulty |
| FSRS | Models forgetting | Doesn't decide what to teach, only when to review |
| KG | Models concept relationships | Static structure, doesn't adapt |
| LLM | Generates natural feedback | No structured learning model |

**Key insight:** Each technique addresses one aspect of adaptive learning but has blind spots. An integrated system where each layer compensates for others' limitations is more powerful than any single technique.

### 8.2 The Integration Gap

No existing system — academic or commercial — integrates all five components:

**Academic systems** typically demonstrate one technique in isolation:
- BKT papers evaluate BKT accuracy but don't build a full recommendation system
- MAB papers assume a fixed difficulty model, not an adaptive one
- FSRS is developed for flashcard apps, never applied to programming exercises

**Commercial platforms** focus on scale, not pedagogical sophistication:
- LeetCode: no adaptation at all (user manually selects problems)
- Codeforces: Elo for competitive ranking, but no pedagogical use
- Duolingo: spaced repetition only, no knowledge tracing or MAB

### 8.3 Position of This Thesis

This thesis fills the integration gap by:
1. Building a **complete pipeline** where KT informs Elo, Elo constrains MAB, MAB respects KG, and FSRS schedules reviews
2. Applying this pipeline to **programming education** specifically, leveraging rich submission signals
3. Evaluating the **end-to-end system** rather than individual components in isolation
4. Providing an **open-source implementation** usable by other researchers and universities

---

## Key References by Section

*See [09-REFERENCES.md](./09-REFERENCES.md) for the complete bibliography.*

**Section 1 (Adaptive Learning):** Brusilovsky 2001, Paramythis 2004, Robins 2003, Luxton-Reilly 2018
**Section 2 (Knowledge Tracing):** Corbett & Anderson 1994, Piech 2015, Doan & Sahebi 2025, EDM 2025
**Section 3 (Spaced Repetition):** Ebbinghaus 1885, Wozniak 1990, Ye 2023, Settles 2016
**Section 4 (MAB):** Thompson 1933, Robbins 1952, Li 2010, Shen 2024
**Section 5 (Elo/IRT):** Elo 1978, Pelánek 2016, Springer 2025, Vygotsky 1978
**Section 6 (KG/GNN):** Chen 2023, Li 2024, Wang 2024, Pan 2024
**Section 7 (LLM):** Chen 2025, Wang 2026
