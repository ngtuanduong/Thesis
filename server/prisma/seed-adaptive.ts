import { PrismaClient, Difficulty } from '@prisma/client';
import { generateStarterCode } from '../src/problems/starter-code.util';
import { TIER1, TIER2, TIER3, TIER4, TIER5 } from './problems';
import type { ProblemDef } from './problems/types';

const prisma = new PrismaClient();

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000';

// ============================================================
// Concept Taxonomy (~35 concepts, organized by tier)
// ============================================================

interface ConceptDef {
  name: string;
  displayName: string;
  description: string;
  topicGroup: string;
  difficultyTier: number;
}

const CONCEPTS: ConceptDef[] = [
  // Tier 1 — Foundations (7 concepts)
  { name: 'variables', displayName: 'Variables and Assignment', description: 'Variable declaration, assignment, naming conventions, and basic memory concepts.', topicGroup: 'basics', difficultyTier: 1 },
  { name: 'data_types', displayName: 'Data Types', description: 'Integers, floats, booleans, strings, type conversion, and type checking.', topicGroup: 'basics', difficultyTier: 1 },
  { name: 'operators', displayName: 'Operators and Expressions', description: 'Arithmetic, comparison, logical, and bitwise operators. Operator precedence.', topicGroup: 'basics', difficultyTier: 1 },
  { name: 'io', displayName: 'Input and Output', description: 'Reading user input, printing output, string formatting, and f-strings.', topicGroup: 'basics', difficultyTier: 1 },
  { name: 'strings', displayName: 'String Operations', description: 'String methods, slicing, concatenation, formatting, and common string algorithms.', topicGroup: 'basics', difficultyTier: 1 },
  { name: 'conditionals', displayName: 'Conditional Statements', description: 'if/elif/else statements, boolean logic, nested conditionals, ternary expressions.', topicGroup: 'control_flow', difficultyTier: 1 },
  { name: 'loops', displayName: 'Loops', description: 'for loops, while loops, break, continue, range(), enumerate(), loop patterns.', topicGroup: 'control_flow', difficultyTier: 1 },

  // Tier 2 — Core Skills (8 concepts)
  { name: 'nested_loops', displayName: 'Nested Loops', description: 'Nested loop patterns, matrix traversal, pattern printing, time complexity implications.', topicGroup: 'control_flow', difficultyTier: 2 },
  { name: 'functions', displayName: 'Functions', description: 'Function definition, calling functions, docstrings, and function design principles.', topicGroup: 'functions', difficultyTier: 2 },
  { name: 'parameters', displayName: 'Parameters and Arguments', description: 'Positional args, keyword args, default values, *args, **kwargs.', topicGroup: 'functions', difficultyTier: 2 },
  { name: 'return_values', displayName: 'Return Values', description: 'Returning values, multiple return values, None, and function composition.', topicGroup: 'functions', difficultyTier: 2 },
  { name: 'lists', displayName: 'Lists', description: 'List creation, indexing, slicing, methods (append, insert, remove), list comprehensions.', topicGroup: 'data_structures', difficultyTier: 2 },
  { name: 'tuples', displayName: 'Tuples', description: 'Tuple creation, immutability, packing/unpacking, named tuples, tuple as dictionary keys.', topicGroup: 'data_structures', difficultyTier: 2 },
  { name: 'dictionaries', displayName: 'Dictionaries', description: 'Dict creation, access, methods, iteration, defaultdict, dict comprehensions.', topicGroup: 'data_structures', difficultyTier: 2 },
  { name: 'searching', displayName: 'Searching Algorithms', description: 'Linear search, binary search, search in sorted/unsorted arrays, search complexity.', topicGroup: 'algorithms', difficultyTier: 2 },

  // Tier 3 — Intermediate (8 concepts)
  { name: 'scope', displayName: 'Variable Scope', description: 'Local vs global scope, LEGB rule, closures, and the global/nonlocal keywords.', topicGroup: 'functions', difficultyTier: 3 },
  { name: 'recursion', displayName: 'Recursion', description: 'Recursive functions, base cases, recursive thinking, stack overflow, tail recursion.', topicGroup: 'functions', difficultyTier: 3 },
  { name: 'sets', displayName: 'Sets', description: 'Set creation, operations (union, intersection, difference), frozen sets, set comprehensions.', topicGroup: 'data_structures', difficultyTier: 3 },
  { name: 'stacks', displayName: 'Stacks', description: 'Stack data structure, LIFO principle, implementation using lists, applications.', topicGroup: 'data_structures', difficultyTier: 3 },
  { name: 'queues', displayName: 'Queues', description: 'Queue data structure, FIFO principle, deque, priority queues, BFS applications.', topicGroup: 'data_structures', difficultyTier: 3 },
  { name: 'classes', displayName: 'Classes and Objects', description: 'Class definition, __init__, instance variables, methods, self parameter.', topicGroup: 'oop', difficultyTier: 3 },
  { name: 'sorting', displayName: 'Sorting Algorithms', description: 'Bubble sort, selection sort, insertion sort, merge sort, quicksort, sort stability.', topicGroup: 'algorithms', difficultyTier: 3 },
  { name: 'sliding_window', displayName: 'Sliding Window', description: 'Fixed and variable size sliding window, window sum/max/min, substring problems.', topicGroup: 'algorithms', difficultyTier: 3 },

  // Tier 4 — Advanced Application (6 concepts)
  { name: 'inheritance', displayName: 'Inheritance', description: 'Single inheritance, super(), method overriding, MRO, multiple inheritance basics.', topicGroup: 'oop', difficultyTier: 4 },
  { name: 'encapsulation', displayName: 'Encapsulation', description: 'Public/private/protected attributes, properties, getters/setters, data hiding.', topicGroup: 'oop', difficultyTier: 4 },
  { name: 'polymorphism', displayName: 'Polymorphism', description: 'Duck typing, method overriding, abstract classes, interfaces via ABC.', topicGroup: 'oop', difficultyTier: 4 },
  { name: 'two_pointers', displayName: 'Two Pointers Technique', description: 'Two pointer approach for sorted arrays, opposite direction, same direction patterns.', topicGroup: 'algorithms', difficultyTier: 4 },
  { name: 'greedy', displayName: 'Greedy Algorithms', description: 'Greedy choice property, activity selection, fractional knapsack, interval scheduling.', topicGroup: 'algorithms', difficultyTier: 4 },
  { name: 'divide_and_conquer', displayName: 'Divide and Conquer', description: 'Problem decomposition, merge sort, quicksort, binary search as D&C, recurrence relations.', topicGroup: 'algorithms', difficultyTier: 4 },

  // Tier 5 — Expert (5 concepts)
  { name: 'dynamic_programming', displayName: 'Dynamic Programming', description: 'Memoization, tabulation, optimal substructure, overlapping subproblems, classic DP problems.', topicGroup: 'advanced', difficultyTier: 5 },
  { name: 'graphs', displayName: 'Graphs', description: 'Graph representation (adjacency list/matrix), BFS, DFS, shortest paths, connected components.', topicGroup: 'advanced', difficultyTier: 5 },
  { name: 'trees', displayName: 'Trees', description: 'Binary trees, BST, tree traversals (inorder, preorder, postorder), tree properties.', topicGroup: 'advanced', difficultyTier: 5 },
  { name: 'backtracking', displayName: 'Backtracking', description: 'Constraint satisfaction, permutations, combinations, N-Queens, sudoku solver concepts.', topicGroup: 'advanced', difficultyTier: 5 },
  { name: 'bit_manipulation', displayName: 'Bit Manipulation', description: 'Bitwise operators, bit masks, common bit tricks, XOR properties, power of two checks.', topicGroup: 'advanced', difficultyTier: 5 },
];

