import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { PaginatedResponse } from '../common/pagination';

@Injectable()
export class InstructorService {
  private readonly logger = new Logger(InstructorService.name);

  constructor(private prisma: PrismaService) {}

  async getDashboard(courseId: string) {
    // Get course problem IDs for filtering
    const courseProblems = await this.prisma.problem.findMany({
      where: { courseId },
      select: { id: true },
    });
    const problemIds = courseProblems.map((p) => p.id);

    const [enrolledCount, totalSubmissions, knowledgeStates] =
      await Promise.all([
        this.prisma.enrollment.count({ where: { courseId } }),
        this.prisma.submission.count({
          where: { problemId: { in: problemIds } },
        }),
        // Get all knowledge states for enrolled students
        this.prisma.knowledgeState.findMany({
          where: {
            student: {
              enrollments: { some: { courseId } },
            },
          },
          select: {
            studentId: true,
            pMastery: true,
          },
        }),
      ]);

    // Calculate average mastery across all students
    const averageMastery =
      knowledgeStates.length > 0
        ? knowledgeStates.reduce((sum, ks) => sum + ks.pMastery, 0) /
          knowledgeStates.length
        : 0;

    // Identify struggling students (average pMastery < 0.5)
    const studentMasteryMap = new Map<string, number[]>();
    for (const ks of knowledgeStates) {
      if (!studentMasteryMap.has(ks.studentId)) {
        studentMasteryMap.set(ks.studentId, []);
      }
      studentMasteryMap.get(ks.studentId)!.push(ks.pMastery);
    }

    const strugglingStudentIds: string[] = [];
    for (const [studentId, masteries] of studentMasteryMap) {
      const avg = masteries.reduce((a, b) => a + b, 0) / masteries.length;
      if (avg < 0.5) {
        strugglingStudentIds.push(studentId);
      }
    }

    const strugglingStudents =
      strugglingStudentIds.length > 0
        ? await this.prisma.user.findMany({
            where: { id: { in: strugglingStudentIds } },
            select: { id: true, email: true, name: true },
          })
        : [];

    // Attach average mastery to each struggling student
    const strugglingWithMastery = strugglingStudents.map((s) => {
      const masteries = studentMasteryMap.get(s.id) || [];
      const avgMastery =
        masteries.length > 0
          ? masteries.reduce((a, b) => a + b, 0) / masteries.length
          : 0;
      return { ...s, averageMastery: Math.round(avgMastery * 1000) / 1000 };
    });

    return {
      enrolledCount,
      totalSubmissions,
      averageMastery: Math.round(averageMastery * 1000) / 1000,
      strugglingStudents: strugglingWithMastery,
    };
  }

  async getStudents(courseId: string) {
    const enrollments = await this.prisma.enrollment.findMany({
      where: { courseId },
      include: {
        user: {
          select: {
            id: true,
            email: true,
            name: true,
            role: true,
            createdAt: true,
          },
        },
      },
    });

    const studentIds = enrollments.map((e) => e.user.id);

    // Get submission counts per student (for course problems)
    const courseProblems = await this.prisma.problem.findMany({
      where: { courseId },
      select: { id: true },
    });
    const problemIds = courseProblems.map((p) => p.id);

    const [submissionCounts, knowledgeStates, eloRatings] = await Promise.all([
      this.prisma.submission.groupBy({
        by: ['userId'],
        where: {
          userId: { in: studentIds },
          problemId: { in: problemIds },
        },
        _count: { id: true },
      }),
      this.prisma.knowledgeState.findMany({
        where: { studentId: { in: studentIds } },
        select: { studentId: true, pMastery: true },
      }),
      this.prisma.eloRating.findMany({
        where: {
          entityId: { in: studentIds },
          entityType: 'STUDENT',
        },
        orderBy: { updatedAt: 'desc' },
      }),
    ]);

    // Build lookup maps
    const submissionCountMap = new Map<string, number>();
    for (const sc of submissionCounts) {
      submissionCountMap.set(sc.userId, sc._count.id);
    }

    const masteryMap = new Map<string, number[]>();
    for (const ks of knowledgeStates) {
      if (!masteryMap.has(ks.studentId)) {
        masteryMap.set(ks.studentId, []);
      }
      masteryMap.get(ks.studentId)!.push(ks.pMastery);
    }

    // Use first (latest) Elo rating per student
    const eloMap = new Map<string, number>();
    for (const elo of eloRatings) {
      if (!eloMap.has(elo.entityId)) {
        eloMap.set(elo.entityId, elo.rating);
      }
    }

    return enrollments.map((enrollment) => {
      const studentId = enrollment.user.id;
      const masteries = masteryMap.get(studentId) || [];
      const avgMastery =
        masteries.length > 0
          ? masteries.reduce((a, b) => a + b, 0) / masteries.length
          : 0;

      return {
        ...enrollment.user,
        enrolledAt: enrollment.createdAt,
        submissionCount: submissionCountMap.get(studentId) || 0,
        averageMastery: Math.round(avgMastery * 1000) / 1000,
        latestEloRating: eloMap.get(studentId) ?? null,
      };
    });
  }

  async getProblemsManage(params: {
    page: number;
    pageSize: number;
    search?: string;
  }): Promise<PaginatedResponse<any>> {
    const { page, pageSize, search } = params;

    const where: any = {};
    if (search) where.title = { contains: search, mode: 'insensitive' };

    const selectFields = {
      id: true,
      title: true,
      description: true,
      difficulty: true,
      courseId: true,
      createdAt: true,
      _count: { select: { submissions: true, testCases: true } },
      problemConcepts: {
        include: {
          concept: { select: { id: true, name: true, displayName: true } },
        },
      },
    };

    const [problems, total] = await Promise.all([
      this.prisma.problem.findMany({
        where,
        select: selectFields,
        orderBy: { createdAt: 'desc' },
        skip: (page - 1) * pageSize,
        take: pageSize,
      }),
      this.prisma.problem.count({ where }),
    ]);

    // Get accepted submission counts only for this page's problems
    const ids = problems.map((p) => p.id);
    const acceptedCounts = ids.length
      ? await this.prisma.submission.groupBy({
          by: ['problemId'],
          where: { problemId: { in: ids }, status: 'ACCEPTED' },
          _count: { id: true },
        })
      : [];

    const acceptedMap = new Map<string, number>();
    for (const ac of acceptedCounts) {
      acceptedMap.set(ac.problemId, ac._count.id);
    }

    const data = problems.map((problem) => {
      const totalSubmissions = problem._count.submissions;
      const accepted = acceptedMap.get(problem.id) || 0;
      const acceptanceRate =
        totalSubmissions > 0
          ? Math.round((accepted / totalSubmissions) * 1000) / 1000
          : 0;

      return {
        id: problem.id,
        title: problem.title,
        description: problem.description,
        difficulty: problem.difficulty,
        courseId: problem.courseId,
        createdAt: problem.createdAt,
        submissionCount: totalSubmissions,
        acceptedCount: accepted,
        acceptanceRate,
        testCaseCount: problem._count.testCases,
        concepts: problem.problemConcepts.map((pc) => ({
          id: pc.concept.id,
          name: pc.concept.name,
          displayName: pc.concept.displayName,
          isPrimary: pc.isPrimary,
        })),
      };
    });

    return { data, total, page, pageSize };
  }
}
