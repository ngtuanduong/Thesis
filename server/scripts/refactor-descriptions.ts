/**
 * refactor-descriptions.ts — One-time script to restructure problem descriptions.
 *
 * For all 170 problems across tier1-5 files:
 *   1. Strip the **Example:** block from `description` (examples come from testCases)
 *   2. Auto-generate a `constraints` field based on test case input types + difficulty
 *   3. Rewrite each tier file in-place
 *
 * Usage:
 *   npx ts-node scripts/refactor-descriptions.ts
 *   npx ts-node scripts/refactor-descriptions.ts --dry-run
 */
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

const isDryRun = process.argv.includes('--dry-run');

const TIER_FILES = [
  join(__dirname, '../prisma/problems/tier1-basics.ts'),
  join(__dirname, '../prisma/problems/tier2-core.ts'),
  join(__dirname, '../prisma/problems/tier3-intermediate.ts'),
  join(__dirname, '../prisma/problems/tier4-advanced.ts'),
  join(__dirname, '../prisma/problems/tier5-expert.ts'),
];

// ─── Constraint generation from test case input patterns ────────────────

function inferConstraints(
  firstInput: string,
  difficulty: string,
): string {
  const ranges: Record<string, { int: string; str: string; arr: string }> = {
    EASY: { int: '10⁴', str: '100', arr: '100' },
    MEDIUM: { int: '10⁵', str: '10⁴', arr: '10⁴' },
    HARD: { int: '10⁹', str: '10⁵', arr: '10⁵' },
  };
  const r = ranges[difficulty] || ranges.MEDIUM;

  let parsed: unknown;
  try {
    // firstInput in file looks like: JSON.stringify({ a: 3, b: 5 })
    // At runtime it's already the JSON string '{"a":3,"b":5}'
    // But we're working on file text, so we need to handle the raw pattern
    parsed = JSON.parse(firstInput);
  } catch {
    return `- Input is a valid string`;
  }

  const lines: string[] = [];

  if (parsed !== null && typeof parsed === 'object' && !Array.isArray(parsed)) {
    for (const [key, val] of Object.entries(parsed as Record<string, unknown>)) {
      if (typeof val === 'boolean') {
        lines.push(`- ${key} ∈ {true, false}`);
      } else if (typeof val === 'number') {
        lines.push(`- -${r.int} ≤ ${key} ≤ ${r.int}`);
      } else if (typeof val === 'string') {
        lines.push(`- 0 ≤ len(${key}) ≤ ${r.str}`);
      } else if (Array.isArray(val)) {
        lines.push(`- 0 ≤ len(${key}) ≤ ${r.arr}`);
        if (val.length > 0 && typeof val[0] === 'number') {
          lines.push(`- -${r.int} ≤ ${key}[i] ≤ ${r.int}`);
        }
      }
    }
  } else if (Array.isArray(parsed)) {
    lines.push(`- 0 ≤ len(data) ≤ ${r.arr}`);
    if (parsed.length > 0 && typeof parsed[0] === 'number') {
      lines.push(`- -${r.int} ≤ data[i] ≤ ${r.int}`);
    }
  } else if (typeof parsed === 'number') {
    lines.push(`- -${r.int} ≤ n ≤ ${r.int}`);
  } else if (typeof parsed === 'string') {
    lines.push(`- 0 ≤ len(s) ≤ ${r.str}`);
  }

  return lines.join('\\n');
}

// ─── File processing ────────────────────────────────────────────────────

