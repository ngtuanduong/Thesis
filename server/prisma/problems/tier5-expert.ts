import { Difficulty } from '@prisma/client';
import { ProblemDef } from './types';

/**
 * Tier 5 — Expert (20 problems)
 * Concepts: dynamic_programming, graphs, trees, backtracking, bit_manipulation
 */
export const TIER5: ProblemDef[] = [
  // === dynamic_programming (6) ===
  {
    title: 'Climbing Stairs DP',
    description: `You are climbing a staircase with n steps. Each time you can climb 1 or 2 steps. How many distinct ways can you climb to the top?`,
    
    constraints: `- -10⁵ ≤ n ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['dynamic-programming'],
    primaryConcept: 'dynamic_programming',
    secondaryConcepts: [],
    testCases: [
      { input: '5', expected: '8', isHidden: false },
      { input: '2', expected: '2', isHidden: false },
      { input: '1', expected: '1', isHidden: true },
      { input: '10', expected: '89', isHidden: true },
      { input: '0', expected: '1', isHidden: true },
    ],
  },
  {
    title: 'House Robber',
    description: `Given a list of house values, return the maximum money you can rob without robbing two adjacent houses.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['dynamic-programming'],
    primaryConcept: 'dynamic_programming',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ nums: [2, 7, 9, 3, 1] }), expected: '12', isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3, 1] }), expected: '4', isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [5] }), expected: '5', isHidden: true },
      { input: JSON.stringify({ nums: [2, 1, 1, 2] }), expected: '4', isHidden: true },
    ],
  },
  {
    title: 'Coin Change DP',
    description: `Given coin denominations and a target amount, return the minimum number of coins to make the amount, or -1 if impossible. Use DP.`,
    
    constraints: `- 0 ≤ len(coins) ≤ 10⁵\n- -10⁹ ≤ coins[i] ≤ 10⁹\n- -10⁹ ≤ amount ≤ 10⁹`,
difficulty: Difficulty.HARD,
    tags: ['dynamic-programming'],
    primaryConcept: 'dynamic_programming',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ coins: [1, 2, 5], amount: 11 }), expected: '3', isHidden: false },
      { input: JSON.stringify({ coins: [2], amount: 3 }), expected: '-1', isHidden: false },
      { input: JSON.stringify({ coins: [1], amount: 0 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ coins: [1, 5, 10, 25], amount: 30 }), expected: '2', isHidden: true },
      { input: JSON.stringify({ coins: [5], amount: 10 }), expected: '2', isHidden: true },
    ],
  },
  {
    title: 'Longest Common Subsequence',
    description: `Given two strings, return the length of their longest common subsequence.`,
    
    constraints: `- 0 ≤ len(a) ≤ 10⁵\n- 0 ≤ len(b) ≤ 10⁵`,
difficulty: Difficulty.HARD,
    tags: ['dynamic-programming', 'strings'],
    primaryConcept: 'dynamic_programming',
    secondaryConcepts: ['strings'],
    testCases: [
      { input: JSON.stringify({ a: 'abcde', b: 'ace' }), expected: '3', isHidden: false },
      { input: JSON.stringify({ a: 'abc', b: 'abc' }), expected: '3', isHidden: false },
      { input: JSON.stringify({ a: 'abc', b: 'def' }), expected: '0', isHidden: true },
      { input: JSON.stringify({ a: '', b: 'abc' }), expected: '0', isHidden: true },
      { input: JSON.stringify({ a: 'programming', b: 'algorithm' }), expected: '3', isHidden: true },
    ],
  },
  {
    title: 'Longest Increasing Subsequence',
    description: `Return the length of the longest strictly increasing subsequence of a list.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁵\n- -10⁹ ≤ nums[i] ≤ 10⁹`,
difficulty: Difficulty.HARD,
    tags: ['dynamic-programming'],
    primaryConcept: 'dynamic_programming',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ nums: [10, 9, 2, 5, 3, 7, 101, 18] }), expected: '4', isHidden: false },
      { input: JSON.stringify({ nums: [0, 1, 0, 3, 2, 3] }), expected: '4', isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [7, 7, 7, 7] }), expected: '1', isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 5] }), expected: '5', isHidden: true },
    ],
  },
  {
    title: 'Zero One Knapsack',
    description: `Given item weights and values, and knapsack capacity W, return the maximum total value you can carry. Each item can be taken at most once.`,
    
    constraints: `- 0 ≤ len(weights) ≤ 10⁵\n- -10⁹ ≤ weights[i] ≤ 10⁹\n- 0 ≤ len(values) ≤ 10⁵\n- -10⁹ ≤ values[i] ≤ 10⁹\n- -10⁹ ≤ W ≤ 10⁹`,
difficulty: Difficulty.HARD,
    tags: ['dynamic-programming', 'knapsack'],
    primaryConcept: 'dynamic_programming',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ weights: [1, 3, 4, 5], values: [1, 4, 5, 7], W: 7 }), expected: '9', isHidden: false },
      { input: JSON.stringify({ weights: [2, 3], values: [3, 4], W: 5 }), expected: '7', isHidden: false },
      { input: JSON.stringify({ weights: [], values: [], W: 10 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ weights: [5], values: [10], W: 4 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ weights: [1, 2], values: [10, 20], W: 3 }), expected: '30', isHidden: true },
    ],
  },

  // === trees (4) ===
  {
    title: 'Binary Tree Max Depth',
    description: `Given a binary tree represented in level-order as a list (with \`null\` for missing nodes), return the maximum depth.`,
    
    constraints: `- 0 ≤ len(tree) ≤ 10⁴\n- -10⁵ ≤ tree[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['trees', 'bfs'],
    primaryConcept: 'trees',
    secondaryConcepts: ['queues'],
    testCases: [
      { input: JSON.stringify({ tree: [3, 9, 20, null, null, 15, 7] }), expected: '3', isHidden: false },
      { input: JSON.stringify({ tree: [1] }), expected: '1', isHidden: false },
      { input: JSON.stringify({ tree: [] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ tree: [1, 2] }), expected: '2', isHidden: true },
      { input: JSON.stringify({ tree: [1, 2, 3, 4, 5, 6, 7] }), expected: '3', isHidden: true },
    ],
  },
  {
    title: 'Count Tree Nodes',
    description: `Given a binary tree as a level-order list (with \`null\`), count the number of non-null nodes.`,
    
    constraints: `- 0 ≤ len(tree) ≤ 100\n- -10⁴ ≤ tree[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['trees'],
    primaryConcept: 'trees',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ tree: [1, 2, 3, null, 4] }), expected: '4', isHidden: false },
      { input: JSON.stringify({ tree: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ tree: [1] }), expected: '1', isHidden: true },
      { input: JSON.stringify({ tree: [1, 2, 3, 4, 5] }), expected: '5', isHidden: true },
      { input: JSON.stringify({ tree: [1, null, 2, null, 3] }), expected: '3', isHidden: true },
    ],
  },
  {
    title: 'Tree Level Order Traversal',
    description: `Given a binary tree as a level-order list (with \`null\`), return a list of levels, where each level is a list of values.`,
    
    constraints: `- 0 ≤ len(tree) ≤ 10⁴\n- -10⁵ ≤ tree[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['trees', 'bfs'],
    primaryConcept: 'trees',
    secondaryConcepts: ['queues'],
    testCases: [
      { input: JSON.stringify({ tree: [3, 9, 20, null, null, 15, 7] }), expected: JSON.stringify([[3], [9, 20], [15, 7]]), isHidden: false },
      { input: JSON.stringify({ tree: [1] }), expected: JSON.stringify([[1]]), isHidden: false },
      { input: JSON.stringify({ tree: [] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ tree: [1, 2, 3] }), expected: JSON.stringify([[1], [2, 3]]), isHidden: true },
      { input: JSON.stringify({ tree: [1, 2, null, 3] }), expected: JSON.stringify([[1], [2], [3]]), isHidden: true },
    ],
  },
  {
    title: 'Sum of Left Leaves',
    description: `Given a binary tree as a level-order list (with \`null\`), return the sum of all left leaves.

A leaf is a node with no children. A left leaf is a leaf that is the left child of its parent.`,
    
    constraints: `- 0 ≤ len(tree) ≤ 10⁴\n- -10⁵ ≤ tree[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['trees'],
    primaryConcept: 'trees',
    secondaryConcepts: ['recursion'],
    testCases: [
      { input: JSON.stringify({ tree: [3, 9, 20, null, null, 15, 7] }), expected: '24', isHidden: false },
      { input: JSON.stringify({ tree: [1] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ tree: [] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ tree: [1, 2, 3] }), expected: '2', isHidden: true },
      { input: JSON.stringify({ tree: [1, null, 2] }), expected: '0', isHidden: true },
    ],
  },

  // === graphs (3) ===
  {
    title: 'Number of Islands',
    description: `Given a 2D grid of 0s (water) and 1s (land), count the number of islands (connected components of 1s, 4-directional).`,
    
    constraints: `- 0 ≤ len(grid) ≤ 10⁵`,
difficulty: Difficulty.HARD,
    tags: ['graphs', 'dfs', 'bfs'],
    primaryConcept: 'graphs',
    secondaryConcepts: ['recursion'],
    testCases: [
      { input: JSON.stringify({ grid: [[1, 1, 0, 0], [1, 0, 0, 1], [0, 0, 0, 1]] }), expected: '2', isHidden: false },
      { input: JSON.stringify({ grid: [[0]] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ grid: [] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ grid: [[1]] }), expected: '1', isHidden: true },
      { input: JSON.stringify({ grid: [[1, 1, 1], [1, 1, 1], [1, 1, 1]] }), expected: '1', isHidden: true },
    ],
  },
  {
    title: 'BFS Shortest Path in Grid',
    description: `Given a 2D grid of 0s (passable) and 1s (obstacle), return the shortest path length from top-left to bottom-right. Move 4-directional. Return -1 if unreachable. Count cells visited (including start and end).`,
    
    constraints: `- 0 ≤ len(grid) ≤ 10⁵`,
difficulty: Difficulty.HARD,
    tags: ['graphs', 'bfs'],
    primaryConcept: 'graphs',
    secondaryConcepts: ['queues'],
    testCases: [
      { input: JSON.stringify({ grid: [[0, 0, 0], [1, 1, 0], [0, 0, 0]] }), expected: '5', isHidden: false },
      { input: JSON.stringify({ grid: [[0, 1], [1, 0]] }), expected: '-1', isHidden: false },
      { input: JSON.stringify({ grid: [[0]] }), expected: '1', isHidden: true },
      { input: JSON.stringify({ grid: [[1]] }), expected: '-1', isHidden: true },
      { input: JSON.stringify({ grid: [[0, 0], [0, 0]] }), expected: '3', isHidden: true },
    ],
  },
  {
    title: 'Course Schedule Cycle Detect',
    description: `Given \`num_courses\` and prerequisites as \`[[a, b], ...]\` meaning to take a you must first take b, return \`True\` if all courses can be finished (i.e., the dependency graph has no cycle).`,
    
    constraints: `- -10⁹ ≤ num_courses ≤ 10⁹\n- 0 ≤ len(prerequisites) ≤ 10⁵`,
difficulty: Difficulty.HARD,
    tags: ['graphs', 'topological-sort'],
    primaryConcept: 'graphs',
    secondaryConcepts: ['queues'],
    testCases: [
      { input: JSON.stringify({ num_courses: 2, prerequisites: [[1, 0]] }), expected: 'true', isHidden: false },
      { input: JSON.stringify({ num_courses: 2, prerequisites: [[1, 0], [0, 1]] }), expected: 'false', isHidden: false },
      { input: JSON.stringify({ num_courses: 1, prerequisites: [] }), expected: 'true', isHidden: true },
      { input: JSON.stringify({ num_courses: 4, prerequisites: [[1, 0], [2, 1], [3, 2]] }), expected: 'true', isHidden: true },
      { input: JSON.stringify({ num_courses: 3, prerequisites: [[0, 1], [1, 2], [2, 0]] }), expected: 'false', isHidden: true },
    ],
  },

  // === backtracking (3) ===
  {
    title: 'All Permutations',
    description: `Given a list of distinct integers, return all possible permutations as a sorted list of lists (ascending lexicographic).`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁵\n- -10⁹ ≤ nums[i] ≤ 10⁹`,
difficulty: Difficulty.HARD,
    tags: ['backtracking'],
    primaryConcept: 'backtracking',
    secondaryConcepts: ['recursion'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3] }), expected: JSON.stringify([[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]), isHidden: false },
      { input: JSON.stringify({ nums: [1] }), expected: JSON.stringify([[1]]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([[]]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2] }), expected: JSON.stringify([[1, 2], [2, 1]]), isHidden: true },
      { input: JSON.stringify({ nums: [5, 3] }), expected: JSON.stringify([[3, 5], [5, 3]]), isHidden: true },
    ],
  },
  {
    title: 'Subsets',
    description: `Given a list of distinct integers, return all subsets sorted ascending by length then by lexicographic order of elements.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['backtracking', 'subsets'],
    primaryConcept: 'backtracking',
    secondaryConcepts: ['recursion'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3] }), expected: JSON.stringify([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([[]]), isHidden: false },
      { input: JSON.stringify({ nums: [1] }), expected: JSON.stringify([[], [1]]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2] }), expected: JSON.stringify([[], [1], [2], [1, 2]]), isHidden: true },
      { input: JSON.stringify({ nums: [5, 3] }), expected: JSON.stringify([[], [3], [5], [3, 5]]), isHidden: true },
    ],
  },
  {
    title: 'N-Queens Count',
    description: `Return the number of distinct solutions to the N-Queens puzzle for a given n (1 ≤ n ≤ 8).`,
    
    constraints: `- -10⁹ ≤ n ≤ 10⁹`,
difficulty: Difficulty.HARD,
    tags: ['backtracking', 'n-queens'],
    primaryConcept: 'backtracking',
    secondaryConcepts: ['recursion'],
    testCases: [
      { input: '4', expected: '2', isHidden: false },
      { input: '1', expected: '1', isHidden: false },
      { input: '2', expected: '0', isHidden: true },
      { input: '3', expected: '0', isHidden: true },
      { input: '5', expected: '10', isHidden: true },
    ],
  },

  // === bit_manipulation (4) ===
  {
    title: 'Single Number XOR',
    description: `Given a list where every element appears twice except one, find the unique element using XOR.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['bit-manipulation', 'xor'],
    primaryConcept: 'bit_manipulation',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ nums: [4, 1, 2, 1, 2] }), expected: '4', isHidden: false },
      { input: JSON.stringify({ nums: [2, 2, 1] }), expected: '1', isHidden: false },
      { input: JSON.stringify({ nums: [1] }), expected: '1', isHidden: true },
      { input: JSON.stringify({ nums: [3, 3, 7, 7, 5] }), expected: '5', isHidden: true },
      { input: JSON.stringify({ nums: [0, 1, 0] }), expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Count Set Bits',
    description: `Return the number of 1-bits in the binary representation of a non-negative integer.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['bit-manipulation'],
    primaryConcept: 'bit_manipulation',
    secondaryConcepts: [],
    testCases: [
      { input: '11', expected: '3', isHidden: false },
      { input: '0', expected: '0', isHidden: false },
      { input: '7', expected: '3', isHidden: true },
      { input: '255', expected: '8', isHidden: true },
      { input: '1024', expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Power of Two Check',
    description: `Return \`True\` if n is a power of two (n > 0), otherwise \`False\`. Use bit manipulation.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    tags: ['bit-manipulation'],
    primaryConcept: 'bit_manipulation',
    secondaryConcepts: ['conditionals'],
    testCases: [
      { input: '16', expected: 'true', isHidden: false },
      { input: '18', expected: 'false', isHidden: false },
      { input: '1', expected: 'true', isHidden: true },
      { input: '0', expected: 'false', isHidden: true },
      { input: '1024', expected: 'true', isHidden: true },
    ],
  },
  {
    title: 'Missing Number XOR',
    description: `Given a list containing n distinct numbers in range [0, n], return the single missing number using XOR.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    tags: ['bit-manipulation', 'xor'],
    primaryConcept: 'bit_manipulation',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ nums: [3, 0, 1] }), expected: '2', isHidden: false },
      { input: JSON.stringify({ nums: [0, 1] }), expected: '2', isHidden: false },
      { input: JSON.stringify({ nums: [9, 6, 4, 2, 3, 5, 7, 0, 1] }), expected: '8', isHidden: true },
      { input: JSON.stringify({ nums: [0] }), expected: '1', isHidden: true },
      { input: JSON.stringify({ nums: [1] }), expected: '0', isHidden: true },
    ],
  },
];
