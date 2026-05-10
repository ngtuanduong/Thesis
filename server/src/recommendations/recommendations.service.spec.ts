import { Test, TestingModule } from '@nestjs/testing';
import { RecommendationsService } from './recommendations.service';
import { PrismaService } from '../prisma/prisma.service';
import { AiService } from '../ai/ai.service';

describe('RecommendationsService', () => {
  let service: RecommendationsService;
  let prisma: Record<string, any>;
  let aiService: Record<string, any>;

  beforeEach(async () => {
    prisma = {
      submission: {
        findMany: jest.fn(),
      },
      problem: {
        findMany: jest.fn(),
      },
    };

    aiService = {
      getRecommendations: jest.fn(),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        RecommendationsService,
        { provide: PrismaService, useValue: prisma },
        { provide: AiService, useValue: aiService },
      ],
    }).compile();

    service = module.get<RecommendationsService>(RecommendationsService);
  });

  describe('getRecommendations', () => {
    it('should return mapped recommendations from AI service', async () => {
      aiService.getRecommendations.mockResolvedValue({
        recommendations: [
          { problem_id: 'p1', title: 'Two Sum', difficulty: 'EASY', score: 0.95 },
          { problem_id: 'p2', title: 'Linked List', difficulty: 'MEDIUM', score: 0.8 },
        ],
      });

      const result = await service.getRecommendations('user-1', 10);

      expect(aiService.getRecommendations).toHaveBeenCalledWith('user-1', 10);
      expect(result).toEqual([
        { id: 'p1', title: 'Two Sum', difficulty: 'EASY', score: 0.95 },
        { id: 'p2', title: 'Linked List', difficulty: 'MEDIUM', score: 0.8 },
      ]);
    });

    it('should fallback to unsolved problems when AI service fails', async () => {
      aiService.getRecommendations.mockRejectedValue(new Error('Service unavailable'));
      prisma.submission.findMany.mockResolvedValue([
        { problemId: 'solved-1' },
        { problemId: 'solved-2' },
      ]);
      const unsolvedProblems = [
        { id: 'p3', title: 'Binary Search', difficulty: 'MEDIUM', createdAt: new Date() },
      ];
      prisma.problem.findMany.mockResolvedValue(unsolvedProblems);

      const result = await service.getRecommendations('user-1', 5);

      expect(prisma.submission.findMany).toHaveBeenCalledWith({
        where: { userId: 'user-1', status: 'ACCEPTED' },
        select: { problemId: true },
        distinct: ['problemId'],
      });
      expect(prisma.problem.findMany).toHaveBeenCalledWith({
        where: { id: { notIn: ['solved-1', 'solved-2'] } },
        take: 5,
        orderBy: { createdAt: 'desc' },
      });
      expect(result).toEqual(unsolvedProblems);
    });

    it('should use default limit of 10', async () => {
      aiService.getRecommendations.mockResolvedValue({ recommendations: [] });

      await service.getRecommendations('user-1');

      expect(aiService.getRecommendations).toHaveBeenCalledWith('user-1', 10);
    });

    it('should return empty fallback when user has solved all problems', async () => {
      aiService.getRecommendations.mockRejectedValue(new Error('down'));
      prisma.submission.findMany.mockResolvedValue([{ problemId: 'p1' }]);
      prisma.problem.findMany.mockResolvedValue([]);

      const result = await service.getRecommendations('user-1', 5);
      expect(result).toEqual([]);
    });
  });
});
