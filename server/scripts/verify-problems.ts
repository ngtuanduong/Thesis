/**
 * verify-problems.ts — submits reference Python solutions through the live
 * server + sandbox pipeline and asserts every seeded tier problem reaches
 * status ACCEPTED.
 *
 * Usage:
 *   npx ts-node scripts/verify-problems.ts                # all tiers
 *   npx ts-node scripts/verify-problems.ts --tier 1       # single tier
 *   npx ts-node scripts/verify-problems.ts --tier all     # same as default
 *   npx ts-node scripts/verify-problems.ts --skip-passed  # resume: skip titles
 *                                                         #   already ACCEPTED
 *                                                         #   in DB for student1
 *
 * Resume: use --skip-passed to continue after an interrupted run. The script
 * queries the submissions table for ACCEPTED entries and skips those titles,
 * so only problems that haven't been verified yet actually run.
 *
 * Requirements:
 *   - NestJS server running (default http://localhost:4000)
 *   - sandbox Docker image available for submissions
 *   - seed already applied (prisma migrate reset --force)
 *
 * Env overrides:
 *   API_BASE_URL   — default http://localhost:4000
 *   STUDENT_EMAIL  — default student1@example.com
 *   STUDENT_PASSWORD — default password123
 */
import { PrismaClient } from '@prisma/client';
import { SOLUTIONS_BY_TIER, ALL_SOLUTIONS } from '../prisma/problems/solutions';
import type { SolutionMap } from '../prisma/problems/types';

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3000/api';
const STUDENT_EMAIL = process.env.STUDENT_EMAIL || 'student1@example.com';
const STUDENT_PASSWORD = process.env.STUDENT_PASSWORD || 'password123';
const POLL_INTERVAL_MS = 500;
// Windows Docker CLI calls are slow (~1-2s per call). A submission with 5
// test cases runs 5 `docker run` invocations + starter checks, which on cold
// cache can take 30-60s total. Bump to 120s to accommodate.
const POLL_TIMEOUT_MS = 120_000;

const prisma = new PrismaClient();

interface Result {
  title: string;
  status: string;
  ok: boolean;
  details?: string;
}

function parseArgs(): { tier: number | 'all'; skipPassed: boolean } {
  const args = process.argv.slice(2);
  const skipPassed = args.includes('--skip-passed');
  const idx = args.indexOf('--tier');
  if (idx === -1) return { tier: 'all', skipPassed };
  const raw = args[idx + 1];
  if (raw === 'all' || raw === undefined) return { tier: 'all', skipPassed };
  const n = Number(raw);
  if (!Number.isInteger(n) || n < 1 || n > 5) {
    throw new Error(`--tier must be 1..5 or "all", got ${raw}`);
  }
  return { tier: n, skipPassed };
}

/**
 * Resume support: query all problem titles for which student1 already has an
 * ACCEPTED submission. Returns a Set for O(1) skip-check.
 */
async function loadPassedTitles(): Promise<Set<string>> {
  const rows = await prisma.submission.findMany({
    where: {
      status: 'ACCEPTED',
      user: { email: STUDENT_EMAIL },
    },
    select: { problem: { select: { title: true } } },
    distinct: ['problemId'],
  });
  return new Set(rows.map((r) => r.problem.title));
}

async function login(): Promise<string> {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: STUDENT_EMAIL, password: STUDENT_PASSWORD }),
  });
  if (!res.ok) {
    throw new Error(`Login failed: HTTP ${res.status} — is the server up at ${API_BASE_URL}?`);
  }
  const body = (await res.json()) as { token?: string; access_token?: string };
  const token = body.token || body.access_token;
  if (!token) {
    throw new Error(`Login response missing token: ${JSON.stringify(body)}`);
  }
  return token;
}

async function submit(token: string, problemId: string, code: string): Promise<string> {
  const res = await fetch(`${API_BASE_URL}/submissions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ problemId, language: 'python', code }),
  });
  if (!res.ok) {
    throw new Error(`Submit failed: HTTP ${res.status}`);
  }
  const body = (await res.json()) as { id: string };
  return body.id;
}

async function pollStatus(token: string, submissionId: string): Promise<{ status: string; output?: string | null }> {
  const start = Date.now();
  while (Date.now() - start < POLL_TIMEOUT_MS) {
    const res = await fetch(`${API_BASE_URL}/submissions/${submissionId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      const body = (await res.json()) as { status: string; output?: string | null };
      if (body.status !== 'PENDING' && body.status !== 'RUNNING') {
        return body;
      }
    }
    await new Promise((r) => setTimeout(r, POLL_INTERVAL_MS));
  }
  return { status: 'TIMEOUT' };
}

