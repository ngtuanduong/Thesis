/**
 * Problem Bank — barrel export.
 *
 * Each tier file holds a ProblemDef[] that `seed-adaptive.ts` concatenates and seeds.
 * Tiers 1–2 are assigned to course1 (Python Intro), tiers 3–5 to course2 (DSA).
 */
export { TIER1 } from './tier1-basics';
export { TIER2 } from './tier2-core';
export { TIER3 } from './tier3-intermediate';
export { TIER4 } from './tier4-advanced';
export { TIER5 } from './tier5-expert';
export type { ProblemDef, SolutionMap } from './types';
