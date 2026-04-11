/**
 * embed-all.ts — triggers batch embedding for all seeded problems
 * via the ai-service `/embed/batch` endpoint. Use this when the
 * embedding step inside seed-adaptive.ts was skipped (ai-service
 * was down at seed time) and you want to backfill embeddings.
 *
 * Usage:
 *   npx ts-node scripts/embed-all.ts
 *
 * Env overrides:
 *   AI_SERVICE_URL — default http://localhost:8000
 */
import { PrismaClient } from '@prisma/client';

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000';
const prisma = new PrismaClient();

async function run() {
  console.log(`🧠 Batch embedding against ${AI_SERVICE_URL}`);
  const problems = await prisma.problem.findMany({
    select: { id: true, title: true, description: true, tags: true },
  });
  console.log(`   Found ${problems.length} problems`);

  if (problems.length === 0) {
    console.log('   Nothing to embed.');
    await prisma.$disconnect();
    return;
  }

  // AI service /embed/batch expects { problems: [{ problem_id, title, description, tags }] }
  const payload = {
    problems: problems.map((p) => ({
      problem_id: p.id,
      title: p.title,
      description: p.description,
      tags: p.tags,
    })),
  };

  try {
    const res = await fetch(`${AI_SERVICE_URL}/embed/batch`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Service-Key': process.env.AI_SERVICE_KEY || 'dev-secret-key',
      },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`ai-service returned HTTP ${res.status}: ${text.slice(0, 200)}`);
    }
    console.log(`   ✅ Embedded ${problems.length} problems`);
  } catch (e) {
    console.error(`   ❌ ${(e as Error).message}`);
    console.error('   Is ai-service running? Start it and retry.');
    process.exit(1);
  } finally {
    await prisma.$disconnect();
  }
}

run();
