export const DEFAULT_STARTER_CODE = `def solution():
    # Write your code here
    pass
`;

/**
 * Infer a Python type hint string from a JavaScript value.
 */
function inferPythonType(val: unknown): string {
  if (Array.isArray(val)) {
    if (val.length > 0 && Array.isArray(val[0])) return 'List[List]';
    return 'List';
  }
  if (typeof val === 'number') return Number.isInteger(val) ? 'int' : 'float';
  if (typeof val === 'string') return 'str';
  if (typeof val === 'boolean') return 'bool';
  return 'Any';
}

/**
 * Auto-generate a Python starter code template from the first test case's input structure.
 *
 * - Dict input  `{"nums":[...], "target":9}` → `def solution(nums, target):`
 * - List input  `[1,2,3]`                     → `def solution(*data):` (prepareCode uses *input)
 * - Scalar int  `121`                          → `def solution(x):`
 * - Scalar str  `"hello"`                      → `def solution(s):`
 */
export function generateStarterCode(
  testCases: { input: string }[],
): string {
  if (!testCases || testCases.length === 0) {
    return DEFAULT_STARTER_CODE;
  }

  const raw = testCases[0].input;
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    // Raw string that isn't valid JSON → single string param
    return `def solution(s):\n    # @param s: str\n    # Write your code here\n    pass\n`;
  }

  // Dict input → named params (prepareCode uses **input)
  if (parsed !== null && typeof parsed === 'object' && !Array.isArray(parsed)) {
    const keys = Object.keys(parsed as Record<string, unknown>);
    const obj = parsed as Record<string, unknown>;
    const paramComments = keys
      .map((k) => `    # @param ${k}: ${inferPythonType(obj[k])}`)
      .join('\n');
    return `def solution(${keys.join(', ')}):\n${paramComments}\n    # Write your code here\n    pass\n`;
  }

  // List input → *args (prepareCode uses *input which unpacks elements as positional args)
  if (Array.isArray(parsed)) {
    const isNested = parsed.length > 0 && Array.isArray(parsed[0]);
    const paramName = isNested ? 'items' : 'data';
    const elemType = parsed.length > 0 ? inferPythonType(parsed[0]) : 'Any';
    return (
      `def solution(*${paramName}):\n` +
      `    # ${paramName} contains unpacked list elements (${elemType} each)\n` +
      `    # Tip: use list(${paramName}) to convert back to a list\n` +
      `    # Write your code here\n` +
      `    pass\n`
    );
  }

  // Scalar
  const paramName = typeof parsed === 'number' ? 'n' : 's';
  const pyType = inferPythonType(parsed);
  return `def solution(${paramName}):\n    # @param ${paramName}: ${pyType}\n    # Write your code here\n    pass\n`;
}
