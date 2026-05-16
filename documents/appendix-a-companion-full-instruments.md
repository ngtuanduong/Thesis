# Appendix A — Companion: Full Evaluation Instruments

This companion file accompanies the condensed Appendix A in `15-appendix-a.md`. It contains the full text of every evaluation instrument used in the pilot study described in Chapter 5: the complete 20-item pre-test, the parallel 20-item post-test, the 10-item retention test, the demographic survey, the System Usability Scale (SUS), the Technology Acceptance Model (TAM) survey, the semi-structured interview guides, and the grading rubric. This file sits outside the 70-page main paper count.

Citations follow the main paper's numbering: SUS [13], TAM [14], thematic analysis [15], FSRS retention rationale [25], G\*Power and effect-size conventions [55].

---

## A.1. Pre-test (Full)

**Purpose.** Establish baseline programming proficiency for stratified randomization (§5.2.1).

**Format.** 20 questions — 12 multiple-choice, 8 short-answer/code-writing.

**Time limit.** 60 minutes.

**Grading.** Multiple-choice items are auto-graded. Code-writing items are auto-graded via the platform's Docker sandbox against hidden test cases. Each question is worth 5 points (100 points total). Partial credit is awarded for code-writing items by proportion of test cases passed.

### Tier 1 — Basics (Variables, Data Types, I/O) — 4 questions

**Q1 (multiple-choice).** What is the output of the following code?

```python
x = 5
print(x + 3)
```

A) 53  B) 8  C) Error  D) None. **Answer: B.**

**Q2 (multiple-choice).** What is the data type of `result` after the following code executes?

```python
result = 10 / 3
```

A) int  B) float  C) str  D) bool. **Answer: B.**

**Q3 (short-answer).** Write a Python program that reads two integers from the user using `input()`, computes their sum, and prints the result in the format `"The sum is: X"` where X is the computed sum.

Sample answer:

```python
a = int(input())
b = int(input())
print(f"The sum is: {a + b}")
```

**Q4 (multiple-choice).** What is the output of the following code?

```python
a = "3"
b = "7"
print(a + b)
```

A) 10  B) 37  C) "37"  D) Error. **Answer: B.**

### Tier 2 — Control Flow (Conditionals, Loops) — 4 questions

**Q5 (multiple-choice).** What is the output of the following code?

```python
x = 15
if x > 20:
    print("A")
elif x > 10:
    print("B")
elif x > 5:
    print("C")
else:
    print("D")
```

A) A  B) B  C) C  D) B and C. **Answer: B.**

**Q6 (short-answer).** Write a Python program that prints all even numbers from 1 to 20 (inclusive), each on a separate line.

Sample answer:

```python
for i in range(1, 21):
    if i % 2 == 0:
        print(i)
```

**Q7 (multiple-choice).** How many times does the following loop execute?

```python
count = 0
i = 1
while i <= 100:
    if i % 3 == 0:
        count += 1
    i += 1
print(count)
```

A) 33  B) 34  C) 99  D) 100. **Answer: A.**

**Q8 (short-answer).** Write a Python program that reads a positive integer `n` from the user and computes the sum 1 + 2 + 3 + … + n using a `for` loop. Print the result.

Sample answer:

```python
n = int(input())
total = 0
for i in range(1, n + 1):
    total += i
print(total)
```

### Tier 3 — Functions (Definition, Parameters, Return Values) — 4 questions

**Q9 (multiple-choice).** What is the output of the following code?

```python
def greet(name="World"):
    return f"Hello, {name}!"

print(greet())
print(greet("Python"))
```

A) `Hello, World!` / `Hello, Python!`  B) `Hello, !` / `Hello, Python!`  C) Error  D) `Hello, World!` / `Hello, World!`. **Answer: A.**

**Q10 (short-answer).** Write a function `is_palindrome(s)` that takes a string `s` and returns `True` if the string reads the same forwards and backwards (case-insensitive), and `False` otherwise. Ignore spaces.

Sample answer:

```python
def is_palindrome(s):
    cleaned = s.replace(" ", "").lower()
    return cleaned == cleaned[::-1]
```

