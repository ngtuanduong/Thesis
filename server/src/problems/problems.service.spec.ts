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

      expect(prisma.problem.create).toHaveBeenCalledWith({
        data: {
          title: dto.title,
          description: dto.description,
          difficulty: dto.difficulty,
          tags: dto.tags,
          courseId: dto.courseId,
          testCases: { create: dto.testCases },
        },
        include: { testCases: true },
      });
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
});
