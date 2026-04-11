import { Difficulty } from '@prisma/client';
import { ProblemDef } from './types';

/**
 * Tier 1 — Basics (40 problems)
 * Concepts: variables, data_types, operators, io, strings, conditionals, loops
 *
 * All problems are EASY and build fundamental Python fluency.
 * Titles are distinct from legacy NEW_PROBLEMS in seed-adaptive.ts.
 */
export const TIER1: ProblemDef[] = [
  // === variables (4) ===
  {
    title: 'Sum of Two Numbers',
    description: `Write a function \`solution(a, b)\` that returns the sum of two integers.`,
    
    constraints: `- -10⁴ ≤ a ≤ 10⁴\n- -10⁴ ≤ b ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'variables',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ a: 3, b: 5 }), expected: '8', isHidden: false },
      { input: JSON.stringify({ a: 0, b: 0 }), expected: '0', isHidden: false },
      { input: JSON.stringify({ a: -5, b: 5 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ a: 100, b: 200 }), expected: '300', isHidden: true },
      { input: JSON.stringify({ a: -10, b: -20 }), expected: '-30', isHidden: true },
    ],
  },
  {
    title: 'Average of Three Numbers',
    description: `Write a function \`solution(a, b, c)\` that returns the arithmetic mean of three numbers as a float rounded to 2 decimal places.`,
    
    constraints: `- -10⁴ ≤ a ≤ 10⁴\n- -10⁴ ≤ b ≤ 10⁴\n- -10⁴ ≤ c ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'variables',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ a: 1, b: 2, c: 3 }), expected: '2.0', isHidden: false },
      { input: JSON.stringify({ a: 10, b: 20, c: 30 }), expected: '20.0', isHidden: false },
      { input: JSON.stringify({ a: 0, b: 0, c: 0 }), expected: '0.0', isHidden: true },
      { input: JSON.stringify({ a: 5, b: 5, c: 10 }), expected: '6.67', isHidden: true },
      { input: JSON.stringify({ a: -3, b: 0, c: 3 }), expected: '0.0', isHidden: true },
    ],
  },
  {
    title: 'Rectangle Area',
    description: `Write a function \`solution(width, height)\` that returns the area of a rectangle.`,
    
    constraints: `- -10⁴ ≤ width ≤ 10⁴\n- -10⁴ ≤ height ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'variables',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ width: 4, height: 5 }), expected: '20', isHidden: false },
      { input: JSON.stringify({ width: 1, height: 1 }), expected: '1', isHidden: false },
      { input: JSON.stringify({ width: 0, height: 10 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ width: 7, height: 3 }), expected: '21', isHidden: true },
      { input: JSON.stringify({ width: 100, height: 50 }), expected: '5000', isHidden: true },
    ],
  },
  {
    title: 'Circle Circumference',
    description: `Write a function \`solution(radius)\` that returns the circumference of a circle, rounded to 2 decimal places. Use \`pi = 3.14159\`.

**Formula:** \`C = 2 * pi * r\``,
    
    constraints: `- -10⁴ ≤ radius ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'variables',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ radius: 1 }), expected: '6.28', isHidden: false },
      { input: JSON.stringify({ radius: 0 }), expected: '0.0', isHidden: false },
      { input: JSON.stringify({ radius: 5 }), expected: '31.42', isHidden: true },
      { input: JSON.stringify({ radius: 10 }), expected: '62.83', isHidden: true },
      { input: JSON.stringify({ radius: 2 }), expected: '12.57', isHidden: true },
    ],
  },

  // === data_types (4) ===
  {
    title: 'Integer to String',
    description: `Write a function \`solution(n)\` that converts an integer to its string representation.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'data_types',
    secondaryConcepts: [],
    testCases: [
      { input: '42', expected: '"42"', isHidden: false },
      { input: '0', expected: '"0"', isHidden: false },
      { input: '-7', expected: '"-7"', isHidden: true },
      { input: '1000', expected: '"1000"', isHidden: true },
      { input: '-100', expected: '"-100"', isHidden: true },
    ],
  },
  {
    title: 'String to Integer',
    description: `Write a function \`solution(s)\` that parses an integer from a string. You may assume the string is a valid integer representation.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'data_types',
    secondaryConcepts: [],
    testCases: [
      { input: '"123"', expected: '123', isHidden: false },
      { input: '"0"', expected: '0', isHidden: false },
      { input: '"-45"', expected: '-45', isHidden: true },
      { input: '"9999"', expected: '9999', isHidden: true },
      { input: '"-1"', expected: '-1', isHidden: true },
    ],
  },
  {
    title: 'Boolean to Integer',
    description: `Write a function \`solution(b)\` that converts a boolean to an integer: \`True\` → 1, \`False\` → 0.`,
    difficulty: Difficulty.EASY,
    primaryConcept: 'data_types',
    secondaryConcepts: [],
    testCases: [
      { input: 'true', expected: '1', isHidden: false },
      { input: 'false', expected: '0', isHidden: false },
      { input: 'true', expected: '1', isHidden: true },
      { input: 'false', expected: '0', isHidden: true },
      { input: 'true', expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Round to Integer',
    description: `Write a function \`solution(x)\` that rounds a float to the nearest integer using Python's \`round()\` built-in.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'data_types',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: '3.7', expected: '4', isHidden: false },
      { input: '3.2', expected: '3', isHidden: false },
      { input: '-2.5', expected: '-2', isHidden: true },
      { input: '0.0', expected: '0', isHidden: true },
      { input: '9.99', expected: '10', isHidden: true },
    ],
  },

  // === operators (6) ===
  {
    title: 'Square a Number',
    description: `Write a function \`solution(n)\` that returns the square of an integer.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'operators',
    secondaryConcepts: [],
    testCases: [
      { input: '5', expected: '25', isHidden: false },
      { input: '0', expected: '0', isHidden: false },
      { input: '-4', expected: '16', isHidden: true },
      { input: '10', expected: '100', isHidden: true },
      { input: '-1', expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Cube a Number',
    description: `Write a function \`solution(n)\` that returns the cube of an integer.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'operators',
    secondaryConcepts: [],
    testCases: [
      { input: '3', expected: '27', isHidden: false },
      { input: '0', expected: '0', isHidden: false },
      { input: '-2', expected: '-8', isHidden: true },
      { input: '5', expected: '125', isHidden: true },
      { input: '1', expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Absolute Value',
    description: `Write a function \`solution(n)\` that returns the absolute value of an integer without using Python's \`abs()\` builtin.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'operators',
    secondaryConcepts: ['conditionals'],
    testCases: [
      { input: '-7', expected: '7', isHidden: false },
      { input: '7', expected: '7', isHidden: false },
      { input: '0', expected: '0', isHidden: true },
      { input: '-100', expected: '100', isHidden: true },
      { input: '42', expected: '42', isHidden: true },
    ],
  },
  {
    title: 'Modulo Remainder',
    description: `Write a function \`solution(a, b)\` that returns \`a % b\` (the remainder when a is divided by b). Assume b is non-zero.`,
    
    constraints: `- -10⁴ ≤ a ≤ 10⁴\n- -10⁴ ≤ b ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'operators',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ a: 10, b: 3 }), expected: '1', isHidden: false },
      { input: JSON.stringify({ a: 20, b: 5 }), expected: '0', isHidden: false },
      { input: JSON.stringify({ a: 7, b: 2 }), expected: '1', isHidden: true },
      { input: JSON.stringify({ a: 100, b: 30 }), expected: '10', isHidden: true },
      { input: JSON.stringify({ a: 1, b: 4 }), expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Integer Division',
    description: `Write a function \`solution(a, b)\` that returns the integer quotient \`a // b\`. Assume b is non-zero.`,
    
    constraints: `- -10⁴ ≤ a ≤ 10⁴\n- -10⁴ ≤ b ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'operators',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ a: 17, b: 5 }), expected: '3', isHidden: false },
      { input: JSON.stringify({ a: 100, b: 10 }), expected: '10', isHidden: false },
      { input: JSON.stringify({ a: 7, b: 2 }), expected: '3', isHidden: true },
      { input: JSON.stringify({ a: 0, b: 5 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ a: 50, b: 7 }), expected: '7', isHidden: true },
    ],
  },
  {
    title: 'Power Calculation',
    description: `Write a function \`solution(base, exp)\` that returns \`base\` raised to the power of \`exp\` using the \`**\` operator. Assume exp is a non-negative integer.`,
    
    constraints: `- -10⁴ ≤ base ≤ 10⁴\n- -10⁴ ≤ exp ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'operators',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ base: 2, exp: 5 }), expected: '32', isHidden: false },
      { input: JSON.stringify({ base: 3, exp: 3 }), expected: '27', isHidden: false },
      { input: JSON.stringify({ base: 10, exp: 0 }), expected: '1', isHidden: true },
      { input: JSON.stringify({ base: 5, exp: 2 }), expected: '25', isHidden: true },
      { input: JSON.stringify({ base: 1, exp: 100 }), expected: '1', isHidden: true },
    ],
  },

  // === io / formatting (2) ===
  {
    title: 'Full Name Formatter',
    description: `Write a function \`solution(first, last)\` that returns a formatted full name string: \`"first last"\`.`,
    
    constraints: `- 0 ≤ len(first) ≤ 100\n- 0 ≤ len(last) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'io',
    secondaryConcepts: ['strings'],
    testCases: [
      { input: JSON.stringify({ first: 'John', last: 'Doe' }), expected: '"John Doe"', isHidden: false },
      { input: JSON.stringify({ first: 'Alice', last: 'Smith' }), expected: '"Alice Smith"', isHidden: false },
      { input: JSON.stringify({ first: 'A', last: 'B' }), expected: '"A B"', isHidden: true },
      { input: JSON.stringify({ first: 'Nguyen', last: 'Duong' }), expected: '"Nguyen Duong"', isHidden: true },
      { input: JSON.stringify({ first: 'Mary', last: 'Jane' }), expected: '"Mary Jane"', isHidden: true },
    ],
  },
  {
    title: 'Format Price Tag',
    description: `Write a function \`solution(amount)\` that formats a numeric amount as a price tag string with a dollar sign and 2 decimal places.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'io',
    secondaryConcepts: ['strings'],
    testCases: [
      { input: '12.5', expected: '"$12.50"', isHidden: false },
      { input: '100', expected: '"$100.00"', isHidden: false },
      { input: '0', expected: '"$0.00"', isHidden: true },
      { input: '3.1415', expected: '"$3.14"', isHidden: true },
      { input: '99.99', expected: '"$99.99"', isHidden: true },
    ],
  },

  // === strings (10) ===
  {
    title: 'Count Vowels',
    description: `Write a function \`solution(s)\` that returns the number of vowels (a, e, i, o, u) in a string. Case-insensitive.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'strings',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: '"Hello"', expected: '2', isHidden: false },
      { input: '"Python"', expected: '1', isHidden: false },
      { input: '""', expected: '0', isHidden: true },
      { input: '"AEIOU"', expected: '5', isHidden: true },
      { input: '"xyz"', expected: '0', isHidden: true },
    ],
  },
  {
    title: 'Count Consonants',
    description: `Write a function \`solution(s)\` that returns the number of consonant letters (alphabetic, non-vowel) in a string. Ignore non-letter characters. Case-insensitive.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'strings',
    secondaryConcepts: ['loops'],
    testCases: [
      { input: '"Hello World"', expected: '7', isHidden: false },
      { input: '"aeiou"', expected: '0', isHidden: false },
      { input: '""', expected: '0', isHidden: true },
      { input: '"Python"', expected: '5', isHidden: true },
      { input: '"abc"', expected: '2', isHidden: true },
    ],
  },
  {
    title: 'To Uppercase',
    description: `Write a function \`solution(s)\` that returns the uppercase version of a string.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'strings',
    secondaryConcepts: [],
    testCases: [
      { input: '"hello"', expected: '"HELLO"', isHidden: false },
      { input: '"Python"', expected: '"PYTHON"', isHidden: false },
      { input: '""', expected: '""', isHidden: true },
      { input: '"Already UPPER"', expected: '"ALREADY UPPER"', isHidden: true },
      { input: '"123 abc"', expected: '"123 ABC"', isHidden: true },
    ],
  },
  {
    title: 'To Lowercase',
    description: `Write a function \`solution(s)\` that returns the lowercase version of a string.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'strings',
    secondaryConcepts: [],
    testCases: [
      { input: '"HELLO"', expected: '"hello"', isHidden: false },
      { input: '"Python"', expected: '"python"', isHidden: false },
      { input: '""', expected: '""', isHidden: true },
      { input: '"MixED Case"', expected: '"mixed case"', isHidden: true },
      { input: '"ABC 123"', expected: '"abc 123"', isHidden: true },
    ],
  },
  {
    title: 'String Length',
    description: `Write a function \`solution(s)\` that returns the length of a string.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'strings',
    secondaryConcepts: [],
    testCases: [
      { input: '"hello"', expected: '5', isHidden: false },
      { input: '""', expected: '0', isHidden: false },
      { input: '"a"', expected: '1', isHidden: true },
      { input: '"hello world"', expected: '11', isHidden: true },
      { input: '"12345"', expected: '5', isHidden: true },
    ],
  },
  {
    title: 'Repeat String N Times',
    description: `Write a function \`solution(s, n)\` that returns the string \`s\` repeated \`n\` times.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100\n- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'strings',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ s: 'ab', n: 3 }), expected: '"ababab"', isHidden: false },
      { input: JSON.stringify({ s: 'x', n: 5 }), expected: '"xxxxx"', isHidden: false },
      { input: JSON.stringify({ s: 'hi', n: 0 }), expected: '""', isHidden: true },
      { input: JSON.stringify({ s: '', n: 10 }), expected: '""', isHidden: true },
      { input: JSON.stringify({ s: 'abc', n: 2 }), expected: '"abcabc"', isHidden: true },
    ],
  },
  {
    title: 'First Character',
    description: `Write a function \`solution(s)\` that returns the first character of a non-empty string. If the string is empty, return an empty string.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'strings',
    secondaryConcepts: ['conditionals'],
    testCases: [
      { input: '"hello"', expected: '"h"', isHidden: false },
      { input: '"a"', expected: '"a"', isHidden: false },
      { input: '""', expected: '""', isHidden: true },
      { input: '"Python"', expected: '"P"', isHidden: true },
      { input: '"123"', expected: '"1"', isHidden: true },
    ],
  },
  {
    title: 'Last Character',
    description: `Write a function \`solution(s)\` that returns the last character of a non-empty string. If the string is empty, return an empty string.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'strings',
    secondaryConcepts: ['conditionals'],
    testCases: [
      { input: '"hello"', expected: '"o"', isHidden: false },
      { input: '"a"', expected: '"a"', isHidden: false },
      { input: '""', expected: '""', isHidden: true },
      { input: '"Python"', expected: '"n"', isHidden: true },
      { input: '"xyz"', expected: '"z"', isHidden: true },
    ],
  },
  {
    title: 'Contains Substring',
    description: `Write a function \`solution(s, sub)\` that returns \`True\` if \`sub\` is a substring of \`s\`, otherwise \`False\`.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100\n- 0 ≤ len(sub) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'strings',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ s: 'hello world', sub: 'world' }), expected: 'true', isHidden: false },
      { input: JSON.stringify({ s: 'python', sub: 'java' }), expected: 'false', isHidden: false },
      { input: JSON.stringify({ s: 'abc', sub: '' }), expected: 'true', isHidden: true },
      { input: JSON.stringify({ s: '', sub: 'x' }), expected: 'false', isHidden: true },
      { input: JSON.stringify({ s: 'banana', sub: 'nan' }), expected: 'true', isHidden: true },
    ],
  },
  {
    title: 'Replace All Occurrences',
    description: `Write a function \`solution(s, old, new_)\` that returns \`s\` with every occurrence of \`old\` replaced by \`new_\`. Use Python's \`str.replace\` method.`,
    
    constraints: `- 0 ≤ len(s) ≤ 100\n- 0 ≤ len(old) ≤ 100\n- 0 ≤ len(new_) ≤ 100`,
difficulty: Difficulty.EASY,
    primaryConcept: 'strings',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ s: 'banana', old: 'a', new_: 'o' }), expected: '"bonono"', isHidden: false },
      { input: JSON.stringify({ s: 'hello', old: 'l', new_: 'L' }), expected: '"heLLo"', isHidden: false },
      { input: JSON.stringify({ s: 'abc', old: 'x', new_: 'y' }), expected: '"abc"', isHidden: true },
      { input: JSON.stringify({ s: '', old: 'a', new_: 'b' }), expected: '""', isHidden: true },
      { input: JSON.stringify({ s: 'aaa', old: 'a', new_: '' }), expected: '""', isHidden: true },
    ],
  },

  // === conditionals (7) ===
  {
    title: 'Maximum of Two',
    description: `Write a function \`solution(a, b)\` that returns the larger of two numbers without using \`max()\`.`,
    
    constraints: `- -10⁴ ≤ a ≤ 10⁴\n- -10⁴ ≤ b ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'conditionals',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ a: 3, b: 7 }), expected: '7', isHidden: false },
      { input: JSON.stringify({ a: 10, b: 5 }), expected: '10', isHidden: false },
      { input: JSON.stringify({ a: -2, b: -5 }), expected: '-2', isHidden: true },
      { input: JSON.stringify({ a: 0, b: 0 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ a: 100, b: 100 }), expected: '100', isHidden: true },
    ],
  },
  {
    title: 'Minimum of Two',
    description: `Write a function \`solution(a, b)\` that returns the smaller of two numbers without using \`min()\`.`,
    
    constraints: `- -10⁴ ≤ a ≤ 10⁴\n- -10⁴ ≤ b ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'conditionals',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ a: 3, b: 7 }), expected: '3', isHidden: false },
      { input: JSON.stringify({ a: 10, b: 5 }), expected: '5', isHidden: false },
      { input: JSON.stringify({ a: -2, b: -5 }), expected: '-5', isHidden: true },
      { input: JSON.stringify({ a: 0, b: 0 }), expected: '0', isHidden: true },
      { input: JSON.stringify({ a: 42, b: 42 }), expected: '42', isHidden: true },
    ],
  },
  {
    title: 'Maximum of Three',
    description: `Write a function \`solution(a, b, c)\` that returns the largest of three integers.`,
    
    constraints: `- -10⁴ ≤ a ≤ 10⁴\n- -10⁴ ≤ b ≤ 10⁴\n- -10⁴ ≤ c ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'conditionals',
    secondaryConcepts: [],
    testCases: [
      { input: JSON.stringify({ a: 3, b: 7, c: 5 }), expected: '7', isHidden: false },
      { input: JSON.stringify({ a: 10, b: 10, c: 10 }), expected: '10', isHidden: false },
      { input: JSON.stringify({ a: -1, b: -5, c: -3 }), expected: '-1', isHidden: true },
      { input: JSON.stringify({ a: 100, b: 50, c: 75 }), expected: '100', isHidden: true },
      { input: JSON.stringify({ a: 0, b: 0, c: 1 }), expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Is Positive',
    description: `Write a function \`solution(n)\` that returns \`True\` if n is strictly positive, otherwise \`False\`.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'conditionals',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: '5', expected: 'true', isHidden: false },
      { input: '-3', expected: 'false', isHidden: false },
      { input: '0', expected: 'false', isHidden: true },
      { input: '100', expected: 'true', isHidden: true },
      { input: '-1', expected: 'false', isHidden: true },
    ],
  },
  {
    title: 'Is Even Number',
    description: `Write a function \`solution(n)\` that returns \`True\` if n is even, otherwise \`False\`.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'conditionals',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: '4', expected: 'true', isHidden: false },
      { input: '7', expected: 'false', isHidden: false },
      { input: '0', expected: 'true', isHidden: true },
      { input: '-6', expected: 'true', isHidden: true },
      { input: '1', expected: 'false', isHidden: true },
    ],
  },
  {
    title: 'Leap Year Check',
    description: `Write a function \`solution(year)\` that returns \`True\` if the year is a leap year, otherwise \`False\`.

A leap year is divisible by 4, EXCEPT if it is divisible by 100 but not by 400.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'conditionals',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: '2020', expected: 'true', isHidden: false },
      { input: '1900', expected: 'false', isHidden: false },
      { input: '2000', expected: 'true', isHidden: true },
      { input: '2023', expected: 'false', isHidden: true },
      { input: '2024', expected: 'true', isHidden: true },
    ],
  },
  {
    title: 'Sign of Number',
    description: `Write a function \`solution(n)\` that returns \`1\` if n is positive, \`-1\` if negative, and \`0\` if zero.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'conditionals',
    secondaryConcepts: [],
    testCases: [
      { input: '5', expected: '1', isHidden: false },
      { input: '-3', expected: '-1', isHidden: false },
      { input: '0', expected: '0', isHidden: true },
      { input: '100', expected: '1', isHidden: true },
      { input: '-100', expected: '-1', isHidden: true },
    ],
  },

  // === loops (7) ===
  {
    title: 'Sum from 1 to N',
    description: `Write a function \`solution(n)\` that returns the sum of integers from 1 to n (inclusive) using a loop. If n < 1, return 0.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'loops',
    secondaryConcepts: [],
    testCases: [
      { input: '5', expected: '15', isHidden: false },
      { input: '1', expected: '1', isHidden: false },
      { input: '0', expected: '0', isHidden: true },
      { input: '10', expected: '55', isHidden: true },
      { input: '100', expected: '5050', isHidden: true },
    ],
  },
  {
    title: 'Iterative Factorial',
    description: `Write a function \`solution(n)\` that computes \`n!\` (n factorial) using a loop. Assume n ≥ 0 and \`0! = 1\`.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'loops',
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
    title: 'Count Digits',
    description: `Write a function \`solution(n)\` that returns the number of digits in a non-negative integer. For n = 0, return 1.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'loops',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: '12345', expected: '5', isHidden: false },
      { input: '7', expected: '1', isHidden: false },
      { input: '0', expected: '1', isHidden: true },
      { input: '1000', expected: '4', isHidden: true },
      { input: '99999999', expected: '8', isHidden: true },
    ],
  },
  {
    title: 'Sum of Digits',
    description: `Write a function \`solution(n)\` that returns the sum of digits of a non-negative integer.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'loops',
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
    title: 'Reverse Integer Digits',
    description: `Write a function \`solution(n)\` that reverses the digits of a non-negative integer and returns the result as an integer. Leading zeros in the reversed result are dropped.`,
    
    constraints: `- -10⁴ ≤ n ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'loops',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: '1230', expected: '321', isHidden: false },
      { input: '12345', expected: '54321', isHidden: false },
      { input: '0', expected: '0', isHidden: true },
      { input: '7', expected: '7', isHidden: true },
      { input: '100', expected: '1', isHidden: true },
    ],
  },
  {
    title: 'Power via Loop',
    description: `Write a function \`solution(base, exp)\` that computes \`base ** exp\` using a loop (not the \`**\` operator or \`pow()\`). Assume exp ≥ 0.`,
    
    constraints: `- -10⁴ ≤ base ≤ 10⁴\n- -10⁴ ≤ exp ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'loops',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ base: 2, exp: 10 }), expected: '1024', isHidden: false },
      { input: JSON.stringify({ base: 3, exp: 4 }), expected: '81', isHidden: false },
      { input: JSON.stringify({ base: 5, exp: 0 }), expected: '1', isHidden: true },
      { input: JSON.stringify({ base: 7, exp: 1 }), expected: '7', isHidden: true },
      { input: JSON.stringify({ base: 10, exp: 3 }), expected: '1000', isHidden: true },
    ],
  },
  {
    title: 'Greatest Common Divisor',
    description: `Write a function \`solution(a, b)\` that returns the greatest common divisor of two positive integers using the Euclidean algorithm (loop-based).`,
    
    constraints: `- -10⁴ ≤ a ≤ 10⁴\n- -10⁴ ≤ b ≤ 10⁴`,
difficulty: Difficulty.EASY,
    primaryConcept: 'loops',
    secondaryConcepts: ['operators'],
    testCases: [
      { input: JSON.stringify({ a: 12, b: 18 }), expected: '6', isHidden: false },
      { input: JSON.stringify({ a: 7, b: 5 }), expected: '1', isHidden: false },
      { input: JSON.stringify({ a: 100, b: 25 }), expected: '25', isHidden: true },
      { input: JSON.stringify({ a: 1, b: 1 }), expected: '1', isHidden: true },
      { input: JSON.stringify({ a: 48, b: 36 }), expected: '12', isHidden: true },
    ],
  },
];