**Q11 (multiple-choice).** What does the following function return when called as `mystery(3, 4)`?

```python
def mystery(a, b):
    if a > b:
        return a
    else:
        return b
```

A) 3  B) 4  C) 7  D) None. **Answer: B.**

**Q12 (short-answer).** Write a function `factorial(n)` that takes a non-negative integer `n` and returns n! using a loop (not recursion). The function should return 1 when `n` is 0.

Sample answer:

```python
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
```

### Tier 4 — Data Structures (Lists, Dictionaries, Strings) — 4 questions

**Q13 (multiple-choice).** What is the output of the following code?

```python
fruits = ["apple", "banana", "cherry", "date"]
print(fruits[1:3])
```

A) `["apple", "banana"]`  B) `["banana", "cherry"]`  C) `["banana", "cherry", "date"]`  D) `["apple", "banana", "cherry"]`. **Answer: B.**

**Q14 (short-answer).** Write a function `count_words(text)` that takes a string and returns a dictionary where keys are words (converted to lowercase) and values are the number of times each word appears.

Sample answer:

```python
def count_words(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

**Q15 (multiple-choice).** What is the output of the following code?

```python
d = {"a": 1, "b": 2, "c": 3}
d["b"] = 5
d["d"] = 4
print(len(d))
```

A) 3  B) 4  C) 5  D) Error. **Answer: B.**

**Q16 (short-answer).** Write a function `remove_duplicates(lst)` that takes a list of integers and returns a new list with duplicates removed, preserving the original order of first occurrence.

Sample answer:

```python
def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```

### Tier 5 — Algorithms (Sorting, Searching, Recursion) — 4 questions

**Q17 (multiple-choice).** What is the time complexity of binary search on a sorted list of *n* elements?

A) O(1)  B) O(log *n*)  C) O(*n*)  D) O(*n* log *n*). **Answer: B.**

**Q18 (short-answer).** Write a function `binary_search(arr, target)` that takes a sorted list `arr` and a target value. Return the index of the target if found, or -1 if not found. Use an iterative approach.

Sample answer:

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**Q19 (multiple-choice).** What is the output of the following recursive function call `fib(5)`?

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

A) 3  B) 5  C) 8  D) 13. **Answer: B.**

**Q20 (short-answer).** Write a function `bubble_sort(arr)` that sorts a list of integers in ascending order using the bubble sort algorithm. The function should modify the list in place and return it.

Sample answer:

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

---

## A.2. Post-test (Full)

**Purpose.** Measure learning gains after the four-week intervention period (§5.2.2). The post-test is a parallel form to the pre-test: identical difficulty distribution and concept coverage, with different items to prevent test-retest effects.

**Format, time, grading.** Same as the pre-test (§A.1).

### Tier 1 — Basics (Variables, Data Types, I/O) — 4 questions

**Q1 (multiple-choice).** What is the output of the following code?

```python
y = 12
print(y - 4)
```

A) 124  B) 8  C) Error  D) None. **Answer: B.**

**Q2 (multiple-choice).** What is the value and type of `z` after executing the following code?

```python
z = 7 // 2
```

A) 3.5 (float)  B) 3 (int)  C) 4 (int)  D) 3 (float). **Answer: B.**

**Q3 (short-answer).** Write a Python program that reads a person's name and age from the user using `input()`, then prints `"Hello, [name]! You will be [age+1] next year."` where `[name]` and `[age+1]` are replaced by the actual values.

Sample answer:

```python
name = input()
age = int(input())
print(f"Hello, {name}! You will be {age + 1} next year.")
```

**Q4 (multiple-choice).** What is the output of the following code?

```python
x = "5"
y = 3
print(x * y)
```

A) 15  B) "555"  C) 555  D) Error. **Answer: C.** (Python prints `555` without quotes; the string `"5"` is repeated 3 times.)

### Tier 2 — Control Flow (Conditionals, Loops) — 4 questions

**Q5 (multiple-choice).** What is the output of the following code?

```python
score = 72
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
print(grade)
```

A) A  B) B  C) C  D) F. **Answer: C.**

**Q6 (short-answer).** Write a Python program that prints all odd numbers from 1 to 25 (inclusive) in reverse order, each on a separate line. Start from 25 and go down to 1.

Sample answer:

```python
for i in range(25, 0, -1):
    if i % 2 != 0:
        print(i)
