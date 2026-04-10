import { SolutionMap } from '../types';
import { TIER1_SOLUTIONS } from './tier1';
import { TIER2_SOLUTIONS } from './tier2';
import { TIER3_SOLUTIONS } from './tier3';
import { TIER4_SOLUTIONS } from './tier4';
import { TIER5_SOLUTIONS } from './tier5';

export { TIER1_SOLUTIONS, TIER2_SOLUTIONS, TIER3_SOLUTIONS, TIER4_SOLUTIONS, TIER5_SOLUTIONS };

export const ALL_SOLUTIONS: SolutionMap = {
  ...TIER1_SOLUTIONS,
  ...TIER2_SOLUTIONS,
  ...TIER3_SOLUTIONS,
  ...TIER4_SOLUTIONS,
  ...TIER5_SOLUTIONS,
};

export const SOLUTIONS_BY_TIER: Record<number, SolutionMap> = {
  1: TIER1_SOLUTIONS,
  2: TIER2_SOLUTIONS,
  3: TIER3_SOLUTIONS,
  4: TIER4_SOLUTIONS,
  5: TIER5_SOLUTIONS,
};
