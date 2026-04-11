import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000';
const AI_SERVICE_KEY = process.env.AI_SERVICE_KEY || 'dev-secret-key';

async function generateEmbeddings() {
  console.log('🤖 Generating problem embeddings...\n');

  // Get all problems
  const problems = await prisma.problem.findMany({
    select: {
      id: true,
      title: true,
      description: true,
      tags: true,
    },
  });

  console.log(`Found ${problems.length} problems\n`);

  for (const problem of problems) {
    try {
      console.log(`📝 Processing: ${problem.title}`);

      const response = await fetch(`${AI_SERVICE_URL}/embed/problem`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Service-Key': AI_SERVICE_KEY,
        },
        body: JSON.stringify({
          problem_id: problem.id,
          title: problem.title,
          description: problem.description,
          tags: problem.tags,
        }),
      });

      if (!response.ok) {
        const text = await response.text();
        console.error(`   ❌ Error: ${response.status} - ${text}`);
        continue;
      }

      const data = await response.json();
      console.log(`   ✅ Generated embedding (${data.embedding.length} dimensions)`);
    } catch (error: any) {
      console.error(`   ❌ Error: ${error.message}`);
    }
  }

  console.log('\n✨ Embedding generation complete!');
  await prisma.$disconnect();
}

generateEmbeddings().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
