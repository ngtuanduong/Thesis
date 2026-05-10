import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { AiService } from '../ai/ai.service';

@Injectable()
export class SkillsService {
  private readonly logger = new Logger(SkillsService.name);

  constructor(
    private prisma: PrismaService,
    private aiService: AiService,
  ) {}

  async getByUser(userId: string) {
    return this.prisma.skillEmbedding.findMany({
      where: { userId },
      orderBy: { score: 'desc' },
    });
  }

  async upsert(userId: string, skillName: string, score: number, embedding: number[]) {
    return this.prisma.skillEmbedding.upsert({
      where: { userId_skillName: { userId, skillName } },
      update: { score, embedding },
      create: { userId, skillName, score, embedding },
    });
  }

  async computeProfile(userId: string) {
    return this.aiService.computeProfile(userId);
  }
}
