# Current Recommendation System Analysis

## Architecture Overview

The current system uses a **Content-Based Filtering** approach with **Sentence Transformer embeddings** and **pgvector cosine similarity**.

```
User solves problems
    -> Tags extracted from solved problems (e.g., "array", "hash-table")
    -> Each tag embedded via all-MiniLM-L6-v2 (384-dim vector)
    -> Weighted by difficulty (EASY=1, MEDIUM=2, HARD=3)
    -> Normalized to 0-1 range
    -> All skill vectors averaged into single profile vector
    -> Cosine similarity against problem embeddings
    -> Top-N most similar unsolved problems returned
```

## Technique Used

| Aspect | Current Approach |
|--------|-----------------|
| Embedding Model | all-MiniLM-L6-v2 (Sentence Transformers) |
| Vector Dimension | 384 |
| Similarity Metric | Cosine distance (pgvector `<=>` operator) |
| User Representation | Average of skill tag embeddings |
| Problem Representation | Embedding of `title + description + tags` |
| Skill Scoring | Difficulty-weighted sum, max-normalized |
| Cold Start | Fallback to newest unsolved problems |

## Critical Weaknesses

### 1. No Knowledge Tracing
The system does not model what the student **actually knows**. It only tracks what tags they have solved problems for. Solving one EASY "array" problem gives the same signal direction as mastering arrays completely.

### 2. No Difficulty Calibration
There is no mechanism to estimate if a problem is too easy or too hard for a specific student. The system recommends problems **similar** to what you've done, not problems at the **right difficulty level** for learning.

### 3. No Zone of Proximal Development (ZPD)
The system recommends problems most similar to the user's profile. This means it recommends more of what you already know, rather than problems that push you into your learning zone.

### 4. No Forgetting Model
If a student learned "recursion" 3 months ago but hasn't practiced since, the system still considers that skill as mastered. There is no decay or spaced repetition.

### 5. Naive Skill Aggregation
Averaging all skill embeddings into one vector loses information about individual skill levels. A student weak in "graphs" but strong in "arrays" gets a blended vector that may not accurately represent either.

### 6. No Exploration-Exploitation Balance
The system always exploits (recommends most similar). It never explores whether the student might benefit from a completely new topic they haven't tried.

### 7. No Prerequisite Awareness
The system doesn't know that "dynamic programming" requires understanding "recursion" first. It may recommend DP problems to a student who hasn't mastered recursion.

### 8. Binary Outcome Only
The system only uses ACCEPTED/not-ACCEPTED. It doesn't consider:
- How many attempts before success
- How long the student took
- What errors they made
- Whether they needed hints

## Verdict

The current approach is a **basic content-based recommender** — the same technique used in simple product recommendation systems (e.g., "users who bought X also bought Y"). It is **not suitable for educational recommendation** because it lacks pedagogical intelligence. It does not model learning, forgetting, difficulty, or prerequisite relationships.

For a thesis, this approach would be considered **outdated and insufficiently novel**. The educational data mining community moved beyond content-based filtering years ago.