// ============================================================
// Prerequisite Edges (from → to means "from" is prerequisite of "to")
// ============================================================

interface EdgeDef {
  from: string;
  to: string;
}

const PREREQUISITE_EDGES: EdgeDef[] = [
  // Within Tier 1 (intra-tier, pedagogical order)
  { from: 'variables', to: 'data_types' },
  { from: 'variables', to: 'operators' },
  { from: 'data_types', to: 'operators' },
  { from: 'operators', to: 'conditionals' },
  { from: 'conditionals', to: 'loops' },
  { from: 'data_types', to: 'strings' },
  { from: 'variables', to: 'io' },
  { from: 'strings', to: 'io' },

  // Tier 1 → Tier 2
  { from: 'loops', to: 'nested_loops' },
  { from: 'loops', to: 'functions' },
  { from: 'loops', to: 'lists' },
  { from: 'loops', to: 'searching' },
  { from: 'strings', to: 'lists' },
  { from: 'functions', to: 'parameters' },
  { from: 'functions', to: 'return_values' },
  { from: 'conditionals', to: 'functions' },

  // Tier 2 → Tier 2 (intra-tier)
  { from: 'lists', to: 'tuples' },
  { from: 'lists', to: 'dictionaries' },
  { from: 'return_values', to: 'searching' },
  { from: 'parameters', to: 'return_values' },

  // Tier 2 → Tier 3
  { from: 'functions', to: 'scope' },
  { from: 'return_values', to: 'recursion' },
  { from: 'functions', to: 'recursion' },
  { from: 'functions', to: 'classes' },
  { from: 'dictionaries', to: 'classes' },
  { from: 'lists', to: 'sets' },
  { from: 'dictionaries', to: 'sets' },
  { from: 'lists', to: 'stacks' },
  { from: 'lists', to: 'queues' },
  { from: 'lists', to: 'sorting' },
  { from: 'searching', to: 'sorting' },
  { from: 'lists', to: 'sliding_window' },
  { from: 'nested_loops', to: 'sorting' },

  // Tier 3 → Tier 4
  { from: 'classes', to: 'inheritance' },
  { from: 'classes', to: 'encapsulation' },
  { from: 'sorting', to: 'two_pointers' },
  { from: 'searching', to: 'two_pointers' },
  { from: 'recursion', to: 'divide_and_conquer' },
  { from: 'sorting', to: 'divide_and_conquer' },
  { from: 'sorting', to: 'greedy' },

  // Tier 4 → Tier 4 (intra-tier)
  { from: 'inheritance', to: 'polymorphism' },
  { from: 'encapsulation', to: 'polymorphism' },

  // Tier 3/4 → Tier 5
  { from: 'recursion', to: 'dynamic_programming' },
  { from: 'recursion', to: 'backtracking' },
  { from: 'recursion', to: 'trees' },
  { from: 'stacks', to: 'trees' },
  { from: 'recursion', to: 'graphs' },
  { from: 'queues', to: 'graphs' },
  { from: 'divide_and_conquer', to: 'dynamic_programming' },
  { from: 'greedy', to: 'dynamic_programming' },

  // Cross-tier long edge (T1 → T5)
  { from: 'operators', to: 'bit_manipulation' },
  { from: 'conditionals', to: 'bit_manipulation' },
];

// ============================================================
// Legacy Problems (25 problems covering the concept taxonomy)
// Kept inline during migration; will be moved into ./problems/tier*-*.ts in later phases.
// ============================================================

