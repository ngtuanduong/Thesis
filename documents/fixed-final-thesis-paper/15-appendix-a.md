# APPENDIX A. EVALUATION INSTRUMENTS

## A.1. Overview

The pilot in Chapter 5 uses six instruments: a pre-test, a post-test, a retention test, a demographic survey, the System Usability Scale (SUS) [13], the Technology Acceptance Model (TAM) survey [14], and a semi-structured interview guide analysed thematically [15]. Pre-test and post-test are parallel forms — same difficulty distribution, different items — so change scores are comparable.

This appendix shows representative items so the reader can judge construct validity. The full instruments live in the companion file `appendix-a-companion-full-instruments.md`, which sits outside the page count.

## A.2. Pre-test (Sample Items)

The pre-test is 20 items, four per concept tier (Basics, Control Flow, Functions, Data Structures, Algorithms), mixing 12 multiple-choice and 8 short-answer/code-writing items. Time limit: 60 minutes; each item is worth 5 points. Multiple-choice items are auto-graded; short-answer items run in the platform's Docker sandbox against hidden test cases, with partial credit by proportion of cases passed. Three representative items follow.

**Q2 (Tier 1, multiple-choice).** What is the data type of `result` after `result = 10 / 3`? A) int B) float C) str D) bool. **Answer: B.**

**Q10 (Tier 3, short-answer).** Write `is_palindrome(s)` that returns `True` if `s` reads the same forwards and backwards (case-insensitive, ignoring spaces). Hidden cases: empty string, single-word palindrome, multi-word with spaces, non-palindrome.

**Q17 (Tier 5, multiple-choice).** What is the time complexity of binary search on a sorted list of *n* elements? A) O(1) B) O(log *n*) C) O(*n*) D) O(*n* log *n*). **Answer: B.**

## A.3. Post-test (Sample Items)

The post-test is a parallel form: same 5-tier structure, same item-type mix, same time limit, same scoring. Items differ from the pre-test to avoid test-retest effects. Three representative items follow.

**Q4 (Tier 1, multiple-choice).** What is printed by `x = "5"; y = 3; print(x * y)`? A) 15 B) "555" C) 555 D) Error. **Answer: C** — Python repeats the string `"5"` three times and prints without quotes.

**Q12 (Tier 3, short-answer).** Write `power(base, exp)` that computes `base ** exp` using a loop, without using `**` or `pow()`. Assume `exp` is a non-negative integer. Hidden cases include `exp = 0` (must return 1), `exp = 1`, and a large `exp`.

**Q19 (Tier 5, multiple-choice).** What does `sum_recursive(4)` return for a function that returns `0` when `n == 0` and `n + sum_recursive(n - 1)` otherwise? A) 4 B) 6 C) 10 D) 24. **Answer: C.**

## A.4. Retention Test (Sample Item)

The retention test is 10 items (6 multiple-choice, 4 short-answer), 30 minutes, 10 points each. It is administered in Week 8 — two weeks after the intervention ends — and covers only concepts the participant reached mastery on (P(L_t) ≥ 0.85) during Weeks 2–5: variables, conditionals, loops, functions, lists.

**R7 (short-answer).** Write `reverse_list(lst)` that returns a new list with the elements of `lst` in reverse order, without using slicing, `reversed()`, or `.reverse()`. Hidden cases: empty list, single-element list, multi-element list of mixed types.

## A.5. Demographic Survey (Question Topics)

The survey runs in Week 1 and feeds the covariates in §5.2.3:

- Year of study (1–4)
- Course of enrollment (Introduction to Programming / Data Structures / Algorithms)
- Prior CS coursework (none / introductory only / data structures or beyond)
- Self-rated programming experience (none / under 6 months / 6–12 months / over 12 months)
- Languages used before this course
- Competitive programming experience (yes/no; estimated rating if yes — used for the §5.2.1 exclusion)
- Hours of programming practice in a typical week
- Access to a personal computer outside class

Full question wording is in the companion file.

## A.6. System Usability Scale (SUS)

Usability is measured with the standard 10-item SUS [13]. Items alternate positive and negative phrasings on a 5-point Likert scale; "the system" refers to the adaptive learning platform with no other wording changes. Scoring follows Brooke: subtract 1 from odd-item raw scores, subtract even-item raw scores from 5, sum the ten adjusted values, multiply by 2.5 — yielding a 0–100 score. A SUS score above 68 is considered above-average usability. Full 10-item form in the companion file.

## A.7. Technology Acceptance Model (TAM)

User acceptance is measured with TAM Perceived Usefulness (PU) and Perceived Ease of Use (PEOU) [14]. Each subscale has six items on a 7-point Likert scale, adapted to reference specific platform features (recommendations, mastery dashboard, review reminders, mastery visualization). Subscale means are reported with standard deviations; internal consistency is checked with Cronbach's α, with α ≥ 0.70 as the acceptable-reliability threshold. Full 12-item form in the companion file.

## A.8. Semi-structured Interview Protocol

Interviews target 10 students per group, sampled to span low, medium, and high learning gains. Sessions run 15–20 minutes, audio-recorded with consent, and transcribed for thematic analysis [15]. Prepared themes: overall experience, perceived recommendation quality, perceived problem difficulty (Zone of Proximal Development), use of the mastery dashboard, experience of review reminders (experimental group only), perceived progress, comparison with prior platforms (LeetCode, HackerRank, Codelearn), and one-thing-to-change. The control guide drops recommendation- and FSRS-specific themes and asks how participants chose problems on their own. Full 8-item experimental and 6-item control guides in the companion file.

## A.9. Grading Rubric Summary

All three tests use a uniform rubric. Multiple-choice items are auto-graded as correct or incorrect. Short-answer code items run in the Docker sandbox against hidden test cases, with partial credit equal to (cases passed / total cases) × item weight. The FSRS rating used during the intervention applies the same correctness-and-effort logic in §4.6.1, Table 4.3 — correct first attempt within 120 s maps to Easy; correct but slow or after multiple attempts maps to Hard; a final wrong answer maps to Again — at finer granularity for review scheduling than the test score.

| Test | Items | Item value | Total |
|---|---|---|---|
| Pre-test | 20 | 5 pts | 100 |
| Post-test | 20 | 5 pts | 100 |
| Retention test | 10 | 10 pts | 100 |

## A.10. Companion File

Full instruments — 20-item pre-test, 20-item post-test, 10-item retention test, complete demographic survey, full SUS and TAM forms, and full interview guides — are in `appendix-a-companion-full-instruments.md`, outside the 70-page main paper count.
