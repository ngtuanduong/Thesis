import { Injectable, Logger } from '@nestjs/common';
import { AiService } from '../ai/ai.service';

@Injectable()
export class AdaptiveService {
  private readonly logger = new Logger(AdaptiveService.name);

  constructor(private aiService: AiService) {}

  async getRecommendations(userId: string, limit = 5) {
    try {
      return await this.aiService.getAdaptiveRecommendations(userId, limit);
    } catch (error) {
      this.logger.error(`Failed to get adaptive recommendations: ${error}`);
      return { recommendations: [], knowledge_summary: null, error: 'AI service unavailable' };
    }
  }

  async getKnowledgeState(userId: string) {
    try {
      return await this.aiService.getKnowledgeState(userId);
    } catch (error) {
      this.logger.error(`Failed to get knowledge state: ${error}`);
      return { concepts: [], error: 'AI service unavailable' };
    }
  }

  async getReviewQueue(userId: string) {
    try {
      return await this.aiService.getReviewQueue(userId);
    } catch (error) {
      this.logger.error(`Failed to get review queue: ${error}`);
      return { due_now: [], upcoming: [], error: 'AI service unavailable' };
    }
  }

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
}
