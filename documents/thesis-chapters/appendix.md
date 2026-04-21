# Appendices

The following appendices provide the complete evaluation instruments, knowledge graph specification, and prerequisite relationships referenced throughout Chapters 3, 4, and 5 of this thesis. Appendix A contains all assessment instruments used in the experimental evaluation: the pre-test, post-test, retention test, System Usability Scale questionnaire, Technology Acceptance Model survey, and semi-structured interview guides. Appendix B provides the full concept inventory and prerequisite edge list that constitute the knowledge graph described in Section 4.2.

---

# Appendix A: Evaluation Instruments

## A.1 Pre-Test Questionnaire

**Purpose:** Establish baseline programming proficiency for stratified randomization (Section 5.2.1).
**Format:** 20 questions --- 12 multiple-choice, 8 short-answer/code-writing.
**Time limit:** 60 minutes.
**Grading:** Multiple-choice items are auto-graded. Code-writing items are auto-graded via the platform's Docker sandbox against hidden test cases.
**Scoring:** Each question is worth 5 points (100 points total). Partial credit is awarded for code-writing questions based on the proportion of test cases passed.

### Tier 1: Basics (Variables, Data Types, I/O) --- 4 Questions

**Q1.** [Multiple Choice] What is the output of the following code?

```python
x = 5
print(x + 3)
```

A) 53 &emsp; B) 8 &emsp; C) Error &emsp; D) None

**Answer: B**

---

**Q2.** [Multiple Choice] What is the data type of the variable `result` after the following code executes?

```python
result = 10 / 3
```

A) int &emsp; B) float &emsp; C) str &emsp; D) bool

**Answer: B**

---

**Q3.** [Short Answer] Write a Python program that reads two integers from the user using `input()`, computes their sum, and prints the result in the format: `"The sum is: X"` where X is the computed sum.

**Sample Answer:**

```python
a = int(input())
b = int(input())
print(f"The sum is: {a + b}")
```

---

**Q4.** [Multiple Choice] What is the output of the following code?

```python
a = "3"
b = "7"
print(a + b)
```

A) 10 &emsp; B) 37 &emsp; C) "37" &emsp; D) Error

**Answer: B**

---

### Tier 2: Control Flow (Conditionals, Loops) --- 4 Questions

**Q5.** [Multiple Choice] What is the output of the following code?

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

A) A &emsp; B) B &emsp; C) C &emsp; D) B and C

**Answer: B**

---

**Q6.** [Short Answer] Write a Python program that prints all even numbers from 1 to 20 (inclusive), each on a separate line.

**Sample Answer:**

```python
for i in range(1, 21):
    if i % 2 == 0:
        print(i)
```

---

**Q7.** [Multiple Choice] How many times does the following loop execute?

```python
count = 0
i = 1
while i <= 100:
    if i % 3 == 0:
        count += 1
    i += 1
print(count)
```

A) 33 &emsp; B) 34 &emsp; C) 99 &emsp; D) 100

**Answer: A**

---

**Q8.** [Short Answer] Write a Python program that reads a positive integer `n` from the user and computes the sum $1 + 2 + 3 + \ldots + n$ using a `for` loop. Print the result.

**Sample Answer:**

```python
n = int(input())
total = 0
for i in range(1, n + 1):
    total += i
print(total)
```

---

### Tier 3: Functions (Definition, Parameters, Return Values) --- 4 Questions

**Q9.** [Multiple Choice] What is the output of the following code?

```python
def greet(name="World"):
    return f"Hello, {name}!"

print(greet())
print(greet("Python"))
```

A) Hello, World! / Hello, Python! &emsp; B) Hello, ! / Hello, Python! &emsp; C) Error &emsp; D) Hello, World! / Hello, World!

**Answer: A**

---

**Q10.** [Short Answer] Write a function `is_palindrome(s)` that takes a string `s` and returns `True` if the string reads the same forwards and backwards (case-insensitive), and `False` otherwise. Ignore spaces.

**Sample Answer:**

```python
def is_palindrome(s):
    cleaned = s.replace(" ", "").lower()
    return cleaned == cleaned[::-1]
```

---

**Q11.** [Multiple Choice] What does the following function return when called as `mystery(3, 4)`?

