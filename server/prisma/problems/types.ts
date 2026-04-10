import { Difficulty } from '@prisma/client';

/**
 * Shared definition for all problem bank entries across tiers.
 *
 * Test case format rules (enforced by code-execution.service.ts):
 * - `input`:
 *    - For fn with named params: JSON.stringify({key1: val1, key2: val2})
 *      → starter code becomes `def solution(key1, key2):`, wrapper calls `solution(**input)`
 *    - For fn with single scalar: bare string like '42' or '"hello"'
 *      → starter code becomes `def solution(n):`, wrapper calls `solution(input)`
 *    - For fn with list unpacking: JSON.stringify([1,2,3])
 *      → starter code becomes `def solution(*data):`, wrapper calls `solution(*input)`
 * - `expected`: JSON-stringified result. Strings must be JSON-quoted: '"result"'.
 *   Comparison is JSON deep-equal with string fallback; both sides are trimmed.
 */
export interface ProblemDef {
  title: string;
  description: string;
  constraints?: string;
  difficulty: Difficulty;
  tags: string[];
  primaryConcept: string;
  secondaryConcepts: string[];
  testCases: { input: string; expected: string; isHidden: boolean }[];
}

/**
 * Python reference solution map: problem title → full Python source.
 * Used by verify-problems.ts to submit a known-correct solution and assert ACCEPTED.
 */
export type SolutionMap = Record<string, string>;
