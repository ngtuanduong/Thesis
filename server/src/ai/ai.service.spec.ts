import { Test, TestingModule } from '@nestjs/testing';
import { ConfigService } from '@nestjs/config';
import { AiService } from './ai.service';

describe('AiService', () => {
  let service: AiService;
  let fetchSpy: jest.SpyInstance;

  const mockConfigService = {
    get: jest.fn((key: string, defaultValue: string) => {
      if (key === 'AI_SERVICE_URL') return 'http://ai-service:8000';
      if (key === 'AI_SERVICE_KEY') return 'test-api-key';
      return defaultValue;
    }),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AiService,
        { provide: ConfigService, useValue: mockConfigService },
      ],
    }).compile();

    service = module.get<AiService>(AiService);

    fetchSpy = jest.spyOn(global, 'fetch').mockImplementation(
      jest.fn().mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue({}),
        text: jest.fn().mockResolvedValue(''),
      }),
    );
  });

  afterEach(() => {
    fetchSpy.mockRestore();
  });

  describe('request headers and base URL', () => {
    it('should include correct Content-Type and X-Service-Key headers', async () => {
      await service.embedProblem({ id: 'p1', title: 'T', description: 'D', tags: [] });

      expect(fetchSpy).toHaveBeenCalledWith(
        expect.stringContaining('http://ai-service:8000'),
        expect.objectContaining({
          headers: {
            'Content-Type': 'application/json',
            'X-Service-Key': 'test-api-key',
          },
        }),
      );
    });
  });

  describe('embedProblem', () => {
    it('should POST to /embed/problem with mapped payload', async () => {
      await service.embedProblem({
        id: 'p1',
        title: 'Two Sum',
        description: 'Find two numbers',
        tags: ['array'],
      });

      expect(fetchSpy).toHaveBeenCalledWith(
        'http://ai-service:8000/embed/problem',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({
            problem_id: 'p1',
            title: 'Two Sum',
            description: 'Find two numbers',
            tags: ['array'],
          }),
        }),
      );
    });
  });

  describe('getRecommendations', () => {
    it('should GET /recommend/{userId} with limit param', async () => {
      fetchSpy.mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValue({ recommendations: [] }),
      });

      await service.getRecommendations('user-1', 5);

      expect(fetchSpy).toHaveBeenCalledWith(
        'http://ai-service:8000/recommend/user-1?limit=5',
        expect.objectContaining({ method: 'GET' }),
      );
    });
  });

  describe('updateAdaptiveLayers', () => {
    it('should POST to /adaptive/update with snake_case mapping', async () => {
      await service.updateAdaptiveLayers({
        studentId: 's1',
        problemId: 'p1',
        isCorrect: true,
        attemptNumber: 2,
        timeSpent: 120,
      });

      expect(fetchSpy).toHaveBeenCalledWith(
        'http://ai-service:8000/adaptive/update',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({
            student_id: 's1',
            problem_id: 'p1',
            is_correct: true,
            attempt_number: 2,
            time_spent_seconds: 120,
          }),
        }),
      );
    });
  });

  describe('generateHint', () => {
    it('should POST to /hints/generate with mapped payload', async () => {
      fetchSpy.mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValue({
          hint: 'Try using a hash map',
          hint_level: 1,
          concepts_referenced: ['hash-map'],
          error: null,
        }),
      });

      const result = await service.generateHint({
        studentId: 's1',
        problemId: 'p1',
        code: 'def solution(): pass',
        errorMessage: 'WA',
        hintLevel: 2,
      });

      expect(fetchSpy).toHaveBeenCalledWith(
        'http://ai-service:8000/hints/generate',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({
            student_id: 's1',
            problem_id: 'p1',
            code: 'def solution(): pass',
            error_message: 'WA',
            hint_level: 2,
          }),
        }),
      );
    });
  });

  describe('getKnowledgeState', () => {
    it('should GET /adaptive/knowledge-state/{userId}', async () => {
      await service.getKnowledgeState('user-1');

      expect(fetchSpy).toHaveBeenCalledWith(
        'http://ai-service:8000/adaptive/knowledge-state/user-1',
        expect.objectContaining({ method: 'GET' }),
      );
    });
  });

  describe('getReviewQueue', () => {
    it('should GET /adaptive/review-queue/{userId}', async () => {
      await service.getReviewQueue('user-1');

      expect(fetchSpy).toHaveBeenCalledWith(
        'http://ai-service:8000/adaptive/review-queue/user-1',
        expect.objectContaining({ method: 'GET' }),
      );
    });
  });

  describe('logEvent', () => {
    it('should POST to /evaluation/log with mapped payload', async () => {
      await service.logEvent({
        userId: 'u1',
        event: 'submission',
        data: { problemId: 'p1' },
        sessionId: 'sess-1',
      });

      expect(fetchSpy).toHaveBeenCalledWith(
        'http://ai-service:8000/evaluation/log',
        expect.objectContaining({
          body: JSON.stringify({
            user_id: 'u1',
            event: 'submission',
            data: { problemId: 'p1' },
            session_id: 'sess-1',
          }),
        }),
      );
    });
  });

  describe('exportEvents', () => {
    it('should include event filter in query string when provided', async () => {
      await service.exportEvents('page_view');

      expect(fetchSpy).toHaveBeenCalledWith(
        'http://ai-service:8000/evaluation/export/events?event=page_view',
        expect.anything(),
      );
    });

    it('should not include query string when no event filter', async () => {
      await service.exportEvents();

      expect(fetchSpy).toHaveBeenCalledWith(
        'http://ai-service:8000/evaluation/export/events',
        expect.anything(),
      );
    });
  });

  describe('error handling', () => {
    it('should throw Error with status code and body text on non-ok response', async () => {
      fetchSpy.mockResolvedValueOnce({
        ok: false,
        status: 500,
        text: jest.fn().mockResolvedValue('Internal Server Error'),
      });

      await expect(service.embedProblem({ id: 'p1', title: '', description: '', tags: [] }))
        .rejects.toThrow('AI service error 500: Internal Server Error');
    });

    it('should throw on 404 response', async () => {
      fetchSpy.mockResolvedValueOnce({
        ok: false,
        status: 404,
        text: jest.fn().mockResolvedValue('Not Found'),
      });

      await expect(service.getKnowledgeState('nonexistent'))
        .rejects.toThrow('AI service error 404: Not Found');
    });
  });

  describe('assignGroup', () => {
    it('should POST to /evaluation/assign-group', async () => {
      await service.assignGroup('u1', 'experimental');

      expect(fetchSpy).toHaveBeenCalledWith(
        'http://ai-service:8000/evaluation/assign-group',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ user_id: 'u1', group: 'experimental' }),
        }),
      );
    });
  });

  describe('getEloHistory', () => {
    it('should GET /elo/student/{userId}', async () => {
      await service.getEloHistory('user-1');

      expect(fetchSpy).toHaveBeenCalledWith(
        'http://ai-service:8000/elo/student/user-1',
        expect.objectContaining({ method: 'GET' }),
      );
    });
  });
});
