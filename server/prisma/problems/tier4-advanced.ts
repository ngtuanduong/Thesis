import { Difficulty } from '@prisma/client';
import { ProblemDef } from './types';

/**
 * Tier 4 — Advanced (25 problems)
 * Concepts: inheritance, encapsulation, polymorphism, two_pointers, greedy, divide_and_conquer
 */
export const TIER4: ProblemDef[] = [
  // === inheritance (4) ===
  {
    title: 'Shape Area Polymorphism',
    description: `Implement base class \`Shape\` with a method \`area()\`, and derived classes \`Circle\`, \`Square\` overriding it. Given a list of shape specs, return the sum of all areas rounded to 2 decimal places.

Shape spec format:
- \`["circle", radius]\` → area = π * r² (use π = 3.14159)
- \`["square", side]\` → area = side²`,
    
    constraints: `- 0 ≤ len(shapes) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'inheritance',
    secondaryConcepts: ['polymorphism', 'classes'],
    testCases: [
      { input: JSON.stringify({ shapes: [['circle', 2], ['square', 3]] }), expected: '21.57', isHidden: false },
      { input: JSON.stringify({ shapes: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ shapes: [['circle', 1]] }), expected: '3.14', isHidden: true },
      { input: JSON.stringify({ shapes: [['square', 5]] }), expected: '25', isHidden: true },
      { input: JSON.stringify({ shapes: [['square', 2], ['square', 3]] }), expected: '13', isHidden: true },
    ],
  },
  {
    title: 'Employee Salary Hierarchy',
    description: `Implement \`Employee\` with method \`pay()\` returning base salary, and \`Manager(Employee)\` overriding \`pay()\` to add a 20% bonus. Given a list of employee specs, return the total payroll.

Spec format:
- \`["employee", salary]\`
- \`["manager", salary]\``,
    
    constraints: `- 0 ≤ len(staff) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'inheritance',
    secondaryConcepts: ['classes'],
    testCases: [
      { input: JSON.stringify({ staff: [['employee', 100], ['manager', 100]] }), expected: '220.0', isHidden: false },
      { input: JSON.stringify({ staff: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ staff: [['manager', 500]] }), expected: '600.0', isHidden: true },
      { input: JSON.stringify({ staff: [['employee', 200], ['employee', 300]] }), expected: '500', isHidden: true },
      { input: JSON.stringify({ staff: [['manager', 1000], ['employee', 500]] }), expected: '1700.0', isHidden: true },
    ],
  },
  {
    title: 'Animal Sound Polymorphism',
    description: `Implement base \`Animal\` with \`sound()\` returning \`"generic"\`, and derived \`Dog\`, \`Cat\`, \`Cow\` returning \`"woof"\`, \`"meow"\`, \`"moo"\` respectively. Given a list of animal types, return a list of sounds.`,
    
    constraints: `- 0 ≤ len(animals) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'inheritance',
    secondaryConcepts: ['polymorphism'],
    testCases: [
      { input: JSON.stringify({ animals: ['dog', 'cat', 'cow'] }), expected: JSON.stringify(['woof', 'meow', 'moo']), isHidden: false },
      { input: JSON.stringify({ animals: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ animals: ['dog'] }), expected: JSON.stringify(['woof']), isHidden: true },
      { input: JSON.stringify({ animals: ['cat', 'cat'] }), expected: JSON.stringify(['meow', 'meow']), isHidden: true },
      { input: JSON.stringify({ animals: ['cow', 'dog', 'cat', 'cow'] }), expected: JSON.stringify(['moo', 'woof', 'meow', 'moo']), isHidden: true },
    ],
  },
  {
    title: 'Vehicle Speed Override',
    description: `Implement \`Vehicle\` with \`max_speed()\` = 100, and \`Car(Vehicle)\` override = 150, \`Bike(Vehicle)\` override = 40. Given a list of vehicle types, return the sum of their max speeds.`,
    
    constraints: `- 0 ≤ len(vehicles) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'inheritance',
    secondaryConcepts: ['classes'],
    testCases: [
      { input: JSON.stringify({ vehicles: ['car', 'bike', 'car'] }), expected: '340', isHidden: false },
      { input: JSON.stringify({ vehicles: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ vehicles: ['bike'] }), expected: '40', isHidden: true },
      { input: JSON.stringify({ vehicles: ['car', 'car', 'car'] }), expected: '450', isHidden: true },
      { input: JSON.stringify({ vehicles: ['bike', 'bike'] }), expected: '80', isHidden: true },
    ],
  },

  // === encapsulation (3) ===
  {
    title: 'Private Balance Protection',
    description: `Implement a SafeAccount class with private balance. Only allow deposit (positive amount) and withdraw (if sufficient). Return the final balance after processing ops.

Ops: \`["deposit", amt]\`, \`["withdraw", amt]\`. Ignore deposits ≤ 0.`,
    
    constraints: `- 0 ≤ len(ops) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'encapsulation',
    secondaryConcepts: ['classes'],
    testCases: [
      { input: JSON.stringify({ ops: [['deposit', 100], ['deposit', -50], ['withdraw', 30]] }), expected: '70', isHidden: false },
      { input: JSON.stringify({ ops: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ ops: [['withdraw', 100]] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ ops: [['deposit', 0]] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ ops: [['deposit', 500], ['withdraw', 600]] }), expected: '500', isHidden: true },
    ],
  },
  {
    title: 'Temperature Validator',
    description: `Implement a Thermometer with private \`_celsius\` that clamps reads to [-50, 100]. Given a list of read values, return the final stored value.`,
    
    constraints: `- 0 ≤ len(readings) ≤ 100\n- -10⁴ ≤ readings[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'encapsulation',
    secondaryConcepts: ['conditionals'],
    testCases: [
      { input: JSON.stringify({ readings: [20, 150, -100, 50] }), expected: '50', isHidden: false },
      { input: JSON.stringify({ readings: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ readings: [200] }), expected: '100', isHidden: true },
      { input: JSON.stringify({ readings: [-200] }), expected: '-50', isHidden: true },
      { input: JSON.stringify({ readings: [0, 0, 0] }), expected: '0', isHidden: true },
    ],
  },
  {
    title: 'Password Strength Check',
    description: `Implement a User class whose \`set_password(pw)\` only accepts passwords with length ≥ 8 AND containing at least one digit. Return \`True\` if all passwords in the list would be accepted.`,
    
    constraints: `- 0 ≤ len(passwords) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'encapsulation',
    secondaryConcepts: ['strings', 'conditionals'],
    testCases: [
      { input: JSON.stringify({ passwords: ['abc12345', 'mypass99'] }), expected: 'true', isHidden: false },
      { input: JSON.stringify({ passwords: ['short1', 'longbutnodigits'] }), expected: 'false', isHidden: false },
      { input: JSON.stringify({ passwords: [] }), expected: 'true', isHidden: true },
      { input: JSON.stringify({ passwords: ['12345678'] }), expected: 'true', isHidden: true },
      { input: JSON.stringify({ passwords: ['abcdefgh'] }), expected: 'false', isHidden: true },
    ],
  },

  // === polymorphism (2) ===
  {
    title: 'Payment Processor Strategies',
    description: `Implement a Payment class with subclasses \`CreditCard\` (2% fee), \`DebitCard\` (1% fee), \`Cash\` (0% fee). Given a list of \`[method, amount]\` transactions, return the total fees collected rounded to 2 decimal places.`,
    
    constraints: `- 0 ≤ len(txs) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'polymorphism',
    secondaryConcepts: ['inheritance'],
    testCases: [
      { input: JSON.stringify({ txs: [['credit', 100], ['debit', 100], ['cash', 100]] }), expected: '3.0', isHidden: false },
      { input: JSON.stringify({ txs: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ txs: [['cash', 1000]] }), expected: '0.0', isHidden: true },
      { input: JSON.stringify({ txs: [['credit', 500]] }), expected: '10.0', isHidden: true },
      { input: JSON.stringify({ txs: [['debit', 200], ['debit', 300]] }), expected: '5.0', isHidden: true },
    ],
  },
  {
    title: 'Notification Dispatcher',
    description: `Implement a Notifier base with subclasses \`EmailNotifier\` (prepends \`"email: "\`), \`SmsNotifier\` (prepends \`"sms: "\`), \`PushNotifier\` (prepends \`"push: "\`). Given a list of \`[channel, message]\` pairs, return a list of formatted strings.`,
    
    constraints: `- 0 ≤ len(items) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'polymorphism',
    secondaryConcepts: ['inheritance'],
    testCases: [
      { input: JSON.stringify({ items: [['email', 'hi'], ['sms', 'ok']] }), expected: JSON.stringify(['email: hi', 'sms: ok']), isHidden: false },
      { input: JSON.stringify({ items: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ items: [['push', 'alert']] }), expected: JSON.stringify(['push: alert']), isHidden: true },
      { input: JSON.stringify({ items: [['email', '']] }), expected: JSON.stringify(['email: ']), isHidden: true },
      { input: JSON.stringify({ items: [['sms', 'a'], ['push', 'b'], ['email', 'c']] }), expected: JSON.stringify(['sms: a', 'push: b', 'email: c']), isHidden: true },
    ],
  },

  // === two_pointers (6) ===
  {
    title: 'Two Sum Sorted',
    description: `Given a sorted ascending list, find indices (1-indexed) of two numbers that add to target. Return \`[i, j]\` with i < j. Use two pointers.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵\n- -10⁵ ≤ target ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'two_pointers',
    secondaryConcepts: ['searching'],
    testCases: [
      { input: JSON.stringify({ nums: [1, 2, 3, 4, 6], target: 6 }), expected: JSON.stringify([2, 4]), isHidden: false },
      { input: JSON.stringify({ nums: [2, 3, 4], target: 6 }), expected: JSON.stringify([1, 3]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3], target: 100 }), expected: JSON.stringify([-1, -1]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 1], target: 2 }), expected: JSON.stringify([1, 2]), isHidden: true },
      { input: JSON.stringify({ nums: [-3, -1, 0, 2, 4], target: 1 }), expected: JSON.stringify([1, 5]), isHidden: true },
    ],
  },
  {
    title: 'Is Palindrome Two Pointers',
    description: `Write a function \`solution(s)\` that returns \`True\` if a string is a palindrome using two pointers (no slicing).`,
    
    constraints: `- 0 ≤ len(s) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'two_pointers',
    secondaryConcepts: ['strings'],
    testCases: [
      { input: '"racecar"', expected: 'true', isHidden: false },
      { input: '"hello"', expected: 'false', isHidden: false },
      { input: '""', expected: 'true', isHidden: true },
      { input: '"a"', expected: 'true', isHidden: true },
      { input: '"abba"', expected: 'true', isHidden: true },
    ],
  },
  {
    title: 'Remove Target In-Place',
    description: `Given a list and a target value, return a new list with all occurrences of target removed, preserving order.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴\n- -10⁴ ≤ target ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'two_pointers',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [3, 2, 2, 3], target: 3 }), expected: JSON.stringify([2, 2]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3, 4], target: 5 }), expected: JSON.stringify([1, 2, 3, 4]), isHidden: false },
      { input: JSON.stringify({ nums: [], target: 1 }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 1, 1], target: 1 }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ nums: [0, 1, 0, 2], target: 0 }), expected: JSON.stringify([1, 2]), isHidden: true },
    ],
  },
  {
    title: 'Container With Most Water',
    description: `Given an array of heights, find two lines that together with the x-axis form a container with the most water. Return the max area. Use two pointers.`,
    
    constraints: `- 0 ≤ len(heights) ≤ 10⁴\n- -10⁵ ≤ heights[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'two_pointers',
    secondaryConcepts: ['greedy'],
    testCases: [
      { input: JSON.stringify({ heights: [1, 8, 6, 2, 5, 4, 8, 3, 7] }), expected: '49', isHidden: false },
      { input: JSON.stringify({ heights: [1, 1] }), expected: '1', isHidden: false },
      { input: JSON.stringify({ heights: [] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ heights: [4, 3, 2, 1, 4] }), expected: '16', isHidden: true },
      { input: JSON.stringify({ heights: [1, 2, 1] }), expected: '2', isHidden: true },
    ],
  },
  {
    title: 'Move Zeroes End Two Pointer',
    description: `Move all zeros in the list to the end while preserving the relative order of non-zero elements. Return the result. Use two pointers.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 100\n- -10⁴ ≤ nums[i] ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'two_pointers',
    secondaryConcepts: ['lists'],
    testCases: [
      { input: JSON.stringify({ nums: [0, 1, 0, 3, 12] }), expected: JSON.stringify([1, 3, 12, 0, 0]), isHidden: false },
      { input: JSON.stringify({ nums: [0, 0, 0] }), expected: JSON.stringify([0, 0, 0]), isHidden: false },
      { input: JSON.stringify({ nums: [1, 2, 3] }), expected: JSON.stringify([1, 2, 3]), isHidden: true },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 0, 1] }), expected: JSON.stringify([1, 1, 0]), isHidden: true },
    ],
  },
  {
    title: 'Sorted Squares',
    description: `Given a sorted ascending list that may contain negatives, return a sorted list of their squares in O(n). Use two pointers.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'two_pointers',
    secondaryConcepts: ['sorting'],
    testCases: [
      { input: JSON.stringify({ nums: [-4, -1, 0, 3, 10] }), expected: JSON.stringify([0, 1, 9, 16, 100]), isHidden: false },
      { input: JSON.stringify({ nums: [-7, -3, 2, 3, 11] }), expected: JSON.stringify([4, 9, 9, 49, 121]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: true },
      { input: JSON.stringify({ nums: [1, 2, 3] }), expected: JSON.stringify([1, 4, 9]), isHidden: true },
      { input: JSON.stringify({ nums: [-3, -2, -1] }), expected: JSON.stringify([1, 4, 9]), isHidden: true },
    ],
  },

  // === greedy (5) ===
  {
    title: 'Assign Cookies',
    description: `Given children's greed factors and cookie sizes, assign cookies to maximize satisfied children. A child i is satisfied if a cookie j has size ≥ greed[i]. Return the maximum number satisfied.`,
    
    constraints: `- 0 ≤ len(greed) ≤ 10⁴\n- -10⁵ ≤ greed[i] ≤ 10⁵\n- 0 ≤ len(cookies) ≤ 10⁴\n- -10⁵ ≤ cookies[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'greedy',
    secondaryConcepts: ['sorting'],
    testCases: [
      { input: JSON.stringify({ greed: [1, 2, 3], cookies: [1, 1] }), expected: '1', isHidden: false },
      { input: JSON.stringify({ greed: [1, 2], cookies: [1, 2, 3] }), expected: '2', isHidden: false },
      { input: JSON.stringify({ greed: [], cookies: [1] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ greed: [10], cookies: [1, 2] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ greed: [1, 1, 1], cookies: [2, 2, 2] }), expected: '3', isHidden: true },
    ],
  },
  {
    title: 'Jump Game Reachable',
    description: `Given a list where each element represents the maximum jump length at that position, determine if you can reach the last index starting from index 0. Greedy.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'greedy',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ nums: [2, 3, 1, 1, 4] }), expected: 'true', isHidden: false },
      { input: JSON.stringify({ nums: [3, 2, 1, 0, 4] }), expected: 'false', isHidden: false },
      { input: JSON.stringify({ nums: [0] }), expected: 'true', isHidden: true },
      { input: JSON.stringify({ nums: [1, 0, 1] }), expected: 'false', isHidden: true },
      { input: JSON.stringify({ nums: [5, 0, 0, 0, 0, 0] }), expected: 'true', isHidden: true },
    ],
  },
  {
    title: 'Gas Station Circuit',
    description: `Given \`gas[i]\` and \`cost[i]\` for n gas stations in a circle, return the starting station index from which you can complete the circuit, or -1 if impossible. Greedy.`,
    
    constraints: `- 0 ≤ len(gas) ≤ 10⁵\n- -10⁹ ≤ gas[i] ≤ 10⁹\n- 0 ≤ len(cost) ≤ 10⁵\n- -10⁹ ≤ cost[i] ≤ 10⁹`,
difficulty: Difficulty.HARD,
    primaryConcept: 'greedy',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ gas: [1, 2, 3, 4, 5], cost: [3, 4, 5, 1, 2] }), expected: '3', isHidden: false },
      { input: JSON.stringify({ gas: [2, 3, 4], cost: [3, 4, 3] }), expected: '-1', isHidden: false },
      { input: JSON.stringify({ gas: [5], cost: [4] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ gas: [1, 1, 1], cost: [1, 1, 1] }), expected: '0', isHidden: true },
      { input: JSON.stringify({ gas: [4], cost: [5] }), expected: '-1', isHidden: true },
    ],
  },
  {
    title: 'Activity Scheduling',
    description: `Given a list of activities as \`[start, end]\` pairs, return the maximum number of non-overlapping activities you can attend. Greedy: sort by end time.`,
    
    constraints: `- 0 ≤ len(activities) ≤ 10⁴`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'greedy',
    secondaryConcepts: ['sorting'],
    testCases: [
      { input: JSON.stringify({ activities: [[1, 3], [2, 4], [3, 5], [0, 6]] }), expected: '2', isHidden: false },
      { input: JSON.stringify({ activities: [] }), expected: '0', isHidden: false },
      { input: JSON.stringify({ activities: [[1, 2]] }), expected: '1', isHidden: true },
      { input: JSON.stringify({ activities: [[1, 2], [2, 3], [3, 4]] }), expected: '3', isHidden: true },
      { input: JSON.stringify({ activities: [[1, 10], [2, 3], [4, 5]] }), expected: '2', isHidden: true },
    ],
  },
  {
    title: 'Coin Change Greedy',
    description: `Given denominations \`[25, 10, 5, 1]\` and a target amount, return the minimum number of coins needed using a greedy approach (largest first).`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'greedy',
    secondaryConcepts: [],
    testCases: [
      { input: '63', expected: '6', isHidden: false },
      { input: '0', expected: '0', isHidden: false },
      { input: '1', expected: '1', isHidden: true },
      { input: '100', expected: '4', isHidden: true },
      { input: '50', expected: '2', isHidden: true },
    ],
  },

  // === divide_and_conquer (5) ===
  {
    title: 'Merge Sort',
    description: `Implement merge sort. Return the list sorted in ascending order.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'divide_and_conquer',
    secondaryConcepts: ['sorting', 'recursion'],
    testCases: [
      { input: JSON.stringify({ nums: [5, 2, 8, 1, 9, 3] }), expected: JSON.stringify([1, 2, 3, 5, 8, 9]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ nums: [1] }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ nums: [3, 3, 3] }), expected: JSON.stringify([3, 3, 3]), isHidden: true },
      { input: JSON.stringify({ nums: [9, 7, 5, 3, 1] }), expected: JSON.stringify([1, 3, 5, 7, 9]), isHidden: true },
    ],
  },
  {
    title: 'Quick Sort',
    description: `Implement quicksort. Return the list sorted in ascending order.`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁴\n- -10⁵ ≤ nums[i] ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'divide_and_conquer',
    secondaryConcepts: ['sorting', 'recursion'],
    testCases: [
      { input: JSON.stringify({ nums: [3, 6, 1, 5, 2, 4] }), expected: JSON.stringify([1, 2, 3, 4, 5, 6]), isHidden: false },
      { input: JSON.stringify({ nums: [] }), expected: JSON.stringify([]), isHidden: false },
      { input: JSON.stringify({ nums: [1] }), expected: JSON.stringify([1]), isHidden: true },
      { input: JSON.stringify({ nums: [5, 5, 5] }), expected: JSON.stringify([5, 5, 5]), isHidden: true },
      { input: JSON.stringify({ nums: [4, 3, 2, 1] }), expected: JSON.stringify([1, 2, 3, 4]), isHidden: true },
    ],
  },
  {
    title: 'Max Subarray Sum DNC',
    description: `Implement maximum subarray sum using divide and conquer (Kadane via D&C is also OK).`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁵\n- -10⁹ ≤ nums[i] ≤ 10⁹`,
difficulty: Difficulty.HARD,
    primaryConcept: 'divide_and_conquer',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ nums: [-2, 1, -3, 4, -1, 2, 1, -5, 4] }), expected: '6', isHidden: false },
      { input: JSON.stringify({ nums: [1] }), expected: '1', isHidden: false },
      { input: JSON.stringify({ nums: [-1, -2, -3] }), expected: '-1', isHidden: true },
      { input: JSON.stringify({ nums: [5, 4, -1, 7, 8] }), expected: '23', isHidden: true },
      { input: JSON.stringify({ nums: [0] }), expected: '0', isHidden: true },
    ],
  },
  {
    title: 'Find Kth Smallest',
    description: `Given a list and k (1-indexed), return the kth smallest element using a divide-and-conquer approach (quickselect).`,
    
    constraints: `- 0 ≤ len(nums) ≤ 10⁵\n- -10⁹ ≤ nums[i] ≤ 10⁹\n- -10⁹ ≤ k ≤ 10⁹`,
difficulty: Difficulty.HARD,
    primaryConcept: 'divide_and_conquer',
    secondaryConcepts: ['sorting'],
    testCases: [
      { input: JSON.stringify({ nums: [3, 1, 4, 1, 5, 9, 2, 6], k: 3 }), expected: '2', isHidden: false },
      { input: JSON.stringify({ nums: [1], k: 1 }), expected: '1', isHidden: false },
      { input: JSON.stringify({ nums: [5, 4, 3, 2, 1], k: 5 }), expected: '5', isHidden: true },
      { input: JSON.stringify({ nums: [2, 2, 2], k: 2 }), expected: '2', isHidden: true },
      { input: JSON.stringify({ nums: [10, 20, 30, 40], k: 2 }), expected: '20', isHidden: true },
    ],
  },
  {
    title: 'Fast Power',
    description: `Implement fast exponentiation \`base^exp\` in O(log exp) using divide and conquer. Return the result modulo 1_000_000_007. Assume exp ≥ 0.`,
    
    constraints: `- -10⁵ ≤ base ≤ 10⁵\n- -10⁵ ≤ exp ≤ 10⁵`,
difficulty: Difficulty.MEDIUM,
    primaryConcept: 'divide_and_conquer',
    secondaryConcepts: ['recursion'],
    testCases: [
      { input: JSON.stringify({ base: 2, exp: 10 }), expected: '1024', isHidden: false },
      { input: JSON.stringify({ base: 3, exp: 5 }), expected: '243', isHidden: false },
      { input: JSON.stringify({ base: 5, exp: 0 }), expected: '1', isHidden: true },
      { input: JSON.stringify({ base: 1, exp: 1000 }), expected: '1', isHidden: true },
      { input: JSON.stringify({ base: 10, exp: 3 }), expected: '1000', isHidden: true },
    ],
  },
];