```

**Q7 (multiple-choice).** What value does the variable `total` hold after the following code executes?

```python
total = 0
for i in range(1, 6):
    if i % 2 == 0:
        total += i
```

A) 6  B) 9  C) 15  D) 2. **Answer: A.**

**Q8 (short-answer).** Write a Python program that reads a positive integer `n` and prints the multiplication table for `n`, from `n * 1` to `n * 10`, with each line in the format `"n x i = result"`.

Sample answer:

```python
n = int(input())
for i in range(1, 11):
    print(f"{n} x {i} = {n * i}")
```

### Tier 3 — Functions (Definition, Parameters, Return Values) — 4 questions

**Q9 (multiple-choice).** What is the output of the following code?

```python
def add(a, b=10):
    return a + b

print(add(5))
print(add(5, 20))
```

A) 15 / 25  B) 5 / 25  C) Error  D) 15 / 15. **Answer: A.**

**Q10 (short-answer).** Write a function `count_vowels(s)` that takes a string `s` and returns the number of vowels (a, e, i, o, u — case-insensitive) in the string.

Sample answer:

```python
def count_vowels(s):
    return sum(1 for c in s.lower() if c in "aeiou")
```

**Q11 (multiple-choice).** What is returned by `compute(10, 3)` given the following function?

```python
def compute(x, y):
    quotient = x // y
    remainder = x % y
    return quotient, remainder
```

A) 3  B) (3, 1)  C) (3.33, 1)  D) Error. **Answer: B.**

**Q12 (short-answer).** Write a function `power(base, exp)` that computes `base` raised to the power `exp` using a loop (not using the `**` operator or `pow()`). Assume `exp` is a non-negative integer.

Sample answer:

```python
def power(base, exp):
    result = 1
    for _ in range(exp):
        result *= base
    return result
```

### Tier 4 — Data Structures (Lists, Dictionaries, Strings) — 4 questions

**Q13 (multiple-choice).** What is the output of the following code?

```python
numbers = [10, 20, 30, 40, 50]
print(numbers[-2:])
```

A) `[40, 50]`  B) `[30, 40]`  C) `[30, 40, 50]`  D) `[50]`. **Answer: A.**

**Q14 (short-answer).** Write a function `invert_dict(d)` that takes a dictionary where all values are unique and returns a new dictionary with keys and values swapped.

Sample answer:

```python
def invert_dict(d):
    return {v: k for k, v in d.items()}
```

**Q15 (multiple-choice).** What is the output of the following code?

```python
inventory = {"apples": 5, "bananas": 3}
inventory["oranges"] = 7
del inventory["bananas"]
print(list(inventory.keys()))
```

A) `["apples", "oranges"]`  B) `["apples", "bananas", "oranges"]`  C) `["apples"]`  D) Error. **Answer: A.**

**Q16 (short-answer).** Write a function `flatten(nested_list)` that takes a list of lists (one level deep) and returns a single flat list containing all elements in order.

Sample answer:

```python
def flatten(nested_list):
    result = []
    for sublist in nested_list:
        result.extend(sublist)
    return result
```

### Tier 5 — Algorithms (Sorting, Searching, Recursion) — 4 questions

**Q17 (multiple-choice).** What is the best-case time complexity of insertion sort on a list of *n* elements?

A) O(1)  B) O(*n*)  C) O(*n* log *n*)  D) O(*n*²). **Answer: B.**

**Q18 (short-answer).** Write a function `linear_search(arr, target)` that takes a list `arr` and a target value. Return the index of the first occurrence of the target, or -1 if not found.

Sample answer:

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

**Q19 (multiple-choice).** What is the output of `sum_recursive(4)` given the following function?

```python
def sum_recursive(n):
    if n == 0:
        return 0
    return n + sum_recursive(n - 1)
