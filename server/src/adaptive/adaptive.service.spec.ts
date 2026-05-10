import { Test, TestingModule } from '@nestjs/testing';
import { AdaptiveService } from './adaptive.service';
import { AiService } from '../ai/ai.service';

describe('AdaptiveService', () => {
  let service: AdaptiveService;
  let aiService: Record<string, jest.Mock>;

  beforeEach(async () => {
    aiService = {
      getAdaptiveRecommendations: jest.fn(),
      getKnowledgeState: jest.fn(),
      getReviewQueue: jest.fn(),
      updateAdaptiveLayers: jest.fn(),
      generateHint: jest.fn(),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AdaptiveService,
        { provide: AiService, useValue: aiService },
      ],
    }).compile();

    service = module.get<AdaptiveService>(AdaptiveService);
  });

  describe('getRecommendations', () => {
    it('should proxy to AI service and return recommendations', async () => {
      const mockResponse = {
        recommendations: [
          { problem_id: 'p1', title: 'Two Sum', score: 0.95 },
        ],
        knowledge_summary: { mastery: 0.7 },
      };
      aiService.getAdaptiveRecommendations.mockResolvedValue(mockResponse);

      const result = await service.getRecommendations('user-1', 5);

      expect(aiService.getAdaptiveRecommendations).toHaveBeenCalledWith(
        'user-1',
        5,
      );
      expect(result).toEqual(mockResponse);
    });

    it('should return fallback on AI service failure', async () => {
      aiService.getAdaptiveRecommendations.mockRejectedValue(
        new Error('Service down'),
      );

      const result = await service.getRecommendations('user-1');

      expect(result).toEqual({
        recommendations: [],
        knowledge_summary: null,
        error: 'AI service unavailable',
      });
    });
  });

  describe('getKnowledgeState', () => {
    it('should proxy to AI service and return knowledge state', async () => {
      const mockResponse = {
        concepts: [{ name: 'arrays', mastery: 0.8 }],
      };
      aiService.getKnowledgeState.mockResolvedValue(mockResponse);

      const result = await service.getKnowledgeState('user-1');

      expect(aiService.getKnowledgeState).toHaveBeenCalledWith('user-1');
      expect(result).toEqual(mockResponse);
    });

    it('should return fallback on AI service failure', async () => {
      aiService.getKnowledgeState.mockRejectedValue(
        new Error('Service down'),
      );

      const result = await service.getKnowledgeState('user-1');

      expect(result).toEqual({
        concepts: [],
        error: 'AI service unavailable',
      });
    });
  });

  describe('getReviewQueue', () => {
    it('should proxy to AI service and return review queue', async () => {
      const mockResponse = {
        due_now: [{ problem_id: 'p1', due_date: '2026-04-07' }],
        upcoming: [],
      };
      aiService.getReviewQueue.mockResolvedValue(mockResponse);

      const result = await service.getReviewQueue('user-1');

      expect(aiService.getReviewQueue).toHaveBeenCalledWith('user-1');
      expect(result).toEqual(mockResponse);
    });

    it('should return fallback on AI service failure', async () => {
      aiService.getReviewQueue.mockRejectedValue(new Error('Service down'));

      const result = await service.getReviewQueue('user-1');

      expect(result).toEqual({
        due_now: [],
        upcoming: [],
        error: 'AI service unavailable',
      });
    });
  });

  describe('generateHint', () => {
    it('should proxy to AI service and return hint', async () => {
      const hintData = {
        studentId: 'user-1',
        problemId: 'problem-1',
        code: 'def solution(): pass',
        errorMessage: 'TypeError',
        hintLevel: 1,
      };
      const mockResponse = {
        hint: 'Consider using a hash map for O(1) lookups',
        hint_level: 1,
        concepts_referenced: ['hash-map'],
        error: null,
      };
      aiService.generateHint.mockResolvedValue(mockResponse);

      const result = await service.generateHint(hintData);

      expect(aiService.generateHint).toHaveBeenCalledWith(hintData);
      expect(result).toEqual(mockResponse);
    });

    it('should return fallback on AI service failure', async () => {
      const hintData = {
        studentId: 'user-1',
        problemId: 'problem-1',
        code: 'def solution(): pass',
      };
      aiService.generateHint.mockRejectedValue(new Error('Service down'));

      const result = await service.generateHint(hintData);

      expect(result).toEqual({
        hint: null,
        error: 'AI service unavailable',
      });
    });
  });

  describe('updateAfterSubmission', () => {
    it('should proxy to AI service for adaptive layer updates', async () => {
      const submissionData = {
        studentId: 'user-1',
        problemId: 'problem-1',
        isCorrect: true,
        attemptNumber: 1,
        timeSpent: 120,
      };
      const mockResponse = { bkt_updated: true, elo_updated: true };
      aiService.updateAdaptiveLayers.mockResolvedValue(mockResponse);

      const result = await service.updateAfterSubmission(submissionData);

      expect(aiService.updateAdaptiveLayers).toHaveBeenCalledWith(
        submissionData,
      );
      expect(result).toEqual(mockResponse);
    });

    it('should return fallback on AI service failure', async () => {
      const submissionData = {
        studentId: 'user-1',
        problemId: 'problem-1',
        isCorrect: false,
        attemptNumber: 2,
        timeSpent: 60,
      };
      aiService.updateAdaptiveLayers.mockRejectedValue(
        new Error('Service down'),
      );

      const result = await service.updateAfterSubmission(submissionData);

      expect(result).toEqual({ error: 'AI service unavailable' });
    });
  });
});
