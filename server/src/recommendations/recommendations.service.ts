import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { AiService } from '../ai/ai.service';

@Injectable()
export class RecommendationsService {
  private readonly logger = new Logger(RecommendationsService.name);

  constructor(
    private prisma: PrismaService,
    private aiService: AiService,
  ) {}

  async getRecommendations(userId: string, limit = 10) {
    try {
      const result = await this.aiService.getRecommendations(userId, limit);
      return result.recommendations.map((r) => ({
        id: r.problem_id,
        title: r.title,
        difficulty: r.difficulty,
        score: r.score,
      }));
    } catch (error) {
      this.logger.warn(
        `AI service unavailable, falling back to basic recommendations: ${error.message}`,
      );
      return this.fallbackRecommendations(userId, limit);
    }
  }

  private async fallbackRecommendations(userId: string, limit: number) {
    const solvedProblemIds = await this.prisma.submission
      .findMany({
        where: { userId, status: 'ACCEPTED' },
        select: { problemId: true },
        distinct: ['problemId'],
      })
      .then((submissions) => submissions.map((s) => s.problemId));

    return this.prisma.problem.findMany({
      where: { id: { notIn: solvedProblemIds } },
      take: limit,
      orderBy: { createdAt: 'desc' },
    });
  }
}