```python
def mystery(a, b):
    if a > b:
        return a
    else:
        return b
```

A) 3 &emsp; B) 4 &emsp; C) 7 &emsp; D) None

**Answer: B**

---

**Q12.** [Short Answer] Write a function `factorial(n)` that takes a non-negative integer `n` and returns $n!$ using a loop (not recursion). The function should return 1 when `n` is 0.

**Sample Answer:**

```python
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
```

---

### Tier 4: Data Structures (Lists, Dictionaries, Strings) --- 4 Questions

**Q13.** [Multiple Choice] What is the output of the following code?

```python
fruits = ["apple", "banana", "cherry", "date"]
print(fruits[1:3])
```

A) ["apple", "banana"] &emsp; B) ["banana", "cherry"] &emsp; C) ["banana", "cherry", "date"] &emsp; D) ["apple", "banana", "cherry"]

**Answer: B**

---

**Q14.** [Short Answer] Write a function `count_words(text)` that takes a string and returns a dictionary where keys are words (converted to lowercase) and values are the number of times each word appears.

**Sample Answer:**

```python
def count_words(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

---

**Q15.** [Multiple Choice] What is the output of the following code?

```python
d = {"a": 1, "b": 2, "c": 3}
d["b"] = 5
d["d"] = 4
print(len(d))
```

A) 3 &emsp; B) 4 &emsp; C) 5 &emsp; D) Error

**Answer: B**

---

**Q16.** [Short Answer] Write a function `remove_duplicates(lst)` that takes a list of integers and returns a new list with duplicates removed, preserving the original order of first occurrence.

**Sample Answer:**

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

---

### Tier 5: Algorithms (Sorting, Searching, Recursion) --- 4 Questions

**Q17.** [Multiple Choice] What is the time complexity of binary search on a sorted list of $n$ elements?

A) $O(1)$ &emsp; B) $O(\log n)$ &emsp; C) $O(n)$ &emsp; D) $O(n \log n)$

**Answer: B**

---

**Q18.** [Short Answer] Write a function `binary_search(arr, target)` that takes a sorted list `arr` and a target value. Return the index of the target if found, or -1 if not found. Use an iterative approach.

**Sample Answer:**

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

---

**Q19.** [Multiple Choice] What is the output of the following recursive function call `fib(5)`?

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

A) 3 &emsp; B) 5 &emsp; C) 8 &emsp; D) 13

**Answer: B**

---

**Q20.** [Short Answer] Write a function `bubble_sort(arr)` that sorts a list of integers in ascending order using the bubble sort algorithm. The function should modify the list in place and return it.

**Sample Answer:**

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

## A.2 Post-Test Questionnaire

**Purpose:** Measure learning gains after the four-week intervention period (Section 5.2.2). This is a parallel form to the pre-test: identical difficulty distribution and concept coverage, but with different items to prevent test-retest effects.
**Format:** 20 questions --- 12 multiple-choice, 8 short-answer/code-writing.
**Time limit:** 60 minutes.
**Grading:** Same as pre-test (Section A.1).

### Tier 1: Basics (Variables, Data Types, I/O) --- 4 Questions

**Q1.** [Multiple Choice] What is the output of the following code?

```python
y = 12
print(y - 4)
```

A) 124 &emsp; B) 8 &emsp; C) Error &emsp; D) None

**Answer: B**

---

**Q2.** [Multiple Choice] What is the value and type of `z` after executing the following code?

```python
z = 7 // 2
```

A) 3.5 (float) &emsp; B) 3 (int) &emsp; C) 4 (int) &emsp; D) 3 (float)

**Answer: B**

---

**Q3.** [Short Answer] Write a Python program that reads a person's name and age from the user using `input()`, then prints: `"Hello, [name]! You will be [age+1] next year."` where `[name]` and `[age+1]` are replaced by the actual values.

**Sample Answer:**

```python
name = input()
age = int(input())
print(f"Hello, {name}! You will be {age + 1} next year.")
```

---

**Q4.** [Multiple Choice] What is the output of the following code?

```python
x = "5"
y = 3
print(x * y)
```

A) 15 &emsp; B) "555" &emsp; C) 555 &emsp; D) Error

**Answer: C**

*Note: Python prints `555` without quotes; the string `"5"` is repeated 3 times.*

---

### Tier 2: Control Flow (Conditionals, Loops) --- 4 Questions

**Q5.** [Multiple Choice] What is the output of the following code?

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

A) A &emsp; B) B &emsp; C) C &emsp; D) F

**Answer: C**

---

**Q6.** [Short Answer] Write a Python program that prints all odd numbers from 1 to 25 (inclusive) in reverse order, each on a separate line. Start from 25 and go down to 1.

**Sample Answer:**

```python
for i in range(25, 0, -1):
    if i % 2 != 0:
        print(i)
