import { Injectable, Logger } from '@nestjs/common';
import { AiService } from '../ai/ai.service';

@Injectable()
export class AdaptiveService {
  private readonly logger = new Logger(AdaptiveService.name);

  constructor(private aiService: AiService) {}

  /** Get adaptive problem recommendations for a student based on BKT/Elo/MAB state. */
  async getRecommendations(userId: string, limit = 5) {
    try {
      return await this.aiService.getAdaptiveRecommendations(userId, limit);
    } catch (error) {
      this.logger.error(`Failed to get adaptive recommendations: ${error}`);
      return { recommendations: [], knowledge_summary: null, error: 'AI service unavailable' };
    }
  }

  /** Retrieve the student's BKT knowledge state across all concepts. */
  async getKnowledgeState(userId: string) {
    try {
      return await this.aiService.getKnowledgeState(userId);
    } catch (error) {
      this.logger.error(`Failed to get knowledge state: ${error}`);
      return { concepts: [], error: 'AI service unavailable' };
    }
  }

  /** Get the FSRS spaced-repetition review queue (due now + upcoming). */
  async getReviewQueue(userId: string) {
    try {
      return await this.aiService.getReviewQueue(userId);
    } catch (error) {
      this.logger.error(`Failed to get review queue: ${error}`);
      return { due_now: [], upcoming: [], error: 'AI service unavailable' };
    }
  }

  /** Update all adaptive layers (BKT, Elo, MAB, FSRS) after a submission is graded. */
  async updateAfterSubmission(data: {
    studentId: string;
    problemId: string;
    isCorrect: boolean;
    attemptNumber: number;
    timeSpent: number;
  }) {
    try {
      return await this.aiService.updateAdaptiveLayers(data);
    } catch (error) {
      this.logger.error(`Failed to update adaptive layers: ${error}`);
      return { error: 'AI service unavailable' };
    }
  }

  /** Generate an LLM-powered Socratic hint for a student's current attempt. */
  async generateHint(data: {
    studentId: string;
    problemId: string;
    code: string;
    errorMessage?: string;
    hintLevel?: number;
  }) {
    try {
      return await this.aiService.generateHint(data);
    } catch (error) {
      this.logger.error(`Failed to generate hint: ${error}`);
      return { hint: null, error: 'AI service unavailable' };
    }
  }

  /** Log a frontend user interaction event for evaluation tracking. */
  async logEvent(data: {
    userId: string;
    event: string;
    data?: Record<string, unknown>;
    sessionId?: string;
  }) {
    try {
      return await this.aiService.logEvent(data);
    } catch (error) {
      this.logger.warn(`Failed to log event: ${error}`);
      return { logged: false };
    }
  }

  /** Get Elo rating history for a student to display trajectory chart. */
  async getEloHistory(userId: string) {
    try {
      return await this.aiService.getEloHistory(userId);
    } catch (error) {
      this.logger.error(`Failed to get Elo history: ${error}`);
      return { rating: 1200, rating_history: [], error: 'AI service unavailable' };
    }
  }
}