function processFile(filePath: string): { modified: number; total: number } {
  let content = readFileSync(filePath, 'utf-8');
  let modified = 0;

  // Count problems (number of `title:` occurrences)
  const titleMatches = content.match(/title:\s*'/g);
  const total = titleMatches ? titleMatches.length : 0;

  // 1. Strip **Example:** blocks from descriptions.
  //    Pattern in file: \n\n**Example... up to closing backtick of template literal
  //    The description ends with `, so we strip from **Example to just before `
  //
  //    Regex: finds `**Example` followed by anything up to the closing backtick-comma
  const exampleBlockRegex = /(\n\n\*\*Example(?:s)?(?:\s*\(.*?\))?:\*\*[\s\S]*?)(`[,]?\s*\n\s*(?:constraints|difficulty):)/g;

  // Simpler approach: find each description block and strip example section
  // Description blocks: description: `...content...`,
  // Match template literals that may contain escaped backticks (\`)
  // [^`\\] matches any char except backtick and backslash
  // \\. matches backslash + any char (handles \`, \\, \n etc.)
  const descBlockRegex = /(description:\s*`)((?:[^`\\]|\\.)*)(`)/g;

  const strippedContent = content.replace(descBlockRegex, (match, prefix, desc, suffix) => {
    const exampleIdx = desc.indexOf('**Example');
    if (exampleIdx < 0) return match;

    const cleanDesc = desc.slice(0, exampleIdx).trimEnd();
    modified++;
    return prefix + cleanDesc + suffix;
  });

  content = strippedContent;

  // 2. Add constraints field where missing.
  //    Find each problem object: after description: `...`, insert constraints before difficulty:
  //    But we need the test case data to generate constraints. Extract from file.
  //
  //    Strategy: find each { title: ... difficulty: ... testCases: [...] } block
  //    and extract the first testCase input to infer param types.

  if (!content.includes('constraints:')) {
    // Extract each problem's first test case input and difficulty to generate constraints
    // Pattern: title → difficulty → testCases → first input
    const problemPattern = /(\s*)(difficulty:\s*Difficulty\.(EASY|MEDIUM|HARD),\n)([\s\S]*?)(testCases:\s*\[[\s\S]*?\{ input:\s*)(JSON\.stringify\(([^)]+)\)|'([^']+)'|"([^"]+)")/g;

    let match;
    const insertions: { pos: number; indent: string; constraints: string }[] = [];

    while ((match = problemPattern.exec(content)) !== null) {
      const indent = match[1];
      const difficulty = match[3];

      // Get the raw first input value
      const jsonStringifyContent = match[7]; // from JSON.stringify(...)
      const singleQuoteContent = match[8]; // from '...'
      const doubleQuoteContent = match[9]; // from "..."

      let firstInput: string;
      if (jsonStringifyContent) {
        // Evaluate JSON.stringify({...}) → need to parse the object literal
        // This is JS object notation, not JSON. Use a safe eval approach.
        try {
          // eslint-disable-next-line no-eval
          firstInput = JSON.stringify(eval(`(${jsonStringifyContent})`));
        } catch {
          firstInput = '{}';
        }
      } else {
        firstInput = singleQuoteContent || doubleQuoteContent || '{}';
      }

      const constraints = inferConstraints(firstInput, difficulty);
      if (constraints) {
        // Insert constraints: `...`, right before difficulty:
        const difficultyPos = content.indexOf(match[2], match.index);
        if (difficultyPos >= 0) {
          insertions.push({
            pos: difficultyPos,
            indent,
            constraints,
          });
        }
      }
    }

    // Apply insertions in reverse order to preserve positions
    for (const ins of insertions.reverse()) {
      const constraintLine = `${ins.indent}constraints: \`${ins.constraints}\`,\n`;
      content = content.slice(0, ins.pos) + constraintLine + content.slice(ins.pos);
    }
  }

  if (!isDryRun) {
    writeFileSync(filePath, content, 'utf-8');
  }

  return { modified, total };
}

// ─── Main ───────────────────────────────────────────────────────────────

function run() {
  console.log(`🔧 Refactoring problem descriptions${isDryRun ? ' (DRY RUN)' : ''}`);
  console.log('');

  let totalModified = 0;
  let totalProblems = 0;

  for (const filePath of TIER_FILES) {
    const { modified, total } = processFile(filePath);
    totalModified += modified;
    totalProblems += total;
    const fileName = filePath.split(/[/\\]/).pop();
    console.log(`  ${fileName}: ${modified}/${total} descriptions stripped`);
  }

  console.log('');
  console.log(`📊 Total: ${totalModified}/${totalProblems} modified`);
  if (isDryRun) console.log('   (dry run — no files written)');
}

run();
