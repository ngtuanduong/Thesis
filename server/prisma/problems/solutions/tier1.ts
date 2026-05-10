import { SolutionMap } from '../types';

/**
 * Python reference solutions for Tier 1 problems.
 * Each solution is submitted by verify-problems.ts against the seeded problem
 * and must result in status=ACCEPTED (all test cases pass).
 */
export const TIER1_SOLUTIONS: SolutionMap = {
  // variables
  'Sum of Two Numbers': `def solution(a, b):
    return a + b`,

  'Average of Three Numbers': `def solution(a, b, c):
    return round((a + b + c) / 3, 2)`,

  'Rectangle Area': `def solution(width, height):
    return width * height`,

  'Circle Circumference': `def solution(radius):
    pi = 3.14159
    return round(2 * pi * radius, 2)`,

  // data_types
  'Integer to String': `def solution(n):
    return str(n)`,

  'String to Integer': `def solution(s):
    return int(s)`,

  'Boolean to Integer': `def solution(b):
    return int(b)`,

  'Round to Integer': `def solution(x):
    return round(x)`,

  // operators
  'Square a Number': `def solution(n):
    return n * n`,

  'Cube a Number': `def solution(n):
    return n ** 3`,

  'Absolute Value': `def solution(n):
    return n if n >= 0 else -n`,

  'Modulo Remainder': `def solution(a, b):
    return a % b`,

  'Integer Division': `def solution(a, b):
    return a // b`,

  'Power Calculation': `def solution(base, exp):
    return base ** exp`,

  // io / formatting
  'Full Name Formatter': `def solution(first, last):
    return f"{first} {last}"`,

  'Format Price Tag': `def solution(amount):
    return f"\${amount:.2f}"`,

  // strings
  'Count Vowels': `def solution(s):
    return sum(1 for c in s.lower() if c in 'aeiou')`,

  'Count Consonants': `def solution(s):
    return sum(1 for c in s.lower() if c.isalpha() and c not in 'aeiou')`,

  'To Uppercase': `def solution(s):
    return s.upper()`,

  'To Lowercase': `def solution(s):
    return s.lower()`,

  'String Length': `def solution(s):
    return len(s)`,

  'Repeat String N Times': `def solution(s, n):
    return s * n`,

  'First Character': `def solution(s):
    return s[0] if s else ""`,

  'Last Character': `def solution(s):
    return s[-1] if s else ""`,

  'Contains Substring': `def solution(s, sub):
    return sub in s`,

  'Replace All Occurrences': `def solution(s, old, new_):
    return s.replace(old, new_)`,

  // conditionals
  'Maximum of Two': `def solution(a, b):
    return a if a >= b else b`,

  'Minimum of Two': `def solution(a, b):
    return a if a <= b else b`,

  'Maximum of Three': `def solution(a, b, c):
    m = a
    if b > m:
        m = b
    if c > m:
        m = c
    return m`,

  'Is Positive': `def solution(n):
    return n > 0`,

  'Is Even Number': `def solution(n):
    return n % 2 == 0`,

  'Leap Year Check': `def solution(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0`,

  'Sign of Number': `def solution(n):
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0`,

  // loops
  'Sum from 1 to N': `def solution(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total`,

  'Iterative Factorial': `def solution(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result`,

  'Count Digits': `def solution(n):
    if n == 0:
        return 1
    count = 0
    while n > 0:
        count += 1
        n //= 10
    return count`,

  'Sum of Digits': `def solution(n):
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total`,

  'Reverse Integer Digits': `def solution(n):
    result = 0
    while n > 0:
        result = result * 10 + n % 10
        n //= 10
    return result`,

  'Power via Loop': `def solution(base, exp):
    result = 1
    for _ in range(exp):
        result *= base
    return result`,

  'Greatest Common Divisor': `def solution(a, b):
    while b:
        a, b = b, a % b
    return a`,
};
