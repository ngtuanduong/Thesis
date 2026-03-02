import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class AiService {
  private readonly logger = new Logger(AiService.name);
  private readonly baseUrl: string;
  private readonly serviceKey: string;

  constructor(private configService: ConfigService) {
    this.baseUrl = this.configService.get<string>(
      'AI_SERVICE_URL',
      'http://localhost:8000',
    );
    this.serviceKey = this.configService.get<string>(
      'AI_SERVICE_KEY',
      'dev-secret-key',
    );
  }

  private async request<T>(
    method: string,
    path: string,
    body?: unknown,
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const res = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-Service-Key': this.serviceKey,
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`AI service error ${res.status}: ${text}`);
    }

    return res.json() as Promise<T>;
  }

  async embedProblem(problem: {
    id: string;
    title: string;
    description: string;
    tags: string[];
  }) {
    return this.request('POST', '/embed/problem', {
      problem_id: problem.id,
      title: problem.title,
      description: problem.description,
      tags: problem.tags,
    });
  }

  async embedBatch(
    problems: {
      id: string;
      title: string;
      description: string;
      tags: string[];
    }[],
  ) {
    return this.request('POST', '/embed/batch', {
      problems: problems.map((p) => ({
        problem_id: p.id,
        title: p.title,
        description: p.description,
        tags: p.tags,
      })),
    });
  }

  async computeProfile(userId: string) {
    return this.request('POST', `/profile/${userId}`, {});
  }

  async getRecommendations(userId: string, limit = 10) {
    return this.request<{
      user_id: string;
      recommendations: {
        problem_id: string;
        title: string;
        difficulty: string;
        score: number;
      }[];
    }>('GET', `/recommend/${userId}?limit=${limit}`);
  }

  async analyzeSkillGap(userId: string) {
    return this.request<{
      user_id: string;
      gaps: {
        skill_name: string;
        current_score: number;
        target_score: number;
        gap: number;
      }[];
    }>('GET', `/skill-gap/${userId}`);
  }

  // === Adaptive Learning Layer Methods ===

  async updateAdaptiveLayers(data: {
    studentId: string;
    problemId: string;
    isCorrect: boolean;
    attemptNumber: number;
    timeSpent: number;
  }) {
    return this.request('POST', '/adaptive/update', {
      student_id: data.studentId,
      problem_id: data.problemId,
      is_correct: data.isCorrect,
      attempt_number: data.attemptNumber,
      time_spent_seconds: data.timeSpent,
    });
  }

  async getAdaptiveRecommendations(userId: string, limit = 5) {
    return this.request('GET', `/adaptive/recommend/${userId}?limit=${limit}`);
  }

  async getKnowledgeState(userId: string) {
    return this.request('GET', `/adaptive/knowledge-state/${userId}`);
  }

  async getReviewQueue(userId: string) {
    return this.request('GET', `/adaptive/review-queue/${userId}`);
  }

  // === Evaluation Methods ===

  async logEvent(data: {
    userId: string;
    event: string;
    data?: Record<string, unknown>;
    sessionId?: string;
  }) {
    return this.request('POST', '/evaluation/log', {
      user_id: data.userId,
      event: data.event,
      data: data.data || {},
      session_id: data.sessionId || null,
    });
  }

  async getUserGroup(userId: string) {
    return this.request<{ user_id: string; group: string | null }>(
      'GET',
      `/evaluation/group/${userId}`,
    );
  }

  async assignGroup(userId: string, group: 'experimental' | 'control') {
    return this.request('POST', '/evaluation/assign-group', {
      user_id: userId,
      group,
    });
  }

  async generateHint(data: {
    studentId: string;
    problemId: string;
    code: string;
    errorMessage?: string;
    hintLevel?: number;
  }) {
    return this.request<{
      hint: string | null;
      hint_level: number;
      concepts_referenced: string[];
      error: string | null;
    }>('POST', '/hints/generate', {
      student_id: data.studentId,
      problem_id: data.problemId,
      code: data.code,
      error_message: data.errorMessage || null,
      hint_level: data.hintLevel || 1,
    });
  }
}