const NEW_PROBLEMS: ProblemDef[] = [
  // === Tier 1: Basics ===
  {
    title: 'Swap Two Variables',
    description: `Write a function \`swap(a, b)\` that takes two values and returns them in swapped order.

**Example:**
\`\`\`
Input: a = 5, b = 10
Output: (10, 5)
\`\`\`

**Note:** Return the result as a tuple.`,
    difficulty: Difficulty.EASY,
    primaryConcept: 'variables',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ a: 5, b: 10 }), expected: JSON.stringify([10, 5]), isHidden: false },
      { input: JSON.stringify({ a: 0, b: 0 }), expected: JSON.stringify([0, 0]), isHidden: false },
      { input: JSON.stringify({ a: -1, b: 1 }), expected: JSON.stringify([1, -1]), isHidden: true },
      { input: JSON.stringify({ a: 100, b: 200 }), expected: JSON.stringify([200, 100]), isHidden: true },
      { input: JSON.stringify({ a: 3, b: 7 }), expected: JSON.stringify([7, 3]), isHidden: true },
    ],
  },
  {
    title: 'Type Checker',
    description: `Write a function \`check_type(value)\` that returns a string describing the type of the input value.

Return one of: "integer", "float", "string", "boolean", "list", or "other".

**Example:**
\`\`\`
Input: value = 42
Output: "integer"

Input: value = 3.14
Output: "float"

Input: value = "hello"
Output: "string"
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'data_types',
    secondaryConcepts: ['conditionals'],
    testCases: [
      { input: JSON.stringify({ value: 42 }), expected: '"integer"', isHidden: false },
      { input: JSON.stringify({ value: 3.14 }), expected: '"float"', isHidden: false },
      { input: JSON.stringify({ value: 'hello' }), expected: '"string"', isHidden: false },
      { input: JSON.stringify({ value: true }), expected: '"boolean"', isHidden: true },
      { input: JSON.stringify({ value: [1, 2, 3] }), expected: '"list"', isHidden: true },
    ],
  },
  {
    title: 'Simple Calculator',
    description: `Write a function \`calculate(a, b, op)\` that performs basic arithmetic operations.

The \`op\` parameter is a string: "+", "-", "*", or "/".
For division by zero, return "Error".

**Example:**
\`\`\`
Input: a = 10, b = 3, op = "+"
Output: 13

Input: a = 10, b = 0, op = "/"
Output: "Error"
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'operators',
    secondaryConcepts: ['conditionals'],
    testCases: [
      { input: JSON.stringify({ a: 10, b: 3, op: '+' }), expected: '13', isHidden: false },
      { input: JSON.stringify({ a: 10, b: 3, op: '-' }), expected: '7', isHidden: false },
      { input: JSON.stringify({ a: 10, b: 3, op: '*' }), expected: '30', isHidden: false },
      { input: JSON.stringify({ a: 10, b: 0, op: '/' }), expected: '"Error"', isHidden: true },
      { input: JSON.stringify({ a: 15, b: 4, op: '/' }), expected: '3.75', isHidden: true },
    ],
  },
  {
    title: 'String Reversal',
    description: `Write a function \`reverse_string(s)\` that returns the reverse of a given string without using the built-in reverse function or slicing shortcut ([::-1]).

**Example:**
\`\`\`
Input: s = "hello"
Output: "olleh"

Input: s = "Python"
Output: "nohtyP"
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'strings',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ s: 'hello' }), expected: '"olleh"', isHidden: false },
      { input: JSON.stringify({ s: 'Python' }), expected: '"nohtyP"', isHidden: false },
      { input: JSON.stringify({ s: '' }), expected: '""', isHidden: true },
      { input: JSON.stringify({ s: 'a' }), expected: '"a"', isHidden: true },
      { input: JSON.stringify({ s: 'racecar' }), expected: '"racecar"', isHidden: true },
    ],
  },

  // === Tier 2: Control Flow ===
  {
    title: 'Grade Calculator',
    description: `Write a function \`get_grade(score)\` that takes a score (0-100) and returns the letter grade.

- 90-100: "A"
- 80-89: "B"
- 70-79: "C"
- 60-69: "D"
- Below 60: "F"

If the score is out of range (< 0 or > 100), return "Invalid".

**Example:**
\`\`\`
Input: score = 85
Output: "B"
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'conditionals',
    secondaryConcepts: [],
    testCases: [
      { input: '85', expected: '"B"', isHidden: false },
      { input: '92', expected: '"A"', isHidden: false },
      { input: '55', expected: '"F"', isHidden: false },
      { input: '100', expected: '"A"', isHidden: true },
      { input: '-5', expected: '"Invalid"', isHidden: true },
    ],
  },
  {
    title: 'FizzBuzz',
    description: `Write a function \`fizzbuzz(n)\` that returns a list of strings from 1 to n where:
- Multiples of 3 are replaced with "Fizz"
- Multiples of 5 are replaced with "Buzz"
- Multiples of both 3 and 5 are replaced with "FizzBuzz"
- All other numbers are converted to strings

**Example:**
\`\`\`
Input: n = 5
Output: ["1", "2", "Fizz", "4", "Buzz"]
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'loops',
    secondaryConcepts: ['conditionals'],
    testCases: [
      { input: '5', expected: JSON.stringify(['1', '2', 'Fizz', '4', 'Buzz']), isHidden: false },
      { input: '3', expected: JSON.stringify(['1', '2', 'Fizz']), isHidden: false },
      { input: '15', expected: JSON.stringify(['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz']), isHidden: true },
      { input: '1', expected: JSON.stringify(['1']), isHidden: true },
      { input: '0', expected: JSON.stringify([]), isHidden: true },
    ],
  },
  {
    title: 'Multiplication Table',
    description: `Write a function \`multiplication_table(n)\` that returns a 2D list representing the multiplication table from 1 to n.

**Example:**
\`\`\`
Input: n = 3
Output: [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'nested_loops',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: '3', expected: JSON.stringify([[1, 2, 3], [2, 4, 6], [3, 6, 9]]), isHidden: false },
      { input: '1', expected: JSON.stringify([[1]]), isHidden: false },
      { input: '2', expected: JSON.stringify([[1, 2], [2, 4]]), isHidden: true },
      { input: '4', expected: JSON.stringify([[1, 2, 3, 4], [2, 4, 6, 8], [3, 6, 9, 12], [4, 8, 12, 16]]), isHidden: true },
      { input: '5', expected: JSON.stringify([[1, 2, 3, 4, 5], [2, 4, 6, 8, 10], [3, 6, 9, 12, 15], [4, 8, 12, 16, 20], [5, 10, 15, 20, 25]]), isHidden: true },
    ],
  },

  // === Tier 3: Functions ===
  {
    title: 'Temperature Converter',
    description: `Write two functions:
- \`celsius_to_fahrenheit(c)\` that converts Celsius to Fahrenheit: F = C × 9/5 + 32
- \`fahrenheit_to_celsius(f)\` that converts Fahrenheit to Celsius: C = (F - 32) × 5/9

Return the result rounded to 2 decimal places.

**Example:**
\`\`\`
Input: celsius_to_fahrenheit(100)
Output: 212.0

Input: fahrenheit_to_celsius(32)
Output: 0.0
\`\`\`

The function to test will be specified in the input as \`func\`.`,
    difficulty: Difficulty.EASY,
    primaryConcept: 'functions',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ func: 'c_to_f', value: 100 }), expected: '212.0', isHidden: false },
      { input: JSON.stringify({ func: 'f_to_c', value: 32 }), expected: '0.0', isHidden: false },
      { input: JSON.stringify({ func: 'c_to_f', value: 0 }), expected: '32.0', isHidden: true },
      { input: JSON.stringify({ func: 'f_to_c', value: 212 }), expected: '100.0', isHidden: true },
      { input: JSON.stringify({ func: 'c_to_f', value: 37 }), expected: '98.6', isHidden: true },
    ],
  },
  {
    title: 'Power Function',
    description: `Write a function \`power(base, exp)\` that computes base raised to the power of exp.

Handle these cases:
- Positive exponents: normal power
- Zero exponent: return 1
- Negative exponents: return the reciprocal (1 / base^|exp|)

Do NOT use the built-in ** operator or pow() function.

**Example:**
\`\`\`
Input: base = 2, exp = 3
Output: 8

Input: base = 2, exp = -2
Output: 0.25
\`\`\``,
    difficulty: Difficulty.MEDIUM,
    primaryConcept: 'parameters',
    secondaryConcepts: ['recursion'],
    testCases: [
      { input: JSON.stringify({ base: 2, exp: 3 }), expected: '8', isHidden: false },
      { input: JSON.stringify({ base: 2, exp: 0 }), expected: '1', isHidden: false },
      { input: JSON.stringify({ base: 2, exp: -2 }), expected: '0.25', isHidden: true },
      { input: JSON.stringify({ base: 5, exp: 3 }), expected: '125', isHidden: true },
      { input: JSON.stringify({ base: 3, exp: 4 }), expected: '81', isHidden: true },
    ],
  },
  {
    title: 'Factorial',
    description: `Write a recursive function \`factorial(n)\` that returns n! (n factorial).

- factorial(0) = 1
- factorial(n) = n × factorial(n-1)

**Example:**
\`\`\`
Input: n = 5
Output: 120

Input: n = 0
Output: 1
\`\`\`

**Constraints:**
- 0 <= n <= 20`,
    difficulty: Difficulty.EASY,
    primaryConcept: 'recursion',
    secondaryConcepts: ['functions'],
    testCases: [
      { input: '5', expected: '120', isHidden: false },
      { input: '0', expected: '1', isHidden: false },
      { input: '1', expected: '1', isHidden: true },
      { input: '10', expected: '3628800', isHidden: true },
      { input: '7', expected: '5040', isHidden: true },
    ],
  },
  {
    title: 'Fibonacci Number',
    description: `Write a function \`fibonacci(n)\` that returns the nth Fibonacci number.

The Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, ...
- fib(0) = 0
- fib(1) = 1
- fib(n) = fib(n-1) + fib(n-2) for n >= 2

**Example:**
\`\`\`
Input: n = 6
Output: 8

Input: n = 10
Output: 55
\`\`\`

**Constraints:**
- 0 <= n <= 30`,
    difficulty: Difficulty.EASY,
    primaryConcept: 'recursion',
    secondaryConcepts: ['dynamic_programming'],
    testCases: [
      { input: '6', expected: '8', isHidden: false },
      { input: '0', expected: '0', isHidden: false },
      { input: '1', expected: '1', isHidden: true },
      { input: '10', expected: '55', isHidden: true },
      { input: '20', expected: '6765', isHidden: true },
    ],
  },

  // === Tier 4: Data Structures ===
  {
    title: 'Remove Duplicates from Sorted Array',
    description: `Given a sorted list of integers, write a function \`remove_duplicates(nums)\` that removes duplicates in-place and returns the new length.

Return the list with duplicates removed (keeping only unique elements).

**Example:**
\`\`\`
Input: nums = [1, 1, 2, 2, 3]
Output: [1, 2, 3]
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['two_pointers'],
    testCases: [
      { input: JSON.stringify([1, 1, 2, 2, 3]), expected: JSON.stringify([1, 2, 3]), isHidden: false },
      { input: JSON.stringify([1, 1, 1]), expected: JSON.stringify([1]), isHidden: false },
      { input: JSON.stringify([]), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify([1, 2, 3, 4, 5]), expected: JSON.stringify([1, 2, 3, 4, 5]), isHidden: true },
      { input: JSON.stringify([0, 0, 1, 1, 1, 2, 2, 3, 3, 4]), expected: JSON.stringify([0, 1, 2, 3, 4]), isHidden: true },
    ],
  },
  {
    title: 'Rotate Array',
    description: `Write a function \`rotate(nums, k)\` that rotates the list to the right by k steps.

**Example:**
\`\`\`
Input: nums = [1, 2, 3, 4, 5, 6, 7], k = 3
Output: [5, 6, 7, 1, 2, 3, 4]
\`\`\`

**Constraints:**
- 1 <= nums.length <= 10^5
- 0 <= k <= 10^5`,
    difficulty: Difficulty.MEDIUM,
    primaryConcept: 'lists',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 5, 6, 7], k: 3 }), expected: JSON.stringify([5, 6, 7, 1, 2, 3, 4]), isHidden: false },
      { input: JSON.stringify({ nums: [-1, -100, 3, 99], k: 2 }), expected: JSON.stringify([3, 99, -1, -100]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 2], k: 3 }), expected: JSON.stringify([2, 1]), isHidden: true },
      { input: JSON.stringify({ nums: [1], k: 0 }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3], k: 6 }), expected: JSON.stringify([1, 2, 3]), isHidden: true },
    ],
  },
  {
    title: 'Word Frequency Counter',
    description: `Write a function \`word_frequency(text)\` that takes a string and returns a dictionary mapping each word (lowercased) to its frequency count.

Words are separated by spaces. Ignore punctuation.

**Example:**
\`\`\`
Input: text = "the cat sat on the mat"
Output: {"the": 2, "cat": 1, "sat": 1, "on": 1, "mat": 1}
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'dictionaries',
    secondaryConcepts: ['strings', 'loops'],
    testCases: [
      { input: JSON.stringify({ text: 'the cat sat on the mat' }), expected: JSON.stringify({ the: 2, cat: 1, sat: 1, on: 1, mat: 1 }), isHidden: false },
      { input: JSON.stringify({ text: 'hello hello hello' }), expected: JSON.stringify({ hello: 3 }), isHidden: false },
      { input: JSON.stringify({ text: 'a' }), expected: JSON.stringify({ a: 1 }), isHidden: true },
      { input: JSON.stringify({ text: 'one two three one two one' }), expected: JSON.stringify({ one: 3, two: 2, three: 1 }), isHidden: true },
      { input: JSON.stringify({ text: '' }), expected: JSON.stringify({}), isHidden: true },
    ],
  },
  {
    title: 'Set Intersection',
    description: `Write a function \`find_intersection(list1, list2)\` that returns a sorted list of elements that appear in both lists.

Do not include duplicates in the result.

**Example:**
\`\`\`
Input: list1 = [1, 2, 2, 3, 4], list2 = [2, 3, 3, 5]
Output: [2, 3]
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'sets',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ list1: [1, 2, 2, 3, 4], list2: [2, 3, 3, 5] }), expected: JSON.stringify([2, 3]), isHidden: false },
      { input: JSON.stringify({ list1: [1, 2, 3], list2: [4, 5, 6] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ list1: [1, 1, 1], list2: [1, 1, 1] }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ list1: [], list2: [1, 2] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ list1: [5, 3, 1], list2: [3, 1, 7] }), expected: JSON.stringify([1, 3]), isHidden: true },
    ],
  },
  {
    title: 'Valid Parentheses',
    description: `Write a function \`is_valid(s)\` that determines if a string containing just the characters '(', ')', '{', '}', '[' and ']' is valid.

A string is valid if:
1. Open brackets are closed by the same type of brackets.
2. Open brackets are closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

**Example:**
\`\`\`
Input: s = "()[]{}"
Output: true

Input: s = "(]"
Output: false
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'stacks',
    secondaryConcepts: ['strings'],
    testCases: [
      { input: '"()[]{}"', expected: 'true', isHidden: false },
      { input: '"(]"', expected: 'false', isHidden: false },
      { input: '"{[]}"', expected: 'true', isHidden: false },
      { input: '"((("', expected: 'false', isHidden: true },
      { input: '""', expected: 'true', isHidden: true },
    ],
  },

  // === Tier 5: OOP ===
  {
    title: 'Rectangle Class',
    description: `Create a class \`Rectangle\` with:
- Constructor that takes \`width\` and \`height\`
- Method \`area()\` that returns the area
- Method \`perimeter()\` that returns the perimeter
- Method \`is_square()\` that returns True if width equals height

**Example:**
\`\`\`
r = Rectangle(5, 3)
r.area()       # 15
r.perimeter()  # 16
r.is_square()  # False
\`\`\`

The test input specifies the method to call.`,
    difficulty: Difficulty.EASY,
    primaryConcept: 'classes',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ w: 5, h: 3, method: 'area' }), expected: '15', isHidden: false },
      { input: JSON.stringify({ w: 5, h: 3, method: 'perimeter' }), expected: '16', isHidden: false },
      { input: JSON.stringify({ w: 4, h: 4, method: 'is_square' }), expected: 'true', isHidden: true },
      { input: JSON.stringify({ w: 10, h: 5, method: 'area' }), expected: '50', isHidden: true },
      { input: JSON.stringify({ w: 1, h: 1, method: 'perimeter' }), expected: '4', isHidden: true },
    ],
  },

  // === Tier 6: Algorithms ===
  {
    title: 'Binary Search',
    description: `Write a function \`binary_search(nums, target)\` that implements binary search on a sorted array.

Return the index of the target if found, or -1 if not found.

**Example:**
\`\`\`
Input: nums = [-1, 0, 3, 5, 9, 12], target = 9
Output: 4

Input: nums = [-1, 0, 3, 5, 9, 12], target = 2
Output: -1
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'searching',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [-1, 0, 3, 5, 9, 12], target: 9 }), expected: '4', isHidden: false },
      { input: JSON.stringify({ nums: [-1, 0, 3, 5, 9, 12], target: 2 }), expected: '-1', isHidden: false },
      { input: JSON.stringify({ nums: [1], target: 1 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [], target: 5 }), expected: '-1', isHidden: true },
      { input: JSON.stringify({ nums: [1, 3, 5, 7, 9, 11, 13], target: 7 }), expected: '3', isHidden: true },
    ],
  },
  {
    title: 'Bubble Sort Implementation',
    description: `Write a function \`bubble_sort(nums)\` that sorts a list of integers in ascending order using the bubble sort algorithm.

Return the sorted list.

**Example:**
\`\`\`
Input: nums = [64, 34, 25, 12, 22, 11, 90]
Output: [11, 12, 22, 25, 34, 64, 90]
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'sorting',
    secondaryConcepts: ['nested_loops', 'lists'],
    testCases: [
      { input: JSON.stringify([64, 34, 25, 12, 22, 11, 90]), expected: JSON.stringify([11, 12, 22, 25, 34, 64, 90]), isHidden: false },
      { input: JSON.stringify([5, 1, 4, 2, 8]), expected: JSON.stringify([1, 2, 4, 5, 8]), isHidden: false },
      { input: JSON.stringify([1]), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify([3, 2, 1]), expected: JSON.stringify([1, 2, 3]), isHidden: true },
      { input: JSON.stringify([1, 2, 3, 4, 5]), expected: JSON.stringify([1, 2, 3, 4, 5]), isHidden: true },
    ],
  },
  // 'Container With Most Water' — REMOVED: duplicate of tier4-advanced.ts entry.
  // The tier4 version uses dict-style input { heights: [...] } which matches
  // the reference solution def solution(heights). Keeping both caused findFirst
  // to pick this legacy version (list-style input) → RUNTIME_ERROR.
  {
    title: 'Maximum Sum Subarray of Size K',
    description: `Write a function \`max_sum_subarray(nums, k)\` that finds the maximum sum of any contiguous subarray of size k.

**Example:**
\`\`\`
Input: nums = [2, 1, 5, 1, 3, 2], k = 3
Output: 9
Explanation: Subarray [5, 1, 3] has the maximum sum of 9.
\`\`\`

**Constraints:**
- 1 <= k <= nums.length <= 10^5`,
    difficulty: Difficulty.MEDIUM,
    primaryConcept: 'sliding_window',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [2, 1, 5, 1, 3, 2], k: 3 }), expected: '9', isHidden: false },
      { input: JSON.stringify({ nums: [2, 3, 4, 1, 5], k: 2 }), expected: '7', isHidden: false },
      { input: JSON.stringify({ nums: [1, 1, 1, 1, 1], k: 5 }), expected: '5', isHidden: true },
      { input: JSON.stringify({ nums: [100], k: 1 }), expected: '100', isHidden: true },
      { input: JSON.stringify({ nums: [1, 4, 2, 10, 2, 3, 1, 0, 20], k: 4 }), expected: '24', isHidden: true },
    ],
  },
  {
    title: 'Activity Selection',
    description: `Write a function \`max_activities(activities)\` that takes a list of activities (each represented as [start, end]) and returns the maximum number of non-overlapping activities.

Activities are sorted by start time. You need to select the maximum number of activities that don't overlap.

**Example:**
\`\`\`
Input: activities = [[1, 3], [2, 5], [3, 6], [5, 7], [8, 9]]
Output: 3
Explanation: Select activities [1,3], [5,7], [8,9]
\`\`\``,
    difficulty: Difficulty.MEDIUM,
    primaryConcept: 'greedy',
    secondaryConcepts: ['sorting'],
    testCases: [
      { input: JSON.stringify([[1, 3], [2, 5], [3, 6], [5, 7], [8, 9]]), expected: '3', isHidden: false },
      { input: JSON.stringify([[1, 2], [3, 4], [5, 6]]), expected: '3', isHidden: false },
      { input: JSON.stringify([[1, 10]]), expected: '1', isHidden: true },
      { input: JSON.stringify([[1, 2], [1, 3], [1, 4]]), expected: '1', isHidden: true },
      { input: JSON.stringify([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]), expected: '5', isHidden: true },
    ],
  },

  // === Tier 7: Advanced ===
  {
    title: 'Climbing Stairs',
    description: `You are climbing a staircase. It takes n steps to reach the top. Each time you can climb 1 or 2 steps.

Write a function \`climb_stairs(n)\` that returns the number of distinct ways you can climb to the top.

**Example:**
\`\`\`
Input: n = 3
Output: 3
Explanation: There are three ways: [1,1,1], [1,2], [2,1]

Input: n = 5
Output: 8
\`\`\`

**Constraints:**
- 1 <= n <= 45`,
    difficulty: Difficulty.EASY,
    primaryConcept: 'dynamic_programming',
    secondaryConcepts: ['recursion'],
    testCases: [
      { input: '3', expected: '3', isHidden: false },
      { input: '5', expected: '8', isHidden: false },
      { input: '1', expected: '1', isHidden: true },
      { input: '2', expected: '2', isHidden: true },
      { input: '10', expected: '89', isHidden: true },
    ],
  },
  {
    title: 'Generate Parentheses',
    description: `Write a function \`generate_parentheses(n)\` that generates all combinations of well-formed (valid) parentheses for n pairs.

Return the list of strings sorted lexicographically.

**Example:**
\`\`\`
Input: n = 3
Output: ["((()))", "(()())", "(())()", "()(())", "()()()"]

Input: n = 1
Output: ["()"]
\`\`\`

**Constraints:**
- 1 <= n <= 8`,
    difficulty: Difficulty.MEDIUM,
    primaryConcept: 'backtracking',
    secondaryConcepts: ['recursion', 'strings'],
    testCases: [
      { input: '3', expected: JSON.stringify(['((()))', '(()())', '(())()', '()(())', '()()()']), isHidden: false },
      { input: '1', expected: JSON.stringify(['()']), isHidden: false },
      { input: '2', expected: JSON.stringify(['(())', '()()']), isHidden: true },
      { input: '4', expected: JSON.stringify(['(((())))', '((()()))', '((())())', '((()))()', '(()(()))', '(()()())', '(()())()', '(())(())', '(())()()', '()((()))', '()(()())', '()(())()', '()()(())', '()()()()']), isHidden: true },
    ],
  },
  {
    title: 'Single Number (XOR)',
    description: `Given a non-empty list of integers where every element appears twice except for one, write a function \`single_number(nums)\` that finds the single element.

You must implement it with O(1) extra space complexity using bit manipulation.

**Example:**
\`\`\`
Input: nums = [2, 2, 1]
Output: 1

Input: nums = [4, 1, 2, 1, 2]
Output: 4
\`\`\``,
    difficulty: Difficulty.EASY,
    primaryConcept: 'bit_manipulation',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify([2, 2, 1]), expected: '1', isHidden: false },
      { input: JSON.stringify([4, 1, 2, 1, 2]), expected: '4', isHidden: false },
      { input: JSON.stringify([1]), expected: '1', isHidden: true },
      { input: JSON.stringify([0, 1, 0]), expected: '1', isHidden: true },
      { input: JSON.stringify([5, 3, 5, 3, 7]), expected: '7', isHidden: true },
    ],
  },
];

