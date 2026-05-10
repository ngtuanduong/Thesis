# Appendix B: Knowledge Graph Specification

## B.1 Complete Concept Inventory

The knowledge graph comprises 34 concepts organized into five difficulty tiers and seven topic groups. This taxonomy was curated manually based on the introductory Python programming curriculum at Hanoi University (Section 4.2.1). The concept names correspond to the `name` field in the `concepts` database table.

*Table B.1. Complete Concept Inventory*

| **#** | **Concept Name** | **Display Name** | **Topic Group** | **Tier** | **Description** |
| --- | --- | --- | --- | --- | --- |
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

### **Summary by Tier and Topic Group**

*Table B.2. Concept Distribution by Tier and Topic Group*

| **Topic Group** | **Tier 1** | **Tier 2** | **Tier 3** | **Tier 4** | **Tier 5** | **Total** |
| --- | --- | --- | --- | --- | --- | --- |
| Basics | 5 | — | — | — | — | 5 |
| Control Flow | 2 | 1 | — | — | — | 3 |
| Functions and Scope | — | 3 | 2 | — | — | 5 |
| Data Structures | — | 3 | 3 | — | — | 6 |
| Object-Oriented Programming | — | — | 1 | 3 | — | 4 |
| Algorithms | — | 1 | 2 | 3 | — | 6 |
| Advanced | — | — | — | — | 5 | 5 |
| Total | 7 | 8 | 8 | 6 | 5 | 34 |

## B.2 Prerequisite Relationships

The knowledge graph contains 47 directed prerequisite edges. Each edge (u, v) indicates that concept u must be mastered (P(L_t) \\geq 0.85) before concept v becomes eligible for recommendation by the Hierarchical MAB (Section 3.3.5). The DAG property is enforced at the application level (Section 4.2.2). All edges have a default weight of 1.0; the weight field is reserved for future weighted prerequisite gating.

*Table B.3. Complete Prerequisite Edge List*

| **#** | **From Concept** | **To Concept** | **Relation** | **Weight** |
| --- | --- | --- | --- | --- |
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

### **Edge Statistics**

- **Total edges:** 52 - **Intra-tier edges:** 11 (edges where both concepts belong to the same tier) - **Cross-tier edges:** 41 (edges spanning different tiers) - **Maximum in-degree:** 4 (dynamic_programming: recursion, divide_and_conquer, greedy; and polymorphism: inheritance, encapsulation) - **Maximum out-degree:** 6 (recursion: divide_and_conquer, dynamic_programming, backtracking, trees, graphs; and lists: tuples, dictionaries, sets, stacks, queues, sorting, sliding_window) - **Root concepts (in-degree 0):** variables (the single root of the entire DAG) - **Leaf concepts (out-degree 0):** io, sliding_window, polymorphism, two_pointers, dynamic_programming, graphs, backtracking, bit_manipulation

The DAG has a longest path of length 9: variables → operators → conditionals → loops → functions → return_values → recursion → divide_and_conquer → dynamic_programming. This longest path corresponds to the maximum number of prerequisite concepts a student must master before reaching the most advanced concept in the graph, and informs the minimum number of interactions required for a student to progress through the entire curriculum.

**Khung bài tham luận 15 phút + 5 phút thảo luận**

**Slide 1 — Problem and motivation (1.5 phút)**

- Vấn đề: lớp lập trình đông, chênh lệch đầu vào, khó cá nhân hóa.

- 1 câu chốt: existing platforms are rich in content but poor in adaptive pedagogy.Mục tiêu: giúp người nghe hiểu “vì sao đề tài này đáng làm”.

**Slide 2 — What exactly this thesis does and does not do (1 phút)**

- **Does:** design, implement, deploy a working adaptive platform.

- **Does not yet:** report classroom intervention outcomes.Đây là slide cực quan trọng để khóa kỳ vọng ban giám khảo ngay từ đầu.

**Slide 3 — Academic contribution in one slide (2 phút)**

Chỉ nói 2 contribution:

1. **An integrated adaptive learning platform**

2. **A pilot evaluation protocol for future empirical validation**Bên dưới mỗi contribution, ghi 1 dòng cực cụ thể:

- Contribution 1 = BKT + Dynamic Elo + H-MAB + FSRS + knowledge graph + deployable system

- Contribution 2 = between-subjects pilot design + metrics + analysis plan + threats to validityĐây là slide để giám khảo thấy “đóng góp học thuật là gì”.

**Slide 4 — Architecture and closed-loop logic (2 phút)**

Dùng Figure 1.3 + workflow.Nói thật ngắn:

- BKT estimates mastery

- Elo calibrates difficulty

- H-MAB chooses next concept/problem

- FSRS schedules review

- All are coordinated by a knowledge graphĐây là “linh hồn học thuật” của bài.

**Slide 5 — What was actually implemented (2.5 phút)**

Đưa bằng chứng kỹ thuật thật:

- working full-stack system

- code execution sandbox

- feature flags for pilot/control

- dashboard / recommendation page / review queue

- roughly 2,500 Python + 4,000 NestJS TS + 3,000 React TSBan giám khảo phải thấy đây không chỉ là “ý tưởng”.

**Slide 6 — Technical decisions that matter academically (2 phút)**

Chọn đúng 3 chi tiết, không hơn:

- mastery threshold 0.85

- dynamic K in Elo

- reward function combining learning gain, difficulty match, efficiencyĐây là slide biến bài từ “làm app” thành “có decision-making mang tính nghiên cứu”.

**Slide 7 — Evaluation protocol and what claims are justified (2 phút)**

- pilot design: control vs adaptive group

- metrics: NLG, AUC, engagement, SUS/TAM

- nhưng **no classroom outcomes yet**

- any future findings should be read as preliminary evidenceSlide này phải rất trung thực.

**Slide 8 — Takeaway and discussion prompts (2 phút)**

One-sentence takeaway:**“The thesis contributes a working adaptive programming-learning platform and a rigorous pilot protocol; its next step is empirical classroom validation.”**Bên dưới gợi sẵn 2 câu hỏi thảo luận:

- Which component is most important to validate first in a real classroom?

- How should future studies isolate the effects of BKT/Elo/MAB/FSRS more cleanly?Cách này sẽ làm phần hỏi đáp có giá trị hơn, thay vì chỉ hỏi vụ format hay thiếu result.


---

**4) Để phần thảo luận 5 phút thực sự giá trị: chuẩn bị trước 4 câu khó**

**Câu 1: “Why are there no experimental results yet?”**Trả lời: *Because the thesis is scoped as an implementation study with a pilot evaluation protocol; the classroom intervention is the next phase, not falsely reported as completed here.*

**Câu 2: “What is the academic contribution, not just the software?”**Trả lời: *The academic contribution lies in operationalizing four adaptive mechanisms into one closed loop for programming education, with explicit interaction logic and a measurable evaluation design.*

**Câu 3: “Why did you choose BKT instead of DKT2?”**Trả lời: *Because this pilot setting has limited data and requires interpretable mastery probabilities for prerequisite gating; BKT is a pragmatic and theoretically grounded choice.*

**Câu 4: “Can you claim H-MAB or FSRS individually works?”**Trả lời: *No. The current design evaluates the integrated platform as a whole; individual causal effects remain future work.*
