import { Test, TestingModule } from '@nestjs/testing';
import { AdminService } from './admin.service';
import { PrismaService } from '../prisma/prisma.service';
import { AiService } from '../ai/ai.service';

describe('AdminService', () => {
  let service: AdminService;
  let prisma: Record<string, any>;
  let aiService: Record<string, any>;

  beforeEach(async () => {
    prisma = {
      user: {
        count: jest.fn().mockResolvedValue(10),
        findMany: jest.fn(),
      },
      submission: {
        count: jest.fn().mockResolvedValue(100),
        findMany: jest.fn(),
      },
      problem: {
        count: jest.fn().mockResolvedValue(30),
      },
      course: {
        count: jest.fn().mockResolvedValue(3),
      },
      experimentGroup: {
        upsert: jest.fn(),
        groupBy: jest.fn(),
      },
      eventLog: {
        findMany: jest.fn(),
      },
    };

    aiService = {
      assignGroup: jest.fn(),
      getExperimentStats: jest.fn(),
      exportEvents: jest.fn(),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AdminService,
        { provide: PrismaService, useValue: prisma },
        { provide: AiService, useValue: aiService },
      ],
    }).compile();

    service = module.get<AdminService>(AdminService);
  });

  describe('getStats', () => {
    it('should return aggregated platform statistics', async () => {
      prisma.submission.findMany.mockResolvedValue([
        { userId: 'u1' },
        { userId: 'u2' },
        { userId: 'u1' },
      ]);

      const result = await service.getStats();

      expect(result).toEqual({
        totalUsers: 10,
        totalSubmissions: 100,
        totalProblems: 30,
        totalCourses: 3,
        activeUsersToday: 3,
      });
      expect(prisma.user.count).toHaveBeenCalled();
      expect(prisma.submission.count).toHaveBeenCalled();
      expect(prisma.problem.count).toHaveBeenCalled();
      expect(prisma.course.count).toHaveBeenCalled();
    });
  });

  describe('getUsers', () => {
    it('should return users with submission counts and experiment groups', async () => {
      const users = [
        {
          id: 'u1',
          email: 'a@test.com',
          name: 'A',
          role: 'STUDENT',
          createdAt: new Date(),
          _count: { submissions: 5 },
          experimentGroup: { groupName: 'experimental', assignedAt: new Date() },
        },
      ];
      prisma.user.findMany.mockResolvedValue(users);
      prisma.user.count.mockResolvedValue(1);

      const result = await service.getUsers({ page: 1, pageSize: 15 });

      expect(prisma.user.findMany).toHaveBeenCalledWith(
        expect.objectContaining({
          select: expect.objectContaining({
            id: true,
            email: true,
            _count: { select: { submissions: true } },
            experimentGroup: expect.any(Object),
          }),
          orderBy: { createdAt: 'desc' },
          skip: 0,
          take: 15,
        }),
      );
      expect(result.data).toEqual(users);
      expect(result.total).toBe(1);
      expect(result.page).toBe(1);
    });
  });

  describe('assignGroup', () => {
    it('should delegate to AI service', async () => {
      const aiResult = { user_id: 'u1', group: 'experimental' };
      aiService.assignGroup.mockResolvedValue(aiResult);

      const result = await service.assignGroup('u1', 'experimental');

      expect(aiService.assignGroup).toHaveBeenCalledWith('u1', 'experimental');
      expect(result).toEqual(aiResult);
    });

    it('should fallback to local upsert when AI service is down', async () => {
      aiService.assignGroup.mockRejectedValue(new Error('Service unavailable'));
      const localResult = { userId: 'u1', groupName: 'control' };
      prisma.experimentGroup.upsert.mockResolvedValue(localResult);

      const result = await service.assignGroup('u1', 'control');

      expect(prisma.experimentGroup.upsert).toHaveBeenCalledWith({
        where: { userId: 'u1' },
        update: { groupName: 'control' },
        create: { userId: 'u1', groupName: 'control' },
      });
      expect(result).toEqual(localResult);
    });
  });

  describe('getExperimentStats', () => {
    it('should return stats from AI service', async () => {
      const stats = { groups: [{ group: 'experimental', count: 5 }] };
      aiService.getExperimentStats.mockResolvedValue(stats);

      const result = await service.getExperimentStats();

      expect(result).toEqual(stats);
    });

    it('should fallback to local groupBy when AI service is down', async () => {
      aiService.getExperimentStats.mockRejectedValue(new Error('down'));
      prisma.experimentGroup.groupBy.mockResolvedValue([
        { groupName: 'experimental', _count: { userId: 5 } },
        { groupName: 'control', _count: { userId: 3 } },
      ]);

      const result = await service.getExperimentStats();

      expect(result).toEqual({
        source: 'local_fallback',
        groups: [
          { groupName: 'experimental', userCount: 5 },
          { groupName: 'control', userCount: 3 },
        ],
      });
    });
  });

  describe('exportEvents', () => {
    it('should delegate to AI service', async () => {
      const events = { events: [{ event: 'submission', data: {} }] };
      aiService.exportEvents.mockResolvedValue(events);

      const result = await service.exportEvents('submission');

      expect(aiService.exportEvents).toHaveBeenCalledWith('submission');
      expect(result).toEqual(events);
    });

    it('should export without filter when event is undefined', async () => {
      aiService.exportEvents.mockResolvedValue({ events: [] });

      await service.exportEvents();

      expect(aiService.exportEvents).toHaveBeenCalledWith(undefined);
    });

    it('should fallback to local query when AI service is down', async () => {
      aiService.exportEvents.mockRejectedValue(new Error('down'));
      const localEvents = [{ id: '1', event: 'page_view', data: {}, createdAt: new Date() }];
      prisma.eventLog.findMany.mockResolvedValue(localEvents);

      const result = await service.exportEvents('page_view');

      expect(prisma.eventLog.findMany).toHaveBeenCalledWith({
        where: { event: 'page_view' },
        orderBy: { createdAt: 'desc' },
        take: 1000,
      });
      expect(result).toEqual({ source: 'local_fallback', events: localEvents });
    });

    it('should fallback with empty where when no event filter', async () => {
      aiService.exportEvents.mockRejectedValue(new Error('down'));
      prisma.eventLog.findMany.mockResolvedValue([]);

      await service.exportEvents();

      expect(prisma.eventLog.findMany).toHaveBeenCalledWith({
        where: {},
        orderBy: { createdAt: 'desc' },
        take: 1000,
      });
    });
  });
});