// ============================================================
// Mapping for the 5 existing problems to concepts
// ============================================================

interface ExistingProblemMapping {
  title: string;
  primaryConcept: string;
  secondaryConcepts: string[];
}

const EXISTING_PROBLEM_MAPPINGS: ExistingProblemMapping[] = [
  { title: 'Two Sum', primaryConcept: 'dictionaries', secondaryConcepts: ['lists'] },
  { title: 'Palindrome Number', primaryConcept: 'operators', secondaryConcepts: ['strings'] },
  { title: 'Reverse Linked List', primaryConcept: 'lists', secondaryConcepts: ['recursion'] },
  { title: 'Maximum Subarray', primaryConcept: 'dynamic_programming', secondaryConcepts: ['lists'] },
  { title: 'Merge K Sorted Lists', primaryConcept: 'divide_and_conquer', secondaryConcepts: ['sorting'] },
];

// ============================================================
// Main Seeder Function
// ============================================================

export async function seedAdaptive(course1Id: string, course2Id: string) {
  console.log('\n🧠 Seeding adaptive learning data...');

  // Clean adaptive data first
  console.log('   Cleaning adaptive tables...');
  try {
    await prisma.fsrsCard.deleteMany();
    await prisma.mabState.deleteMany();
    await prisma.eloRating.deleteMany();
    await prisma.knowledgeState.deleteMany();
    await prisma.problemConcept.deleteMany();
    await prisma.knowledgeGraphEdge.deleteMany();
    await prisma.concept.deleteMany();
  } catch {
    console.log('   (Adaptive tables may not exist yet, skipping cleanup)');
  }

  // --- 1. Seed Concepts ---
  console.log('   📊 Creating concepts...');
  const conceptMap = new Map<string, number>();

  for (const c of CONCEPTS) {
    const concept = await prisma.concept.create({
      data: {
        name: c.name,
        displayName: c.displayName,
        description: c.description,
        topicGroup: c.topicGroup,
        difficultyTier: c.difficultyTier,
      },
    });
    conceptMap.set(c.name, concept.id);
  }
  console.log(`   ✅ Created ${CONCEPTS.length} concepts`);

  // --- 2. Seed Prerequisite Edges ---
  console.log('   🔗 Creating prerequisite edges...');
  let edgeCount = 0;
  for (const edge of PREREQUISITE_EDGES) {
    const fromId = conceptMap.get(edge.from);
    const toId = conceptMap.get(edge.to);
    if (fromId !== undefined && toId !== undefined) {
      await prisma.knowledgeGraphEdge.create({
        data: {
          fromConceptId: fromId,
          toConceptId: toId,
          relationType: 'PREREQUISITE',
          weight: 1.0,
        },
      });
      edgeCount++;
    } else {
      console.warn(`   ⚠️  Edge ${edge.from} → ${edge.to}: concept not found`);
    }
  }
  console.log(`   ✅ Created ${edgeCount} prerequisite edges`);

  // --- 3. Seed New Problems ---
  // Problems are sourced from:
  //   (a) The legacy inline NEW_PROBLEMS array below (kept during migration, all on course1)
  //   (b) The tier bank files in ./problems/tier{1..5}-*.ts
  //       - TIER1/TIER2 → course1 (Python Intro)
  //       - TIER3/TIER4/TIER5 → course2 (DSA)
  // As problems are migrated from NEW_PROBLEMS into tier files, the legacy array shrinks.
  console.log('   ❓ Creating new problems...');
  const problemConceptData: { problemId: string; conceptName: string; isPrimary: boolean }[] = [];

  const problemBatches: { items: ProblemDef[]; courseId: string; label: string }[] = [
    { items: NEW_PROBLEMS, courseId: course1Id, label: 'legacy' },
    { items: TIER1, courseId: course1Id, label: 'T1' },
    { items: TIER2, courseId: course1Id, label: 'T2' },
    { items: TIER3, courseId: course2Id, label: 'T3' },
    { items: TIER4, courseId: course2Id, label: 'T4' },
    { items: TIER5, courseId: course2Id, label: 'T5' },
  ];

  let newProblemTotal = 0;
  for (const batch of problemBatches) {
    for (const p of batch.items) {
      const problem = await prisma.problem.create({
        data: {
          title: p.title,
          description: p.description,
          difficulty: p.difficulty,
          constraints: p.constraints || null,
          courseId: batch.courseId,
          starterCode: generateStarterCode(p.testCases),
          testCases: {
            create: p.testCases,
          },
        },
      });

      // Track for concept mapping
      problemConceptData.push({ problemId: problem.id, conceptName: p.primaryConcept, isPrimary: true });
      for (const sc of p.secondaryConcepts) {
        problemConceptData.push({ problemId: problem.id, conceptName: sc, isPrimary: false });
      }
      newProblemTotal++;
    }
    if (batch.items.length > 0) {
      console.log(`      • ${batch.label}: ${batch.items.length} problems`);
    }
  }
  console.log(`   ✅ Created ${newProblemTotal} new problems`);

  // --- 4. Map Existing Problems to Concepts ---
  console.log('   🗺️  Mapping existing problems to concepts...');
  for (const mapping of EXISTING_PROBLEM_MAPPINGS) {
    const problem = await prisma.problem.findFirst({ where: { title: mapping.title } });
    if (problem) {
      problemConceptData.push({ problemId: problem.id, conceptName: mapping.primaryConcept, isPrimary: true });
      for (const sc of mapping.secondaryConcepts) {
        problemConceptData.push({ problemId: problem.id, conceptName: sc, isPrimary: false });
      }
    } else {
      console.warn(`   ⚠️  Problem "${mapping.title}" not found for concept mapping`);
    }
  }

  // --- 5. Create Problem-Concept Mappings ---
  console.log('   📎 Creating problem-concept mappings...');
  let mappingCount = 0;
  for (const pc of problemConceptData) {
    const conceptId = conceptMap.get(pc.conceptName);
    if (conceptId !== undefined) {
      await prisma.problemConcept.create({
        data: {
          problemId: pc.problemId,
          conceptId: conceptId,
          isPrimary: pc.isPrimary,
        },
      });
      mappingCount++;
    } else {
      console.warn(`   ⚠️  Concept "${pc.conceptName}" not found for problem mapping`);
    }
  }
  console.log(`   ✅ Created ${mappingCount} problem-concept mappings`);

  // --- 6. Initialize Elo Ratings for Problems ---
  console.log('   📈 Initializing problem Elo ratings...');
  const allProblems = await prisma.problem.findMany();
  const eloMap: Record<string, number> = {
    EASY: 1000,
    MEDIUM: 1400,
    HARD: 1800,
  };
  for (const prob of allProblems) {
    await prisma.eloRating.create({
      data: {
        entityId: prob.id,
        entityType: 'PROBLEM',
        rating: eloMap[prob.difficulty] ?? 1200,
        kValue: 40.0,
        nAttempts: 0,
        ratingHistory: [],
      },
    });
  }
  console.log(`   ✅ Initialized Elo for ${allProblems.length} problems`);

  // --- 7. Generate Embeddings via AI Service (batch) ---
  // Non-fatal: if ai-service is down, log a warning and continue.
  // Re-run later with `npm run seed:embed` once ai-service is up.
  console.log('   🧠 Triggering batch embedding via ai-service...');
  try {
    const problemIds = allProblems.map((p) => p.id);
    const res = await fetch(`${AI_SERVICE_URL}/embed/batch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problem_ids: problemIds }),
    });
    if (!res.ok) {
      throw new Error(`ai-service returned HTTP ${res.status}`);
    }
    console.log(`   ✅ Embedded ${problemIds.length} problems`);
  } catch (e) {
    console.warn(`   ⚠️  Embedding skipped: ${(e as Error).message}`);
    console.warn('   → Run `npm run seed:embed` later when ai-service is up.');
  }

  // Print summary
  const totalBankProblems =
    NEW_PROBLEMS.length + TIER1.length + TIER2.length + TIER3.length + TIER4.length + TIER5.length;
  console.log('\n📊 Adaptive Learning Data Summary:');
  console.log(
    `   - Concepts: ${CONCEPTS.length} (T1:${CONCEPTS.filter((c) => c.difficultyTier === 1).length}, T2:${CONCEPTS.filter((c) => c.difficultyTier === 2).length}, T3:${CONCEPTS.filter((c) => c.difficultyTier === 3).length}, T4:${CONCEPTS.filter((c) => c.difficultyTier === 4).length}, T5:${CONCEPTS.filter((c) => c.difficultyTier === 5).length})`,
  );
  console.log(`   - Prerequisite edges: ${edgeCount}`);
  console.log(
    `   - New problems: ${totalBankProblems} (legacy:${NEW_PROBLEMS.length}, T1:${TIER1.length}, T2:${TIER2.length}, T3:${TIER3.length}, T4:${TIER4.length}, T5:${TIER5.length})`,
  );
  console.log(`   - Total problems: ${allProblems.length}`);
  console.log(`   - Problem-concept mappings: ${mappingCount}`);
  console.log(`   - Problem Elo ratings initialized: ${allProblems.length}`);
}
