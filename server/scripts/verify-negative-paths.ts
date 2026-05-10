/**
 * verify-negative-paths.ts — negative-path smoke tests for the submission pipeline.
 *
 * verify-problems.ts only covers the happy path (reference solution → ACCEPTED).
 * This script asserts the pipeline correctly classifies the three failure modes
 * from CodeExecutionService:
 *
 *   - WRONG_ANSWER   (output doesn't match expected)
 *   - TIME_LIMIT     (SIGTERM after 5s timeout)
 *   - RUNTIME_ERROR  (Python traceback / syntax error)
 *
 * If a future refactor breaks the classification logic in
 * code-execution.service.ts (e.g. starts reporting TIME_LIMIT as RUNTIME_ERROR),
 * this test catches it.
 *
 * Usage:
 *   npx ts-node scripts/verify-negative-paths.ts
 *   npm run seed:verify:negative
 *
 * Requirements:
 *   - NestJS server running (default http://localhost:4000)
 *   - Sandbox Docker image available
 *   - DB seeded (needs at least one tier-1 problem + student1@example.com)
 */
import { PrismaClient, SubmissionStatus } from '@prisma/client';

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3000/api';
const STUDENT_EMAIL = process.env.STUDENT_EMAIL || 'student1@example.com';
const STUDENT_PASSWORD = process.env.STUDENT_PASSWORD || 'password123';
const POLL_INTERVAL_MS = 500;
const POLL_TIMEOUT_MS = 120_000;

const prisma = new PrismaClient();

interface Case {
  name: string;
  code: string;
  expected: SubmissionStatus;
}

const CASES: Case[] = [
  {
    name: 'WRONG_ANSWER (returns wrong value)',
    code: `def solution(*args, **kwargs):
    return -999999`,
    expected: SubmissionStatus.WRONG_ANSWER,
  },
  {
    name: 'TIME_LIMIT (infinite loop)',
    code: `def solution(*args, **kwargs):
    while True:
        pass`,
    expected: SubmissionStatus.TIME_LIMIT,
  },
  {
    name: 'RUNTIME_ERROR (syntax error)',
    code: `def solution(
    this is not valid python`,
    expected: SubmissionStatus.RUNTIME_ERROR,
  },
];

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

async function pollStatus(
  token: string,
  submissionId: string,
): Promise<{ status: string; output?: string | null }> {
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

/**
 * Pick a stable tier-1 problem to run the negative cases against. We query
 * the DB to avoid hard-coding a title that might get renamed — just grab any
 * EASY problem with test cases.
 */
async function pickTargetProblem(): Promise<{ id: string; title: string }> {
  const problem = await prisma.problem.findFirst({
    where: { difficulty: 'EASY' },
    orderBy: { title: 'asc' },
    include: { testCases: { take: 1 } },
  });
  if (!problem) {
    throw new Error('No EASY problem found in DB — is the seed applied?');
  }
  if (problem.testCases.length === 0) {
    throw new Error(`Problem "${problem.title}" has no test cases`);
  }
  return { id: problem.id, title: problem.title };
}

async function run() {
  console.log('🔎 Negative-path smoke tests');
  console.log(`   API: ${API_BASE_URL}`);
  console.log(`   User: ${STUDENT_EMAIL}`);
  console.log('');

  let token: string;
  try {
    token = await login();
  } catch (e) {
    console.error(`❌ ${(e as Error).message}`);
    console.error('   Make sure the NestJS server is running: npm run start:dev');
    await prisma.$disconnect();
    process.exit(1);
  }

  const target = await pickTargetProblem();
  console.log(`   Target problem: "${target.title}" (${target.id})`);
  console.log('');

  const results: { name: string; expected: string; actual: string; ok: boolean }[] = [];

  for (const c of CASES) {
    process.stdout.write(`  ${c.name.padEnd(45)} ... `);
    try {
      const submissionId = await submit(token, target.id, c.code);
      const result = await pollStatus(token, submissionId);
      const ok = result.status === c.expected;
      results.push({ name: c.name, expected: c.expected, actual: result.status, ok });
      process.stdout.write(`${ok ? '✅' : `❌ got ${result.status}`}\n`);
    } catch (e) {
      results.push({
        name: c.name,
        expected: c.expected,
        actual: `ERROR: ${(e as Error).message}`,
        ok: false,
      });
      process.stdout.write(`❌ ${(e as Error).message}\n`);
    }
  }

  const okCount = results.filter((r) => r.ok).length;
  console.log('');
  console.log('📊 Summary');
  console.log(`   Passed: ${okCount}/${results.length}`);
  if (okCount !== results.length) {
    console.log('');
    for (const r of results.filter((r) => !r.ok)) {
      console.log(`   ❌ ${r.name}`);
      console.log(`      expected: ${r.expected}`);
      console.log(`      actual:   ${r.actual}`);
    }
  }

  await prisma.$disconnect();
  process.exit(okCount === results.length ? 0 : 1);
}

run().catch(async (e) => {
  console.error('Fatal:', e);
  await prisma.$disconnect();
  process.exit(1);
});
