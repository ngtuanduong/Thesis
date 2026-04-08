import { Test, TestingModule } from '@nestjs/testing';
import { NotFoundException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { SubmissionsService } from './submissions.service';
import { PrismaService } from '../prisma/prisma.service';
import { CodeExecutionService } from './code-execution.service';
import { AdaptiveService } from '../adaptive/adaptive.service';

describe('SubmissionsService', () => {
  let service: SubmissionsService;
  let prisma: Record<string, any>;

  const mockSubmission = {
    id: 'sub-1',
    userId: 'user-1',
    problemId: 'problem-1',
    code: 'def solution(nums, target): pass',
    language: 'python',
    status: 'PENDING',
    output: null,
    runtime: null,
    memory: null,
    createdAt: new Date(),
    updatedAt: new Date(),
  };

  beforeEach(async () => {
    prisma = {
      submission: {
        create: jest.fn(),
        findUnique: jest.fn(),
        findMany: jest.fn(),
        update: jest.fn(),
        count: jest.fn(),
      },
      testCase: {
        findMany: jest.fn(),
      },
    };

    const mockCodeExecutionService = {
      executeCode: jest.fn(),
    };

    const mockConfigService = {
      get: jest.fn().mockReturnValue('http://localhost:8000'),
    };

    const mockAdaptiveService = {
      updateAfterSubmission: jest.fn().mockResolvedValue({}),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        SubmissionsService,
        { provide: PrismaService, useValue: prisma },
        { provide: CodeExecutionService, useValue: mockCodeExecutionService },
        { provide: ConfigService, useValue: mockConfigService },
        { provide: AdaptiveService, useValue: mockAdaptiveService },
      ],
    }).compile();

    service = module.get<SubmissionsService>(SubmissionsService);
  });

  describe('create', () => {
    it('should create a submission with PENDING status', async () => {
      prisma.submission.create.mockResolvedValue(mockSubmission);

      const dto = {
        problemId: 'problem-1',
        code: 'def solution(nums, target): pass',
        language: 'python',
      };

      const result = await service.create(dto, 'user-1');

      expect(prisma.submission.create).toHaveBeenCalledWith({
        data: {
          ...dto,
          userId: 'user-1',
          status: 'PENDING',
        },
      });
      expect(result).toEqual(mockSubmission);
      expect(result.status).toBe('PENDING');
    });
  });

  describe('findById', () => {
    it('should return a submission when found', async () => {
      prisma.submission.findUnique.mockResolvedValue(mockSubmission);

      const result = await service.findById('sub-1');

      expect(prisma.submission.findUnique).toHaveBeenCalledWith({
        where: { id: 'sub-1' },
      });
      expect(result).toEqual(mockSubmission);
    });

    it('should throw NotFoundException when not found', async () => {
      prisma.submission.findUnique.mockResolvedValue(null);

      await expect(service.findById('nonexistent')).rejects.toThrow(
        NotFoundException,
      );
    });
  });

  describe('findByUser', () => {
    it('should return user submissions ordered by date', async () => {
      const submissions = [mockSubmission];
      prisma.submission.findMany.mockResolvedValue(submissions);

      const result = await service.findByUser('user-1');

      expect(prisma.submission.findMany).toHaveBeenCalledWith({
        where: { userId: 'user-1' },
        include: {
          problem: { select: { id: true, title: true, difficulty: true } },
        },
        orderBy: { createdAt: 'desc' },
      });
      expect(result).toEqual(submissions);
    });
  });

  describe('findByProblem', () => {
    it('should return submissions for a problem by user', async () => {
      const submissions = [mockSubmission];
      prisma.submission.findMany.mockResolvedValue(submissions);

      const result = await service.findByProblem('problem-1', 'user-1');

      expect(prisma.submission.findMany).toHaveBeenCalledWith({
        where: { problemId: 'problem-1', userId: 'user-1' },
        orderBy: { createdAt: 'desc' },
      });
      expect(result).toEqual(submissions);
    });
  });
});