```

A) 4  B) 6  C) 10  D) 24. **Answer: C.**

**Q20 (short-answer).** Write a function `selection_sort(arr)` that sorts a list of integers in ascending order using the selection sort algorithm. The function should modify the list in place and return it.

Sample answer:

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

---

## A.3. Retention Test (Full)

**Purpose.** Assess short-term retention of concepts mastered during the intervention. Administered in Week 8, two weeks after the intervention ends (§5.2.2). Two weeks is short for forgetting-curve effects but is the minimum window in which FSRS stability differences become observable [25].

**Scope.** Concepts the participant reached mastery on (P(L_t) ≥ 0.85) during Weeks 2–5: variables, conditionals, loops, functions, lists.

**Format.** 10 questions — 6 multiple-choice, 4 short-answer/code-writing.

**Time limit.** 30 minutes. Each question is worth 10 points (100 points total). Grading follows the pre-test rubric.

**R1 (multiple-choice).** What is the output of the following code?

```python
a = 8
b = a
a = 3
print(b)
```

A) 3  B) 8  C) Error  D) None. **Answer: B.**

**R2 (multiple-choice).** What is the output of the following code?

```python
x = -5
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")
```

A) positive  B) zero  C) negative  D) Error. **Answer: C.**

**R3 (short-answer).** Write a Python program that uses a `while` loop to compute the sum of all integers from 1 to 50 and prints the result.

Sample answer:

```python
total = 0
i = 1
while i <= 50:
    total += i
    i += 1
print(total)
```

**R4 (multiple-choice).** What is the output of the following code?

```python
for i in range(3):
    for j in range(2):
        print(f"{i},{j}", end=" ")
```

A) `0,0 0,1 1,0 1,1 2,0 2,1`  B) `0,0 1,1 2,2`  C) `0,0 0,1 0,2 1,0 1,1 1,2`  D) Error. **Answer: A.**

**R5 (short-answer).** Write a function `find_max(lst)` that takes a non-empty list of numbers and returns the largest number without using the built-in `max()` function.

Sample answer:

```python
def find_max(lst):
    largest = lst[0]
    for num in lst[1:]:
        if num > largest:
            largest = num
    return largest
```

**R6 (multiple-choice).** What does the following function return when called as `process([1, 2, 3, 4, 5])`?

```python
def process(lst):
    return [x ** 2 for x in lst if x % 2 != 0]
```

A) `[1, 4, 9, 16, 25]`  B) `[1, 9, 25]`  C) `[4, 16]`  D) `[2, 4]`. **Answer: B.**

**R7 (short-answer).** Write a function `reverse_list(lst)` that returns a new list containing the elements of `lst` in reverse order without using slicing, `reversed()`, or `.reverse()`.

Sample answer:

```python
def reverse_list(lst):
    result = []
    for i in range(len(lst) - 1, -1, -1):
        result.append(lst[i])
    return result
```

**R8 (multiple-choice).** What is the output of the following code?

```python
def add_item(lst, item):
    lst.append(item)
    return lst

original = [1, 2, 3]
new_list = add_item(original, 4)
print(len(original))
```

A) 3  B) 4  C) Error  D) None. **Answer: B.**

**R9 (multiple-choice).** What is the output of the following code?

```python
def greet(name):
    return "Hi, " + name

result = greet("Duong")
print(result.upper())
```

A) `Hi, Duong`  B) `HI, DUONG`  C) `hi, duong`  D) Error. **Answer: B.**

**R10 (short-answer).** Write a function `filter_passing(scores)` that takes a dictionary mapping student names (strings) to their scores (integers) and returns a list of names of students who scored 50 or above, sorted alphabetically.

Sample answer:

```python
def filter_passing(scores):
    return sorted([name for name, score in scores.items() if score >= 50])
