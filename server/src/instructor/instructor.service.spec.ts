import { Test, TestingModule } from '@nestjs/testing';
import { InstructorService } from './instructor.service';
import { PrismaService } from '../prisma/prisma.service';

describe('InstructorService', () => {
  let service: InstructorService;
  let prisma: Record<string, any>;

  beforeEach(async () => {
    prisma = {
      problem: {
        findMany: jest.fn(),
      },
      enrollment: {
        count: jest.fn(),
        findMany: jest.fn(),
      },
      submission: {
        count: jest.fn(),
        groupBy: jest.fn(),
      },
      knowledgeState: {
        findMany: jest.fn(),
      },
      eloRating: {
        findMany: jest.fn(),
      },
      user: {
        findMany: jest.fn(),
      },
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        InstructorService,
        { provide: PrismaService, useValue: prisma },
      ],
    }).compile();

    service = module.get<InstructorService>(InstructorService);
  });

  describe('getDashboard', () => {
    it('should return enrolled count, total submissions, avg mastery, struggling students', async () => {
      prisma.problem.findMany.mockResolvedValue([
        { id: 'p1' },
        { id: 'p2' },
      ]);
      prisma.enrollment.count.mockResolvedValue(15);
      prisma.submission.count.mockResolvedValue(200);
      prisma.knowledgeState.findMany.mockResolvedValue([
        { studentId: 's1', pMastery: 0.8 },
        { studentId: 's1', pMastery: 0.6 },
        { studentId: 's2', pMastery: 0.3 },
        { studentId: 's2', pMastery: 0.2 },
      ]);
      // s2 avg = 0.25 < 0.5 → struggling
      prisma.user.findMany.mockResolvedValue([
        { id: 's2', email: 's2@test.com', name: 'Student 2' },
      ]);

      const result = await service.getDashboard('course-1');

      expect(result.enrolledCount).toBe(15);
      expect(result.totalSubmissions).toBe(200);
      expect(result.averageMastery).toBeGreaterThan(0);
      expect(result.strugglingStudents).toHaveLength(1);
      expect(result.strugglingStudents[0].id).toBe('s2');
      expect(result.strugglingStudents[0].averageMastery).toBe(0.25);
    });

    it('should handle empty course (no problems, no enrollments)', async () => {
      prisma.problem.findMany.mockResolvedValue([]);
      prisma.enrollment.count.mockResolvedValue(0);
      prisma.submission.count.mockResolvedValue(0);
      prisma.knowledgeState.findMany.mockResolvedValue([]);

      const result = await service.getDashboard('empty-course');

      expect(result.enrolledCount).toBe(0);
      expect(result.totalSubmissions).toBe(0);
      expect(result.averageMastery).toBe(0);
      expect(result.strugglingStudents).toEqual([]);
    });

    it('should identify all students below 0.5 mastery as struggling', async () => {
      prisma.problem.findMany.mockResolvedValue([{ id: 'p1' }]);
      prisma.enrollment.count.mockResolvedValue(3);
      prisma.submission.count.mockResolvedValue(50);
      prisma.knowledgeState.findMany.mockResolvedValue([
        { studentId: 's1', pMastery: 0.9 },
        { studentId: 's2', pMastery: 0.4 },
        { studentId: 's3', pMastery: 0.3 },
      ]);
      prisma.user.findMany.mockResolvedValue([
        { id: 's2', email: 's2@test.com', name: 'Student 2' },
        { id: 's3', email: 's3@test.com', name: 'Student 3' },
      ]);

      const result = await service.getDashboard('course-1');

      expect(result.strugglingStudents).toHaveLength(2);
    });
  });

  describe('getStudents', () => {
    it('should return enriched student list with submission counts, mastery, elo', async () => {
      prisma.enrollment.findMany.mockResolvedValue([
        {
          createdAt: new Date('2024-01-01'),
          user: { id: 's1', email: 's1@test.com', name: 'Alice', role: 'STUDENT', createdAt: new Date() },
        },
      ]);
      prisma.problem.findMany.mockResolvedValue([{ id: 'p1' }]);
      prisma.submission.groupBy.mockResolvedValue([
        { userId: 's1', _count: { id: 10 } },
      ]);
      prisma.knowledgeState.findMany.mockResolvedValue([
        { studentId: 's1', pMastery: 0.8 },
        { studentId: 's1', pMastery: 0.6 },
      ]);
      prisma.eloRating.findMany.mockResolvedValue([
        { entityId: 's1', rating: 1200, updatedAt: new Date() },
      ]);

      const result = await service.getStudents('course-1');

      expect(result).toHaveLength(1);
      expect(result[0].name).toBe('Alice');
      expect(result[0].submissionCount).toBe(10);
      expect(result[0].averageMastery).toBe(0.7);
      expect(result[0].latestEloRating).toBe(1200);
    });

    it('should handle students with no submissions or mastery', async () => {
      prisma.enrollment.findMany.mockResolvedValue([
        {
          createdAt: new Date(),
          user: { id: 's1', email: 's1@test.com', name: 'Bob', role: 'STUDENT', createdAt: new Date() },
        },
      ]);
      prisma.problem.findMany.mockResolvedValue([{ id: 'p1' }]);
      prisma.submission.groupBy.mockResolvedValue([]);
      prisma.knowledgeState.findMany.mockResolvedValue([]);
      prisma.eloRating.findMany.mockResolvedValue([]);

      const result = await service.getStudents('course-1');

      expect(result[0].submissionCount).toBe(0);
      expect(result[0].averageMastery).toBe(0);
      expect(result[0].latestEloRating).toBeNull();
    });
  });

  describe('getProblemsManage', () => {
    it('should return problems with acceptance rate and concept mapping', async () => {
      prisma.problem.findMany.mockResolvedValue([
        {
          id: 'p1',
          title: 'Two Sum',
          description: 'Find two numbers',
          difficulty: 'EASY',
          tags: ['array'],
          courseId: 'c1',
          createdAt: new Date(),
          _count: { submissions: 20, testCases: 3 },
          problemConcepts: [
            {
              isPrimary: true,
              concept: { id: 1, name: 'arrays', displayName: 'Arrays' },
            },
          ],
        },
      ]);
      prisma.problem.count.mockResolvedValue(1);
      prisma.submission.groupBy.mockResolvedValue([
        { problemId: 'p1', _count: { id: 15 } },
      ]);

      const result = await service.getProblemsManage({ page: 1, pageSize: 10 });

      expect(result.data).toHaveLength(1);
      expect(result.data[0].title).toBe('Two Sum');
      expect(result.data[0].submissionCount).toBe(20);
      expect(result.data[0].acceptedCount).toBe(15);
      expect(result.data[0].acceptanceRate).toBe(0.75);
      expect(result.data[0].testCaseCount).toBe(3);
      expect(result.data[0].concepts).toEqual([
        { id: 1, name: 'arrays', displayName: 'Arrays', isPrimary: true },
      ]);
      expect(result.total).toBe(1);
      expect(result.page).toBe(1);
    });

    it('should handle problems with zero submissions (acceptanceRate = 0)', async () => {
      prisma.problem.findMany.mockResolvedValue([
        {
          id: 'p2',
          title: 'New Problem',
          description: 'Desc',
          difficulty: 'HARD',
          tags: [],
          courseId: null,
          createdAt: new Date(),
          _count: { submissions: 0, testCases: 1 },
          problemConcepts: [],
        },
      ]);
      prisma.problem.count.mockResolvedValue(1);
      prisma.submission.groupBy.mockResolvedValue([]);

      const result = await service.getProblemsManage({ page: 1, pageSize: 10 });

      expect(result.data[0].submissionCount).toBe(0);
      expect(result.data[0].acceptedCount).toBe(0);
      expect(result.data[0].acceptanceRate).toBe(0);
      expect(result.data[0].concepts).toEqual([]);
    });
  });
});