```

---

**Q7.** [Multiple Choice] What value does the variable `total` hold after the following code executes?

```python
total = 0
for i in range(1, 6):
    if i % 2 == 0:
        total += i
```

A) 6 &emsp; B) 9 &emsp; C) 15 &emsp; D) 2

**Answer: A**

---

**Q8.** [Short Answer] Write a Python program that reads a positive integer `n` and prints the multiplication table for `n`, from `n * 1` to `n * 10`, with each line in the format: `"n x i = result"`.

**Sample Answer:**

```python
n = int(input())
for i in range(1, 11):
    print(f"{n} x {i} = {n * i}")
```

---

### Tier 3: Functions (Definition, Parameters, Return Values) --- 4 Questions

**Q9.** [Multiple Choice] What is the output of the following code?

```python
def add(a, b=10):
    return a + b

print(add(5))
print(add(5, 20))
```

A) 15 / 25 &emsp; B) 5 / 25 &emsp; C) Error &emsp; D) 15 / 15

**Answer: A**

---

**Q10.** [Short Answer] Write a function `count_vowels(s)` that takes a string `s` and returns the number of vowels (a, e, i, o, u --- case-insensitive) in the string.

**Sample Answer:**

```python
def count_vowels(s):
    return sum(1 for c in s.lower() if c in "aeiou")
```

---

**Q11.** [Multiple Choice] What is returned by `compute(10, 3)` given the following function?

```python
def compute(x, y):
    quotient = x // y
    remainder = x % y
    return quotient, remainder
```

A) 3 &emsp; B) (3, 1) &emsp; C) (3.33, 1) &emsp; D) Error

**Answer: B**

---

**Q12.** [Short Answer] Write a function `power(base, exp)` that computes `base` raised to the power `exp` using a loop (not using the `**` operator or `pow()`). Assume `exp` is a non-negative integer.

**Sample Answer:**

```python
def power(base, exp):
    result = 1
    for _ in range(exp):
        result *= base
    return result
```

---

### Tier 4: Data Structures (Lists, Dictionaries, Strings) --- 4 Questions

**Q13.** [Multiple Choice] What is the output of the following code?

```python
numbers = [10, 20, 30, 40, 50]
print(numbers[-2:])
```

A) [40, 50] &emsp; B) [30, 40] &emsp; C) [30, 40, 50] &emsp; D) [50]

**Answer: A**

---

**Q14.** [Short Answer] Write a function `invert_dict(d)` that takes a dictionary where all values are unique and returns a new dictionary with keys and values swapped.

**Sample Answer:**

```python
def invert_dict(d):
    return {v: k for k, v in d.items()}
```

---

**Q15.** [Multiple Choice] What is the output of the following code?

```python
inventory = {"apples": 5, "bananas": 3}
inventory["oranges"] = 7
del inventory["bananas"]
print(list(inventory.keys()))
```

A) ["apples", "oranges"] &emsp; B) ["apples", "bananas", "oranges"] &emsp; C) ["apples"] &emsp; D) Error

**Answer: A**

---

**Q16.** [Short Answer] Write a function `flatten(nested_list)` that takes a list of lists (one level deep) and returns a single flat list containing all elements in order.

**Sample Answer:**

```python
def flatten(nested_list):
    result = []
    for sublist in nested_list:
        result.extend(sublist)
    return result
