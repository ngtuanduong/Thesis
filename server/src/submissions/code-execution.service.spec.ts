import { Test, TestingModule } from '@nestjs/testing';
import { CodeExecutionService } from './code-execution.service';

/**
 * We cannot easily mock promisify+exec due to jest.mock hoisting.
 * Instead, we mock the entire service's private methods via prototype spying.
 * Or we test the service's public API by mocking at the exec level.
 *
 * Strategy: mock child_process.exec to use a callback-based mock,
 * mock fs/promises for file operations.
 */

// We define the mock fn INSIDE the jest.mock factory so it's available at hoist-time
jest.mock('child_process', () => {
  const fn = jest.fn();
  return {
    exec: fn,
    __mockExec: fn, // Expose for test access
  };
});

jest.mock('util', () => {
  const actual = jest.requireActual('util');
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  const cp = require('child_process');
  const asyncFn = jest.fn();
  cp.__mockExecAsync = asyncFn;
  return {
    ...actual,
    promisify: () => asyncFn,
  };
});

jest.mock('fs/promises', () => {
  const fns = {
    writeFile: jest.fn().mockResolvedValue(undefined),
    unlink: jest.fn().mockResolvedValue(undefined),
    mkdir: jest.fn().mockResolvedValue(undefined),
  };
  return {
    ...fns,
    __mocks: fns,
  };
});

