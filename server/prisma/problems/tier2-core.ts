import { Difficulty } from '@prisma/client';
import { ProblemDef } from './types';

/**
 * Tier 2 — Core Skills (45 problems)
 * Concepts: nested_loops, functions, parameters, return_values, lists, tuples, dictionaries, searching
 * Difficulty mix: mostly EASY with some MEDIUM
 */
export const TIER2: ProblemDef[] = [
  // === nested_loops (5) ===
  {
    title: 'Matrix Sum',
    description: `Write a function \`solution(matrix)\` that returns the sum of all elements in a 2D list (matrix).`,
    
    constraints: `- 0 ≤ len(matrix) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'nested_loops',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ matrix: [[1, 2, 3], [4, 5, 6]] }), expected: '21', isHidden: false },
      { input: JSON.stringify({ matrix: [[1]] }), expected: '1', isHidden: false },
      { input: JSON.stringify({ matrix: [] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ matrix: [[1, 1], [1, 1], [1, 1]] }), expected: '6', isHidden: true },
      { input: JSON.stringify({ matrix: [[-1, 1], [-2, 2]] }), expected: '0', isHidden: true },
    ],
  },
  {
    title: 'Identity Matrix',
    description: `Write a function \`solution(n)\` that returns an n×n identity matrix as a list of lists (1 on diagonal, 0 elsewhere).`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'nested_loops',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: '3', expected: JSON.stringify([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), isHidden: false },
      { input: '1', expected: JSON.stringify([[1]]), isHidden: false },
      { input: '2', expected: JSON.stringify([[1, 0], [0, 1]]), isHidden: true },
      { input: '4', expected: JSON.stringify([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]), isHidden: true },
      { input: '5', expected: JSON.stringify([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]), isHidden: true },
    ],
  },
  {
    title: 'Count Pairs with Sum',
    description: `Write a function \`solution(nums, target)\` that returns the number of unordered pairs (i, j) with i < j such that nums[i] + nums[j] == target. Use nested loops.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴\n- -10⁴ ≤ target ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'nested_loops',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4], target: 5 }), expected: '2', isHidden: false },
      { input: JSON.stringify({ nums: [1, 1, 1, 1], target: 2 }), expected: '6', isHidden: false },
      { input: JSON.stringify({ nums: [], target: 0 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [5], target: 10 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [0, 0, 0], target: 0 }), expected: '3', isHidden: true },
    ],
  },
  {
    title: 'Transpose Matrix',
    description: `Write a function \`solution(matrix)\` that returns the transpose of a 2D matrix (rows become columns).`,
    
    constraints: `- 0 ≤ len(matrix) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'nested_loops',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ matrix: [[1, 2, 3], [4, 5, 6]] }), expected: JSON.stringify([[1, 4], [2, 5], [3, 6]]), isHidden: false },
      { input: JSON.stringify({ matrix: [[1]] }), expected: JSON.stringify([[1]]), isHidden: false },
      { input: JSON.stringify({ matrix: [[1, 2], [3, 4]] }), expected: JSON.stringify([[1, 3], [2, 4]]), isHidden: true },
      { input: JSON.stringify({ matrix: [[1], [2], [3]] }), expected: JSON.stringify([[1, 2, 3]]), isHidden: true },
      { input: JSON.stringify({ matrix: [[1, 2, 3]] }), expected: JSON.stringify([[1], [2], [3]]), isHidden: true },
    ],
  },
  {
    title: 'Matrix Diagonal Sum',
    description: `Write a function \`solution(matrix)\` that returns the sum of the main diagonal of a square matrix.`,
    
    constraints: `- 0 ≤ len(matrix) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'nested_loops',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ matrix: [[1, 2, 3], [4, 5, 6], [7, 8, 9]] }), expected: '15', isHidden: false },
      { input: JSON.stringify({ matrix: [[1]] }), expected: '1', isHidden: false },
      { input: JSON.stringify({ matrix: [[2, 0], [0, 3]] }), expected: '5', isHidden: true },
      { input: JSON.stringify({ matrix: [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]] }), expected: '4', isHidden: true },
      { input: JSON.stringify({ matrix: [[-1, 2], [3, -4]] }), expected: '-5', isHidden: true },
    ],
  },

  // === functions / parameters / return_values (5) ===
  {
    title: 'Min Max Pair',
    description: `Write a function \`solution(nums)\` that returns a list \`[minimum, maximum]\` of a non-empty list of integers.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'return_values',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [3, 1, 4, 1, 5, 9] }), expected: JSON.stringify([1, 9]), isHidden: false },
      { input: JSON.stringify({ nums: [7] }), expected: JSON.stringify([7, 7]), isHidden: false },
      { input: JSON.stringify({ nums: [-5, -2, -10] }), expected: JSON.stringify([-10, -2]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 5] }), expected: JSON.stringify([1, 5]), isHidden: true },
      { input: JSON.stringify({ nums: [0, 0, 0] }), expected: JSON.stringify([0, 0]), isHidden: true },
    ],
  },
  {
    title: 'Sum and Product',
    description: `Write a function \`solution(a, b)\` that returns a list \`[sum, product]\` of two integers.`,
    
    constraints: `- -10⁴ ≤ a ≤ 10⁴\n- -10⁴ ≤ b ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'return_values',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ a: 3, b: 4 }), expected: JSON.stringify([7, 12]), isHidden: false },
      { input: JSON.stringify({ a: 0, b: 5 }), expected: JSON.stringify([5, 0]), isHidden: false },
      { input: JSON.stringify({ a: -2, b: 3 }), expected: JSON.stringify([1, -6]), isHidden: true },
      { input: JSON.stringify({ a: 10, b: 10 }), expected: JSON.stringify([20, 100]), isHidden: true },
      { input: JSON.stringify({ a: 1, b: 1 }), expected: JSON.stringify([2, 1]), isHidden: true },
    ],
  },
  {
    title: 'Apply Discount',
    description: `Write a function \`solution(price, discount_percent)\` that returns the discounted price rounded to 2 decimal places. \`discount_percent\` is between 0 and 100.`,
    
    constraints: `- -10⁴ ≤ price ≤ 10⁴\n- -10⁴ ≤ discount_percent ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'parameters',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ price: 100, discount_percent: 20 }), expected: '80.0', isHidden: false },
      { input: JSON.stringify({ price: 50, discount_percent: 10 }), expected: '45.0', isHidden: false },
      { input: JSON.stringify({ price: 0, discount_percent: 50 }), expected: '0.0', isHidden: true },
      { input: JSON.stringify({ price: 99.99, discount_percent: 0 }), expected: '99.99', isHidden: true },
      { input: JSON.stringify({ price: 200, discount_percent: 100 }), expected: '0.0', isHidden: true },
    ],
  },
  {
    title: 'BMI Calculator',
    description: `Write a function \`solution(weight_kg, height_m)\` that returns BMI rounded to 2 decimal places.

**Formula:** \`BMI = weight / (height ** 2)\``,
    
    constraints: `- -10⁴ ≤ weight_kg ≤ 10⁴\n- -10⁴ ≤ height_m ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'parameters',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ weight_kg: 70, height_m: 1.75 }), expected: '22.86', isHidden: false },
      { input: JSON.stringify({ weight_kg: 60, height_m: 1.6 }), expected: '23.44', isHidden: false },
      { input: JSON.stringify({ weight_kg: 80, height_m: 1.8 }), expected: '24.69', isHidden: true },
      { input: JSON.stringify({ weight_kg: 50, height_m: 1.5 }), expected: '22.22', isHidden: true },
      { input: JSON.stringify({ weight_kg: 100, height_m: 2 }), expected: '25.0', isHidden: true },
    ],
  },
  {
    title: 'Compound Interest',
    description: `Write a function \`solution(principal, rate, years)\` that returns the compound interest final amount rounded to 2 decimal places. \`rate\` is the annual rate as a decimal (e.g. 0.05 for 5%), compounded yearly.

**Formula:** \`A = P * (1 + r) ** n\``,
    
    constraints: `- -10⁴ ≤ principal ≤ 10⁴\n- -10⁴ ≤ rate ≤ 10⁴\n- -10⁴ ≤ years ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'parameters',
    secondaryConcepts: ['return_values', 'operators'],
    testCases: [
      { input: JSON.stringify({ principal: 1000, rate: 0.05, years: 10 }), expected: '1628.89', isHidden: false },
      { input: JSON.stringify({ principal: 100, rate: 0.1, years: 1 }), expected: '110.0', isHidden: false },
      { input: JSON.stringify({ principal: 0, rate: 0.05, years: 5 }), expected: '0.0', isHidden: true },
      { input: JSON.stringify({ principal: 500, rate: 0, years: 10 }), expected: '500.0', isHidden: true },
      { input: JSON.stringify({ principal: 2000, rate: 0.03, years: 5 }), expected: '2318.55', isHidden: true },
    ],
  },

  // === lists (12) ===
  {
    title: 'List Sum',
    description: `Write a function \`solution(nums)\` that returns the sum of a list of integers. Return 0 for an empty list.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 5] }), expected: '15', isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ nums: [-1, 1] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [100] }), expected: '100', isHidden: true },
      { input: JSON.stringify({ nums: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] }), expected: '10', isHidden: true },
    ],
  },
  {
    title: 'List Maximum',
    description: `Write a function \`solution(nums)\` that returns the maximum value of a non-empty list.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ nums: [3, 1, 4, 1, 5, 9, 2, 6] }), expected: '9', isHidden: false },
      { input: JSON.stringify({ nums: [1] }), expected: '1', isHidden: false },
      { input: JSON.stringify({ nums: [-5, -3, -10] }), expected: '-3', isHidden: true },
      { input: JSON.stringify({ nums: [0, 0, 0] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [100, 200, 150] }), expected: '200', isHidden: true },
    ],
  },
  {
    title: 'List Minimum',
    description: `Write a function \`solution(nums)\` that returns the minimum value of a non-empty list.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ nums: [3, 1, 4, 1, 5] }), expected: '1', isHidden: false },
      { input: JSON.stringify({ nums: [7] }), expected: '7', isHidden: false },
      { input: JSON.stringify({ nums: [-1, -5, -3] }), expected: '-5', isHidden: true },
      { input: JSON.stringify({ nums: [10, 20, 30] }), expected: '10', isHidden: true },
      { input: JSON.stringify({ nums: [0, 1, 0] }), expected: '0', isHidden: true },
    ],
  },
  {
    title: 'Count Occurrences',
    description: `Write a function \`solution(nums, target)\` that returns how many times \`target\` appears in the list.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴\n- -10⁴ ≤ target ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 2, 3, 2, 4], target: 2 }), expected: '3', isHidden: false },
      { input: JSON.stringify({ nums: [1, 1, 1, 1], target: 1 }), expected: '4', isHidden: false },
      { input: JSON.stringify({ nums: [], target: 5 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3], target: 5 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [0, 0, 1, 0], target: 0 }), expected: '3', isHidden: true },
    ],
  },
  {
    title: 'Remove Duplicates Preserve Order',
    description: `Write a function \`solution(nums)\` that returns the list with duplicates removed, preserving first-seen order.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 1, 3, 2, 4] }), expected: JSON.stringify([1, 2, 3, 4]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 1, 1] }), expected: JSON.stringify([1]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ nums: [5, 4, 3, 2, 1] }), expected: JSON.stringify([5, 4, 3, 2, 1]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3, 1, 2, 3] }), expected: JSON.stringify([1, 2, 3]), isHidden: true },
    ],
  },
  {
    title: 'Flatten 2D List',
    description: `Write a function \`solution(matrix)\` that returns a flat 1D list containing all elements of a 2D list, row by row.`,
    
    constraints: `- 0 ≤ len(matrix) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['nested_loops'],
    testCases: [
      { input: JSON.stringify({ matrix: [[1, 2], [3, 4], [5]] }), expected: JSON.stringify([1, 2, 3, 4, 5]), isHidden: false },
      { input: JSON.stringify({ matrix: [[1]] }), expected: JSON.stringify([1]), isHidden: false },
      { input: JSON.stringify({ matrix: [] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ matrix: [[], []] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ matrix: [[1, 2, 3], [4, 5, 6]] }), expected: JSON.stringify([1, 2, 3, 4, 5, 6]), isHidden: true },
    ],
  },
  {
    title: 'Rotate List Right',
    description: `Write a function \`solution(nums, k)\` that rotates the list \`nums\` to the right by \`k\` positions and returns the result. \`k\` can be larger than the list length.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵\n- -10⁵ ≤ k ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'lists',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 5], k: 2 }), expected: JSON.stringify([4, 5, 1, 2, 3]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3], k: 1 }), expected: JSON.stringify([3, 1, 2]), isHidden: false },
      { input: JSON.stringify({ nums: [], k: 3 }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ nums: [1], k: 100 }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3, 4], k: 6 }), expected: JSON.stringify([3, 4, 1, 2]), isHidden: true },
    ],
  },
  {
    title: 'Second Largest',
    description: `Write a function \`solution(nums)\` that returns the second largest distinct value in a list. If fewer than 2 distinct values exist, return \`None\`.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'lists',
    secondaryConcepts: ['conditionals'],
    testCases: [
      { input: JSON.stringify({ nums: [3, 1, 4, 1, 5, 9, 2, 6] }), expected: '6', isHidden: false },
      { input: JSON.stringify({ nums: [5, 5, 5] }), expected: 'null', isHidden: false },
      { input: JSON.stringify({ nums: [1, 2] }), expected: '1', isHidden: true },
      { input: JSON.stringify({ nums: [10] }), expected: 'null', isHidden: true },
      { input: JSON.stringify({ nums: [7, 7, 8, 8] }), expected: '7', isHidden: true },
    ],
  },
  {
    title: 'Reverse a List',
    description: `Write a function \`solution(nums)\` that returns the reverse of a list without using \`reversed()\` or slicing tricks. Use a loop.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4] }), expected: JSON.stringify([4, 3, 2, 1]), isHidden: false },
      { input: JSON.stringify({ nums: [1] }), expected: JSON.stringify([1]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2] }), expected: JSON.stringify([2, 1]), isHidden: true },
      { input: JSON.stringify({ nums: [5, 5, 5, 5] }), expected: JSON.stringify([5, 5, 5, 5]), isHidden: true },
    ],
  },
  {
    title: 'Even Numbers Only',
    description: `Write a function \`solution(nums)\` that returns a list containing only the even numbers from the input, in original order.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['conditionals'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 5, 6] }), expected: JSON.stringify([2, 4, 6]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 3, 5] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ nums: [2, 4, 6, 8] }), expected: JSON.stringify([2, 4, 6, 8]), isHidden: true },
      { input: JSON.stringify({ nums: [-2, -1, 0, 1, 2] }), expected: JSON.stringify([-2, 0, 2]), isHidden: true },
    ],
  },
  {
    title: 'Double Each Element',
    description: `Write a function \`solution(nums)\` that returns a new list with each element doubled.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3] }), expected: JSON.stringify([2, 4, 6]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ nums: [0, -1, -2] }), expected: JSON.stringify([0, -2, -4]), isHidden: true },
      { input: JSON.stringify({ nums: [5] }), expected: JSON.stringify([10]), isHidden: true },
      { input: JSON.stringify({ nums: [10, 20, 30, 40] }), expected: JSON.stringify([20, 40, 60, 80]), isHidden: true },
    ],
  },
  {
    title: 'Concatenate Lists',
    description: `Write a function \`solution(a, b)\` that returns the concatenation of two lists.`,
    
    constraints: `- 0 ≤ len(a) ≤ 100\n- -10⁴ ≤ a[i] ≤ 10⁴\n- 0 ≤ len(b) ≤ 100\n- -10⁴ ≤ b[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ a: [1, 2], b: [3, 4] }), expected: JSON.stringify([1, 2, 3, 4]), isHidden: false },
      { input: JSON.stringify({ a: [], b: [1] }), expected: JSON.stringify([1]), isHidden: false },
      { input: JSON.stringify({ a: [1], b: [] }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ a: [], b: [] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ a: [1, 2, 3], b: [4, 5, 6] }), expected: JSON.stringify([1, 2, 3, 4, 5, 6]), isHidden: true },
    ],
  },

  // === tuples (3) ===
  {
    title: 'Tuple Swap',
    description: `Write a function \`solution(pair)\` that takes a list of two elements and returns them swapped as a list.`,
    
    constraints: `- 0 ≤ len(pair) ≤ 100\n- -10⁴ ≤ pair[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'tuples',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ pair: [1, 2] }), expected: JSON.stringify([2, 1]), isHidden: false },
      { input: JSON.stringify({ pair: [5, 5] }), expected: JSON.stringify([5, 5]), isHidden: false },
      { input: JSON.stringify({ pair: [0, 100] }), expected: JSON.stringify([100, 0]), isHidden: true },
      { input: JSON.stringify({ pair: [-1, 1] }), expected: JSON.stringify([1, -1]), isHidden: true },
      { input: JSON.stringify({ pair: [42, 0] }), expected: JSON.stringify([0, 42]), isHidden: true },
    ],
  },
  {
    title: 'Split Even Odd',
    description: `Write a function \`solution(nums)\` that returns a list \`[evens, odds]\` where evens and odds are lists of even and odd numbers respectively.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'tuples',
    secondaryConcepts: ['lists', 'conditionals'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 5] }), expected: JSON.stringify([[2, 4], [1, 3, 5]]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([[], []]), isHidden: false },
      { input: JSON.stringify({ nums: [2, 4, 6] }), expected: JSON.stringify([[2, 4, 6], []]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 3, 5] }), expected: JSON.stringify([[], [1, 3, 5]]), isHidden: true },
      { input: JSON.stringify({ nums: [0] }), expected: JSON.stringify([[0], []]), isHidden: true },
    ],
  },
  {
    title: 'Coordinate Distance',
    description: `Write a function \`solution(p1, p2)\` that computes the Euclidean distance between two 2D points given as lists \`[x, y]\`, rounded to 2 decimal places.`,
    
    constraints: `- 0 ≤ len(p1) ≤ 100\n- -10⁴ ≤ p1[i] ≤ 10⁴\n- 0 ≤ len(p2) ≤ 100\n- -10⁴ ≤ p2[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'tuples',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ p1: [0, 0], p2: [3, 4] }), expected: '5.0', isHidden: false },
      { input: JSON.stringify({ p1: [1, 1], p2: [1, 1] }), expected: '0.0', isHidden: false },
      { input: JSON.stringify({ p1: [0, 0], p2: [1, 1] }), expected: '1.41', isHidden: true },
      { input: JSON.stringify({ p1: [-1, -1], p2: [2, 3] }), expected: '5.0', isHidden: true },
      { input: JSON.stringify({ p1: [0, 0], p2: [6, 8] }), expected: '10.0', isHidden: true },
    ],
  },

  // === dictionaries (8) ===
  {
    title: 'Dict from Pairs',
    description: `Write a function \`solution(pairs)\` that converts a list of \`[key, value]\` pairs into a dictionary. If a key appears multiple times, later values overwrite earlier ones.`,
    
    constraints: `- 0 ≤ len(pairs) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'dictionaries',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ pairs: [['a', 1], ['b', 2]] }), expected: JSON.stringify({ a: 1, b: 2 }), isHidden: false },
      { input: JSON.stringify({ pairs: [] }), expected: JSON.stringify({}), isHidden: false },
      { input: JSON.stringify({ pairs: [['x', 1], ['x', 2]] }), expected: JSON.stringify({ x: 2 }), isHidden: true },
      { input: JSON.stringify({ pairs: [['only', 42]] }), expected: JSON.stringify({ only: 42 }), isHidden: true },
      { input: JSON.stringify({ pairs: [['a', 1], ['b', 2], ['c', 3]] }), expected: JSON.stringify({ a: 1, b: 2, c: 3 }), isHidden: true },
    ],
  },
  {
    title: 'Character Frequency',
    description: `Write a function \`solution(s)\` that returns a dictionary mapping each character in the string to its frequency.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'dictionaries',
    secondaryConcepts: ['strings', 'loops'],
    testCases: [
      { input: '"hello"', expected: JSON.stringify({ h: 1, e: 1, l: 2, o: 1 }), isHidden: false },
      { input: '"aaa"', expected: JSON.stringify({ a: 3 }), isHidden: false },
      { input: '""', expected: JSON.stringify({}), isHidden: true },
      { input: '"ab"', expected: JSON.stringify({ a: 1, b: 1 }), isHidden: true },
      { input: '"aabbcc"', expected: JSON.stringify({ a: 2, b: 2, c: 2 }), isHidden: true },
    ],
  },
  {
    title: 'Word Count',
    description: `Write a function \`solution(sentence)\` that returns a dictionary mapping each unique word to how many times it appears in the sentence. Words are separated by spaces.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'dictionaries',
    secondaryConcepts: ['strings'],
    testCases: [
      { input: '"the cat sat on the mat"', expected: JSON.stringify({ the: 2, cat: 1, sat: 1, on: 1, mat: 1 }), isHidden: false },
      { input: '"hello world"', expected: JSON.stringify({ hello: 1, world: 1 }), isHidden: false },
      { input: '""', expected: JSON.stringify({}), isHidden: true },
      { input: '"a a a"', expected: JSON.stringify({ a: 3 }), isHidden: true },
      { input: '"one"', expected: JSON.stringify({ one: 1 }), isHidden: true },
    ],
  },
  {
    title: 'Merge Two Dicts',
    description: `Write a function \`solution(a, b)\` that merges two dictionaries. On key conflict, values from \`b\` win.`,
    difficulty: Difficulty.EASY,
    primaryConcept: 'dictionaries',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ a: { x: 1, y: 2 }, b: { y: 20, z: 30 } }), expected: JSON.stringify({ x: 1, y: 20, z: 30 }), isHidden: false },
      { input: JSON.stringify({ a: {}, b: { a: 1 } }), expected: JSON.stringify({ a: 1 }), isHidden: false },
      { input: JSON.stringify({ a: { a: 1 }, b: {} }), expected: JSON.stringify({ a: 1 }), isHidden: true },
      { input: JSON.stringify({ a: {}, b: {} }), expected: JSON.stringify({}), isHidden: true },
      { input: JSON.stringify({ a: { k: 1 }, b: { k: 2 } }), expected: JSON.stringify({ k: 2 }), isHidden: true },
    ],
  },
  {
    title: 'Invert Dict',
    description: `Write a function \`solution(d)\` that swaps keys and values in a dictionary. Assume values are unique and hashable.`,
    difficulty: Difficulty.EASY,
    primaryConcept: 'dictionaries',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ d: { a: 1, b: 2 } }), expected: JSON.stringify({ '1': 'a', '2': 'b' }), isHidden: false },
      { input: JSON.stringify({ d: {} }), expected: JSON.stringify({}), isHidden: false },
      { input: JSON.stringify({ d: { only: 99 } }), expected: JSON.stringify({ '99': 'only' }), isHidden: true },
      { input: JSON.stringify({ d: { x: 10, y: 20, z: 30 } }), expected: JSON.stringify({ '10': 'x', '20': 'y', '30': 'z' }), isHidden: true },
      { input: JSON.stringify({ d: { hello: 1 } }), expected: JSON.stringify({ '1': 'hello' }), isHidden: true },
    ],
  },
  {
    title: 'Most Frequent Element',
    description: `Write a function \`solution(nums)\` that returns the element that appears the most in a non-empty list. If there are ties, return the smallest such element.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'dictionaries',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 2, 3, 3, 3] }), expected: '3', isHidden: false },
      { input: JSON.stringify({ nums: [5] }), expected: '5', isHidden: false },
      { input: JSON.stringify({ nums: [1, 1, 2, 2] }), expected: '1', isHidden: true },
      { input: JSON.stringify({ nums: [4, 4, 4, 4] }), expected: '4', isHidden: true },
      { input: JSON.stringify({ nums: [10, 20, 10, 20, 30] }), expected: '10', isHidden: true },
    ],
  },
  {
    title: 'Dict Key Sum',
    description: `Write a function \`solution(d)\` that returns the sum of all numeric values in a dictionary.`,
    difficulty: Difficulty.EASY,
    primaryConcept: 'dictionaries',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ d: { a: 10, b: 20, c: 5 } }), expected: '35', isHidden: false },
      { input: JSON.stringify({ d: {} }), expected: '0', isHidden: false },
      { input: JSON.stringify({ d: { only: 42 } }), expected: '42', isHidden: true },
      { input: JSON.stringify({ d: { a: -1, b: 1 } }), expected: '0', isHidden: true },
      { input: JSON.stringify({ d: { x: 1, y: 2, z: 3, w: 4 } }), expected: '10', isHidden: true },
    ],
  },
  {
    title: 'Dict Contains Value',
    description: `Write a function \`solution(d, target)\` that returns \`True\` if \`target\` exists anywhere in the values of the dictionary.`,
    
    constraints: `- -10⁴ ≤ target ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'dictionaries',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ d: { a: 1, b: 2, c: 3 }, target: 2 }), expected: 'true', isHidden: false },
      { input: JSON.stringify({ d: { a: 1 }, target: 99 }), expected: 'false', isHidden: false },
      { input: JSON.stringify({ d: {}, target: 0 }), expected: 'false', isHidden: true },
      { input: JSON.stringify({ d: { x: 5, y: 5 }, target: 5 }), expected: 'true', isHidden: true },
      { input: JSON.stringify({ d: { a: 10 }, target: 10 }), expected: 'true', isHidden: true },
    ],
  },

  // === searching (7) ===
  {
    title: 'Linear Search',
    description: `Write a function \`solution(nums, target)\` that returns the first index of \`target\` in \`nums\`, or -1 if not found.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴\n- -10⁴ ≤ target ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'searching',
    secondaryConcepts: ['lists', 'loops'],
    testCases: [
      { input: JSON.stringify({ nums: [5, 3, 8, 1, 9], target: 8 }), expected: '2', isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3], target: 99 }), expected: '-1', isHidden: false },
      { input: JSON.stringify({ nums: [], target: 5 }), expected: '-1', isHidden: true },
      { input: JSON.stringify({ nums: [1, 1, 1], target: 1 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [5], target: 5 }), expected: '0', isHidden: true },
    ],
  },
  {
    title: 'Iterative Binary Search',
    description: `Write a function \`solution(nums, target)\` that performs binary search on a sorted list and returns the index of \`target\`, or -1 if not found. Use iteration.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵\n- -10⁵ ≤ target ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'searching',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 3, 5, 7, 9, 11], target: 7 }), expected: '3', isHidden: false },
      { input: JSON.stringify({ nums: [1, 3, 5, 7, 9, 11], target: 2 }), expected: '-1', isHidden: false },
      { input: JSON.stringify({ nums: [], target: 5 }), expected: '-1', isHidden: true },
      { input: JSON.stringify({ nums: [10], target: 10 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 5], target: 1 }), expected: '0', isHidden: true },
    ],
  },
  {
    title: 'Find Minimum Index',
    description: `Write a function \`solution(nums)\` that returns the index of the minimum element in a non-empty list. If there are ties, return the smallest index.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'searching',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [5, 2, 8, 2, 1, 4] }), expected: '4', isHidden: false },
      { input: JSON.stringify({ nums: [1] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ nums: [3, 3, 3] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [-1, -5, -3] }), expected: '1', isHidden: true },
      { input: JSON.stringify({ nums: [10, 20, 5, 30] }), expected: '2', isHidden: true },
    ],
  },
  {
    title: 'Count Less Than',
    description: `Write a function \`solution(nums, threshold)\` that returns how many elements are strictly less than \`threshold\`.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴\n- -10⁴ ≤ threshold ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'searching',
    secondaryConcepts: ['conditionals'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 5, 3, 8, 2], threshold: 4 }), expected: '3', isHidden: false },
      { input: JSON.stringify({ nums: [], threshold: 5 }), expected: '0', isHidden: false },
      { input: JSON.stringify({ nums: [1, 1, 1], threshold: 2 }), expected: '3', isHidden: true },
      { input: JSON.stringify({ nums: [10, 20, 30], threshold: 5 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [5, 5, 5], threshold: 5 }), expected: '0', isHidden: true },
    ],
  },
  {
    title: 'Find Pair with Sum',
    description: `Write a function \`solution(nums, target)\` that returns \`True\` if any two distinct indices have values summing to \`target\`, otherwise \`False\`.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵\n- -10⁵ ≤ target ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'searching',
    secondaryConcepts: ['nested_loops'],
    testCases: [
      { input: JSON.stringify({ nums: [2, 7, 11, 15], target: 9 }), expected: 'true', isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3], target: 99 }), expected: 'false', isHidden: false },
      { input: JSON.stringify({ nums: [], target: 0 }), expected: 'false', isHidden: true },
      { input: JSON.stringify({ nums: [3, 3], target: 6 }), expected: 'true', isHidden: true },
      { input: JSON.stringify({ nums: [5], target: 5 }), expected: 'false', isHidden: true },
    ],
  },
  {
    title: 'First Duplicate',
    description: `Write a function \`solution(nums)\` that returns the first element that appears more than once (scanning left to right), or \`None\` if no duplicate exists.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'searching',
    secondaryConcepts: ['dictionaries'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 2, 1] }), expected: '2', isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3] }), expected: 'null', isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: 'null', isHidden: true },
      { input: JSON.stringify({ nums: [5, 5] }), expected: '5', isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 3] }), expected: '3', isHidden: true },
    ],
  },
  {
    title: 'Range Contains',
    description: `Write a function \`solution(nums, lo, hi)\` that returns how many elements of \`nums\` fall in the inclusive range [lo, hi].`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴\n- -10⁴ ≤ lo ≤ 10⁴\n- -10⁴ ≤ hi ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'searching',
    secondaryConcepts: ['conditionals'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 3, 5, 7, 9], lo: 3, hi: 7 }), expected: '3', isHidden: false },
      { input: JSON.stringify({ nums: [], lo: 0, hi: 10 }), expected: '0', isHidden: false },
      { input: JSON.stringify({ nums: [5, 5, 5], lo: 5, hi: 5 }), expected: '3', isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3], lo: 10, hi: 20 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ nums: [-5, 0, 5], lo: -3, hi: 3 }), expected: '1', isHidden: true },
    ],
  },

  // === extra lists/dict fillers (5) ===
  {
    title: 'Sum Even Indices',
    description: `Write a function \`solution(nums)\` that returns the sum of elements at even indices (0, 2, 4, ...).`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 5] }), expected: '9', isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ nums: [10] }), expected: '10', isHidden: true },
      { input: JSON.stringify({ nums: [1, 2] }), expected: '1', isHidden: true },
      { input: JSON.stringify({ nums: [1, 1, 1, 1, 1, 1] }), expected: '3', isHidden: true },
    ],
  },
  {
    title: 'Running Sum',
    description: `Write a function \`solution(nums)\` that returns the running cumulative sum of a list.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4] }), expected: JSON.stringify([1, 3, 6, 10]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ nums: [5] }), expected: JSON.stringify([5]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 1, 1, 1, 1] }), expected: JSON.stringify([1, 2, 3, 4, 5]), isHidden: true },
      { input: JSON.stringify({ nums: [-1, 2, -3, 4] }), expected: JSON.stringify([-1, 1, -2, 2]), isHidden: true },
    ],
  },
  {
    title: 'Move Zeros to End',
    description: `Write a function \`solution(nums)\` that returns the list with all zeros moved to the end, preserving the order of non-zero elements.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: JSON.stringify({ nums: [0, 1, 0, 3, 12] }), expected: JSON.stringify([1, 3, 12, 0, 0]), isHidden: false },
      { input: JSON.stringify({ nums: [0, 0, 0] }), expected: JSON.stringify([0, 0, 0]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3] }), expected: JSON.stringify([1, 2, 3]), isHidden: true },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ nums: [0, 0, 1] }), expected: JSON.stringify([1, 0, 0]), isHidden: true },
    ],
  },
  {
    title: 'Odd Length Strings',
    description: `Write a function \`solution(words)\` that returns a list of words whose lengths are odd.`,
    
    constraints: `- 0 ≤ len(words) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'lists',
    secondaryConcepts: ['strings', 'conditionals'],
    testCases: [
      { input: JSON.stringify({ words: ['a', 'bb', 'ccc', 'dddd'] }), expected: JSON.stringify(['a', 'ccc']), isHidden: false },
      { input: JSON.stringify({ words: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ words: ['hello', 'world'] }), expected: JSON.stringify(['hello', 'world']), isHidden: true },
      { input: JSON.stringify({ words: ['ab', 'cd'] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ words: ['', 'x'] }), expected: JSON.stringify(['x']), isHidden: true },
    ],
  },
  {
    title: 'Dict from Keys',
    description: `Write a function \`solution(keys, default_value)\` that returns a dictionary with each key mapped to \`default_value\`.`,
    
    constraints: `- 0 ≤ len(keys) ≤ 100\n- -10⁴ ≤ default_value ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'dictionaries',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ keys: ['a', 'b', 'c'], default_value: 0 }), expected: JSON.stringify({ a: 0, b: 0, c: 0 }), isHidden: false },
      { input: JSON.stringify({ keys: [], default_value: 1 }), expected: JSON.stringify({}), isHidden: false },
      { input: JSON.stringify({ keys: ['x'], default_value: 99 }), expected: JSON.stringify({ x: 99 }), isHidden: true },
      { input: JSON.stringify({ keys: ['a', 'b'], default_value: -1 }), expected: JSON.stringify({ a: -1, b: -1 }), isHidden: true },
      { input: JSON.stringify({ keys: ['one', 'two', 'three'], default_value: 5 }), expected: JSON.stringify({ one: 5, two: 5, three: 5 }), isHidden: true },
    ],
  },
];