```

---

### Tier 5: Algorithms (Sorting, Searching, Recursion) --- 4 Questions

**Q17.** [Multiple Choice] What is the best-case time complexity of insertion sort on a list of $n$ elements?

A) $O(1)$ &emsp; B) $O(n)$ &emsp; C) $O(n \log n)$ &emsp; D) $O(n^2)$

**Answer: B**

---

**Q18.** [Short Answer] Write a function `linear_search(arr, target)` that takes a list `arr` and a target value. Return the index of the first occurrence of the target, or -1 if not found.

**Sample Answer:**

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

---

**Q19.** [Multiple Choice] What is the output of `sum_recursive(4)` given the following function?

```python
def sum_recursive(n):
    if n == 0:
        return 0
    return n + sum_recursive(n - 1)
```

A) 4 &emsp; B) 6 &emsp; C) 10 &emsp; D) 24

**Answer: C**

---

**Q20.** [Short Answer] Write a function `selection_sort(arr)` that sorts a list of integers in ascending order using the selection sort algorithm. The function should modify the list in place and return it.

**Sample Answer:**

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

## A.3 Retention Test

**Purpose:** Assess long-term retention of concepts mastered during the intervention. Administered at Week 8, two weeks after the intervention ends (Section 5.2.2).
**Scope:** Concepts that students were expected to have mastered ($P(L_t) \geq 0.85$) during Weeks 2--5: variables, conditionals, loops, functions, lists.
**Format:** 10 questions --- 6 multiple-choice, 4 short-answer/code-writing.
**Time limit:** 30 minutes.
**Grading:** Same as pre-test (Section A.1). Each question is worth 10 points (100 points total).

---

**R1.** [Multiple Choice] What is the output of the following code?

```python
a = 8
b = a
a = 3
print(b)
```

A) 3 &emsp; B) 8 &emsp; C) Error &emsp; D) None

**Answer: B**

---

**R2.** [Multiple Choice] What is the output of the following code?

```python
x = -5
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")
```

A) positive &emsp; B) zero &emsp; C) negative &emsp; D) Error

**Answer: C**

---

**R3.** [Short Answer] Write a Python program that uses a `while` loop to compute the sum of all integers from 1 to 50 and prints the result.

**Sample Answer:**

```python
total = 0
i = 1
while i <= 50:
    total += i
    i += 1
print(total)
```

---

**R4.** [Multiple Choice] What is the output of the following code?

```python
for i in range(3):
    for j in range(2):
        print(f"{i},{j}", end=" ")
```

A) 0,0 0,1 1,0 1,1 2,0 2,1 &emsp; B) 0,0 1,1 2,2 &emsp; C) 0,0 0,1 0,2 1,0 1,1 1,2 &emsp; D) Error

**Answer: A**

---

**R5.** [Short Answer] Write a function `find_max(lst)` that takes a non-empty list of numbers and returns the largest number without using the built-in `max()` function.

**Sample Answer:**

```python
def find_max(lst):
    largest = lst[0]
    for num in lst[1:]:
        if num > largest:
            largest = num
    return largest
```

---

**R6.** [Multiple Choice] What does the following function return when called as `process([1, 2, 3, 4, 5])`?

```python
def process(lst):
    return [x ** 2 for x in lst if x % 2 != 0]
```

A) [1, 4, 9, 16, 25] &emsp; B) [1, 9, 25] &emsp; C) [4, 16] &emsp; D) [2, 4]

**Answer: B**

---

**R7.** [Short Answer] Write a function `reverse_list(lst)` that returns a new list containing the elements of `lst` in reverse order without using slicing, `reversed()`, or `.reverse()`.

**Sample Answer:**

```python
def reverse_list(lst):
    result = []
    for i in range(len(lst) - 1, -1, -1):
        result.append(lst[i])
    return result
```

---

**R8.** [Multiple Choice] What is the output of the following code?

```python
def add_item(lst, item):
    lst.append(item)
    return lst

original = [1, 2, 3]
new_list = add_item(original, 4)
print(len(original))
```

A) 3 &emsp; B) 4 &emsp; C) Error &emsp; D) None

**Answer: B**

---

**R9.** [Multiple Choice] What is the output of the following code?

```python
def greet(name):
    return "Hi, " + name