async function verifyProblem(
  token: string,
  title: string,
  code: string,
): Promise<Result> {
  const problem = await prisma.problem.findFirst({ where: { title } });
  if (!problem) {
    return { title, status: 'NOT_FOUND', ok: false, details: 'Problem not seeded' };
  }
  try {
    const submissionId = await submit(token, problem.id, code);
    const result = await pollStatus(token, submissionId);
    const ok = result.status === 'ACCEPTED';
    return {
      title,
      status: result.status,
      ok,
      details: ok ? undefined : (result.output ?? undefined) || undefined,
    };
  } catch (e) {
    return { title, status: 'ERROR', ok: false, details: (e as Error).message };
  }
}

async function run() {
  const { tier, skipPassed } = parseArgs();
  console.log(`🔎 Verifying tier: ${tier}${skipPassed ? ' (skip-passed)' : ''}`);
  console.log(`   API: ${API_BASE_URL}`);
  console.log(`   User: ${STUDENT_EMAIL}`);

  let token: string;
  try {
    token = await login();
  } catch (e) {
    console.error(`❌ ${(e as Error).message}`);
    console.error('   Make sure the NestJS server is running: npm run start:dev');
    process.exit(1);
  }

  // Resume support: pre-load titles already marked ACCEPTED in DB.
  const passedTitles = skipPassed ? await loadPassedTitles() : new Set<string>();
  if (skipPassed) {
    console.log(`   Resume: ${passedTitles.size} problems already ACCEPTED, will skip\n`);
  }

  const solutionSets: { tier: number; solutions: SolutionMap }[] =
    tier === 'all'
      ? Object.entries(SOLUTIONS_BY_TIER).map(([k, v]) => ({ tier: Number(k), solutions: v }))
      : [{ tier, solutions: SOLUTIONS_BY_TIER[tier] }];

  const allResults: { tier: number; results: Result[]; skipped: number }[] = [];

  for (const { tier: t, solutions } of solutionSets) {
    console.log(`\n── Tier ${t} (${Object.keys(solutions).length} problems) ──`);
    const results: Result[] = [];
    let skipped = 0;
    for (const [title, code] of Object.entries(solutions)) {
      if (skipPassed && passedTitles.has(title)) {
        skipped += 1;
        results.push({ title, status: 'SKIPPED', ok: true });
        continue;
      }
      process.stdout.write(`  ${title.padEnd(40)} ... `);
      const r = await verifyProblem(token, title, code);
      results.push(r);
      process.stdout.write(`${r.ok ? '✅' : '❌ ' + r.status}\n`);
    }
    if (skipped > 0) {
      console.log(`  (skipped ${skipped} already-passed)`);
    }
    allResults.push({ tier: t, results, skipped });
  }

  // Summary
  console.log('\n📊 Summary');
  let totalOk = 0;
  let totalCount = 0;
  let totalSkipped = 0;
  for (const { tier: t, results, skipped } of allResults) {
    const ok = results.filter((r) => r.ok).length;
    totalOk += ok;
    totalCount += results.length;
    totalSkipped += skipped;
    const skipNote = skipped > 0 ? ` (${skipped} skipped)` : '';
    console.log(`   Tier ${t}: ${ok}/${results.length}${skipNote} ${ok === results.length ? '✅' : '❌'}`);
    const failed = results.filter((r) => !r.ok);
    if (failed.length > 0) {
      for (const f of failed) {
        console.log(`      ❌ ${f.title}: ${f.status}${f.details ? ` — ${f.details.slice(0, 120)}` : ''}`);
      }
    }
  }
  const skipNote = totalSkipped > 0 ? ` (${totalSkipped} skipped)` : '';
  console.log(`\n   TOTAL: ${totalOk}/${totalCount}${skipNote}`);
  await prisma.$disconnect();
  process.exit(totalOk === totalCount ? 0 : 1);
}

run().catch(async (e) => {
  console.error('Fatal:', e);
  await prisma.$disconnect();
  process.exit(1);
});
