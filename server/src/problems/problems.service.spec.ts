import { Test, TestingModule } from '@nestjs/testing';
import { NotFoundException } from '@nestjs/common';
import { ProblemsService } from './problems.service';
import { PrismaService } from '../prisma/prisma.service';
import { AiService } from '../ai/ai.service';

describe('ProblemsService', () => {
  let service: ProblemsService;
  let prisma: Record<string, any>;
  let aiService: Record<string, any>;

  const mockProblem = {
    id: 'problem-1',
    title: 'Two Sum',
    description: 'Find two numbers that add up to target',
    difficulty: 'EASY',
    tags: ['array', 'hash-map'],
    courseId: 'course-1',
    starterCode: '',
    testCases: [
      { id: 'tc-1', input: '[2,7,11,15], 9', expected: '[0,1]', isHidden: false },
    ],
  };

  beforeEach(async () => {
    prisma = {
      problem: {
        create: jest.fn(),
        findMany: jest.fn(),
        findUnique: jest.fn(),
        update: jest.fn(),
        delete: jest.fn(),
      },
    };

    aiService = {
      embedProblem: jest.fn().mockResolvedValue(undefined),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ProblemsService,
        { provide: PrismaService, useValue: prisma },
        { provide: AiService, useValue: aiService },
      ],
    }).compile();

    service = module.get<ProblemsService>(ProblemsService);
  });

  describe('create', () => {
    it('should create a problem and trigger embedding', async () => {
      prisma.problem.create.mockResolvedValue(mockProblem);

      const dto = {
        title: 'Two Sum',
        description: 'Find two numbers that add up to target',
        difficulty: 'EASY' as any,
        tags: ['array', 'hash-map'],
        courseId: 'course-1',
        testCases: [
          { input: '[2,7,11,15], 9', expected: '[0,1]', isHidden: false },
        ],
      };

      const result = await service.create(dto);

      expect(prisma.problem.create).toHaveBeenCalledWith(
        expect.objectContaining({
          data: expect.objectContaining({
            title: dto.title,
            description: dto.description,
            difficulty: dto.difficulty,
            tags: dto.tags,
            courseId: dto.courseId,
            testCases: { create: dto.testCases },
          }),
          include: { testCases: true },
        }),
      );
      expect(result).toEqual(mockProblem);
      // embedProblem is fire-and-forget, just verify it was called
      expect(aiService.embedProblem).toHaveBeenCalledWith(mockProblem);
    });
  });

  describe('findAll', () => {
    it('should return all problems when no courseId provided', async () => {
      prisma.problem.findMany.mockResolvedValue([mockProblem]);

      const result = await service.findAll();

      expect(prisma.problem.findMany).toHaveBeenCalledWith({
        where: undefined,
        include: { testCases: { where: { isHidden: false } } },
      });
      expect(result).toEqual([mockProblem]);
    });

    it('should filter by courseId when provided', async () => {
      prisma.problem.findMany.mockResolvedValue([mockProblem]);

      const result = await service.findAll('course-1');

      expect(prisma.problem.findMany).toHaveBeenCalledWith({
        where: { courseId: 'course-1' },
        include: { testCases: { where: { isHidden: false } } },
      });
      expect(result).toEqual([mockProblem]);
    });
  });

  describe('findById', () => {
    it('should return a problem when found', async () => {
      prisma.problem.findUnique.mockResolvedValue(mockProblem);

      const result = await service.findById('problem-1');

      expect(prisma.problem.findUnique).toHaveBeenCalledWith({
        where: { id: 'problem-1' },
        include: { testCases: true },
      });
      expect(result).toEqual(mockProblem);
    });

    it('should throw NotFoundException when not found', async () => {
      prisma.problem.findUnique.mockResolvedValue(null);

      await expect(service.findById('nonexistent')).rejects.toThrow(
        NotFoundException,
      );
    });
  });

  describe('update', () => {
    it('should update problem data', async () => {
      prisma.problem.findUnique.mockResolvedValue(mockProblem);
      const updatedProblem = { ...mockProblem, title: 'Updated Title' };
      prisma.problem.update.mockResolvedValue(updatedProblem);

      const result = await service.update('problem-1', {
        title: 'Updated Title',
      });

      expect(prisma.problem.update).toHaveBeenCalledWith({
        where: { id: 'problem-1' },
        data: { title: 'Updated Title' },
        include: { testCases: true },
      });
      expect(result).toEqual(updatedProblem);
    });
  });

  describe('remove', () => {
    it('should delete a problem', async () => {
      prisma.problem.findUnique.mockResolvedValue(mockProblem);
      prisma.problem.delete.mockResolvedValue(mockProblem);

      const result = await service.remove('problem-1');

      expect(prisma.problem.delete).toHaveBeenCalledWith({
        where: { id: 'problem-1' },
      });
      expect(result).toEqual({ deleted: true });
    });
  });

  describe('create — starterCode generation', () => {
    it('should auto-generate starterCode from test cases when not provided', async () => {
      prisma.problem.create.mockResolvedValue(mockProblem);

      const dto = {
        title: 'Two Sum',
        description: 'Find two numbers',
        testCases: [{ input: '{"nums":[2,7], "target":9}', expected: '[0,1]', isHidden: false }],
      };

      await service.create(dto as any);

      expect(prisma.problem.create).toHaveBeenCalledWith(
        expect.objectContaining({
          data: expect.objectContaining({
            starterCode: expect.stringContaining('def solution(nums, target):'),
          }),
        }),
      );
    });

    it('should NOT overwrite explicit starterCode', async () => {
      prisma.problem.create.mockResolvedValue(mockProblem);

      const dto = {
        title: 'Two Sum',
        description: 'Find two numbers',
        starterCode: 'def my_solution():\n    pass',
        testCases: [{ input: '{"nums":[2,7], "target":9}', expected: '[0,1]', isHidden: false }],
      };

      await service.create(dto as any);

      expect(prisma.problem.create).toHaveBeenCalledWith(
        expect.objectContaining({
          data: expect.objectContaining({
            starterCode: 'def my_solution():\n    pass',
          }),
        }),
      );
    });

    it('should handle embedding failure gracefully (fire-and-forget)', async () => {
      prisma.problem.create.mockResolvedValue(mockProblem);
      aiService.embedProblem.mockRejectedValue(new Error('AI down'));

      const dto = {
        title: 'Test',
        description: 'Desc',
        testCases: [],
      };

      // Should not throw even though embedding fails
      const result = await service.create(dto as any);
      expect(result).toEqual(mockProblem);
    });
  });

  describe('update — enhanced', () => {
    it('should replace testCases with deleteMany+create when testCases provided', async () => {
      prisma.problem.findUnique.mockResolvedValue(mockProblem);
      prisma.problem.update.mockResolvedValue(mockProblem);

      await service.update('problem-1', {
        testCases: [{ input: '1', expected: '2', isHidden: false }],
      } as any);

      expect(prisma.problem.update).toHaveBeenCalledWith(
        expect.objectContaining({
          data: expect.objectContaining({
            testCases: {
              deleteMany: {},
              create: [{ input: '1', expected: '2', isHidden: false }],
            },
          }),
        }),
      );
    });

    it('should regenerate starterCode when test cases change and no explicit starterCode', async () => {
      prisma.problem.findUnique.mockResolvedValue(mockProblem);
      prisma.problem.update.mockResolvedValue(mockProblem);

      await service.update('problem-1', {
        testCases: [{ input: '{"x":1}', expected: '2', isHidden: false }],
      } as any);

      expect(prisma.problem.update).toHaveBeenCalledWith(
        expect.objectContaining({
          data: expect.objectContaining({
            starterCode: expect.stringContaining('def solution(x):'),
          }),
        }),
      );
    });

    it('should throw NotFoundException for non-existent problem', async () => {
      prisma.problem.findUnique.mockResolvedValue(null);

      await expect(service.update('nonexistent', { title: 'X' })).rejects.toThrow(
        NotFoundException,
      );
    });
  });
});
