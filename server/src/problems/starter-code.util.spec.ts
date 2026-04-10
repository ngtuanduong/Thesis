import { generateStarterCode, DEFAULT_STARTER_CODE } from './starter-code.util';

describe('generateStarterCode', () => {
  it('should return DEFAULT_STARTER_CODE when no test cases provided', () => {
    expect(generateStarterCode([])).toBe(DEFAULT_STARTER_CODE);
  });

  it('should return DEFAULT_STARTER_CODE when testCases is null/undefined', () => {
    expect(generateStarterCode(null as any)).toBe(DEFAULT_STARTER_CODE);
    expect(generateStarterCode(undefined as any)).toBe(DEFAULT_STARTER_CODE);
  });

  describe('dict input', () => {
    it('should generate named params for dict input {"nums":[1,2], "target":3}', () => {
      const result = generateStarterCode([
        { input: '{"nums":[1,2], "target":3}' },
      ]);
      expect(result).toContain('def solution(nums, target):');
      expect(result).toContain('# @param nums: List');
      expect(result).toContain('# @param target: int');
      expect(result).toContain('pass');
    });

    it('should generate params for dict with string values', () => {
      const result = generateStarterCode([
        { input: '{"s":"hello","k":2}' },
      ]);
      expect(result).toContain('def solution(s, k):');
      expect(result).toContain('# @param s: str');
      expect(result).toContain('# @param k: int');
    });

    it('should generate params for single key dict', () => {
      const result = generateStarterCode([
        { input: '{"nums":[1,2,3]}' },
      ]);
      expect(result).toContain('def solution(nums):');
      expect(result).toContain('# @param nums: List');
    });
  });

  describe('list input', () => {
    it('should generate *data for flat list input [1,2,3]', () => {
      const result = generateStarterCode([{ input: '[1,2,3]' }]);
      expect(result).toContain('def solution(*data):');
      expect(result).toContain('data contains unpacked list elements (int each)');
      expect(result).toContain('list(data)');
    });

    it('should generate *items for nested list input [[1,2],[3,4]]', () => {
      const result = generateStarterCode([{ input: '[[1,2],[3,4]]' }]);
      expect(result).toContain('def solution(*items):');
      expect(result).toContain('List');
    });

    it('should handle empty list', () => {
      const result = generateStarterCode([{ input: '[]' }]);
      expect(result).toContain('def solution(*data):');
      expect(result).toContain('Any each');
    });

    it('should handle list of strings', () => {
      const result = generateStarterCode([{ input: '["a","b","c"]' }]);
      expect(result).toContain('def solution(*data):');
      expect(result).toContain('str each');
    });
  });

  describe('scalar input', () => {
    it('should generate single param for scalar int input', () => {
      const result = generateStarterCode([{ input: '121' }]);
      expect(result).toContain('def solution(n):');
      expect(result).toContain('# @param n: int');
    });

    it('should generate single param for scalar float input', () => {
      const result = generateStarterCode([{ input: '3.14' }]);
      expect(result).toContain('def solution(n):');
      expect(result).toContain('# @param n: float');
    });

    it('should generate single param for scalar string input', () => {
      const result = generateStarterCode([{ input: '"hello"' }]);
      expect(result).toContain('def solution(s):');
      expect(result).toContain('# @param s: str');
    });

    it('should generate single param for boolean input', () => {
      const result = generateStarterCode([{ input: 'true' }]);
      expect(result).toContain('def solution(s):');
      expect(result).toContain('# @param s: bool');
    });
  });

  describe('non-JSON input', () => {
    it('should generate string param for non-JSON input', () => {
      const result = generateStarterCode([{ input: 'hello world' }]);
      expect(result).toContain('def solution(s):');
      expect(result).toContain('# @param s: str');
    });
  });

  it('should use only the first test case for inference', () => {
    const result = generateStarterCode([
      { input: '{"x":1}' },
      { input: '[1,2,3]' },
    ]);
    expect(result).toContain('def solution(x):');
  });
});