```

---

## A.4. Demographic Survey (Full)

**Purpose.** Capture covariates for §5.2.3 and the §5.2.1 exclusion check. Administered in Week 1 alongside the pre-test.

**Format.** Web form, single submission. No personally identifying information beyond a participant code is recorded; the code is generated at random by the platform.

1. Year of study: 1 / 2 / 3 / 4.
2. Course of enrollment: Introduction to Programming / Data Structures / Algorithms.
3. Have you taken any computer science courses before this one? None / Introductory programming only / Data structures, algorithms, or beyond.
4. How would you rate your prior programming experience? None / Under 6 months / 6–12 months / Over 12 months.
5. Which programming languages have you used before this course? (Open text — list all.)
6. Have you participated in competitive programming (e.g., Codeforces, ACM ICPC, school olympiad)? Yes / No.
7. If yes to question 6, what is your most recent estimated competitive programming rating (e.g., Codeforces rating)? (Open text — leave blank if not applicable.)
8. In a typical week, how many hours do you spend on programming practice outside of required class assignments? Under 1 / 1–3 / 4–7 / 8 or more.
9. Do you have access to a personal computer (laptop or desktop) outside class hours? Yes / No.
10. Optional: anything else you would like the researcher to know about your background? (Open text.)

Question 7 is the gate for the §5.2.1 exclusion criterion (estimated rating above 1600).

---

## A.5. System Usability Scale (SUS) — Full Form

**Source.** Brooke, J. (1996), "SUS: A quick and dirty usability scale," *Usability Evaluation in Industry*, 189–194 [13].

**Adaptation.** Item wording is unchanged from the standard SUS instrument. The phrase "the system" refers to the adaptive learning platform.

**Scale.** Each item is rated on a 5-point Likert scale: 1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree.

### SUS Items

1. I think that I would like to use this system frequently.
2. I found the system unnecessarily complex.
3. I thought the system was easy to use.
4. I think that I would need the support of a technical person to be able to use this system.
5. I found the various functions in this system were well integrated.
6. I thought there was too much inconsistency in this system.
7. I would imagine that most people would learn to use this system very quickly.
8. I found the system very cumbersome to use.
9. I felt very confident using the system.
10. I needed to learn a lot of things before I could get going with this system.

### Scoring Instructions

For odd-numbered items (1, 3, 5, 7, 9 — positive statements): subtract 1 from the raw score. For even-numbered items (2, 4, 6, 8, 10 — negative statements): subtract the raw score from 5. Sum all ten adjusted scores and multiply by 2.5 to obtain the SUS score on a 0–100 scale. A SUS score above 68 is considered above-average usability [13].

---

## A.6. Technology Acceptance Model (TAM) Survey — Full Form

**Theoretical basis.** Davis, F. D. (1989), "Perceived usefulness, perceived ease of use, and user acceptance of information technology," *MIS Quarterly*, 13(3), 319–340 [14].

**Adaptation.** Items are adapted from the original TAM instrument to reference specific features of the adaptive learning platform.

**Scale.** Each item is rated on a 7-point Likert scale: 1 = Strongly Disagree, 2 = Disagree, 3 = Somewhat Disagree, 4 = Neutral, 5 = Somewhat Agree, 6 = Agree, 7 = Strongly Agree.

### Perceived Usefulness (PU) — 6 items

- **PU1.** Using the adaptive platform improved my programming skills more effectively than studying on my own.
- **PU2.** The personalized problem recommendations saved me time compared to selecting problems manually.
- **PU3.** The difficulty level of recommended problems matched my current ability level well.
- **PU4.** The progress dashboard (mastery chart, Elo rating) helped me understand my strengths and weaknesses.
- **PU5.** The review reminders helped me retain programming concepts that I had previously learned.
- **PU6.** Overall, the adaptive features of the platform were useful for my learning.

### Perceived Ease of Use (PEOU) — 6 items

- **PEOU1.** The platform interface was easy to navigate and understand.
- **PEOU2.** I found it easy to submit code and view the execution results.
- **PEOU3.** I found it easy to understand why the system recommended specific problems to me.
- **PEOU4.** The mastery visualization (concept tree, radar chart) was easy to interpret.
- **PEOU5.** Learning to use the platform required minimal effort.
- **PEOU6.** Overall, I found the adaptive platform easy to use.

### Scoring Instructions

Compute the mean score for each subscale (PU and PEOU) by averaging the six items within each subscale. Report individual item means, subscale means, and standard deviations. Internal consistency is assessed using Cronbach's α, with α ≥ 0.70 as the threshold for acceptable reliability.

---

## A.7. Semi-structured Interview Guide (Full)

**Purpose.** Gather qualitative insights into student experiences with the platform (RQ4).

**Sampling.** 10 students from the experimental group and 10 from the control group, selected to represent high, medium, and low learning gains based on pre-/post-test difference.

**Recording.** Audio-recorded with participant consent; transcribed for thematic analysis [15].

### Experimental Group Interview Guide (~20 minutes)

**Opening.** Thank the participant. Remind them that the interview is confidential, that their name will be replaced with a code, and that there are no right or wrong answers.

- **E1.** How would you describe your overall experience using the platform over the past four weeks?
- **E2.** How did you feel about the problems the system recommended to you? Were they relevant to what you needed to learn?
- **E3.** Did the recommended problems feel appropriately challenging — not too easy and not too hard? Can you give a specific example?
- **E4.** The platform tracked your mastery of each concept and displayed it on the dashboard. Did you find this information helpful? How did it influence your study behavior?
- **E5.** The system sent you review reminders for concepts you had previously mastered. How did you experience these reminders? Did you find them useful or disruptive?
- **E6.** Did you feel you were making measurable progress in your programming skills over the four weeks? What evidence do you point to?
- **E7.** Have you used other programming learning platforms (for example, LeetCode, HackerRank, Codelearn)? How does this platform compare?
- **E8.** If you could change one thing about the platform, what would it be?

### Control Group Interview Guide (~15 minutes)

**Opening.** Same as experimental group.

- **C1.** How would you describe your overall experience using the platform over the past four weeks?
- **C2.** How did you go about selecting which problems to work on? What criteria did you use?
- **C3.** Did you feel the problems you chose were at an appropriate difficulty level? Were there times when problems felt too easy or too hard?
- **C4.** Did you feel you were making progress in your programming skills? How did you track your own progress?
- **C5.** Was there anything about the platform that you wished worked differently, for example in how problems were organized or recommended?
- **C6.** Have you used other programming learning platforms? How does this platform compare?

---

## A.8. Grading Rubric (Full)

**Multiple-choice items.** Auto-graded as correct (full item value) or incorrect (zero). No partial credit.

**Short-answer / code-writing items.** Submitted code runs in the platform's Docker sandbox against a fixed set of hidden test cases per item. The score for an item is

`score = item_value × (test_cases_passed / total_test_cases)`

rounded to one decimal place. Compilation or runtime errors that prevent any test case from running yield a score of zero for the item. Items have between 4 and 8 hidden test cases each, designed to cover normal cases, boundary conditions (empty input, single-element input, large input), and edge cases (negative numbers where applicable, type mismatches where the prompt allows them).

**Item value summary.**

| Test | Items | Item value | Total |
|---|---|---|---|
| Pre-test | 20 | 5 pts | 100 |
| Post-test | 20 | 5 pts | 100 |
| Retention test | 10 | 10 pts | 100 |

**Relation to FSRS rating during the intervention.** During Weeks 2–5, every submission also drives Layer 4 (FSRS) review scheduling. The submission-to-FSRS-rating mapping in §4.6.1, Table 4.3 uses the same correctness-and-effort signals at finer granularity: correct on the first attempt within 120 s maps to Easy (rating 4); correct in 120–300 s on the first attempt maps to Good (rating 3); correct but slow or after multiple attempts maps to Hard (rating 2); a final wrong answer maps to Again (rating 1). The graded test scores in §A.1–A.3 are not used as FSRS ratings — they measure outcomes; the FSRS rating measures the practice signal.

**Inter-rater reliability.** Multiple-choice and code-test scoring is fully automated and deterministic; no inter-rater check is needed. For interview thematic analysis, two coders code 20% of transcripts independently. Cohen's κ is computed; disagreements are resolved by discussion before the remaining 80% are coded by a single coder [15].
