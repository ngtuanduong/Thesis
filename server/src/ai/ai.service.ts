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

  /** Generate and store a vector embedding for a single problem. */
  async embedProblem(problem: {
    id: string;
    title: string;
    description: string;
    problemConcepts?: { concept: { name: string } }[];
  }) {
    const tags = problem.problemConcepts?.map((pc) => pc.concept.name) ?? [];
    return this.request('POST', '/embed/problem', {
      problem_id: problem.id,
      title: problem.title,
      description: problem.description,
      tags,
    });
  }

  /** Generate and store vector embeddings for multiple problems in a single request. */
  async embedBatch(
    problems: {
      id: string;
      title: string;
      description: string;
      problemConcepts?: { concept: { name: string } }[];
    }[],
  ) {
    return this.request('POST', '/embed/batch', {
      problems: problems.map((p) => ({
        problem_id: p.id,
        title: p.title,
        description: p.description,
        tags: p.problemConcepts?.map((pc) => pc.concept.name) ?? [],
      })),
    });
  }

  /** Recompute the user's skill profile based on their submission history. */
  async computeProfile(userId: string) {
    return this.request('POST', `/profile/${userId}`, {});
  }

  /** Get content-based problem recommendations using embedding similarity. */
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

  /** Analyze the gap between a user's current skills and target proficiency. */
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

  /** Send a submission result to the AI service to update BKT, Elo, MAB, and FSRS models. */
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

  /** Get adaptive recommendations combining all five learning layers. */
  async getAdaptiveRecommendations(userId: string, limit = 5) {
    return this.request('GET', `/adaptive/recommend/${userId}?limit=${limit}`);
  }

  /** Retrieve the student's BKT knowledge state for all tracked concepts. */
  async getKnowledgeState(userId: string) {
    return this.request('GET', `/adaptive/knowledge-state/${userId}`);
  }

  /** Select the best practice problem for a specific concept using MAB. */
  async getPracticeForConcept(userId: string, conceptId: number) {
    return this.request<{ problem_id: string | null; title: string | null }>(
      'GET',
      `/mab/practice?student_id=${userId}&concept_id=${conceptId}`,
    );
  }

  /** Get the FSRS spaced-repetition review queue for a student. */
  async getReviewQueue(userId: string) {
    return this.request('GET', `/adaptive/review-queue/${userId}`);
  }

  /** Get ALL FSRS review cards with full statistics. */
  async getReviewCards(userId: string) {
    return this.request('GET', `/adaptive/review-cards/${userId}`);
  }

  // === Evaluation Methods ===

  /** Log a user interaction event for A/B testing and experiment tracking. */
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

  /** Get the A/B experiment group assignment for a user. */
  async getUserGroup(userId: string) {
    return this.request<{ user_id: string; group: string | null }>(
      'GET',
      `/evaluation/group/${userId}`,
    );
  }

  /** Assign a user to an A/B experiment group (experimental or control). */
  async assignGroup(userId: string, group: 'experimental' | 'control') {
    return this.request('POST', '/evaluation/assign-group', {
      user_id: userId,
      group,
    });
  }

  /** Generate a Socratic hint using the LLM, considering the student's code and knowledge state. */
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

  /** Send a message to the chatbot and receive a response. */
  async chatbotRespond(data: {
    message: string;
    conversationHistory: { role: string; content: string }[];
    userRole: string;
  }) {
    return this.request<{
      response: string | null;
      tokens_used: number;
      error: string | null;
    }>('POST', '/chatbot/respond', {
      message: data.message,
      conversation_history: data.conversationHistory,
      user_role: data.userRole,
    });
  }

  /** Retrieve aggregate statistics for the A/B experiment. */
  async getExperimentStats() {
    return this.request('GET', '/evaluation/stats');
  }

  /** Export evaluation events, optionally filtered by event type. */
  async exportEvents(event?: string) {
    const path = event
      ? `/evaluation/export/events?event=${encodeURIComponent(event)}`
      : '/evaluation/export/events';
    return this.request('GET', path);
  }

  /** Get the Elo rating history for a student over time. */
  async getEloHistory(userId: string) {
    return this.request('GET', `/elo/student/${userId}`);
  }
}
