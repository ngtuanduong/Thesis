import { Injectable, Logger, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { AiService } from '../ai/ai.service';
import { CreateProblemDto } from './dto/create-problem.dto';
import { generateStarterCode } from './starter-code.util';
import { paginate } from '../common/pagination';

@Injectable()
export class ProblemsService {
  private readonly logger = new Logger(ProblemsService.name);

  constructor(
    private prisma: PrismaService,
    private aiService: AiService,
  ) {}

  async create(dto: CreateProblemDto) {
    const { testCases, conceptIds, ...problemData } = dto;

    // Auto-generate starterCode from test cases if not provided
    if (!problemData.starterCode && testCases && testCases.length > 0) {
      problemData.starterCode = generateStarterCode(testCases);
    }

    const problem = await this.prisma.problem.create({
      data: {
        ...problemData,
        testCases: testCases ? { create: testCases } : undefined,
        ...(conceptIds?.length && {
          problemConcepts: {
            create: conceptIds.map((cid, idx) => ({
              conceptId: cid,
              isPrimary: idx === 0,
            })),
          },
        }),
      },
      include: { testCases: true, problemConcepts: { include: { concept: true } } },
    });

    // Fire-and-forget: generate embedding for the new problem
    this.aiService.embedProblem(problem).catch((err) => {
      this.logger.warn(`Failed to embed problem ${problem.id}: ${err.message}`);
    });

    return problem;
  }

  async findAll(courseId?: string) {
    return this.prisma.problem.findMany({
      where: courseId ? { courseId } : undefined,
      include: {
        testCases: { where: { isHidden: false } },
        problemConcepts: { include: { concept: true } },
      },
    });
  }

  async findPaginated(params: {
    page: number;
    pageSize: number;
    courseId?: string;
    search?: string;
    difficulty?: string[];
    conceptIds?: number[];
  }) {
    const { page, pageSize, courseId, search, difficulty, conceptIds } = params;

    const where: any = {};
    if (courseId) where.courseId = courseId;
    if (search) where.title = { contains: search, mode: 'insensitive' };
    if (difficulty?.length) where.difficulty = { in: difficulty };
    if (conceptIds?.length) {
      where.problemConcepts = { some: { conceptId: { in: conceptIds } } };
    }

    return paginate(this.prisma.problem, {
      where,
      orderBy: { createdAt: 'asc' },
      include: {
        testCases: { where: { isHidden: false } },
        problemConcepts: { include: { concept: true } },
      },
    }, { page, pageSize });
  }

  async findById(id: string) {
    const problem = await this.prisma.problem.findUnique({
      where: { id },
      include: {
        testCases: true,
        problemConcepts: { include: { concept: true } },
      },
    });
    if (!problem) {
      throw new NotFoundException('Problem not found');
    }
    return problem;
  }

  async update(id: string, dto: Partial<CreateProblemDto>) {
    await this.findById(id);
    const { testCases, conceptIds, ...problemData } = dto;

    // Re-generate starterCode when test cases change and no explicit starterCode provided
    if (testCases && testCases.length > 0 && !problemData.starterCode) {
      problemData.starterCode = generateStarterCode(testCases);
    }

    return this.prisma.problem.update({
      where: { id },
      data: {
        ...problemData,
        ...(testCases !== undefined && {
          testCases: {
            deleteMany: {},
            create: testCases,
          },
        }),
        ...(conceptIds !== undefined && {
          problemConcepts: {
            deleteMany: {},
            create: conceptIds.map((cid, idx) => ({
              conceptId: cid,
              isPrimary: idx === 0,
            })),
          },
        }),
      },
      include: { testCases: true, problemConcepts: { include: { concept: true } } },
    });
  }

  async remove(id: string) {
    await this.findById(id);
    await this.prisma.problem.delete({ where: { id } });
    return { deleted: true };
  }
}
