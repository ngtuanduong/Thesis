/**
 * verify-problem-data.ts — static validation of the problem bank.
 *
 * Runs OFFLINE (no server, no Docker, no DB). Catches data issues before the
 * slow end-to-end verify-problems.ts runs them through the sandbox.
 *
 * Checks for every ProblemDef in TIER1..TIER5:
 *   1. A reference solution exists in ALL_SOLUTIONS keyed by title (this is
 *      the coverage gap verify-problems.ts silently misses).
 *   2. testCases.length >= 1 and at least one visible (isHidden: false) test.
 *   3. Every testCase.input parses as JSON OR is a bare scalar that
 *      code-execution.service's prepareCode() can handle.
 *   4. Every testCase.expected parses as JSON OR is a bare scalar.
 *   5. generateStarterCode() does not throw and returns a non-empty string.
 *   6. Titles are unique across all 170 problems (title is the natural key
 *      used by verify-problems.ts to look up the DB row).
 *
 * Usage:
 *   npx ts-node scripts/verify-problem-data.ts
 *   npm run seed:verify:data
 *
 * Exits 0 if clean, 1 if any violation found.
 */
import { TIER1, TIER2, TIER3, TIER4, TIER5 } from '../prisma/problems';
import type { ProblemDef } from '../prisma/problems/types';
import { ALL_SOLUTIONS } from '../prisma/problems/solutions';
import { generateStarterCode } from '../src/problems/starter-code.util';

interface Violation {
  tier: number;
  title: string;
  rule: string;
  detail: string;
}

const TIERS: { tier: number; problems: ProblemDef[] }[] = [
  { tier: 1, problems: TIER1 },
  { tier: 2, problems: TIER2 },
  { tier: 3, problems: TIER3 },
  { tier: 4, problems: TIER4 },
  { tier: 5, problems: TIER5 },
];

/** A value is "valid test case text" if it's valid JSON or a non-empty bare string. */
function isParseable(raw: string): boolean {
  if (typeof raw !== 'string' || raw.length === 0) return false;
  try {
    JSON.parse(raw);
    return true;
  } catch {
    // code-execution.service.prepareCode falls back to treating non-JSON input
    // as a bare scalar string. Accept any non-empty string.
    return raw.trim().length > 0;
  }
}

function validateProblem(tier: number, p: ProblemDef): Violation[] {
  const out: Violation[] = [];

  // Rule 1: solution coverage
  const sol = ALL_SOLUTIONS[p.title];
  if (!sol || typeof sol !== 'string' || sol.trim().length === 0) {
    out.push({
      tier,
      title: p.title,
      rule: 'missing-solution',
      detail: `No entry in ALL_SOLUTIONS for title "${p.title}"`,
    });
  }

  // Rule 2: test case count + visibility
  if (!Array.isArray(p.testCases) || p.testCases.length === 0) {
    out.push({
      tier,
      title: p.title,
      rule: 'no-test-cases',
      detail: 'testCases array is empty',
    });
    return out; // remaining rules depend on test cases
  }
  const visible = p.testCases.filter((t) => t.isHidden === false);
  if (visible.length === 0) {
    out.push({
      tier,
      title: p.title,
      rule: 'no-visible-test',
      detail: 'all test cases are hidden — student UI will show nothing',
    });
  }

  // Rule 3 + 4: input / expected parseability
  p.testCases.forEach((tc, idx) => {
    if (!isParseable(tc.input)) {
      out.push({
        tier,
        title: p.title,
        rule: 'bad-input',
        detail: `testCases[${idx}].input is empty or non-parseable`,
      });
    }
    if (!isParseable(tc.expected)) {
      out.push({
        tier,
        title: p.title,
        rule: 'bad-expected',
        detail: `testCases[${idx}].expected is empty or non-parseable`,
      });
    }
  });

  // Rule 5: starter code infers without throwing
  try {
    const starter = generateStarterCode(p.testCases);
    if (!starter || starter.trim().length === 0) {
      out.push({
        tier,
        title: p.title,
        rule: 'empty-starter',
        detail: 'generateStarterCode returned empty string',
      });
    }
  } catch (e) {
    out.push({
      tier,
      title: p.title,
      rule: 'starter-throw',
      detail: `generateStarterCode threw: ${(e as Error).message}`,
    });
  }

  return out;
}

function run(): void {
  console.log('🔎 Static validation of problem bank');
  console.log('');

  const violations: Violation[] = [];
  const seenTitles = new Map<string, number>(); // title → tier that first defined it
  const tierSummary: { tier: number; count: number; ok: number }[] = [];

  for (const { tier, problems } of TIERS) {
    let tierOk = 0;
    for (const p of problems) {
      // Rule 6: duplicate title detection (tracked across all tiers)
      if (seenTitles.has(p.title)) {
        violations.push({
          tier,
          title: p.title,
          rule: 'duplicate-title',
          detail: `already defined in tier ${seenTitles.get(p.title)}`,
        });
      } else {
        seenTitles.set(p.title, tier);
      }

      const problemViolations = validateProblem(tier, p);
      if (problemViolations.length === 0) {
        tierOk += 1;
      } else {
        violations.push(...problemViolations);
      }
    }
    tierSummary.push({ tier, count: problems.length, ok: tierOk });
    console.log(
      `   Tier ${tier}: ${tierOk}/${problems.length} ${tierOk === problems.length ? '✅' : '❌'}`,
    );
  }

  const totalProblems = tierSummary.reduce((s, t) => s + t.count, 0);
  const totalOk = tierSummary.reduce((s, t) => s + t.ok, 0);

  console.log('');
  console.log('📊 Summary');
  console.log(`   Problems checked: ${totalProblems}`);
  console.log(`   Passed:           ${totalOk}`);
  console.log(`   Violations:       ${violations.length}`);
  console.log(`   Solutions total:  ${Object.keys(ALL_SOLUTIONS).length}`);

  if (violations.length > 0) {
    console.log('');
    console.log('❌ Violations:');
    // group by rule for readability
    const byRule = new Map<string, Violation[]>();
    for (const v of violations) {
      const bucket = byRule.get(v.rule) ?? [];
      bucket.push(v);
      byRule.set(v.rule, bucket);
    }
    for (const [rule, list] of byRule) {
      console.log(`\n   [${rule}] (${list.length})`);
      for (const v of list) {
        console.log(`      tier${v.tier} • ${v.title} — ${v.detail}`);
      }
    }
    console.log('');
    process.exit(1);
  }

  // Warn if there are orphan solutions (defined but no matching problem).
  const orphanSolutions = Object.keys(ALL_SOLUTIONS).filter(
    (title) => !seenTitles.has(title),
  );
  if (orphanSolutions.length > 0) {
    console.log('');
    console.log(`⚠️  ${orphanSolutions.length} orphan solution(s) without matching problem:`);
    for (const title of orphanSolutions) {
      console.log(`      ${title}`);
    }
  }

  console.log('');
  console.log(`✅ ${totalOk}/${totalProblems} problems valid`);
  process.exit(0);
}

run();