describe('CodeExecutionService', () => {
  let service: CodeExecutionService;
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  let mockExecAsync: jest.Mock;
  let fsMocks: { writeFile: jest.Mock; unlink: jest.Mock; mkdir: jest.Mock };

  beforeEach(async () => {
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const cp = require('child_process');
    mockExecAsync = cp.__mockExecAsync;

    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const fs = require('fs/promises');
    fsMocks = fs.__mocks;

    jest.clearAllMocks();
    // Restore default mock implementations after clear
    fsMocks.writeFile.mockResolvedValue(undefined);
    fsMocks.unlink.mockResolvedValue(undefined);
    fsMocks.mkdir.mockResolvedValue(undefined);

    const module: TestingModule = await Test.createTestingModule({
      providers: [CodeExecutionService],
    }).compile();

    service = module.get<CodeExecutionService>(CodeExecutionService);
  });

  /** Mock ensureSandboxImage to succeed (docker info + image exists) */
  function mockSandboxReady() {
    mockExecAsync.mockResolvedValueOnce({ stdout: '', stderr: '' });
    mockExecAsync.mockResolvedValueOnce({ stdout: 'abc123', stderr: '' });
  }

  describe('ensureSandboxImage', () => {
    it('should throw descriptive error when Docker is not available', async () => {
      mockExecAsync.mockRejectedValueOnce(
        new Error('Cannot connect to the Docker daemon'),
      );

      await expect(service.ensureSandboxImage()).rejects.toThrow(
        'Docker is not available',
      );
    });

    it('should throw on Docker API version mismatch', async () => {
      mockExecAsync.mockRejectedValueOnce(
        new Error('API version negotiation: client is too old'),
      );

      await expect(service.ensureSandboxImage()).rejects.toThrow(
        'Docker API version mismatch',
      );
    });

    it('should build sandbox image when it does not exist', async () => {
      mockExecAsync.mockResolvedValueOnce({ stdout: '', stderr: '' });
      mockExecAsync.mockResolvedValueOnce({ stdout: '', stderr: '' });
      mockExecAsync.mockResolvedValueOnce({ stdout: 'built', stderr: '' });

      await expect(service.ensureSandboxImage()).resolves.not.toThrow();
      expect(mockExecAsync).toHaveBeenCalledTimes(3);
      expect(mockExecAsync).toHaveBeenLastCalledWith(
        expect.stringContaining('docker build'),
        expect.anything(),
      );
    });

    it('should skip build when sandbox image already exists', async () => {
      mockExecAsync.mockResolvedValueOnce({ stdout: '', stderr: '' });
      mockExecAsync.mockResolvedValueOnce({ stdout: 'abc123\n', stderr: '' });

      await expect(service.ensureSandboxImage()).resolves.not.toThrow();
      expect(mockExecAsync).toHaveBeenCalledTimes(2);
    });
  });

  describe('executeCode', () => {
    it('should return RUNTIME_ERROR for unsupported language', async () => {
      mockSandboxReady();

      const result = await service.executeCode('code', 'javascript', [
        { input: '1', expected: '1' },
      ]);

      expect(result.status).toBe('RUNTIME_ERROR');
      expect(result.error).toContain('Only Python');
    });

    it('should return ACCEPTED when all test cases pass', async () => {
      mockSandboxReady();
      mockExecAsync.mockResolvedValueOnce({ stdout: '[0, 1]\n', stderr: '' });
      mockExecAsync.mockResolvedValueOnce({ stdout: '[1, 2]\n', stderr: '' });

      const result = await service.executeCode(
        'def solution(nums, target): pass',
        'python',
        [
          { input: '{"nums":[2,7], "target":9}', expected: '[0, 1]' },
          { input: '{"nums":[3,2,4], "target":6}', expected: '[1, 2]' },
        ],
      );

      expect(result.status).toBe('ACCEPTED');
      expect(result.output).toBe('All test cases passed');
      expect(result.runtime).toBeDefined();
    });

    it('should return WRONG_ANSWER on first failing test case', async () => {
      mockSandboxReady();
      mockExecAsync.mockResolvedValueOnce({ stdout: '[0, 1]\n', stderr: '' });
      mockExecAsync.mockResolvedValueOnce({ stdout: '[0, 0]\n', stderr: '' });

      const result = await service.executeCode('def solution(): pass', 'python', [
        { input: '1', expected: '[0, 1]' },
        { input: '2', expected: '[1, 2]' },
      ]);

      expect(result.status).toBe('WRONG_ANSWER');
      expect(result.output).toContain('Expected');
      expect(result.output).toContain('Got');
    });

    it('should return TIME_LIMIT when docker times out', async () => {
      mockSandboxReady();
      const timeoutError = new Error('Process killed');
      (timeoutError as any).killed = true;
      mockExecAsync.mockRejectedValueOnce(timeoutError);

      const result = await service.executeCode('while True: pass', 'python', [
        { input: '1', expected: '1' },
      ]);

      expect(result.status).toBe('TIME_LIMIT');
      expect(result.error).toContain('Time limit exceeded');
    });

    it('should return RUNTIME_ERROR on stderr output', async () => {
      mockSandboxReady();
      mockExecAsync.mockResolvedValueOnce({
        stdout: '',
        stderr: 'NameError: name x is not defined',
      });

      const result = await service.executeCode('print(x)', 'python', [
        { input: '1', expected: '1' },
      ]);

      expect(result.status).toBe('RUNTIME_ERROR');
      expect(result.error).toContain('NameError');
    });

    it('should return RUNTIME_ERROR when Docker exec throws with stderr', async () => {
      mockSandboxReady();
      const execError = new Error('Command failed');
      (execError as any).stderr = 'SyntaxError: invalid syntax';
      mockExecAsync.mockRejectedValueOnce(execError);

      const result = await service.executeCode('def :', 'python', [
        { input: '1', expected: '1' },
      ]);

      expect(result.status).toBe('RUNTIME_ERROR');
      expect(result.error).toContain('SyntaxError');
    });

    it('should stop at first failing test and not run remaining', async () => {
      mockSandboxReady();
      const error = new Error('Command failed');
      (error as any).stderr = 'Error';
      (error as any).killed = false;
      mockExecAsync.mockRejectedValueOnce(error);

      const result = await service.executeCode('bad code', 'python', [
        { input: '1', expected: '1' },
        { input: '2', expected: '2' },
        { input: '3', expected: '3' },
      ]);

      expect(result.status).toBe('RUNTIME_ERROR');
      // 2 sandbox calls + 1 test execution = 3 total
      expect(mockExecAsync).toHaveBeenCalledTimes(3);
    });
  });

  describe('compareOutputs (via executeCode)', () => {
    it('should match JSON-parsed values for structured equality', async () => {
      mockSandboxReady();
      mockExecAsync.mockResolvedValueOnce({ stdout: '[0,1]\n', stderr: '' });

      const result = await service.executeCode('code', 'python', [
        { input: '1', expected: '[0, 1]' },
      ]);

      expect(result.status).toBe('ACCEPTED');
    });

    it('should fallback to string comparison for non-JSON', async () => {
      mockSandboxReady();
      mockExecAsync.mockResolvedValueOnce({ stdout: 'hello world\n', stderr: '' });

      const result = await service.executeCode('code', 'python', [
        { input: '"test"', expected: 'hello world' },
      ]);

      expect(result.status).toBe('ACCEPTED');
    });
  });

  describe('cleanup', () => {
    it('should attempt to cleanup temp files even on success', async () => {
      mockSandboxReady();
      mockExecAsync.mockResolvedValueOnce({ stdout: '1\n', stderr: '' });

      await service.executeCode('code', 'python', [
        { input: '1', expected: '1' },
      ]);

      expect(fsMocks.mkdir).toHaveBeenCalled();
      expect(fsMocks.writeFile).toHaveBeenCalled();
      expect(fsMocks.unlink).toHaveBeenCalled();
    });
  });
});
