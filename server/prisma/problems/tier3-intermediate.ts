import { Difficulty } from '@prisma/client';
import { ProblemDef } from './types';

/**
 * Tier 3 — Intermediate (40 problems)
 * Concepts: scope, recursion, sets, stacks, queues, classes, sorting, sliding_window
 */
export const TIER3: ProblemDef[] = [
  // === scope (3) ===
  {
    title: 'Counter Accumulator',
    description: `Write a function \`solution(nums)\` that uses a nested helper function to count how many positive numbers are in the list, demonstrating local scope.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['scope', 'functions'],
    primaryConcept: 'scope',
    secondaryConcepts: ['functions'],
    testCases: [
      { input: JSON.stringify({ nums: [1, -2, 3, -4, 5] }), expected: '3', isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ nums: [-1, -2] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3] }), expected: '3', isHidden: true },
      { input: JSON.stringify({ nums: [0, 0, 1] }), expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Closure Multiplier',
    description: `Write a function \`solution(factor, nums)\` that uses a nested closure to multiply each element of \`nums\` by \`factor\` and returns the resulting list.`,
    
    constraints: `- -10⁴ ≤ factor ≤ 10⁴\n- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['scope', 'closure'],
    primaryConcept: 'scope',
    secondaryConcepts: ['functions'],
    testCases: [
      { input: JSON.stringify({ factor: 3, nums: [1, 2, 3] }), expected: JSON.stringify([3, 6, 9]), isHidden: false },
      { input: JSON.stringify({ factor: 0, nums: [1, 2] }), expected: JSON.stringify([0, 0]), isHidden: false },
      { input: JSON.stringify({ factor: -1, nums: [1, -2, 3] }), expected: JSON.stringify([-1, 2, -3]), isHidden: true },
      { input: JSON.stringify({ factor: 2, nums: [] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ factor: 10, nums: [1] }), expected: JSON.stringify([10]), isHidden: true },
    ],
  },
  {
    title: 'Running Max with Helper',
    description: `Write a function \`solution(nums)\` that returns a list of running maxima. Use a nested helper that tracks the max so far.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['scope', 'lists'],
    primaryConcept: 'scope',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 3, 2, 5, 4] }), expected: JSON.stringify([1, 3, 3, 5, 5]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ nums: [5, 4, 3, 2, 1] }), expected: JSON.stringify([5, 5, 5, 5, 5]), isHidden: true },
      { input: JSON.stringify({ nums: [1] }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 5] }), expected: JSON.stringify([1, 2, 3, 4, 5]), isHidden: true },
    ],
  },

  // === recursion (7) ===
  {
    title: 'Recursive Factorial',
    description: `Write a recursive function \`solution(n)\` that computes n! without using any loops. Assume n ≥ 0.`,
    
    constraints: `- -10⁵ ≤ n ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['recursion', 'math'],
    primaryConcept: 'recursion',
    secondaryConcepts: [],
    testCases: [
      { input: '5', expected: '120', isHidden: false },
      { input: '0', expected: '1', isHidden: false },
      { input: '1', expected: '1', isHidden: true },
      { input: '6', expected: '720', isHidden: true },
      { input: '10', expected: '3628800', isHidden: true },
    ],
  },
  {
    title: 'Recursive Fibonacci',
    description: `Write a recursive function \`solution(n)\` that returns the n-th Fibonacci number (0-indexed). F(0)=0, F(1)=1. You may memoize.`,
    
    constraints: `- -10⁵ ≤ n ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['recursion', 'math'],
    primaryConcept: 'recursion',
    secondaryConcepts: [],
    testCases: [
      { input: '10', expected: '55', isHidden: false },
      { input: '0', expected: '0', isHidden: false },
      { input: '1', expected: '1', isHidden: true },
      { input: '15', expected: '610', isHidden: true },
      { input: '20', expected: '6765', isHidden: true },
    ],
  },
  {
    title: 'Recursive Sum of Digits',
    description: `Write a recursive function \`solution(n)\` that returns the sum of digits of a non-negative integer.`,
    
    constraints: `- -10⁵ ≤ n ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['recursion', 'math'],
    primaryConcept: 'recursion',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: '1234', expected: '10', isHidden: false },
      { input: '0', expected: '0', isHidden: false },
      { input: '9', expected: '9', isHidden: true },
      { input: '999', expected: '27', isHidden: true },
      { input: '100', expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Recursive Power',
    description: `Write a recursive function \`solution(base, exp)\` that computes \`base ** exp\` without using the \`**\` operator. Assume exp ≥ 0.`,
    
    constraints: `- -10⁵ ≤ base ≤ 10⁵\n- -10⁵ ≤ exp ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['recursion', 'math'],
    primaryConcept: 'recursion',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ base: 2, exp: 10 }), expected: '1024', isHidden: false },
      { input: JSON.stringify({ base: 3, exp: 4 }), expected: '81', isHidden: false },
      { input: JSON.stringify({ base: 5, exp: 0 }), expected: '1', isHidden: true },
      { input: JSON.stringify({ base: 7, exp: 1 }), expected: '7', isHidden: true },
      { input: JSON.stringify({ base: 10, exp: 3 }), expected: '1000', isHidden: true },
    ],
  },
  {
    title: 'Recursive String Reverse',
    description: `Write a recursive function \`solution(s)\` that reverses a string without using slicing or loops.`,
    
    constraints: `- 0 ≤ len(s) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    tags: ['recursion', 'strings'],
    primaryConcept: 'recursion',
    secondaryConcepts: ['strings'],
    testCases: [
      { input: '"hello"', expected: '"olleh"', isHidden: false },
      { input: '""', expected: '""', isHidden: false },
      { input: '"a"', expected: '"a"', isHidden: true },
      { input: '"Python"', expected: '"nohtyP"', isHidden: true },
      { input: '"racecar"', expected: '"racecar"', isHidden: true },
    ],
  },
  {
    title: 'Recursive List Sum',
    description: `Write a recursive function \`solution(nums)\` that returns the sum of a list without using \`sum()\` or loops.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['recursion', 'lists'],
    primaryConcept: 'recursion',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4] }), expected: '10', isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ nums: [5] }), expected: '5', isHidden: true },
      { input: JSON.stringify({ nums: [-1, 1] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [10, 20, 30, 40, 50] }), expected: '150', isHidden: true },
    ],
  },
  {
    title: 'Tower of Hanoi Moves',
    description: `Write a function \`solution(n)\` that returns the minimum number of moves required to solve the Tower of Hanoi with n disks. Use recursion: \`f(n) = 2 * f(n-1) + 1\`.`,
    
    constraints: `- -10⁵ ≤ n ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['recursion', 'math'],
    primaryConcept: 'recursion',
    secondaryConcepts: [],
    testCases: [
      { input: '3', expected: '7', isHidden: false },
      { input: '1', expected: '1', isHidden: false },
      { input: '0', expected: '0', isHidden: true },
      { input: '5', expected: '31', isHidden: true },
      { input: '10', expected: '1023', isHidden: true },
    ],
  },

  // === sets (4) ===
  {
    title: 'Unique Elements Count',
    description: `Write a function \`solution(nums)\` that returns the number of distinct values in the list using a set.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['sets'],
    primaryConcept: 'sets',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 2, 3, 3, 3, 4] }), expected: '4', isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ nums: [5, 5, 5] }), expected: '1', isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 5] }), expected: '5', isHidden: true },
      { input: JSON.stringify({ nums: [0] }), expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Set Intersection Sorted',
    description: `Write a function \`solution(a, b)\` that returns the sorted ascending list of elements common to both lists.`,
    
    constraints: `- 0 ≤ len(a) ≤ 100\n- -10⁴ ≤ a[i] ≤ 10⁴\n- 0 ≤ len(b) ≤ 100\n- -10⁴ ≤ b[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['sets', 'lists'],
    primaryConcept: 'sets',
    secondaryConcepts: ['sorting'],
    testCases: [
      { input: JSON.stringify({ a: [1, 2, 3, 4], b: [3, 4, 5, 6] }), expected: JSON.stringify([3, 4]), isHidden: false },
      { input: JSON.stringify({ a: [], b: [1, 2] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ a: [1, 1, 1], b: [1] }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ a: [1, 2, 3], b: [4, 5, 6] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ a: [5, 4, 3, 2, 1], b: [1, 2, 3] }), expected: JSON.stringify([1, 2, 3]), isHidden: true },
    ],
  },
  {
    title: 'Set Union Sorted',
    description: `Write a function \`solution(a, b)\` that returns a sorted ascending list of all elements in either list (distinct).`,
    
    constraints: `- 0 ≤ len(a) ≤ 100\n- -10⁴ ≤ a[i] ≤ 10⁴\n- 0 ≤ len(b) ≤ 100\n- -10⁴ ≤ b[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['sets', 'lists'],
    primaryConcept: 'sets',
    secondaryConcepts: ['sorting'],
    testCases: [
      { input: JSON.stringify({ a: [1, 2, 3], b: [3, 4, 5] }), expected: JSON.stringify([1, 2, 3, 4, 5]), isHidden: false },
      { input: JSON.stringify({ a: [], b: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ a: [1, 1], b: [2, 2] }), expected: JSON.stringify([1, 2]), isHidden: true },
      { input: JSON.stringify({ a: [3], b: [] }), expected: JSON.stringify([3]), isHidden: true },
      { input: JSON.stringify({ a: [1, 2], b: [1, 2] }), expected: JSON.stringify([1, 2]), isHidden: true },
    ],
  },
  {
    title: 'Symmetric Difference',
    description: `Write a function \`solution(a, b)\` that returns a sorted list of elements that appear in exactly one of the two lists.`,
    
    constraints: `- 0 ≤ len(a) ≤ 10⁴\n- -10⁵ ≤ a[i] ≤ 10⁵\n- 0 ≤ len(b) ≤ 10⁴\n- -10⁵ ≤ b[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['sets'],
    primaryConcept: 'sets',
    secondaryConcepts: ['sorting'],
    testCases: [
      { input: JSON.stringify({ a: [1, 2, 3], b: [3, 4, 5] }), expected: JSON.stringify([1, 2, 4, 5]), isHidden: false },
      { input: JSON.stringify({ a: [1, 2, 3], b: [1, 2, 3] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ a: [], b: [1] }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ a: [1, 1, 2], b: [2, 3, 3] }), expected: JSON.stringify([1, 3]), isHidden: true },
      { input: JSON.stringify({ a: [1, 2], b: [] }), expected: JSON.stringify([1, 2]), isHidden: true },
    ],
  },

  // === stacks (4) ===
  {
    title: 'Valid Parentheses Simple',
    description: `Write a function \`solution(s)\` that returns \`True\` if a string of only \`()\`, \`[]\`, \`{}\` is balanced, otherwise \`False\`. Use a stack.`,
    
    constraints: `- 0 ≤ len(s) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    tags: ['stacks', 'strings'],
    primaryConcept: 'stacks',
    secondaryConcepts: ['strings'],
    testCases: [
      { input: '"({[]})"', expected: 'true', isHidden: false },
      { input: '"([)]"', expected: 'false', isHidden: false },
      { input: '""', expected: 'true', isHidden: true },
      { input: '"((("', expected: 'false', isHidden: true },
      { input: '"()()"', expected: 'true', isHidden: true },
    ],
  },
  {
    title: 'Reverse Using Stack',
    description: `Write a function \`solution(nums)\` that reverses a list using a stack (append then pop).`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['stacks', 'lists'],
    primaryConcept: 'stacks',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3] }), expected: JSON.stringify([3, 2, 1]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ nums: [1] }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2] }), expected: JSON.stringify([2, 1]), isHidden: true },
      { input: JSON.stringify({ nums: [5, 4, 3, 2, 1] }), expected: JSON.stringify([1, 2, 3, 4, 5]), isHidden: true },
    ],
  },
  {
    title: 'Stack Operations Result',
    description: `Write a function \`solution(ops)\` that simulates a stack given a list of operations. Each op is a list:
- \`["push", value]\` pushes value
- \`["pop"]\` pops (no-op on empty)

Return the final stack as a list.`,
    
    constraints: `- 0 ≤ len(ops) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    tags: ['stacks'],
    primaryConcept: 'stacks',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ ops: [['push', 1], ['push', 2], ['pop'], ['push', 3]] }), expected: JSON.stringify([1, 3]), isHidden: false },
      { input: JSON.stringify({ ops: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ ops: [['push', 5], ['pop'], ['pop']] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ ops: [['push', 1], ['push', 2], ['push', 3]] }), expected: JSON.stringify([1, 2, 3]), isHidden: true },
      { input: JSON.stringify({ ops: [['pop']] }), expected: JSON.stringify([]), isHidden: true },
    ],
  },
  {
    title: 'Next Greater Element',
    description: `Write a function \`solution(nums)\` that returns, for each element, the value of the next greater element to its right, or -1 if none exists. Use a stack.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['stacks', 'lists'],
    primaryConcept: 'stacks',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [2, 1, 2, 4, 3] }), expected: JSON.stringify([4, 2, 4, -1, -1]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3] }), expected: JSON.stringify([2, 3, -1]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ nums: [5, 4, 3, 2, 1] }), expected: JSON.stringify([-1, -1, -1, -1, -1]), isHidden: true },
      { input: JSON.stringify({ nums: [1] }), expected: JSON.stringify([-1]), isHidden: true },
    ],
  },

  // === queues (3) ===
  {
    title: 'Queue FIFO Simulation',
    description: `Write a function \`solution(ops)\` that simulates a FIFO queue. Each op is a list:
- \`["enq", value]\` enqueues
- \`["deq"]\` dequeues (no-op on empty)

Return the final queue as a list from front to back.`,
    
    constraints: `- 0 ≤ len(ops) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    tags: ['queues'],
    primaryConcept: 'queues',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ ops: [['enq', 1], ['enq', 2], ['deq'], ['enq', 3]] }), expected: JSON.stringify([2, 3]), isHidden: false },
      { input: JSON.stringify({ ops: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ ops: [['enq', 5], ['deq'], ['deq']] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ ops: [['enq', 1], ['enq', 2], ['enq', 3]] }), expected: JSON.stringify([1, 2, 3]), isHidden: true },
      { input: JSON.stringify({ ops: [['deq']] }), expected: JSON.stringify([]), isHidden: true },
    ],
  },
  {
    title: 'Rotate Queue Left',
    description: `Write a function \`solution(nums, k)\` that rotates a list left by k positions (treating it as a queue). k may exceed len(nums).`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴\n- -10⁴ ≤ k ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['queues', 'lists'],
    primaryConcept: 'queues',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 5], k: 2 }), expected: JSON.stringify([3, 4, 5, 1, 2]), isHidden: false },
      { input: JSON.stringify({ nums: [1], k: 3 }), expected: JSON.stringify([1]), isHidden: false },
      { input: JSON.stringify({ nums: [], k: 1 }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3], k: 6 }), expected: JSON.stringify([1, 2, 3]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3, 4], k: 1 }), expected: JSON.stringify([2, 3, 4, 1]), isHidden: true },
    ],
  },
  {
    title: 'Level Order Sum',
    description: `Given a list representing a binary tree in level-order (with \`null\` for missing children), return the total sum of all non-null nodes.`,
    
    constraints: `- 0 ≤ len(tree) ≤ 10⁴\n- -10⁵ ≤ tree[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['queues', 'trees'],
    primaryConcept: 'queues',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ tree: [1, 2, 3, null, 4] }), expected: '10', isHidden: false },
      { input: JSON.stringify({ tree: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ tree: [5] }), expected: '5', isHidden: true },
      { input: JSON.stringify({ tree: [1, null, 2, null, 3] }), expected: '6', isHidden: true },
      { input: JSON.stringify({ tree: [1, 2, 3, 4, 5, 6, 7] }), expected: '28', isHidden: true },
    ],
  },

  // === classes (5) ===
  {
    title: 'BankAccount Class',
    description: `Implement a function \`solution(ops)\` that simulates a BankAccount with an initial balance of 0. Operations:
- \`["deposit", amount]\` adds amount
- \`["withdraw", amount]\` subtracts amount if sufficient funds, otherwise no-op

Return the final balance.`,
    
    constraints: `- 0 ≤ len(ops) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    tags: ['classes', 'oop'],
    primaryConcept: 'classes',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ ops: [['deposit', 100], ['withdraw', 30], ['deposit', 50]] }), expected: '120', isHidden: false },
      { input: JSON.stringify({ ops: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ ops: [['withdraw', 50]] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ ops: [['deposit', 200], ['withdraw', 100], ['withdraw', 50]] }), expected: '50', isHidden: true },
      { input: JSON.stringify({ ops: [['deposit', 1000]] }), expected: '1000', isHidden: true },
    ],
  },
  {
    title: 'Counter Class',
    description: `Implement a Counter that starts at 0 and processes a list of operations. Ops: \`["inc"]\`, \`["dec"]\`, \`["reset"]\`. Return the final count.`,
    
    constraints: `- 0 ≤ len(ops) ≤ 100`,
difficulty: Difficulty.EASY,
    tags: ['classes', 'oop'],
    primaryConcept: 'classes',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ ops: [['inc'], ['inc'], ['dec'], ['inc']] }), expected: '2', isHidden: false },
      { input: JSON.stringify({ ops: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ ops: [['inc'], ['inc'], ['reset']] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ ops: [['dec'], ['dec']] }), expected: '-2', isHidden: true },
      { input: JSON.stringify({ ops: [['inc']] }), expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Point Class Distance',
    description: `Given two points each as a list \`[x, y]\`, return the Manhattan distance |x1 - x2| + |y1 - y2| between them. Implement via a Point class internally.`,
    
    constraints: `- 0 ≤ len(p1) ≤ 100\n- -10⁴ ≤ p1[i] ≤ 10⁴\n- 0 ≤ len(p2) ≤ 100\n- -10⁴ ≤ p2[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['classes', 'oop'],
    primaryConcept: 'classes',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ p1: [1, 2], p2: [4, 6] }), expected: '7', isHidden: false },
      { input: JSON.stringify({ p1: [0, 0], p2: [0, 0] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ p1: [-1, -1], p2: [1, 1] }), expected: '4', isHidden: true },
      { input: JSON.stringify({ p1: [3, 0], p2: [0, 4] }), expected: '7', isHidden: true },
      { input: JSON.stringify({ p1: [10, 10], p2: [5, 5] }), expected: '10', isHidden: true },
    ],
  },
  {
    title: 'Inventory Class',
    description: `Implement an Inventory that tracks item quantities. Given a list of operations, return the final inventory as a dictionary sorted by key.

Ops:
- \`["add", name, qty]\` adds qty to item
- \`["remove", name, qty]\` subtracts (clamping at 0)`,
    
    constraints: `- 0 ≤ len(ops) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    tags: ['classes', 'dictionaries'],
    primaryConcept: 'classes',
    secondaryConcepts: ['dictionaries'],
    testCases: [
      { input: JSON.stringify({ ops: [['add', 'apple', 5], ['add', 'banana', 3], ['remove', 'apple', 2]] }), expected: JSON.stringify({ apple: 3, banana: 3 }), isHidden: false },
      { input: JSON.stringify({ ops: [] }), expected: JSON.stringify({}), isHidden: false },
      { input: JSON.stringify({ ops: [['add', 'x', 10], ['remove', 'x', 20]] }), expected: JSON.stringify({ x: 0 }), isHidden: true },
      { input: JSON.stringify({ ops: [['add', 'a', 1], ['add', 'a', 2]] }), expected: JSON.stringify({ a: 3 }), isHidden: true },
      { input: JSON.stringify({ ops: [['add', 'only', 5]] }), expected: JSON.stringify({ only: 5 }), isHidden: true },
    ],
  },
  {
    title: 'Timer Class Elapsed',
    description: `Implement a Timer that accumulates elapsed seconds. Given a list of intervals \`[start, end]\`, return the total elapsed time by summing each interval's duration.`,
    
    constraints: `- 0 ≤ len(intervals) ≤ 100`,
difficulty: Difficulty.EASY,
    tags: ['classes'],
    primaryConcept: 'classes',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ intervals: [[0, 5], [10, 15], [20, 22]] }), expected: '12', isHidden: false },
      { input: JSON.stringify({ intervals: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ intervals: [[0, 100]] }), expected: '100', isHidden: true },
      { input: JSON.stringify({ intervals: [[5, 5]] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ intervals: [[1, 2], [3, 4], [5, 6]] }), expected: '3', isHidden: true },
    ],
  },

  // === sorting (7) ===
  {
    title: 'Bubble Sort Ascending',
    description: `Implement bubble sort. Write \`solution(nums)\` that returns the sorted list in ascending order without using \`sorted()\` or \`list.sort()\`.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['sorting', 'bubble-sort'],
    primaryConcept: 'sorting',
    secondaryConcepts: ['nested_loops'],
    testCases: [
      { input: JSON.stringify({ nums: [5, 2, 8, 1, 9] }), expected: JSON.stringify([1, 2, 5, 8, 9]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ nums: [1] }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ nums: [3, 3, 3] }), expected: JSON.stringify([3, 3, 3]), isHidden: true },
      { input: JSON.stringify({ nums: [9, 7, 5, 3, 1] }), expected: JSON.stringify([1, 3, 5, 7, 9]), isHidden: true },
    ],
  },
  {
    title: 'Selection Sort',
    description: `Implement selection sort. Return the list sorted in ascending order.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['sorting', 'selection-sort'],
    primaryConcept: 'sorting',
    secondaryConcepts: ['nested_loops'],
    testCases: [
      { input: JSON.stringify({ nums: [64, 25, 12, 22, 11] }), expected: JSON.stringify([11, 12, 22, 25, 64]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ nums: [5, 4, 3, 2, 1] }), expected: JSON.stringify([1, 2, 3, 4, 5]), isHidden: true },
      { input: JSON.stringify({ nums: [1] }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ nums: [2, 2, 1, 1] }), expected: JSON.stringify([1, 1, 2, 2]), isHidden: true },
    ],
  },
  {
    title: 'Insertion Sort',
    description: `Implement insertion sort. Return the list sorted in ascending order.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['sorting', 'insertion-sort'],
    primaryConcept: 'sorting',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ nums: [12, 11, 13, 5, 6] }), expected: JSON.stringify([5, 6, 11, 12, 13]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3] }), expected: JSON.stringify([1, 2, 3]), isHidden: true },
      { input: JSON.stringify({ nums: [3, 2, 1] }), expected: JSON.stringify([1, 2, 3]), isHidden: true },
      { input: JSON.stringify({ nums: [5] }), expected: JSON.stringify([5]), isHidden: true },
    ],
  },
  {
    title: 'Sort Descending',
    description: `Write a function \`solution(nums)\` that returns the list sorted in descending order.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['sorting'],
    primaryConcept: 'sorting',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ nums: [3, 1, 4, 1, 5, 9] }), expected: JSON.stringify([9, 5, 4, 3, 1, 1]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ nums: [1] }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ nums: [5, 5, 5] }), expected: JSON.stringify([5, 5, 5]), isHidden: true },
      { input: JSON.stringify({ nums: [-1, -5, -2] }), expected: JSON.stringify([-1, -2, -5]), isHidden: true },
    ],
  },
  {
    title: 'Sort by Absolute Value',
    description: `Write a function \`solution(nums)\` that returns the list sorted by absolute value in ascending order. Ties broken by original value.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['sorting'],
    primaryConcept: 'sorting',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ nums: [-3, 1, -2, 5, -4] }), expected: JSON.stringify([1, -2, -3, -4, 5]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ nums: [0] }), expected: JSON.stringify([0]), isHidden: true },
      { input: JSON.stringify({ nums: [-1, 1] }), expected: JSON.stringify([-1, 1]), isHidden: true },
      { input: JSON.stringify({ nums: [-5, -3, -1] }), expected: JSON.stringify([-1, -3, -5]), isHidden: true },
    ],
  },
  {
    title: 'Sort Words by Length',
    description: `Write a function \`solution(words)\` that returns the list sorted by word length ascending. Ties broken by alphabetical order.`,
    
    constraints: `- 0 ≤ len(words) ≤ 100`,
difficulty: Difficulty.EASY,
    tags: ['sorting', 'strings'],
    primaryConcept: 'sorting',
    secondaryConcepts: ['strings'],
    testCases: [
      { input: JSON.stringify({ words: ['banana', 'apple', 'kiwi', 'fig'] }), expected: JSON.stringify(['fig', 'kiwi', 'apple', 'banana']), isHidden: false },
      { input: JSON.stringify({ words: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ words: ['a', 'b', 'c'] }), expected: JSON.stringify(['a', 'b', 'c']), isHidden: true },
      { input: JSON.stringify({ words: ['ab', 'ba', 'a'] }), expected: JSON.stringify(['a', 'ab', 'ba']), isHidden: true },
      { input: JSON.stringify({ words: ['python'] }), expected: JSON.stringify(['python']), isHidden: true },
    ],
  },
  {
    title: 'Merge Two Sorted',
    description: `Write a function \`solution(a, b)\` that merges two sorted ascending lists into one sorted list in O(n + m) time.`,
    
    constraints: `- 0 ≤ len(a) ≤ 10⁴\n- -10⁵ ≤ a[i] ≤ 10⁵\n- 0 ≤ len(b) ≤ 10⁴\n- -10⁵ ≤ b[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['sorting', 'two-pointers'],
    primaryConcept: 'sorting',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ a: [1, 3, 5], b: [2, 4, 6] }), expected: JSON.stringify([1, 2, 3, 4, 5, 6]), isHidden: false },
      { input: JSON.stringify({ a: [], b: [1, 2, 3] }), expected: JSON.stringify([1, 2, 3]), isHidden: false },
      { input: JSON.stringify({ a: [1, 2, 3], b: [] }), expected: JSON.stringify([1, 2, 3]), isHidden: true },
      { input: JSON.stringify({ a: [], b: [] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ a: [1, 1, 1], b: [2, 2, 2] }), expected: JSON.stringify([1, 1, 1, 2, 2, 2]), isHidden: true },
    ],
  },

  // === sliding_window (7) ===
  {
    title: 'Max Sum Subarray of Size K',
    description: `Write a function \`solution(nums, k)\` that returns the maximum sum of any contiguous subarray of size k. Assume 1 ≤ k ≤ len(nums).`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵\n- -10⁵ ≤ k ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['sliding-window', 'lists'],
    primaryConcept: 'sliding_window',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 4, 2, 10, 2, 3, 1, 0, 20], k: 4 }), expected: '24', isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3], k: 2 }), expected: '5', isHidden: false },
      { input: JSON.stringify({ nums: [5], k: 1 }), expected: '5', isHidden: true },
      { input: JSON.stringify({ nums: [1, 1, 1, 1], k: 2 }), expected: '2', isHidden: true },
      { input: JSON.stringify({ nums: [10, -5, 2, 8], k: 2 }), expected: '10', isHidden: true },
    ],
  },
  {
    title: 'Longest Substring No Repeat',
    description: `Write a function \`solution(s)\` that returns the length of the longest substring without repeating characters.`,
    
    constraints: `- 0 ≤ len(s) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    tags: ['sliding-window', 'strings'],
    primaryConcept: 'sliding_window',
    secondaryConcepts: ['strings', 'sets'],
    testCases: [
      { input: '"abcabcbb"', expected: '3', isHidden: false },
      { input: '"bbbbb"', expected: '1', isHidden: false },
      { input: '""', expected: '0', isHidden: true },
      { input: '"pwwkew"', expected: '3', isHidden: true },
      { input: '"abcdef"', expected: '6', isHidden: true },
    ],
  },
  {
    title: 'Min Subarray Sum ≥ Target',
    description: `Write a function \`solution(nums, target)\` that returns the smallest length of a contiguous subarray whose sum ≥ target. Return 0 if none exists. All elements are positive.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵\n- -10⁵ ≤ target ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['sliding-window'],
    primaryConcept: 'sliding_window',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [2, 3, 1, 2, 4, 3], target: 7 }), expected: '2', isHidden: false },
      { input: JSON.stringify({ nums: [1, 1, 1], target: 10 }), expected: '0', isHidden: false },
      { input: JSON.stringify({ nums: [5], target: 5 }), expected: '1', isHidden: true },
      { input: JSON.stringify({ nums: [], target: 5 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [1, 4, 4], target: 4 }), expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Average of Subarrays',
    description: `Write a function \`solution(nums, k)\` that returns a list of averages of every contiguous subarray of size k, each rounded to 2 decimal places.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵\n- -10⁵ ≤ k ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['sliding-window'],
    primaryConcept: 'sliding_window',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4], k: 2 }), expected: JSON.stringify([1.5, 2.5, 3.5]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 1, 1, 1], k: 2 }), expected: JSON.stringify([1.0, 1.0, 1.0]), isHidden: false },
      { input: JSON.stringify({ nums: [10], k: 1 }), expected: JSON.stringify([10.0]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3], k: 3 }), expected: JSON.stringify([2.0]), isHidden: true },
      { input: JSON.stringify({ nums: [4, 8], k: 1 }), expected: JSON.stringify([4.0, 8.0]), isHidden: true },
    ],
  },
  {
    title: 'Count Distinct in Windows',
    description: `Write a function \`solution(nums, k)\` that returns, for each window of size k (from left to right), the count of distinct values in that window, as a list.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁵\n- -10⁹ ≤ nums[i] ≤ 10⁹\n- -10⁹ ≤ k ≤ 10⁹`,
difficulty: Difficulty.HARD,
    tags: ['sliding-window', 'dictionaries'],
    primaryConcept: 'sliding_window',
    secondaryConcepts: ['dictionaries'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 1, 3, 4, 2, 3], k: 4 }), expected: JSON.stringify([3, 4, 4, 3]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 1, 1], k: 2 }), expected: JSON.stringify([1, 1]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3], k: 3 }), expected: JSON.stringify([3]), isHidden: true },
      { input: JSON.stringify({ nums: [5], k: 1 }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 1, 2], k: 2 }), expected: JSON.stringify([2, 2, 2]), isHidden: true },
    ],
  },
  {
    title: 'Longest Substring K Distinct',
    description: `Write a function \`solution(s, k)\` that returns the length of the longest substring with at most k distinct characters.`,
    
    constraints: `- 0 ≤ len(s) ≤ 10⁵\n- -10⁹ ≤ k ≤ 10⁹`,
difficulty: Difficulty.HARD,
    tags: ['sliding-window', 'strings'],
    primaryConcept: 'sliding_window',
    secondaryConcepts: ['strings', 'dictionaries'],
    testCases: [
      { input: JSON.stringify({ s: 'eceba', k: 2 }), expected: '3', isHidden: false },
      { input: JSON.stringify({ s: 'aa', k: 1 }), expected: '2', isHidden: false },
      { input: JSON.stringify({ s: '', k: 3 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ s: 'abc', k: 0 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ s: 'abaccc', k: 2 }), expected: '4', isHidden: true },
    ],
  },
  {
    title: 'Fixed Window Max',
    description: `Write a function \`solution(nums, k)\` that returns a list of maximum values of each contiguous window of size k.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁵\n- -10⁹ ≤ nums[i] ≤ 10⁹\n- -10⁹ ≤ k ≤ 10⁹`,
difficulty: Difficulty.HARD,
    tags: ['sliding-window'],
    primaryConcept: 'sliding_window',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 3, -1, -3, 5, 3, 6, 7], k: 3 }), expected: JSON.stringify([3, 3, 5, 5, 6, 7]), isHidden: false },
      { input: JSON.stringify({ nums: [1], k: 1 }), expected: JSON.stringify([1]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3], k: 3 }), expected: JSON.stringify([3]), isHidden: true },
      { input: JSON.stringify({ nums: [5, 4, 3, 2, 1], k: 2 }), expected: JSON.stringify([5, 4, 3, 2]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 1, 1, 1], k: 2 }), expected: JSON.stringify([1, 1, 1]), isHidden: true },
    ],
  },
];