result = greet("Duong")
print(result.upper())
```

A) Hi, Duong &emsp; B) HI, DUONG &emsp; C) hi, duong &emsp; D) Error

**Answer: B**

---

**R10.** [Short Answer] Write a function `filter_passing(scores)` that takes a dictionary mapping student names (strings) to their scores (integers) and returns a list of names of students who scored 50 or above, sorted alphabetically.

**Sample Answer:**

```python
def filter_passing(scores):
    return sorted([name for name, score in scores.items() if score >= 50])
```

---

## A.4 System Usability Scale (SUS)

**Purpose:** Evaluate the perceived usability of the adaptive learning platform (RQ4).
**Source:** Brooke, J. (1996). "SUS: A quick and dirty usability scale." *Usability Evaluation in Industry*, 189--194.
**Adaptation:** Item wording is unchanged from the standard SUS instrument. The phrase "the system" refers to the adaptive learning platform.
**Scale:** Each item is rated on a 5-point Likert scale: 1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree.

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

For odd-numbered items (1, 3, 5, 7, 9 --- positive statements): subtract 1 from the raw score. For even-numbered items (2, 4, 6, 8, 10 --- negative statements): subtract the raw score from 5. Sum all ten adjusted scores and multiply by 2.5 to obtain the SUS score on a 0--100 scale. A SUS score above 68 is considered above average usability [51].

---

## A.5 Technology Acceptance Model (TAM) Survey

**Purpose:** Measure Perceived Usefulness (PU) and Perceived Ease of Use (PEOU) of the adaptive learning platform (RQ4).
**Theoretical basis:** Davis, F. D. (1989). "Perceived usefulness, perceived ease of use, and user acceptance of information technology." *MIS Quarterly*, 13(3), 319--340 [52].
**Adaptation:** Items are adapted from the original TAM instrument to reference specific features of the adaptive learning platform.
**Scale:** Each item is rated on a 7-point Likert scale: 1 = Strongly Disagree, 2 = Disagree, 3 = Somewhat Disagree, 4 = Neutral, 5 = Somewhat Agree, 6 = Agree, 7 = Strongly Agree.

### Perceived Usefulness (PU) --- 6 Items

PU1. Using the adaptive platform improved my programming skills more effectively than studying on my own.

PU2. The personalized problem recommendations saved me time compared to selecting problems manually.

PU3. The difficulty level of recommended problems matched my current ability level well.

PU4. The progress dashboard (mastery chart, Elo rating) helped me understand my strengths and weaknesses.

PU5. The review reminders helped me retain programming concepts that I had previously learned.

PU6. Overall, the adaptive features of the platform were useful for my learning.

### Perceived Ease of Use (PEOU) --- 6 Items

PEOU1. The platform interface was easy to navigate and understand.

PEOU2. I found it easy to submit code and view the execution results.

PEOU3. I found it easy to understand why the system recommended specific problems to me.

PEOU4. The mastery visualization (concept tree, radar chart) was easy to interpret.

PEOU5. Learning to use the platform required minimal effort.

PEOU6. Overall, I found the adaptive platform easy to use.

### Scoring Instructions

Compute the mean score for each subscale (PU and PEOU) by averaging the six items within each subscale. Report individual item means, subscale means, and standard deviations. Internal consistency is assessed using Cronbach's alpha, with $\alpha \geq 0.70$ as the threshold for acceptable reliability [53].

---

## A.6 Semi-Structured Interview Guide

**Purpose:** Gather qualitative insights into student experiences with the platform (RQ4).
**Sampling:** 10 students from the experimental group and 10 from the control group, selected to represent high, medium, and low learning gains based on pre-test/post-test difference.
**Recording:** Audio-recorded with participant consent; transcribed for thematic analysis [54].

### Experimental Group Interview Guide (~20 minutes)

**Opening.** Thank the participant. Remind them that the interview is confidential, that their name will be replaced with a code, and that there are no right or wrong answers.

**E1.** How would you describe your overall experience using the platform over the past four weeks?

**E2.** How did you feel about the problems the system recommended to you? Were they relevant to what you needed to learn?

**E3.** Did the recommended problems feel appropriately challenging --- not too easy and not too hard? Can you give a specific example?

**E4.** The platform tracked your mastery of each concept and displayed it on the dashboard. Did you find this information helpful? How did it influence your study behavior?

**E5.** The system sent you review reminders for concepts you had previously mastered. How did you experience these reminders? Did you find them useful or disruptive?

**E6.** Did you feel you were making measurable progress in your programming skills over the four weeks? What evidence do you point to?

**E7.** Have you used other programming learning platforms (e.g., LeetCode, HackerRank, Codelearn)? How does this platform compare?

**E8.** If you could change one thing about the platform, what would it be?

### Control Group Interview Guide (~15 minutes)

**Opening.** Same as experimental group.

**C1.** How would you describe your overall experience using the platform over the past four weeks?

**C2.** How did you go about selecting which problems to work on? What criteria did you use?

**C3.** Did you feel the problems you chose were at an appropriate difficulty level? Were there times when problems felt too easy or too hard?

**C4.** Did you feel you were making progress in your programming skills? How did you track your own progress?

**C5.** Was there anything about the platform that you wished worked differently, for example in how problems were organized or recommended?

**C6.** Have you used other programming learning platforms? How does this platform compare?

---

# Appendix B: Knowledge Graph Specification

## B.1 Complete Concept Inventory

The knowledge graph comprises 34 concepts organized into five difficulty tiers and seven topic groups. This taxonomy was curated manually based on the introductory Python programming curriculum at Hanoi University (Section 4.2.1). The concept names correspond to the `name` field in the `concepts` database table.

*Table B.1. Complete Concept Inventory*

| # | Concept Name | Display Name | Topic Group | Tier | Description |
|---|---|---|---|---|---|
| 1 | variables | Variables and Assignment | Basics | 1 | Variable declaration, assignment, naming conventions, and basic memory concepts |
| 2 | data_types | Data Types | Basics | 1 | Integers, floats, booleans, strings, type conversion, and type checking |
| 3 | operators | Operators and Expressions | Basics | 1 | Arithmetic, comparison, logical, and bitwise operators; operator precedence |
| 4 | io | Input and Output | Basics | 1 | Reading user input, printing output, string formatting, and f-strings |
| 5 | strings | String Operations | Basics | 1 | String methods, slicing, concatenation, formatting, and common string algorithms |
| 6 | conditionals | Conditional Statements | Control Flow | 1 | if/elif/else statements, boolean logic, nested conditionals, ternary expressions |
| 7 | loops | Loops | Control Flow | 1 | for loops, while loops, break, continue, range(), enumerate(), loop patterns |
| 8 | nested_loops | Nested Loops | Control Flow | 2 | Nested loop patterns, matrix traversal, pattern printing, time complexity implications |
| 9 | functions | Functions | Functions and Scope | 2 | Function definition, calling functions, docstrings, and function design principles |
| 10 | parameters | Parameters and Arguments | Functions and Scope | 2 | Positional args, keyword args, default values, *args, **kwargs |
| 11 | return_values | Return Values | Functions and Scope | 2 | Returning values, multiple return values, None, and function composition |
| 12 | lists | Lists | Data Structures | 2 | List creation, indexing, slicing, methods (append, insert, remove), list comprehensions |
| 13 | tuples | Tuples | Data Structures | 2 | Tuple creation, immutability, packing/unpacking, named tuples, tuple as dictionary keys |
| 14 | dictionaries | Dictionaries | Data Structures | 2 | Dict creation, access, methods, iteration, defaultdict, dict comprehensions |
| 15 | searching | Searching Algorithms | Algorithms | 2 | Linear search, binary search, search in sorted/unsorted arrays, search complexity |
| 16 | scope | Variable Scope | Functions and Scope | 3 | Local vs global scope, LEGB rule, closures, and the global/nonlocal keywords |
| 17 | recursion | Recursion | Functions and Scope | 3 | Recursive functions, base cases, recursive thinking, stack overflow, tail recursion |
| 18 | sets | Sets | Data Structures | 3 | Set creation, operations (union, intersection, difference), frozen sets, set comprehensions |
| 19 | stacks | Stacks | Data Structures | 3 | Stack data structure, LIFO principle, implementation using lists, applications |
| 20 | queues | Queues | Data Structures | 3 | Queue data structure, FIFO principle, deque, priority queues, BFS applications |
| 21 | classes | Classes and Objects | Object-Oriented Programming | 3 | Class definition, __init__, instance variables, methods, self parameter |
| 22 | sorting | Sorting Algorithms | Algorithms | 3 | Bubble sort, selection sort, insertion sort, merge sort, quicksort, sort stability |
| 23 | sliding_window | Sliding Window | Algorithms | 3 | Fixed and variable size sliding window, window sum/max/min, substring problems |
| 24 | inheritance | Inheritance | Object-Oriented Programming | 4 | Single inheritance, super(), method overriding, MRO, multiple inheritance basics |
| 25 | encapsulation | Encapsulation | Object-Oriented Programming | 4 | Public/private/protected attributes, properties, getters/setters, data hiding |
| 26 | polymorphism | Polymorphism | Object-Oriented Programming | 4 | Duck typing, method overriding, abstract classes, interfaces via ABC |
| 27 | two_pointers | Two Pointers Technique | Algorithms | 4 | Two pointer approach for sorted arrays, opposite direction, same direction patterns |
| 28 | greedy | Greedy Algorithms | Algorithms | 4 | Greedy choice property, activity selection, fractional knapsack, interval scheduling |
| 29 | divide_and_conquer | Divide and Conquer | Algorithms | 4 | Problem decomposition, merge sort, quicksort, binary search as D&C, recurrence relations |
| 30 | dynamic_programming | Dynamic Programming | Advanced | 5 | Memoization, tabulation, optimal substructure, overlapping subproblems, classic DP problems |
| 31 | graphs | Graphs | Advanced | 5 | Graph representation (adjacency list/matrix), BFS, DFS, shortest paths, connected components |
| 32 | trees | Trees | Advanced | 5 | Binary trees, BST, tree traversals (inorder, preorder, postorder), tree properties |
| 33 | backtracking | Backtracking | Advanced | 5 | Constraint satisfaction, permutations, combinations, N-Queens, sudoku solver concepts |
| 34 | bit_manipulation | Bit Manipulation | Advanced | 5 | Bitwise operators, bit masks, common bit tricks, XOR properties, power of two checks |

### Summary by Tier and Topic Group

*Table B.2. Concept Distribution by Tier and Topic Group*

| Topic Group | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 | Total |
|---|---|---|---|---|---|---|
| Basics | 5 | --- | --- | --- | --- | 5 |
| Control Flow | 2 | 1 | --- | --- | --- | 3 |
| Functions and Scope | --- | 3 | 2 | --- | --- | 5 |
| Data Structures | --- | 3 | 3 | --- | --- | 6 |
| Object-Oriented Programming | --- | --- | 1 | 3 | --- | 4 |
| Algorithms | --- | 1 | 2 | 3 | --- | 6 |
| Advanced | --- | --- | --- | --- | 5 | 5 |
| **Total** | **7** | **8** | **8** | **6** | **5** | **34** |

---

## B.2 Prerequisite Relationships

The knowledge graph contains 47 directed prerequisite edges. Each edge $(u, v)$ indicates that concept $u$ must be mastered ($P(L_t) \geq 0.85$) before concept $v$ becomes eligible for recommendation by the Hierarchical MAB (Section 3.3.5). The DAG property is enforced at the application level (Section 4.2.2). All edges have a default weight of 1.0; the weight field is reserved for future weighted prerequisite gating.

*Table B.3. Complete Prerequisite Edge List*

| # | From Concept | To Concept | Relation | Weight |
|---|---|---|---|---|
| 1 | variables | data_types | PREREQUISITE | 1.0 |
| 2 | variables | operators | PREREQUISITE | 1.0 |
| 3 | data_types | operators | PREREQUISITE | 1.0 |
| 4 | operators | conditionals | PREREQUISITE | 1.0 |
| 5 | conditionals | loops | PREREQUISITE | 1.0 |
| 6 | data_types | strings | PREREQUISITE | 1.0 |
| 7 | variables | io | PREREQUISITE | 1.0 |
| 8 | strings | io | PREREQUISITE | 1.0 |
| 9 | loops | nested_loops | PREREQUISITE | 1.0 |
| 10 | loops | functions | PREREQUISITE | 1.0 |
| 11 | loops | lists | PREREQUISITE | 1.0 |
| 12 | loops | searching | PREREQUISITE | 1.0 |
| 13 | strings | lists | PREREQUISITE | 1.0 |
| 14 | functions | parameters | PREREQUISITE | 1.0 |
| 15 | functions | return_values | PREREQUISITE | 1.0 |
| 16 | conditionals | functions | PREREQUISITE | 1.0 |
| 17 | lists | tuples | PREREQUISITE | 1.0 |
| 18 | lists | dictionaries | PREREQUISITE | 1.0 |
| 19 | return_values | searching | PREREQUISITE | 1.0 |
| 20 | parameters | return_values | PREREQUISITE | 1.0 |
| 21 | functions | scope | PREREQUISITE | 1.0 |
| 22 | return_values | recursion | PREREQUISITE | 1.0 |
| 23 | functions | recursion | PREREQUISITE | 1.0 |
| 24 | functions | classes | PREREQUISITE | 1.0 |
| 25 | dictionaries | classes | PREREQUISITE | 1.0 |
| 26 | lists | sets | PREREQUISITE | 1.0 |
| 27 | dictionaries | sets | PREREQUISITE | 1.0 |
| 28 | lists | stacks | PREREQUISITE | 1.0 |
| 29 | lists | queues | PREREQUISITE | 1.0 |
| 30 | lists | sorting | PREREQUISITE | 1.0 |
| 31 | searching | sorting | PREREQUISITE | 1.0 |
| 32 | lists | sliding_window | PREREQUISITE | 1.0 |
| 33 | nested_loops | sorting | PREREQUISITE | 1.0 |
| 34 | classes | inheritance | PREREQUISITE | 1.0 |
| 35 | classes | encapsulation | PREREQUISITE | 1.0 |
| 36 | sorting | two_pointers | PREREQUISITE | 1.0 |
| 37 | searching | two_pointers | PREREQUISITE | 1.0 |
| 38 | recursion | divide_and_conquer | PREREQUISITE | 1.0 |
| 39 | sorting | divide_and_conquer | PREREQUISITE | 1.0 |
| 40 | sorting | greedy | PREREQUISITE | 1.0 |
| 41 | inheritance | polymorphism | PREREQUISITE | 1.0 |
| 42 | encapsulation | polymorphism | PREREQUISITE | 1.0 |
| 43 | recursion | dynamic_programming | PREREQUISITE | 1.0 |
| 44 | recursion | backtracking | PREREQUISITE | 1.0 |
| 45 | recursion | trees | PREREQUISITE | 1.0 |
| 46 | stacks | trees | PREREQUISITE | 1.0 |
| 47 | recursion | graphs | PREREQUISITE | 1.0 |
| 48 | queues | graphs | PREREQUISITE | 1.0 |
| 49 | divide_and_conquer | dynamic_programming | PREREQUISITE | 1.0 |
| 50 | greedy | dynamic_programming | PREREQUISITE | 1.0 |
| 51 | operators | bit_manipulation | PREREQUISITE | 1.0 |
| 52 | conditionals | bit_manipulation | PREREQUISITE | 1.0 |

### Edge Statistics

- **Total edges:** 52
- **Intra-tier edges:** 11 (edges where both concepts belong to the same tier)
- **Cross-tier edges:** 41 (edges spanning different tiers)
- **Maximum in-degree:** 4 (dynamic_programming: recursion, divide_and_conquer, greedy; and polymorphism: inheritance, encapsulation)
- **Maximum out-degree:** 6 (recursion: divide_and_conquer, dynamic_programming, backtracking, trees, graphs; and lists: tuples, dictionaries, sets, stacks, queues, sorting, sliding_window)
- **Root concepts (in-degree 0):** variables (the single root of the entire DAG)
- **Leaf concepts (out-degree 0):** io, sliding_window, polymorphism, two_pointers, dynamic_programming, graphs, backtracking, bit_manipulation

The DAG has a longest path of length 9: variables $\to$ operators $\to$ conditionals $\to$ loops $\to$ functions $\to$ return_values $\to$ recursion $\to$ divide_and_conquer $\to$ dynamic_programming. This longest path corresponds to the maximum number of prerequisite concepts a student must master before reaching the most advanced concept in the graph, and informs the minimum number of interactions required for a student to progress through the entire curriculum.
