import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { AiService } from '../ai/ai.service';

@Injectable()
export class AdminService {
  private readonly logger = new Logger(AdminService.name);

  constructor(
    private prisma: PrismaService,
    private aiService: AiService,
  ) {}

  async getStats() {
    const todayStart = new Date();
    todayStart.setHours(0, 0, 0, 0);

    const [totalUsers, totalSubmissions, totalProblems, totalCourses, activeUsersToday] =
      await Promise.all([
        this.prisma.user.count(),
        this.prisma.submission.count(),
        this.prisma.problem.count(),
        this.prisma.course.count(),
        this.prisma.submission
          .findMany({
            where: { createdAt: { gte: todayStart } },
            select: { userId: true },
            distinct: ['userId'],
          })
          .then((rows) => rows.length),
      ]);

    return {
      totalUsers,
      totalSubmissions,
      totalProblems,
      totalCourses,
      activeUsersToday,
    };
  }

  async getUsers() {
    return this.prisma.user.findMany({
      select: {
        id: true,
        email: true,
        name: true,
        role: true,
        createdAt: true,
        _count: { select: { submissions: true } },
        experimentGroup: {
          select: { groupName: true, assignedAt: true },
        },
      },
      orderBy: { createdAt: 'desc' },
    });
  }

  async assignGroup(userId: string, groupName: string) {
    try {
      const result = await this.aiService.assignGroup(
        userId,
        groupName as 'experimental' | 'control',
      );
      return result;
    } catch (error) {
      this.logger.warn(
        `AI service unavailable for assignGroup, falling back to local upsert: ${error.message}`,
      );
      // Fallback: upsert locally if AI service is down
      return this.prisma.experimentGroup.upsert({
        where: { userId },
        update: { groupName },
        create: { userId, groupName },
      });
    }
  }

  async getExperimentStats() {
    try {
      return await this.aiService.getExperimentStats();
    } catch (error) {
      this.logger.warn(
        `AI service unavailable for experiment stats: ${error.message}`,
      );
      const groups = await this.prisma.experimentGroup.groupBy({
        by: ['groupName'],
        _count: { userId: true },
      });
      return {
        source: 'local_fallback',
        groups: groups.map((g) => ({
          groupName: g.groupName,
          userCount: g._count.userId,
        })),
      };
    }
  }

  async exportEvents(event?: string) {
    try {
      return await this.aiService.exportEvents(event);
    } catch (error) {
      this.logger.warn(
        `AI service unavailable for export events: ${error.message}`,
      );
      const where = event ? { event } : {};
      const events = await this.prisma.eventLog.findMany({
        where,
        orderBy: { createdAt: 'desc' },
        take: 1000,
      });
      return { source: 'local_fallback', events };
    }
  }
}
