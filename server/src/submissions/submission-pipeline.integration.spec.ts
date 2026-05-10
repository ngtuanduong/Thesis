import { Test, TestingModule } from '@nestjs/testing';
import { ConfigService } from '@nestjs/config';
import { SubmissionsService } from './submissions.service';
import { PrismaService } from '../prisma/prisma.service';
import { CodeExecutionService } from './code-execution.service';
import { AdaptiveService } from '../adaptive/adaptive.service';
import { SubmissionStatus } from '@prisma/client';

/**
 * Integration test: verifies the full submission pipeline orchestration.
 * Uses real SubmissionsService with mocked dependencies.
 */
describe('Submission Pipeline Integration', () => {
  let service: SubmissionsService;
  let prisma: Record<string, any>;
  let codeExecService: Record<string, any>;
  let adaptiveService: Record<string, any>;

  const mockSubmission = {
    id: 'sub-1',
    userId: 'user-1',
    problemId: 'problem-1',
    code: 'def solution(n): return n + 1',
    language: 'python',
    status: 'PENDING',
    output: null,
    runtime: null,
    memory: null,
    createdAt: new Date(),
    updatedAt: new Date(),
  };

  const mockTestCases = [
    { input: '1', expected: '2' },
    { input: '5', expected: '6' },
  ];

  beforeEach(async () => {
    prisma = {
      submission: {
        create: jest.fn().mockResolvedValue(mockSubmission),
        update: jest.fn().mockImplementation((args) => ({
          ...mockSubmission,
          ...args.data,
        })),
        count: jest.fn().mockResolvedValue(1),
        findUnique: jest.fn(),
        findMany: jest.fn(),
      },
      testCase: {
        findMany: jest.fn().mockResolvedValue(mockTestCases),
      },
    };

    codeExecService = {
      executeCode: jest.fn(),
    };

    adaptiveService = {
      updateAfterSubmission: jest.fn().mockResolvedValue({}),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        SubmissionsService,
        { provide: PrismaService, useValue: prisma },
        { provide: CodeExecutionService, useValue: codeExecService },
        { provide: ConfigService, useValue: { get: jest.fn().mockReturnValue('http://localhost:8000') } },
        { provide: AdaptiveService, useValue: adaptiveService },
      ],
    }).compile();

    service = module.get<SubmissionsService>(SubmissionsService);
  });

  const wait = (ms = 100) => new Promise((r) => setTimeout(r, ms));

  describe('ACCEPTED pipeline', () => {
    it('should: create PENDING → RUNNING → ACCEPTED → update adaptive layers', async () => {
      codeExecService.executeCode.mockResolvedValue({
        status: SubmissionStatus.ACCEPTED,
        output: 'All test cases passed',
        runtime: 150,
      });

      // Mock fetch for updateUserSkills
      jest.spyOn(global, 'fetch').mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ skills: [] }),
        text: () => Promise.resolve(''),
      } as any);

      const result = await service.create(
        { problemId: 'problem-1', code: 'def solution(n): return n+1', language: 'python' },
        'user-1',
      );

      expect(result.status).toBe('PENDING');
      await wait();

      // Verify status transitions
      expect(prisma.submission.update).toHaveBeenCalledWith(
        expect.objectContaining({
          data: expect.objectContaining({ status: SubmissionStatus.RUNNING }),
        }),
      );
      expect(prisma.submission.update).toHaveBeenCalledWith(
        expect.objectContaining({
          data: expect.objectContaining({ status: SubmissionStatus.ACCEPTED }),
        }),
      );

      // Verify adaptive layers updated
      expect(adaptiveService.updateAfterSubmission).toHaveBeenCalledWith(
        expect.objectContaining({
          studentId: 'user-1',
          problemId: 'problem-1',
          isCorrect: true,
        }),
      );

      (global.fetch as jest.Mock).mockRestore();
    });
  });

  describe('WRONG_ANSWER pipeline', () => {
    it('should: create PENDING → RUNNING → WRONG_ANSWER → update adaptive layers', async () => {
      codeExecService.executeCode.mockResolvedValue({
        status: SubmissionStatus.WRONG_ANSWER,
        output: 'Expected: 2\nGot: 3',
        runtime: 100,
      });

      await service.create(
        { problemId: 'problem-1', code: 'def solution(n): return n+2', language: 'python' },
        'user-1',
      );
      await wait();

      // Verify adaptive layers updated with isCorrect=false
      expect(adaptiveService.updateAfterSubmission).toHaveBeenCalledWith(
        expect.objectContaining({
          isCorrect: false,
        }),
      );
    });
  });

  describe('RUNTIME_ERROR pipeline', () => {
    it('should: create PENDING → RUNNING → RUNTIME_ERROR → NOT update adaptive layers', async () => {
      codeExecService.executeCode.mockResolvedValue({
        status: SubmissionStatus.RUNTIME_ERROR,
        output: '',
        error: 'NameError: name x is not defined',
      });

      await service.create(
        { problemId: 'problem-1', code: 'print(x)', language: 'python' },
        'user-1',
      );
      await wait();

      // Adaptive layers should NOT be called for RUNTIME_ERROR
      expect(adaptiveService.updateAfterSubmission).not.toHaveBeenCalled();
    });
  });

  describe('TIME_LIMIT pipeline', () => {
    it('should: PENDING → RUNNING → TIME_LIMIT → NOT update adaptive layers', async () => {
      codeExecService.executeCode.mockResolvedValue({
        status: SubmissionStatus.TIME_LIMIT,
        output: '',
        error: 'Time limit exceeded',
      });

      await service.create(
        { problemId: 'problem-1', code: 'while True: pass', language: 'python' },
        'user-1',
      );
      await wait();

      expect(adaptiveService.updateAfterSubmission).not.toHaveBeenCalled();
    });
  });

  describe('Execution error pipeline', () => {
    it('should catch execution errors and set RUNTIME_ERROR status', async () => {
      codeExecService.executeCode.mockRejectedValue(new Error('Docker crashed'));

      await service.create(
        { problemId: 'problem-1', code: 'code', language: 'python' },
        'user-1',
      );
      await wait();

      expect(prisma.submission.update).toHaveBeenCalledWith(
        expect.objectContaining({
          data: expect.objectContaining({
            status: SubmissionStatus.RUNTIME_ERROR,
            output: expect.stringContaining('Docker crashed'),
          }),
        }),
      );
    });
  });
});
